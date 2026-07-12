from __future__ import annotations

from collections import Counter
from collections.abc import Callable
from dataclasses import dataclass, replace
from fractions import Fraction

from p2c_engine.canonical.hashes import sha256_canonical
from p2c_engine.decisions import RecordingDecisionSource, SeededDecisionSource
from p2c_engine.domain.candidate import Candidate
from p2c_engine.domain.decision import DecisionRecord
from p2c_engine.domain.defects import SamplingContractDefect
from p2c_engine.domain.enums import Rarity
from p2c_engine.domain.item_state import ItemState, ModifierInstance
from p2c_engine.domain.versions import RNG_STREAM_VERSION, SAMPLING_ALGORITHM_ID
from p2c_engine.legality.state_validation import validate_item_state
from p2c_engine.sampling.digest import pool_digest
from p2c_engine.sampling.exact import branch_options
from p2c_engine.static_data.game_data import StaticGameData

from .ordinary_add import M32_VALUE_POLICY, M32InvariantViolation, M32MonteCarloError


FRACTURING_ORB_OPERATION_ID = "fracturing_orb"
M46A_FRACTURE_SCHEMA_VERSION = "p2c.m46a.fracture_core_runtime.v1"
M46A_FRACTURE_SEMANTICS_VERSION = "p2c.m46.fracture_core.project_model.v1"
M46A_FIXED_SEEDS = (46_001, 46_002, 46_003)
M46A_SAMPLE_TIERS = (512, 2_048, 8_192)


class M46AFractureError(M32MonteCarloError):
    """Base class for the clean M46-A Fracture runtime."""


class M46AFractureInvariantViolation(M46AFractureError, M32InvariantViolation):
    """Raised when Fracture violates its admitted project-model contract."""


@dataclass(frozen=True, slots=True)
class FractureOperation:
    mode_id: str
    operation_id: str = FRACTURING_ORB_OPERATION_ID
    item_class: str = "quarterstaff"
    semantics_version: str = M46A_FRACTURE_SEMANTICS_VERSION


@dataclass(frozen=True, slots=True)
class FractureCandidateMetadata:
    candidate_key: str
    mod_id: str
    crafted: bool
    desecrated: bool
    fractured: bool
    duplicate_ordinal: int
    side: str


@dataclass(frozen=True, slots=True)
class FracturePoolResult:
    candidates: tuple[Candidate, ...]
    metadata: tuple[FractureCandidateMetadata, ...]
    candidate_digest: str | None
    result_fingerprint: str
    empty_reason: str | None


@dataclass(frozen=True, slots=True)
class FractureTrajectory:
    sample_index: int
    outcome: str
    pre_state_hash: str
    post_state_hash: str
    decision_id: str | None
    selected_candidate_key: str | None
    selected_mod_id: str | None
    selected_duplicate_ordinal: int | None
    selected_was_crafted: bool | None
    candidate_count: int
    candidate_digest: str | None
    pool_fingerprint: str
    no_transition_reason: str | None

    def public_payload(self) -> dict[str, object]:
        return {
            "sample_index": self.sample_index,
            "outcome": self.outcome,
            "pre_state_hash": self.pre_state_hash,
            "post_state_hash": self.post_state_hash,
            "decision_id": self.decision_id,
            "selected_candidate_key": self.selected_candidate_key,
            "selected_mod_id": self.selected_mod_id,
            "selected_duplicate_ordinal": self.selected_duplicate_ordinal,
            "selected_was_crafted": self.selected_was_crafted,
            "candidate_count": self.candidate_count,
            "candidate_digest": self.candidate_digest,
            "pool_fingerprint": self.pool_fingerprint,
            "no_transition_reason": self.no_transition_reason,
        }


@dataclass(frozen=True, slots=True)
class ExactFracturePath:
    path_key: str | None
    terminal_state: ItemState
    terminal_state_hash: str
    outcome: str
    selected_candidate_key: str | None
    selected_mod_id: str | None
    selected_duplicate_ordinal: int | None
    selected_was_crafted: bool | None
    candidate_count: int
    candidate_digest: str | None
    pool_fingerprint: str
    no_transition_reason: str | None
    probability_numerator: int
    probability_denominator: int


