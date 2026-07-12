from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, replace
from fractions import Fraction

from p2c_engine.canonical.hashes import sha256_canonical
from p2c_engine.decisions import RecordingDecisionSource, SeededDecisionSource
from p2c_engine.domain.candidate import Candidate
from p2c_engine.domain.decision import DecisionRecord
from p2c_engine.domain.defects import SamplingContractDefect
from p2c_engine.domain.enums import Rarity, Side
from p2c_engine.domain.item_state import DesecratedPlaceholder, ItemState, ModifierInstance
from p2c_engine.domain.versions import RNG_STREAM_VERSION, SAMPLING_ALGORITHM_ID
from p2c_engine.legality.capacity import capacity_snapshot
from p2c_engine.legality.state_validation import validate_item_state
from p2c_engine.sampling.digest import pool_digest
from p2c_engine.sampling.exact import branch_options
from p2c_engine.static_data.game_data import StaticGameData

from .ordinary_add import M32_VALUE_POLICY, M32InvariantViolation, M32MonteCarloError


M47A1_OPERATION_IDS = frozenset(
    {"gnawed_jawbone", "preserved_jawbone", "ancient_jawbone"}
)
M47A1_SCHEMA_VERSION = "p2c.m47a1.jawbone_placeholder_runtime.v1"
M47A1_SEMANTICS_VERSION = "p2c.m47a1.jawbone_placeholder.project_model.v1"
M47A1_FIXED_SEEDS = (47_101, 47_102, 47_103)
M47A1_SAMPLE_TIERS = (512, 2_048, 8_192)


class M47A1JawboneError(M32MonteCarloError):
    """Base error for the clean Jawbone placeholder runtime."""


class M47A1JawboneInvariantViolation(M47A1JawboneError, M32InvariantViolation):
    """Raised when the accepted D1-A/D2-A contract is violated."""


@dataclass(frozen=True, slots=True)
class JawboneOperation:
    mode_id: str
    operation_id: str
    item_class: str = "quarterstaff"
    item_level_max: int | None = None
    reveal_mml: int | None = None
    lich_tag_constraint: str | None = None
    semantics_version: str = M47A1_SEMANTICS_VERSION


@dataclass(frozen=True, slots=True)
class JawboneCandidateMetadata:
    candidate_key: str
    action: str
    side: Side
    mod_id: str | None = None
    crafted: bool | None = None
    desecrated: bool | None = None
    fractured: bool | None = None
    duplicate_ordinal: int | None = None


@dataclass(frozen=True, slots=True)
class JawbonePoolResult:
    candidates: tuple[Candidate, ...]
    metadata: tuple[JawboneCandidateMetadata, ...]
    candidate_digest: str | None
    result_fingerprint: str
    policy_branch: str
    empty_reason: str | None


@dataclass(frozen=True, slots=True)
class ExactJawbonePath:
    path_key: str | None
    terminal_state: ItemState
    terminal_state_hash: str
    outcome: str
    selected_side: Side | None
    selected_replacement_key: str | None
    candidate_count: int
    candidate_digest: str | None
    pool_fingerprint: str
    policy_branch: str
    no_transition_reason: str | None
    probability_numerator: int
    probability_denominator: int


@dataclass(frozen=True, slots=True)
class ExactJawboneTerminal:
    terminal_state: ItemState
    terminal_state_hash: str
    path_count: int
    path_keys: tuple[str | None, ...]
    probability_numerator: int
    probability_denominator: int


@dataclass(frozen=True, slots=True)
class JawboneTrajectory:
    sample_index: int
    outcome: str
    pre_state_hash: str
    post_state_hash: str
    decision_id: str | None
    selected_candidate_key: str | None
    selected_side: Side | None
    selected_replacement_key: str | None
    candidate_count: int
    candidate_digest: str | None
    pool_fingerprint: str
    policy_branch: str
    no_transition_reason: str | None

    def public_payload(self) -> dict[str, object]:
        return {
            "sample_index": self.sample_index,
            "outcome": self.outcome,
            "pre_state_hash": self.pre_state_hash,
            "post_state_hash": self.post_state_hash,
            "decision_id": self.decision_id,
            "selected_candidate_key": self.selected_candidate_key,
            "selected_side": self.selected_side.value if self.selected_side else None,
            "selected_replacement_key": self.selected_replacement_key,
            "candidate_count": self.candidate_count,
            "candidate_digest": self.candidate_digest,
            "pool_fingerprint": self.pool_fingerprint,
            "policy_branch": self.policy_branch,
            "no_transition_reason": self.no_transition_reason,
        }


