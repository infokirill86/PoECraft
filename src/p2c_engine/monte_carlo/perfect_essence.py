from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from p2c_engine.canonical.hashes import sha256_canonical
from p2c_engine.decisions import RecordingDecisionSource, SeededDecisionSource
from p2c_engine.domain.candidate import Candidate
from p2c_engine.domain.candidate_pool import pool_digest
from p2c_engine.domain.decision import DecisionRecord
from p2c_engine.domain.defects import SamplingContractDefect
from p2c_engine.domain.enums import Rarity, Side
from p2c_engine.domain.item_state import ItemState, ModifierInstance
from p2c_engine.domain.pool_building import PoolBuildResult, RemovalInstanceMetadata
from p2c_engine.domain.versions import RNG_STREAM_VERSION, SAMPLING_ALGORITHM_ID
from p2c_engine.legality.capacity import capacity_snapshot
from p2c_engine.legality.pool_builders import RemovalPoolRequest, build_removal_pool
from p2c_engine.legality.state_validation import validate_item_state
from p2c_engine.sampling.exact import branch_options
from p2c_engine.static_data.game_data import StaticGameData

from .annulment import (
    _assert_fractured_modifiers_unchanged,
    _metadata_by_candidate_key,
    _remove_modifier_instance,
    _validate_annulment_pool,
)
from .ordinary_add import M32InvariantViolation, M32MonteCarloError


M42A_SCHEMA_VERSION = "p2c.m42a.perfect_essence_quarterstaff.v1"
M42A_SEMANTICS_VERSION = "p2c.m42a.perfect_essence.project_model.v1"
M42A_CRAFTED_CAPACITY_POLICY = "crafted_count_zero_source_open"
M42A_REMOVAL_POLICY = "uniform_over_terminal_feasible_nonfractured_instances"
M42A_OPERATION_IDS = frozenset(
    {
        "perfect_essence_abrasion",
        "perfect_essence_flames",
        "perfect_essence_ice",
        "perfect_essence_electricity",
        "perfect_essence_battle",
        "perfect_essence_haste",
    }
)
ACCEPTED_RUNTIME_STATUS = "accepted_executable_runtime"


class M42APerfectEssenceError(M32MonteCarloError):
    """Base error for the M42-A Perfect Essence runtime."""


class M42APerfectEssenceInvariantViolation(
    M42APerfectEssenceError, M32InvariantViolation
):
    """Raised when M42-A data or execution violates the accepted contract."""


@dataclass(frozen=True, slots=True)
class PerfectEssenceOperation:
    mode_id: str
    operation_id: str
    item_class: str
    guaranteed_mod_id: str
    guaranteed_family_id: str
    guaranteed_side: Side
    input_rarities: tuple[Rarity, ...] = (Rarity.RARE,)
    output_rarity: Rarity = Rarity.RARE
    crafted: bool = True
    removal_side_filter: Side | None = None
    active_modifier_ids: tuple[str, ...] = ()
    semantics_version: str = M42A_SEMANTICS_VERSION


@dataclass(frozen=True, slots=True)
class PerfectEssenceFeasiblePool:
    candidates: tuple[Candidate, ...]
    removal_metadata: tuple[RemovalInstanceMetadata, ...]
    candidate_digest: str | None
    result_fingerprint: str
    base_pool_fingerprint: str | None
    target_side_was_full: bool
    empty_reason: str | None


@dataclass(frozen=True, slots=True)
class ExactPerfectEssencePath:
    path_key: str | None
    terminal_state_hash: str
    outcome: str
    selected_removal_candidate_key: str | None
    selected_mod_id: str | None
    selected_duplicate_ordinal: int | None
    guaranteed_mod_id: str | None
    candidate_count: int
    candidate_digest: str | None
    removal_pool_fingerprint: str
    no_transition_reason: str | None
    probability_numerator: int
    probability_denominator: int


@dataclass(frozen=True, slots=True)
class ExactPerfectEssenceTerminal:
    terminal_state_hash: str
    probability_numerator: int
    probability_denominator: int
    path_count: int
    path_keys: tuple[str | None, ...]