@dataclass(frozen=True, slots=True)
class ExactFractureTerminal:
    terminal_state: ItemState
    terminal_state_hash: str
    path_count: int
    path_keys: tuple[str | None, ...]
    probability_numerator: int
    probability_denominator: int


@dataclass(frozen=True, slots=True)
class FractureRunResult:
    schema_version: str
    run_id: str
    seed: int
    sample_count: int
    mode_id: str
    operation_id: str
    rng_stream_version: int
    sampling_algorithm_id: str
    source_fingerprint: str
    semantic_fingerprint: str
    code_version: str
    trajectories: tuple[FractureTrajectory, ...]
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
            "rng_stream_version": self.rng_stream_version,
            "sampling_algorithm_id": self.sampling_algorithm_id,
            "source_fingerprint": self.source_fingerprint,
            "semantic_fingerprint": self.semantic_fingerprint,
            "code_version": self.code_version,
            "trajectory_count": len(self.trajectories),
            "decision_count": len(self.decisions),
            "result_hash": self.result_hash,
        }


FracturePoolBuilder = Callable[
    [ItemState, FractureOperation, StaticGameData], FracturePoolResult
]


def build_fracture_pool(
    state: ItemState,
    operation: FractureOperation,
    static: StaticGameData,
) -> FracturePoolResult:
    reason = _fracture_precondition_failure(state, operation, static)
    if reason is not None:
        return _empty_pool(state, operation, reason)

    seen: Counter[tuple[str, bool, bool, bool]] = Counter()
    candidates: list[Candidate] = []
    metadata: list[FractureCandidateMetadata] = []
    for instance in state.modifiers:
        identity = _instance_identity(instance)
        ordinal = seen[identity]
        seen[identity] += 1
        static_mod = static.modifier_index[instance.mod_id]
        key = (
            f"fracture:{instance.mod_id}:c{int(instance.crafted)}:"
            f"d{int(instance.desecrated)}:f{int(instance.fractured)}:o{ordinal}"
        )
        candidates.append(Candidate(key, 1))
        metadata.append(
            FractureCandidateMetadata(
                candidate_key=key,
                mod_id=instance.mod_id,
                crafted=instance.crafted,
                desecrated=instance.desecrated,
                fractured=instance.fractured,
                duplicate_ordinal=ordinal,
                side=static_mod.side.value,
            )
        )

    candidate_tuple = tuple(candidates)
    digest = pool_digest(candidate_tuple) if candidate_tuple else None
    result = FracturePoolResult(
        candidates=candidate_tuple,
        metadata=tuple(metadata),
        candidate_digest=digest,
        result_fingerprint=_pool_fingerprint(
            state, operation, tuple(metadata), None
        ),
        empty_reason=None if candidate_tuple else "fracture_candidate_pool_exhausted",
    )
    _validate_fracture_pool(result, static)
    return result