@dataclass(frozen=True, slots=True)
class JawboneRunResult:
    schema_version: str
    run_id: str
    seed: int
    sample_count: int
    mode_id: str
    operation_id: str
    source_fingerprint: str
    semantic_fingerprint: str
    code_version: str
    trajectories: tuple[JawboneTrajectory, ...]
    decisions: tuple[DecisionRecord, ...]
    result_hash: str

    def public_summary(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "status": "PASS",
            "numeric_probability_free": True,
            "public_numeric_release": False,
            "probability_values_printed": False,
            "value_policy": M32_VALUE_POLICY,
            "run_id": self.run_id,
            "seed": self.seed,
            "sample_count": self.sample_count,
            "mode_id": self.mode_id,
            "operation_id": self.operation_id,
            "source_fingerprint": self.source_fingerprint,
            "semantic_fingerprint": self.semantic_fingerprint,
            "code_version": self.code_version,
            "trajectory_count": len(self.trajectories),
            "decision_count": len(self.decisions),
            "result_hash": self.result_hash,
        }


def build_jawbone_pool(
    state: ItemState,
    operation: JawboneOperation,
    static: StaticGameData,
) -> JawbonePoolResult:
    reason = _precondition_failure(state, operation, static)
    if reason is not None:
        return _empty_pool(state, operation, reason)

    capacity = capacity_snapshot(state, static)
    free_sides = tuple(
        side
        for side, used, limit in (
            (Side.PREFIX, capacity.prefix_used, capacity.prefix_capacity),
            (Side.SUFFIX, capacity.suffix_used, capacity.suffix_capacity),
        )
        if used < limit
    )
    if free_sides:
        metadata = tuple(
            JawboneCandidateMetadata(
                candidate_key=f"jawbone:install:{side.value}",
                action="install_free_side",
                side=side,
            )
            for side in free_sides
        )
        branch = "d1_free_capacity"
    else:
        seen: Counter[tuple[str, bool, bool, bool]] = Counter()
        rows: list[JawboneCandidateMetadata] = []
        for instance in state.modifiers:
            identity = _instance_identity(instance)
            ordinal = seen[identity]
            seen[identity] += 1
            if instance.fractured:
                continue
            side = static.modifier_index[instance.mod_id].side
            key = (
                f"jawbone:replace:{instance.mod_id}:c{int(instance.crafted)}:"
                f"d{int(instance.desecrated)}:f{int(instance.fractured)}:o{ordinal}"
            )
            rows.append(
                JawboneCandidateMetadata(
                    candidate_key=key,
                    action="replace_full_item",
                    side=side,
                    mod_id=instance.mod_id,
                    crafted=instance.crafted,
                    desecrated=instance.desecrated,
                    fractured=instance.fractured,
                    duplicate_ordinal=ordinal,
                )
            )
        metadata = tuple(rows)
        branch = "d2_full_item_replacement"

    candidates = tuple(Candidate(row.candidate_key, 1) for row in metadata)
    result = JawbonePoolResult(
        candidates=candidates,
        metadata=metadata,
        candidate_digest=pool_digest(candidates) if candidates else None,
        result_fingerprint=_pool_fingerprint(
            state,
            operation,
            metadata,
            branch,
            None if candidates else "jawbone_transition_pool_exhausted",
        ),
        policy_branch=branch,
        empty_reason=None if candidates else "jawbone_transition_pool_exhausted",
    )
    _validate_pool(result)
    return result