@dataclass(frozen=True, slots=True)
class PerfectEssenceTrajectory:
    sample_index: int
    outcome: str
    operation_id: str
    initial_state_hash: str
    terminal_state_hash: str
    decision_id: str | None
    selected_removal_candidate_key: str | None
    selected_mod_id: str | None
    selected_duplicate_ordinal: int | None
    guaranteed_mod_id: str | None
    candidate_count: int
    candidate_digest: str | None
    removal_pool_fingerprint: str
    no_transition_reason: str | None

    def public_payload(self) -> dict[str, object]:
        return {
            "sample_index": self.sample_index,
            "outcome": self.outcome,
            "operation_id": self.operation_id,
            "initial_state_hash": self.initial_state_hash,
            "terminal_state_hash": self.terminal_state_hash,
            "decision_id": self.decision_id,
            "selected_removal_candidate_key": self.selected_removal_candidate_key,
            "selected_mod_id": self.selected_mod_id,
            "selected_duplicate_ordinal": self.selected_duplicate_ordinal,
            "guaranteed_mod_id": self.guaranteed_mod_id,
            "candidate_count": self.candidate_count,
            "candidate_digest": self.candidate_digest,
            "removal_pool_fingerprint": self.removal_pool_fingerprint,
            "no_transition_reason": self.no_transition_reason,
        }


@dataclass(frozen=True, slots=True)
class PerfectEssenceRunResult:
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
    removal_policy: str
    crafted_capacity_policy: str
    trajectories: tuple[PerfectEssenceTrajectory, ...]
    decisions: tuple[DecisionRecord, ...]
    result_hash: str

    def public_summary(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "status": "PASS",
            "numeric_probability_free": True,
            "public_numeric_release": False,
            "probability_values_printed": False,
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
            "removal_policy": self.removal_policy,
            "crafted_capacity_policy": self.crafted_capacity_policy,
            "trajectory_count": len(self.trajectories),
            "decision_count": len(self.decisions),
            "terminal_state_hash_count": len(
                {row.terminal_state_hash for row in self.trajectories}
            ),
            "result_hash": self.result_hash,
        }


RemovalPoolBuilder = Callable[[RemovalPoolRequest, StaticGameData], PoolBuildResult]