class FractureHarness:
    """Exact and seeded-MC harness for the clean base Fracturing Orb."""

    def __init__(
        self,
        *,
        static: StaticGameData,
        pool_builder: FracturePoolBuilder = build_fracture_pool,
        code_version: str = "p2c.m46a.dev",
    ) -> None:
        self.static = static
        self.pool_builder = pool_builder
        self.code_version = code_version

    def build_pool(
        self, state: ItemState, operation: FractureOperation
    ) -> FracturePoolResult:
        _validate_operation_definition(operation)
        pool = self.pool_builder(state, operation, self.static)
        _validate_fracture_pool(pool, self.static)
        return pool

    def enumerate_paths(
        self,
        *,
        state: ItemState,
        operation: FractureOperation,
        decision_id: str,
    ) -> tuple[ExactFracturePath, ...]:
        pool = self.build_pool(state, operation)
        if not pool.candidates:
            _assert_no_transition_unchanged(state, state)
            return (
                ExactFracturePath(
                    path_key=None,
                    terminal_state=state,
                    terminal_state_hash=state.state_hash(),
                    outcome="no_transition_no_consumption",
                    selected_candidate_key=None,
                    selected_mod_id=None,
                    selected_duplicate_ordinal=None,
                    selected_was_crafted=None,
                    candidate_count=0,
                    candidate_digest=None,
                    pool_fingerprint=pool.result_fingerprint,
                    no_transition_reason=pool.empty_reason,
                    probability_numerator=1,
                    probability_denominator=1,
                ),
            )

        metadata = _metadata_by_candidate_key(pool)
        output: list[ExactFracturePath] = []
        for option in branch_options(decision_id, pool.candidates):
            selected = metadata[option.selected_key]
            terminal = _fracture_modifier_instance(state, selected)
            _assert_fracture_transition(state, terminal, selected, self.static)
            output.append(
                ExactFracturePath(
                    path_key=option.selected_key,
                    terminal_state=terminal,
                    terminal_state_hash=terminal.state_hash(),
                    outcome="applied",
                    selected_candidate_key=option.selected_key,
                    selected_mod_id=selected.mod_id,
                    selected_duplicate_ordinal=selected.duplicate_ordinal,
                    selected_was_crafted=selected.crafted,
                    candidate_count=len(pool.candidates),
                    candidate_digest=option.candidate_digest,
                    pool_fingerprint=pool.result_fingerprint,
                    no_transition_reason=None,
                    probability_numerator=option.probability_numerator,
                    probability_denominator=option.probability_denominator,
                )
            )
        return tuple(output)

    def enumerate_terminal_distribution(
        self,
        *,
        state: ItemState,
        operation: FractureOperation,
        decision_id: str,
    ) -> tuple[ExactFractureTerminal, ...]:
        paths = self.enumerate_paths(
            state=state, operation=operation, decision_id=decision_id
        )
        masses: dict[str, Fraction] = {}
        path_keys: dict[str, list[str | None]] = {}
        terminals: dict[str, ItemState] = {}
        for path in paths:
            key = path.terminal_state_hash
            masses[key] = masses.get(key, Fraction(0, 1)) + Fraction(
                path.probability_numerator, path.probability_denominator
            )
            path_keys.setdefault(key, []).append(path.path_key)
            terminals[key] = path.terminal_state
        return tuple(
            ExactFractureTerminal(
                terminal_state=terminals[key],
                terminal_state_hash=key,
                path_count=len(path_keys[key]),
                path_keys=tuple(sorted(path_keys[key], key=lambda value: value or "")),
                probability_numerator=masses[key].numerator,
                probability_denominator=masses[key].denominator,
            )
            for key in sorted(masses)
        )

    def sample_once(
        self,
        *,
        state: ItemState,
        operation: FractureOperation,
        decision_source: RecordingDecisionSource,
        sample_index: int,
        run_id: str,
        decision_id: str | None = None,
    ) -> FractureTrajectory:
        pool = self.build_pool(state, operation)
        pre_hash = state.state_hash()
        if not pool.candidates:
            _assert_no_transition_unchanged(state, state)
            return FractureTrajectory(
                sample_index=sample_index,
                outcome="no_transition_no_consumption",
                pre_state_hash=pre_hash,
                post_state_hash=pre_hash,
                decision_id=None,
                selected_candidate_key=None,
                selected_mod_id=None,
                selected_duplicate_ordinal=None,
                selected_was_crafted=None,
                candidate_count=0,
                candidate_digest=None,
                pool_fingerprint=pool.result_fingerprint,
                no_transition_reason=pool.empty_reason,
            )

        selected_decision_id = decision_id or (
            f"{run_id}.sample_{sample_index}.step_0."
            f"{operation.operation_id}.{operation.mode_id}"
        )
        decision = decision_source.choose_one(selected_decision_id, pool.candidates)
        selected = _metadata_by_candidate_key(pool)[decision.selected.key]
        terminal = _fracture_modifier_instance(state, selected)
        _assert_fracture_transition(state, terminal, selected, self.static)
        return FractureTrajectory(
            sample_index=sample_index,
            outcome="applied",
            pre_state_hash=pre_hash,
            post_state_hash=terminal.state_hash(),
            decision_id=decision.record.decision_id,
            selected_candidate_key=decision.selected.key,
            selected_mod_id=selected.mod_id,
            selected_duplicate_ordinal=selected.duplicate_ordinal,
            selected_was_crafted=selected.crafted,
            candidate_count=decision.record.candidate_count,
            candidate_digest=decision.record.candidate_digest,
            pool_fingerprint=pool.result_fingerprint,
            no_transition_reason=None,
        )

    def run(
        self,
        *,
        initial_state: ItemState,
        operation: FractureOperation,
        seed: int,
        sample_count: int,
        run_id: str,
    ) -> FractureRunResult:
        if (
            not isinstance(sample_count, int)
            or isinstance(sample_count, bool)
            or sample_count < 0
        ):
            raise SamplingContractDefect(
                "sample_count must be a non-negative non-bool integer"
            )
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
            "schema_version": M46A_FRACTURE_SCHEMA_VERSION,
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
        result_hash = sha256_canonical(payload, schema_version=1)
        return FractureRunResult(
            schema_version=M46A_FRACTURE_SCHEMA_VERSION,
            run_id=run_id,
            seed=seed,
            sample_count=sample_count,
            mode_id=operation.mode_id,
            operation_id=operation.operation_id,
            rng_stream_version=RNG_STREAM_VERSION,
            sampling_algorithm_id=SAMPLING_ALGORITHM_ID,
            source_fingerprint=self.static.source_fingerprint,
            semantic_fingerprint=self.static.semantic_fingerprint,
            code_version=self.code_version,
            trajectories=trajectories,
            decisions=source.records,
            result_hash=result_hash,
        )