class JawboneHarness:
    def __init__(self, *, static: StaticGameData, code_version: str = "p2c.m47a1.dev") -> None:
        self.static = static
        self.code_version = code_version

    def build_pool(self, state: ItemState, operation: JawboneOperation) -> JawbonePoolResult:
        _validate_operation(operation)
        pool = build_jawbone_pool(state, operation, self.static)
        _validate_pool(pool)
        return pool

    def enumerate_paths(
        self, *, state: ItemState, operation: JawboneOperation, decision_id: str
    ) -> tuple[ExactJawbonePath, ...]:
        pool = self.build_pool(state, operation)
        if not pool.candidates:
            return (
                ExactJawbonePath(
                    path_key=None,
                    terminal_state=state,
                    terminal_state_hash=state.state_hash(),
                    outcome="no_transition_no_consumption",
                    selected_side=None,
                    selected_replacement_key=None,
                    candidate_count=0,
                    candidate_digest=None,
                    pool_fingerprint=pool.result_fingerprint,
                    policy_branch=pool.policy_branch,
                    no_transition_reason=pool.empty_reason,
                    probability_numerator=1,
                    probability_denominator=1,
                ),
            )
        metadata = _metadata_by_key(pool)
        paths: list[ExactJawbonePath] = []
        for option in branch_options(decision_id, pool.candidates):
            selected = metadata[option.selected_key]
            terminal = _apply_candidate(state, operation, selected)
            _assert_transition(state, terminal, operation, selected, self.static)
            paths.append(
                ExactJawbonePath(
                    path_key=option.selected_key,
                    terminal_state=terminal,
                    terminal_state_hash=terminal.state_hash(),
                    outcome="applied",
                    selected_side=selected.side,
                    selected_replacement_key=(
                        selected.candidate_key if selected.action == "replace_full_item" else None
                    ),
                    candidate_count=len(pool.candidates),
                    candidate_digest=option.candidate_digest,
                    pool_fingerprint=pool.result_fingerprint,
                    policy_branch=pool.policy_branch,
                    no_transition_reason=None,
                    probability_numerator=option.probability_numerator,
                    probability_denominator=option.probability_denominator,
                )
            )
        _assert_mass(paths)
        return tuple(paths)

    def enumerate_terminal_distribution(
        self, *, state: ItemState, operation: JawboneOperation, decision_id: str
    ) -> tuple[ExactJawboneTerminal, ...]:
        paths = self.enumerate_paths(state=state, operation=operation, decision_id=decision_id)
        masses: dict[str, Fraction] = {}
        states: dict[str, ItemState] = {}
        keys: dict[str, list[str | None]] = {}
        for path in paths:
            key = path.terminal_state_hash
            masses[key] = masses.get(key, Fraction()) + Fraction(
                path.probability_numerator, path.probability_denominator
            )
            states[key] = path.terminal_state
            keys.setdefault(key, []).append(path.path_key)
        return tuple(
            ExactJawboneTerminal(
                terminal_state=states[key],
                terminal_state_hash=key,
                path_count=len(keys[key]),
                path_keys=tuple(sorted(keys[key], key=lambda value: value or "")),
                probability_numerator=masses[key].numerator,
                probability_denominator=masses[key].denominator,
            )
            for key in sorted(masses)
        )

    def sample_once(
        self,
        *,
        state: ItemState,
        operation: JawboneOperation,
        decision_source: RecordingDecisionSource,
        sample_index: int,
        run_id: str,
        decision_id: str | None = None,
    ) -> JawboneTrajectory:
        pool = self.build_pool(state, operation)
        pre_hash = state.state_hash()
        if not pool.candidates:
            return JawboneTrajectory(
                sample_index, "no_transition_no_consumption", pre_hash, pre_hash,
                None, None, None, None, 0, None, pool.result_fingerprint,
                pool.policy_branch, pool.empty_reason,
            )
        chosen_id = decision_id or (
            f"{run_id}.sample_{sample_index}.step_0.{operation.operation_id}.{operation.mode_id}"
        )
        decision = decision_source.choose_one(chosen_id, pool.candidates)
        selected = _metadata_by_key(pool)[decision.selected.key]
        terminal = _apply_candidate(state, operation, selected)
        _assert_transition(state, terminal, operation, selected, self.static)
        return JawboneTrajectory(
            sample_index=sample_index,
            outcome="applied",
            pre_state_hash=pre_hash,
            post_state_hash=terminal.state_hash(),
            decision_id=decision.record.decision_id,
            selected_candidate_key=decision.selected.key,
            selected_side=selected.side,
            selected_replacement_key=(
                selected.candidate_key if selected.action == "replace_full_item" else None
            ),
            candidate_count=decision.record.candidate_count,
            candidate_digest=decision.record.candidate_digest,
            pool_fingerprint=pool.result_fingerprint,
            policy_branch=pool.policy_branch,
            no_transition_reason=None,
        )

    def run(
        self,
        *,
        initial_state: ItemState,
        operation: JawboneOperation,
        seed: int,
        sample_count: int,
        run_id: str,
    ) -> JawboneRunResult:
        if isinstance(sample_count, bool) or not isinstance(sample_count, int) or sample_count < 0:
            raise SamplingContractDefect("sample_count must be a non-negative non-bool integer")
        source = RecordingDecisionSource(SeededDecisionSource(seed))
        trajectories = tuple(
            self.sample_once(
                state=initial_state,
                operation=operation,
                decision_source=source,
                sample_index=index,
                run_id=run_id,
            )
            for index in range(sample_count)
        )
        payload = {
            "schema_version": M47A1_SCHEMA_VERSION,
            "run_id": run_id,
            "seed": seed,
            "sample_count": sample_count,
            "mode_id": operation.mode_id,
            "operation_id": operation.operation_id,
            "rng_stream_version": RNG_STREAM_VERSION,
            "sampling_algorithm_id": SAMPLING_ALGORITHM_ID,
            "source_fingerprint": self.static.source_fingerprint,
            "semantic_fingerprint": self.static.semantic_fingerprint,
            "code_version": self.code_version,
            "trajectories": [row.public_payload() for row in trajectories],
            "decisions": list(source.records),
        }
        return JawboneRunResult(
            schema_version=M47A1_SCHEMA_VERSION,
            run_id=run_id,
            seed=seed,
            sample_count=sample_count,
            mode_id=operation.mode_id,
            operation_id=operation.operation_id,
            source_fingerprint=self.static.source_fingerprint,
            semantic_fingerprint=self.static.semantic_fingerprint,
            code_version=self.code_version,
            trajectories=trajectories,
            decisions=source.records,
            result_hash=sha256_canonical(payload, schema_version=1),
        )