class PerfectEssenceHarness:
    """Exact/oracle and seeded runtime for six admitted Perfect Essences."""

    def __init__(
        self,
        *,
        static: StaticGameData,
        removal_pool_builder: RemovalPoolBuilder = build_removal_pool,
        code_version: str = "p2c.m42a.dev",
    ) -> None:
        self.static = static
        self.removal_pool_builder = removal_pool_builder
        self.code_version = code_version

    def validate_operation_contract(self, operation: PerfectEssenceOperation) -> None:
        if operation.semantics_version != M42A_SEMANTICS_VERSION:
            raise M42APerfectEssenceInvariantViolation(
                "M42-A Perfect Essence semantics version mismatch"
            )
        if operation.operation_id not in M42A_OPERATION_IDS:
            raise M42APerfectEssenceInvariantViolation(
                f"unsupported M42-A operation_id: {operation.operation_id}"
            )
        if (
            operation.input_rarities != (Rarity.RARE,)
            or operation.output_rarity != Rarity.RARE
            or operation.crafted is not True
        ):
            raise M42APerfectEssenceInvariantViolation(
                f"invalid Perfect Essence operation shape: {operation.operation_id}"
            )

        row = _operation_row(self.static.operations, operation.operation_id)
        if row is None:
            raise M42APerfectEssenceInvariantViolation(
                f"missing Perfect Essence operation row: {operation.operation_id}"
            )
        if row.get("runtime_admission_status") != ACCEPTED_RUNTIME_STATUS:
            raise M42APerfectEssenceInvariantViolation(
                f"operation is not executable-admitted: {operation.operation_id}"
            )
        if row.get("group") != "perfect_essence" or row.get(
            "active_in_current_simulation"
        ) is not True:
            raise M42APerfectEssenceInvariantViolation(
                f"Perfect Essence activation mismatch: {operation.operation_id}"
            )

        transition = row.get("transition")
        remove = transition.get("remove") if isinstance(transition, Mapping) else None
        prevalidate = (
            transition.get("prevalidate") if isinstance(transition, Mapping) else None
        )
        required_prevalidate = {
            "family_absent",
            "crafted_count_zero",
            "feasible_removal_pool_nonempty",
        }
        if (
            not isinstance(transition, Mapping)
            or transition.get("atomic") is not True
            or transition.get("output_rarity") != "rare"
            or transition.get("crafted") is not True
            or not isinstance(remove, Mapping)
            or remove.get("kind") != "uniform_feasible_installed_instance"
            or remove.get("count") != 1
            or "fractured" not in (remove.get("exclude_flags") or ())
            or remove.get("selection") != "uniform"
            or remove.get("feasible_if")
            != "guaranteed_modifier_installable_after_removal"
            or set(prevalidate or ()) != required_prevalidate
        ):
            raise M42APerfectEssenceInvariantViolation(
                f"unsupported Perfect Essence transition shape: {operation.operation_id}"
            )

        output = _essence_output_row(self.static.essence_outputs, operation.operation_id)
        if output is None:
            raise M42APerfectEssenceInvariantViolation(
                f"missing Perfect Essence output row: {operation.operation_id}"
            )
        canonical = self.static.modifier_index.get(operation.guaranteed_mod_id)
        if canonical is None:
            raise M42APerfectEssenceInvariantViolation(
                "guaranteed modifier missing from canonical index: "
                f"{operation.guaranteed_mod_id}"
            )

        row_contract = (
            transition.get("guaranteed_mod_id"),
            transition.get("guaranteed_family_id"),
            transition.get("guaranteed_side"),
            transition.get("crafted"),
        )
        output_contract = (
            output.get("guaranteed_mod_id"),
            output.get("family_id"),
            output.get("side"),
            output.get("crafted"),
        )
        operation_contract = (
            operation.guaranteed_mod_id,
            operation.guaranteed_family_id,
            operation.guaranteed_side.value,
            operation.crafted,
        )
        canonical_contract = (
            canonical.mod_id,
            canonical.family_id,
            canonical.side.value,
            True,
        )
        if not (
            row_contract == output_contract == operation_contract == canonical_contract
        ):
            raise M42APerfectEssenceInvariantViolation(
                f"Perfect Essence canonical contract mismatch: {operation.operation_id}"
            )
        if canonical.static_category != "perfect_essence" or canonical.tier != 1:
            raise M42APerfectEssenceInvariantViolation(
                f"invalid canonical Perfect Essence modifier: {canonical.mod_id}"
            )
        if tuple(canonical.group_ids) != tuple(
            sorted(str(value) for value in (output.get("group_ids") or ()))
        ):
            raise M42APerfectEssenceInvariantViolation(
                f"Perfect Essence group contract mismatch: {operation.operation_id}"
            )
        if operation.item_class not in (output.get("item_classes") or ()):
            raise M42APerfectEssenceInvariantViolation(
                f"Perfect Essence output does not apply to item class: {operation.item_class}"
            )
        from p2c_engine.operations.omen import M45AOmenAdmissionError, compile_omen_effects

        try:
            effects = compile_omen_effects(
                self.static.omens,
                operation_group="perfect_essence",
                active_modifier_ids=operation.active_modifier_ids,
            )
        except M45AOmenAdmissionError as exc:
            raise M42APerfectEssenceInvariantViolation(str(exc)) from exc
        if effects.removal_side_filter != operation.removal_side_filter:
            raise M42APerfectEssenceInvariantViolation(
                "Perfect Essence Omen effect plan mismatch"
            )

    def build_feasible_pool(
        self,
        state: ItemState,
        operation: PerfectEssenceOperation,
    ) -> PerfectEssenceFeasiblePool:
        self.validate_operation_contract(operation)
        reason = self._precondition_failure(state, operation)
        if reason is not None:
            return self._empty_pool(state, operation, reason)

        base_pool = self.removal_pool_builder(
            RemovalPoolRequest(
                item_class=operation.item_class,
                state=state,
                side_filter=operation.removal_side_filter,
            ),
            self.static,
        )
        _validate_annulment_pool(base_pool)
        if not base_pool.candidates:
            return self._empty_pool(
                state,
                operation,
                base_pool.empty_reason or "removal_pool_exhausted",
                base_pool_fingerprint=base_pool.result_fingerprint,
            )

        metadata = _metadata_by_candidate_key(base_pool)
        feasible_candidates: list[Candidate] = []
        feasible_metadata: list[RemovalInstanceMetadata] = []
        for candidate in base_pool.candidates:
            selected = metadata[candidate.key]
            terminal = self._terminal_for_candidate(state, operation, selected)
            if terminal is None:
                continue
            feasible_candidates.append(Candidate(candidate.key, 1))
            feasible_metadata.append(selected)

        candidates = tuple(feasible_candidates)
        rows = tuple(feasible_metadata)
        target_side_was_full = self._target_side_free_slots(
            state, operation.guaranteed_side
        ) == 0
        reason = None if candidates else "feasible_removal_pool_exhausted"
        fingerprint = sha256_canonical(
            {
                "builder": "m42a_perfect_essence_feasible_removal_pool",
                "state_hash": state.state_hash(),
                "operation_id": operation.operation_id,
                "guaranteed_side": operation.guaranteed_side.value,
                "removal_side_filter": (
                    operation.removal_side_filter.value
                    if operation.removal_side_filter is not None
                    else None
                ),
                "removal_policy": M42A_REMOVAL_POLICY,
                "crafted_capacity_policy": M42A_CRAFTED_CAPACITY_POLICY,
                "base_pool_fingerprint": base_pool.result_fingerprint,
                "candidate_keys": [candidate.key for candidate in candidates],
                "empty_reason": reason,
            },
            schema_version=1,
        )
        return PerfectEssenceFeasiblePool(
            candidates=candidates,
            removal_metadata=rows,
            candidate_digest=pool_digest(candidates) if candidates else None,
            result_fingerprint=fingerprint,
            base_pool_fingerprint=base_pool.result_fingerprint,
            target_side_was_full=target_side_was_full,
            empty_reason=reason,
        )

    def enumerate_paths(
        self,
        *,
        initial_state: ItemState,
        operation: PerfectEssenceOperation,
        decision_id: str,
    ) -> tuple[ExactPerfectEssencePath, ...]:
        pool = self.build_feasible_pool(initial_state, operation)
        initial_hash = initial_state.state_hash()
        metadata = {row.candidate_key: row for row in pool.removal_metadata}
        if not pool.candidates:
            return (
                ExactPerfectEssencePath(
                    path_key=None,
                    terminal_state_hash=initial_hash,
                    outcome="no_transition_no_consumption",
                    selected_removal_candidate_key=None,
                    selected_mod_id=None,
                    selected_duplicate_ordinal=None,
                    guaranteed_mod_id=None,
                    candidate_count=0,
                    candidate_digest=None,
                    removal_pool_fingerprint=pool.result_fingerprint,
                    no_transition_reason=pool.empty_reason,
                    probability_numerator=1,
                    probability_denominator=1,
                ),
            )

        paths: list[ExactPerfectEssencePath] = []
        for option in branch_options(decision_id, pool.candidates):
            selected = metadata[option.selected_key]
            terminal = self._terminal_for_candidate(initial_state, operation, selected)
            if terminal is None:
                raise M42APerfectEssenceInvariantViolation(
                    "feasible removal candidate became invalid during exact execution"
                )
            self._assert_terminal_invariants(
                initial_state, terminal, operation, selected
            )
            paths.append(
                ExactPerfectEssencePath(
                    path_key=option.selected_key,
                    terminal_state_hash=terminal.state_hash(),
                    outcome="completed",
                    selected_removal_candidate_key=option.selected_key,
                    selected_mod_id=selected.mod_id,
                    selected_duplicate_ordinal=selected.duplicate_ordinal,
                    guaranteed_mod_id=operation.guaranteed_mod_id,
                    candidate_count=len(pool.candidates),
                    candidate_digest=option.candidate_digest,
                    removal_pool_fingerprint=pool.result_fingerprint,
                    no_transition_reason=None,
                    probability_numerator=option.probability_numerator,
                    probability_denominator=option.probability_denominator,
                )
            )
        self._assert_path_mass(paths)
        return tuple(paths)

    def enumerate_terminal_distribution(
        self,
        *,
        initial_state: ItemState,
        operation: PerfectEssenceOperation,
        decision_id: str,
    ) -> tuple[ExactPerfectEssenceTerminal, ...]:
        paths = self.enumerate_paths(
            initial_state=initial_state,
            operation=operation,
            decision_id=decision_id,
        )
        grouped: dict[str, Fraction] = {}
        keys: dict[str, list[str | None]] = {}
        for path in paths:
            grouped[path.terminal_state_hash] = grouped.get(
                path.terminal_state_hash, Fraction(0, 1)
            ) + Fraction(path.probability_numerator, path.probability_denominator)
            keys.setdefault(path.terminal_state_hash, []).append(path.path_key)
        terminals = tuple(
            ExactPerfectEssenceTerminal(
                terminal_state_hash=terminal_hash,
                probability_numerator=probability.numerator,
                probability_denominator=probability.denominator,
                path_count=len(keys[terminal_hash]),
                path_keys=tuple(
                    sorted(keys[terminal_hash], key=lambda value: value or "")
                ),
            )
            for terminal_hash, probability in sorted(grouped.items())
        )
        if sum(
            Fraction(row.probability_numerator, row.probability_denominator)
            for row in terminals
        ) != Fraction(1, 1):
            raise M42APerfectEssenceInvariantViolation(
                "M42-A terminal mass does not sum to 1"
            )
        return terminals

    def sample_once(
        self,
        *,
        initial_state: ItemState,
        operation: PerfectEssenceOperation,
        decision_source: RecordingDecisionSource,
        sample_index: int,
        run_id: str,
    ) -> PerfectEssenceTrajectory:
        pool = self.build_feasible_pool(initial_state, operation)
        initial_hash = initial_state.state_hash()
        if not pool.candidates:
            return PerfectEssenceTrajectory(
                sample_index=sample_index,
                outcome="no_transition_no_consumption",
                operation_id=operation.operation_id,
                initial_state_hash=initial_hash,
                terminal_state_hash=initial_hash,
                decision_id=None,
                selected_removal_candidate_key=None,
                selected_mod_id=None,
                selected_duplicate_ordinal=None,
                guaranteed_mod_id=None,
                candidate_count=0,
                candidate_digest=None,
                removal_pool_fingerprint=pool.result_fingerprint,
                no_transition_reason=pool.empty_reason,
            )

        decision_id = (
            f"{run_id}.sample_{sample_index}.step_0."
            f"{operation.operation_id}.{operation.mode_id}.remove"
        )
        decision = decision_source.choose_one(decision_id, pool.candidates)
        metadata = {row.candidate_key: row for row in pool.removal_metadata}
        selected = metadata[decision.selected.key]
        terminal = self._terminal_for_candidate(initial_state, operation, selected)
        if terminal is None:
            raise M42APerfectEssenceInvariantViolation(
                "feasible removal candidate became invalid during seeded execution"
            )
        self._assert_terminal_invariants(initial_state, terminal, operation, selected)
        return PerfectEssenceTrajectory(
            sample_index=sample_index,
            outcome="completed",
            operation_id=operation.operation_id,
            initial_state_hash=initial_hash,
            terminal_state_hash=terminal.state_hash(),
            decision_id=decision.record.decision_id,
            selected_removal_candidate_key=decision.selected.key,
            selected_mod_id=selected.mod_id,
            selected_duplicate_ordinal=selected.duplicate_ordinal,
            guaranteed_mod_id=operation.guaranteed_mod_id,
            candidate_count=decision.record.candidate_count,
            candidate_digest=decision.record.candidate_digest,
            removal_pool_fingerprint=pool.result_fingerprint,
            no_transition_reason=None,
        )

    def run(
        self,
        *,
        initial_state: ItemState,
        operation: PerfectEssenceOperation,
        seed: int,
        sample_count: int,
        run_id: str,
    ) -> PerfectEssenceRunResult:
        if (
            isinstance(sample_count, bool)
            or not isinstance(sample_count, int)
            or sample_count < 0
        ):
            raise SamplingContractDefect(
                "sample_count must be a non-negative non-bool integer"
            )
        decision_source = RecordingDecisionSource(SeededDecisionSource(seed))
        trajectories = tuple(
            self.sample_once(
                initial_state=initial_state,
                operation=operation,
                decision_source=decision_source,
                sample_index=index,
                run_id=run_id,
            )
            for index in range(sample_count)
        )
        payload = {
            "schema_version": M42A_SCHEMA_VERSION,
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
            "removal_policy": M42A_REMOVAL_POLICY,
            "crafted_capacity_policy": M42A_CRAFTED_CAPACITY_POLICY,
            "trajectories": [row.public_payload() for row in trajectories],
            "decisions": [record for record in decision_source.records],
        }
        return PerfectEssenceRunResult(
            schema_version=M42A_SCHEMA_VERSION,
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
            removal_policy=M42A_REMOVAL_POLICY,
            crafted_capacity_policy=M42A_CRAFTED_CAPACITY_POLICY,
            trajectories=trajectories,
            decisions=decision_source.records,
            result_hash=sha256_canonical(payload, schema_version=1),
        )

    def _precondition_failure(
        self,
        state: ItemState,
        operation: PerfectEssenceOperation,
    ) -> str | None:
        if state.item_class != operation.item_class:
            return "item_class_mismatch"
        if state.rarity not in operation.input_rarities:
            return "invalid_source_rarity"
        validation = validate_item_state(state, self.static)
        if not validation.ok:
            return "invalid_source_state"
        if capacity_snapshot(state, self.static).crafted_count != 0:
            return "crafted_count_not_zero"

        guaranteed = self.static.modifier_index[operation.guaranteed_mod_id]
        installed = [self.static.modifier_index[row.mod_id] for row in state.modifiers]
        if any(row.family_id == guaranteed.family_id for row in installed):
            return "guaranteed_family_present"
        installed_groups = {group for row in installed for group in row.group_ids}
        if not installed_groups.isdisjoint(guaranteed.group_ids):
            return "guaranteed_group_present"
        return None

    def _terminal_for_candidate(
        self,
        state: ItemState,
        operation: PerfectEssenceOperation,
        selected: RemovalInstanceMetadata,
    ) -> ItemState | None:
        if selected.fractured:
            raise M42APerfectEssenceInvariantViolation(
                "fractured modifier entered feasible removal evaluation"
            )
        post_removal = _remove_modifier_instance(state, selected)
        terminal = post_removal.with_modifiers(
            post_removal.modifiers
            + (
                ModifierInstance(
                    operation.guaranteed_mod_id,
                    crafted=True,
                    desecrated=False,
                    fractured=False,
                ),
            )
        )
        if not validate_item_state(terminal, self.static).ok:
            return None
        return terminal

    def _assert_terminal_invariants(
        self,
        initial_state: ItemState,
        terminal_state: ItemState,
        operation: PerfectEssenceOperation,
        selected: RemovalInstanceMetadata,
    ) -> None:
        if terminal_state.rarity != Rarity.RARE:
            raise M42APerfectEssenceInvariantViolation(
                "Perfect Essence terminal rarity must remain rare"
            )
        if len(terminal_state.modifiers) != len(initial_state.modifiers):
            raise M42APerfectEssenceInvariantViolation(
                "Perfect Essence must remove one and add one modifier atomically"
            )
        _assert_fractured_modifiers_unchanged(
            initial_state, terminal_state, self.static.modifier_index
        )
        expected = ModifierInstance(operation.guaranteed_mod_id, crafted=True)
        if terminal_state.modifiers[-1] != expected:
            raise M42APerfectEssenceInvariantViolation(
                "Perfect Essence did not install the exact guaranteed modifier"
            )
        if selected.fractured:
            raise M42APerfectEssenceInvariantViolation(
                "Perfect Essence selected a fractured modifier"
            )
        if not validate_item_state(terminal_state, self.static).ok:
            raise M42APerfectEssenceInvariantViolation(
                "Perfect Essence produced an invalid terminal state"
            )

    def _target_side_free_slots(self, state: ItemState, side: Side) -> int:
        capacity = capacity_snapshot(state, self.static)
        if side == Side.PREFIX:
            return capacity.prefix_capacity - capacity.prefix_used
        return capacity.suffix_capacity - capacity.suffix_used

    def _empty_pool(
        self,
        state: ItemState,
        operation: PerfectEssenceOperation,
        reason: str,
        *,
        base_pool_fingerprint: str | None = None,
    ) -> PerfectEssenceFeasiblePool:
        fingerprint = sha256_canonical(
            {
                "builder": "m42a_perfect_essence_feasible_removal_pool",
                "state_hash": state.state_hash(),
                "operation_id": operation.operation_id,
                "removal_policy": M42A_REMOVAL_POLICY,
                "crafted_capacity_policy": M42A_CRAFTED_CAPACITY_POLICY,
                "base_pool_fingerprint": base_pool_fingerprint,
                "candidate_keys": [],
                "empty_reason": reason,
            },
            schema_version=1,
        )
        return PerfectEssenceFeasiblePool(
            candidates=(),
            removal_metadata=(),
            candidate_digest=None,
            result_fingerprint=fingerprint,
            base_pool_fingerprint=base_pool_fingerprint,
            target_side_was_full=self._target_side_free_slots(
                state, operation.guaranteed_side
            )
            == 0
            if state.rarity == Rarity.RARE
            else False,
            empty_reason=reason,
        )

    @staticmethod
    def _assert_path_mass(paths: list[ExactPerfectEssencePath]) -> None:
        if sum(
            Fraction(path.probability_numerator, path.probability_denominator)
            for path in paths
        ) != Fraction(1, 1):
            raise M42APerfectEssenceInvariantViolation(
                "M42-A exact path mass does not sum to 1"
            )


def _operation_row(operations: Any, operation_id: str) -> Mapping[str, Any] | None:
    if not isinstance(operations, Mapping):
        return None
    for row in operations.get("operations") or ():
        if isinstance(row, Mapping) and row.get("operation_id") == operation_id:
            return row
    return None


def _essence_output_row(
    essence_outputs: Any, operation_id: str
) -> Mapping[str, Any] | None:
    if not isinstance(essence_outputs, Mapping):
        return None
    for row in essence_outputs.get("perfect") or ():
        if isinstance(row, Mapping) and row.get("operation_id") == operation_id:
            return row
    return None


__all__ = [
    "M42A_CRAFTED_CAPACITY_POLICY",
    "M42A_OPERATION_IDS",
    "M42A_REMOVAL_POLICY",
    "M42A_SCHEMA_VERSION",
    "M42A_SEMANTICS_VERSION",
    "ExactPerfectEssencePath",
    "ExactPerfectEssenceTerminal",
    "M42APerfectEssenceError",
    "M42APerfectEssenceInvariantViolation",
    "PerfectEssenceFeasiblePool",
    "PerfectEssenceHarness",
    "PerfectEssenceOperation",
    "PerfectEssenceRunResult",
    "PerfectEssenceTrajectory",
]