def _fracture_precondition_failure(
    state: ItemState,
    operation: FractureOperation,
    static: StaticGameData,
) -> str | None:
    if state.item_class != "quarterstaff" or state.item_class != operation.item_class:
        return "unsupported_item_class"
    if state.rarity is not Rarity.RARE:
        return "rare_input_required"
    installed_count = len(state.modifiers) + int(
        state.unrevealed_desecrated is not None
    )
    if installed_count < 4:
        return "at_least_four_explicit_modifiers_required"
    if any(instance.fractured for instance in state.modifiers):
        return "existing_fractured_modifier_forbidden"
    if any(instance.desecrated for instance in state.modifiers):
        return "desecrated_modifier_state_forbidden"
    if any(instance.mod_id not in static.modifier_index for instance in state.modifiers):
        return "unknown_installed_modifier"
    if not validate_item_state(state, static).ok:
        return "invalid_source_state"
    return None


def _validate_operation_definition(operation: FractureOperation) -> None:
    if operation.operation_id != FRACTURING_ORB_OPERATION_ID:
        raise M46AFractureInvariantViolation(
            f"unsupported operation_id: {operation.operation_id}"
        )
    if operation.item_class != "quarterstaff":
        raise M46AFractureInvariantViolation(
            "M46-A admits quarterstaff Fracture only"
        )
    if operation.semantics_version != M46A_FRACTURE_SEMANTICS_VERSION:
        raise M46AFractureInvariantViolation("fracture semantics version mismatch")


def _empty_pool(
    state: ItemState, operation: FractureOperation, reason: str
) -> FracturePoolResult:
    return FracturePoolResult(
        candidates=(),
        metadata=(),
        candidate_digest=None,
        result_fingerprint=_pool_fingerprint(state, operation, (), reason),
        empty_reason=reason,
    )


def _pool_fingerprint(
    state: ItemState,
    operation: FractureOperation,
    metadata: tuple[FractureCandidateMetadata, ...],
    reason: str | None,
) -> str:
    return sha256_canonical(
        {
            "semantics_version": operation.semantics_version,
            "operation_id": operation.operation_id,
            "mode_id": operation.mode_id,
            "pre_state_hash": state.state_hash(),
            "candidate_keys": [row.candidate_key for row in metadata],
            "empty_reason": reason,
        },
        schema_version=1,
    )


def _metadata_by_candidate_key(
    pool: FracturePoolResult,
) -> dict[str, FractureCandidateMetadata]:
    return {row.candidate_key: row for row in pool.metadata}