def _precondition_failure(
    state: ItemState, operation: JawboneOperation, static: StaticGameData
) -> str | None:
    if state.item_class != "quarterstaff" or state.item_class != operation.item_class:
        return "unsupported_item_class"
    if state.rarity is not Rarity.RARE:
        return "rare_input_required"
    if operation.item_level_max is not None and state.item_level > operation.item_level_max:
        return "item_level_above_jawbone_maximum"
    if state.unrevealed_desecrated is not None or any(row.desecrated for row in state.modifiers):
        return "desecrated_limit_reached"
    if any(row.mod_id not in static.modifier_index for row in state.modifiers):
        return "unknown_installed_modifier"
    if not validate_item_state(state, static).ok:
        return "invalid_source_state"
    return None


def _apply_candidate(
    state: ItemState, operation: JawboneOperation, selected: JawboneCandidateMetadata
) -> ItemState:
    working = state
    if selected.action == "replace_full_item":
        if selected.fractured:
            raise M47A1JawboneInvariantViolation("fractured replacement candidate selected")
        working = working.with_modifiers(_remove_selected(working.modifiers, selected))
    placeholder = DesecratedPlaceholder(
        side=selected.side,
        jawbone_id=operation.operation_id,
        reveal_mml=operation.reveal_mml,
        lich_tag_constraint=operation.lich_tag_constraint,
    )
    return replace(working, unrevealed_desecrated=placeholder)


def _remove_selected(
    modifiers: tuple[ModifierInstance, ...], selected: JawboneCandidateMetadata
) -> tuple[ModifierInstance, ...]:
    identity = (selected.mod_id, selected.crafted, selected.desecrated, selected.fractured)
    ordinal = 0
    output: list[ModifierInstance] = []
    removed = False
    for instance in modifiers:
        if _instance_identity(instance) == identity:
            if ordinal == selected.duplicate_ordinal and not removed:
                removed = True
                ordinal += 1
                continue
            ordinal += 1
        output.append(instance)
    if not removed:
        raise M47A1JawboneInvariantViolation("selected replacement instance not found")
    return tuple(output)