def _validate_fracture_pool(
    pool: FracturePoolResult, static: StaticGameData
) -> None:
    metadata = _metadata_by_candidate_key(pool)
    if {candidate.key for candidate in pool.candidates} != set(metadata):
        raise M46AFractureInvariantViolation("fracture candidate metadata mismatch")
    if not pool.candidates:
        if pool.empty_reason is None:
            raise M46AFractureInvariantViolation(
                "empty Fracture pool requires an explicit reason"
            )
        return
    if pool.empty_reason is not None:
        raise M46AFractureInvariantViolation(
            "non-empty Fracture pool cannot declare an empty reason"
        )
    for candidate in pool.candidates:
        row = metadata[candidate.key]
        if candidate.weight != 1:
            raise M46AFractureInvariantViolation(
                "Fracture candidates must use uniform unit weight"
            )
        if row.fractured or row.desecrated:
            raise M46AFractureInvariantViolation(
                f"ineligible candidate leaked into Fracture pool: {candidate.key}"
            )
        if row.mod_id not in static.modifier_index:
            raise M46AFractureInvariantViolation(
                f"unknown modifier leaked into Fracture pool: {row.mod_id}"
            )


def _fracture_modifier_instance(
    state: ItemState, selected: FractureCandidateMetadata
) -> ItemState:
    seen = 0
    changed = False
    output: list[ModifierInstance] = []
    for instance in state.modifiers:
        if _instance_identity(instance) == (
            selected.mod_id,
            selected.crafted,
            selected.desecrated,
            selected.fractured,
        ):
            if seen == selected.duplicate_ordinal:
                if instance.fractured or instance.desecrated:
                    raise M46AFractureInvariantViolation(
                        "attempted to fracture an ineligible modifier"
                    )
                output.append(replace(instance, fractured=True))
                changed = True
                seen += 1
                continue
            seen += 1
        output.append(instance)
    if not changed:
        raise M46AFractureInvariantViolation(
            f"selected Fracture candidate not found: {selected.candidate_key}"
        )
    return state.with_modifiers(tuple(output))


def _assert_fracture_transition(
    pre_state: ItemState,
    post_state: ItemState,
    selected: FractureCandidateMetadata,
    static: StaticGameData,
) -> None:
    if pre_state.with_modifiers(post_state.modifiers) != post_state:
        raise M46AFractureInvariantViolation(
            "Fracture changed item state outside installed modifiers"
        )
    if len(pre_state.modifiers) != len(post_state.modifiers):
        raise M46AFractureInvariantViolation(
            "Fracture must preserve installed modifier count"
        )
    pre_counts = Counter(_instance_identity(row) for row in pre_state.modifiers)
    post_counts = Counter(_instance_identity(row) for row in post_state.modifiers)
    original = (
        selected.mod_id,
        selected.crafted,
        selected.desecrated,
        selected.fractured,
    )
    fractured = (
        selected.mod_id,
        selected.crafted,
        selected.desecrated,
        True,
    )
    expected = pre_counts.copy()
    expected[original] -= 1
    if expected[original] == 0:
        del expected[original]
    expected[fractured] += 1
    if post_counts != expected:
        raise M46AFractureInvariantViolation(
            "Fracture must change exactly the selected instance flag"
        )
    if sum(instance.fractured for instance in post_state.modifiers) != 1:
        raise M46AFractureInvariantViolation(
            "Fracture must create exactly one fractured modifier"
        )
    if selected.mod_id not in static.modifier_index:
        raise M46AFractureInvariantViolation(
            f"fractured modifier is absent from canonical index: {selected.mod_id}"
        )


def _assert_no_transition_unchanged(
    pre_state: ItemState, post_state: ItemState
) -> None:
    if pre_state != post_state or pre_state.state_hash() != post_state.state_hash():
        raise M46AFractureInvariantViolation("no-transition mutated item state")


def _instance_identity(instance: ModifierInstance) -> tuple[str, bool, bool, bool]:
    return (
        instance.mod_id,
        instance.crafted,
        instance.desecrated,
        instance.fractured,
    )


__all__ = [
    "FRACTURING_ORB_OPERATION_ID",
    "M46A_FIXED_SEEDS",
    "M46A_FRACTURE_SCHEMA_VERSION",
    "M46A_FRACTURE_SEMANTICS_VERSION",
    "M46A_SAMPLE_TIERS",
    "ExactFracturePath",
    "ExactFractureTerminal",
    "FractureCandidateMetadata",
    "FractureHarness",
    "FractureOperation",
    "FracturePoolResult",
    "FractureRunResult",
    "FractureTrajectory",
    "M46AFractureError",
    "M46AFractureInvariantViolation",
    "build_fracture_pool",
]