def _assert_transition(
    pre: ItemState,
    post: ItemState,
    operation: JawboneOperation,
    selected: JawboneCandidateMetadata,
    static: StaticGameData,
) -> None:
    placeholder = post.unrevealed_desecrated
    if placeholder is None or placeholder.side != selected.side:
        raise M47A1JawboneInvariantViolation("canonical placeholder was not installed")
    if placeholder.jawbone_id != operation.operation_id:
        raise M47A1JawboneInvariantViolation("placeholder source operation mismatch")
    if placeholder.reveal_mml != operation.reveal_mml:
        raise M47A1JawboneInvariantViolation("placeholder MML context mismatch")
    if selected.action == "install_free_side":
        if post.modifiers != pre.modifiers:
            raise M47A1JawboneInvariantViolation("D1-A changed installed modifiers")
    elif len(post.modifiers) != len(pre.modifiers) - 1:
        raise M47A1JawboneInvariantViolation("D2-A did not replace exactly one instance")
    if any(row.fractured for row in pre.modifiers if row not in post.modifiers):
        raise M47A1JawboneInvariantViolation("D2-A removed a fractured modifier")
    if not validate_item_state(post, static).ok:
        raise M47A1JawboneInvariantViolation("Jawbone produced an invalid state")


def _validate_operation(operation: JawboneOperation) -> None:
    if operation.operation_id not in M47A1_OPERATION_IDS:
        raise M47A1JawboneInvariantViolation("unsupported Jawbone operation")
    if operation.item_class != "quarterstaff":
        raise M47A1JawboneInvariantViolation("M47-A1 admits quarterstaff only")
    if operation.semantics_version != M47A1_SEMANTICS_VERSION:
        raise M47A1JawboneInvariantViolation("Jawbone semantics version mismatch")


def _validate_pool(pool: JawbonePoolResult) -> None:
    keys = [candidate.key for candidate in pool.candidates]
    if len(keys) != len(set(keys)) or set(keys) != {row.candidate_key for row in pool.metadata}:
        raise M47A1JawboneInvariantViolation("Jawbone candidate metadata mismatch")
    if any(candidate.weight != 1 for candidate in pool.candidates):
        raise M47A1JawboneInvariantViolation("Jawbone selection must use uniform unit weights")
    if any(row.fractured for row in pool.metadata):
        raise M47A1JawboneInvariantViolation("fractured modifier entered replacement pool")
    if pool.policy_branch == "d1_free_capacity" and any(
        row.action != "install_free_side" for row in pool.metadata
    ):
        raise M47A1JawboneInvariantViolation("D1-A pool contains replacement candidate")


def _empty_pool(
    state: ItemState, operation: JawboneOperation, reason: str
) -> JawbonePoolResult:
    branch = "precondition_failure"
    return JawbonePoolResult(
        candidates=(),
        metadata=(),
        candidate_digest=None,
        result_fingerprint=_pool_fingerprint(state, operation, (), branch, reason),
        policy_branch=branch,
        empty_reason=reason,
    )


def _pool_fingerprint(
    state: ItemState,
    operation: JawboneOperation,
    metadata: tuple[JawboneCandidateMetadata, ...],
    branch: str,
    reason: str | None,
) -> str:
    return sha256_canonical(
        {
            "semantics_version": operation.semantics_version,
            "operation_id": operation.operation_id,
            "mode_id": operation.mode_id,
            "pre_state_hash": state.state_hash(),
            "policy_branch": branch,
            "candidate_keys": [row.candidate_key for row in metadata],
            "empty_reason": reason,
        },
        schema_version=1,
    )


def _metadata_by_key(pool: JawbonePoolResult) -> dict[str, JawboneCandidateMetadata]:
    return {row.candidate_key: row for row in pool.metadata}


def _instance_identity(instance: ModifierInstance) -> tuple[str, bool, bool, bool]:
    return (instance.mod_id, instance.crafted, instance.desecrated, instance.fractured)


def _assert_mass(paths: list[ExactJawbonePath]) -> None:
    if sum(
        (Fraction(row.probability_numerator, row.probability_denominator) for row in paths),
        Fraction(),
    ) != Fraction(1, 1):
        raise M47A1JawboneInvariantViolation("Jawbone exact path mass does not sum to one")


__all__ = [
    "M47A1_FIXED_SEEDS",
    "M47A1_OPERATION_IDS",
    "M47A1_SCHEMA_VERSION",
    "M47A1_SEMANTICS_VERSION",
    "ExactJawbonePath",
    "ExactJawboneTerminal",
    "JawboneCandidateMetadata",
    "JawboneHarness",
    "JawboneOperation",
    "JawbonePoolResult",
    "JawboneRunResult",
    "JawboneTrajectory",
    "M47A1JawboneError",
    "M47A1JawboneInvariantViolation",
    "build_jawbone_pool",
]
