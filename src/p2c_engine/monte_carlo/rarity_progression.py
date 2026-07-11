from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable, Mapping
from dataclasses import dataclass, replace
from fractions import Fraction
from typing import Any

from p2c_engine.canonical.hashes import sha256_canonical
from p2c_engine.decisions import RecordingDecisionSource, SeededDecisionSource
from p2c_engine.domain.decision import DecisionRecord
from p2c_engine.domain.defects import SamplingContractDefect
from p2c_engine.domain.enums import Rarity, Side
from p2c_engine.domain.item_state import ItemState
from p2c_engine.domain.pool_building import PoolBuildResult
from p2c_engine.domain.versions import RNG_STREAM_VERSION, SAMPLING_ALGORITHM_ID
from p2c_engine.legality.capacity import capacity_snapshot
from p2c_engine.legality.pool_builders import OrdinaryAddPoolRequest, build_ordinary_add_pool
from p2c_engine.sampling.exact import branch_options
from p2c_engine.static_data.game_data import StaticGameData

from .ordinary_add import (
    M32_VALUE_POLICY,
    M32InvariantViolation,
    M32MonteCarloError,
    _append_ordinary_modifier,
    _assert_capacity,
    _assert_duplicate_family_and_groups,
    _assert_fractured_modifiers_unchanged,
)


M40A_SCHEMA_VERSION = "p2c.m40a.rarity_progression_single_add.v1"
M40A_SEMANTICS_VERSION = "p2c.m40a.rarity_progression.project_model.v1"
M40A_OPERATION_IDS = frozenset(
    {
        "transmutation",
        "greater_transmutation",
        "perfect_transmutation",
        "augmentation",
        "greater_augmentation",
        "perfect_augmentation",
        "regal",
        "greater_regal",
        "perfect_regal",
        "exalted",
    }
)
M40A_OPERATION_GROUPS = {
    "transmutation": "transmutation",
    "greater_transmutation": "transmutation",
    "perfect_transmutation": "transmutation",
    "augmentation": "augmentation",
    "greater_augmentation": "augmentation",
    "perfect_augmentation": "augmentation",
    "regal": "regal",
    "greater_regal": "regal",
    "perfect_regal": "regal",
    "exalted": "exalted",
}
ACCEPTED_RUNTIME_STATUS = "accepted_executable_runtime"


class M40ARarityProgressionError(M32MonteCarloError):
    """Base error for the M40-A data-driven catalog single-add runtime."""


class M40ARarityProgressionInvariantViolation(
    M40ARarityProgressionError, M32InvariantViolation
):
    """Raised when an admitted catalog row or transition violates M40-A."""


@dataclass(frozen=True, slots=True)
class CatalogSingleAddPrecondition:
    kind: str
    operator: str
    value: int | str


@dataclass(frozen=True, slots=True)
class CatalogSingleAddOperation:
    mode_id: str
    operation_id: str
    item_class: str
    input_rarities: tuple[Rarity, ...]
    pool_build_rarity: Rarity
    output_rarity: Rarity
    preconditions: tuple[CatalogSingleAddPrecondition, ...] = ()
    mml: int | None = None
    side_filter: Side | None = None
    active_modifier_ids: tuple[str, ...] = ()
    add_count: int = 1
    semantics_version: str = M40A_SEMANTICS_VERSION


@dataclass(frozen=True, slots=True)
class CatalogSingleAddExactPath:
    path_key: str | None
    outcome: str
    terminal_state_hash: str
    selected_mod_id: str | None
    candidate_count: int
    candidate_digest: str | None
    no_transition_reason: str | None
    probability_numerator: int
    probability_denominator: int


@dataclass(frozen=True, slots=True)
class CatalogSingleAddExactTerminal:
    terminal_state_hash: str
    probability_numerator: int
    probability_denominator: int
    path_count: int
    path_keys: tuple[str | None, ...]


@dataclass(frozen=True, slots=True)
class CatalogSingleAddTrajectory:
    sample_index: int
    outcome: str
    operation_id: str
    pre_state_hash: str
    post_state_hash: str
    source_rarity: str
    pool_build_rarity: str
    output_rarity: str
    decision_id: str | None
    selected_mod_id: str | None
    candidate_count: int
    candidate_digest: str | None
    no_transition_reason: str | None

    def public_payload(self) -> dict[str, object]:
        return {
            "sample_index": self.sample_index,
            "outcome": self.outcome,
            "operation_id": self.operation_id,
            "pre_state_hash": self.pre_state_hash,
            "post_state_hash": self.post_state_hash,
            "source_rarity": self.source_rarity,
            "pool_build_rarity": self.pool_build_rarity,
            "output_rarity": self.output_rarity,
            "decision_id": self.decision_id,
            "selected_mod_id": self.selected_mod_id,
            "candidate_count": self.candidate_count,
            "candidate_digest": self.candidate_digest,
            "no_transition_reason": self.no_transition_reason,
        }


@dataclass(frozen=True, slots=True)
class CatalogSingleAddRunResult:
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
    trajectories: tuple[CatalogSingleAddTrajectory, ...]
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
            "terminal_state_hash_count": len(
                {trajectory.post_state_hash for trajectory in self.trajectories}
            ),
            "result_hash": self.result_hash,
        }


PoolBuilder = Callable[[OrdinaryAddPoolRequest, StaticGameData], PoolBuildResult]


class CatalogSingleAddHarness:
    """Exact and seeded-MC runtime for the admitted M40-A one-add family.

    Target-rarity operations build the accepted ordinary-add pool against an
    isolated working state. The original state is never mutated, and target
    rarity plus the selected modifier become visible only in the terminal state.
    """

    def __init__(
        self,
        *,
        static: StaticGameData,
        pool_builder: PoolBuilder = build_ordinary_add_pool,
        code_version: str = "p2c.m40a.dev",
    ) -> None:
        self.static = static
        self.pool_builder = pool_builder
        self.code_version = code_version

    def build_pool(
        self, state: ItemState, operation: CatalogSingleAddOperation
    ) -> PoolBuildResult:
        self._validate_operation_contract(operation)
        failure = self._precondition_failure(state, operation)
        if failure is not None:
            raise M40ARarityProgressionInvariantViolation(
                f"cannot build pool after failed precondition: {failure}"
            )
        working_state = self._working_state(state, operation)
        request = OrdinaryAddPoolRequest(
            item_class=operation.item_class,
            state=working_state,
            side_filter=operation.side_filter,
            mml=operation.mml,
        )
        return self.pool_builder(request, self.static)

    def enumerate_paths(
        self,
        *,
        initial_state: ItemState,
        operation: CatalogSingleAddOperation,
        decision_id: str,
    ) -> tuple[CatalogSingleAddExactPath, ...]:
        self._validate_operation_contract(operation)
        precondition_failure = self._precondition_failure(initial_state, operation)
        if precondition_failure is not None:
            return (self._no_transition_path(initial_state, precondition_failure),)

        pool = self.build_pool(initial_state, operation)
        if not pool.candidates:
            return (
                self._no_transition_path(
                    initial_state,
                    pool.empty_reason or "ordinary_add_pool_exhausted",
                    candidate_digest=pool.candidate_digest,
                ),
            )

        working_state = self._working_state(initial_state, operation)
        paths: list[CatalogSingleAddExactPath] = []
        for option in branch_options(decision_id, pool.candidates):
            terminal_state = _append_ordinary_modifier(working_state, option.selected_key)
            self._assert_applied_transition(initial_state, terminal_state, operation)
            paths.append(
                CatalogSingleAddExactPath(
                    path_key=option.selected_key,
                    outcome="applied",
                    terminal_state_hash=terminal_state.state_hash(),
                    selected_mod_id=option.selected_key,
                    candidate_count=len(pool.candidates),
                    candidate_digest=option.candidate_digest,
                    no_transition_reason=None,
                    probability_numerator=option.probability_numerator,
                    probability_denominator=option.probability_denominator,
                )
            )
        _assert_exact_mass_one(paths)
        return tuple(paths)

    def enumerate_terminal_distribution(
        self,
        *,
        initial_state: ItemState,
        operation: CatalogSingleAddOperation,
        decision_id: str,
    ) -> tuple[CatalogSingleAddExactTerminal, ...]:
        paths = self.enumerate_paths(
            initial_state=initial_state,
            operation=operation,
            decision_id=decision_id,
        )
        masses: dict[str, Fraction] = defaultdict(Fraction)
        path_keys: dict[str, list[str | None]] = defaultdict(list)
        for path in paths:
            masses[path.terminal_state_hash] += Fraction(
                path.probability_numerator, path.probability_denominator
            )
            path_keys[path.terminal_state_hash].append(path.path_key)
        terminals = tuple(
            CatalogSingleAddExactTerminal(
                terminal_state_hash=terminal_hash,
                probability_numerator=mass.numerator,
                probability_denominator=mass.denominator,
                path_count=len(path_keys[terminal_hash]),
                path_keys=tuple(
                    sorted(path_keys[terminal_hash], key=lambda value: "" if value is None else value)
                ),
            )
            for terminal_hash, mass in sorted(masses.items())
        )
        if sum(
            (
                Fraction(row.probability_numerator, row.probability_denominator)
                for row in terminals
            ),
            Fraction(0, 1),
        ) != Fraction(1, 1):
            raise M40ARarityProgressionInvariantViolation(
                "M40-A exact terminal mass does not sum to one"
            )
        return terminals

    def sample_once(
        self,
        *,
        state: ItemState,
        operation: CatalogSingleAddOperation,
        decision_source: RecordingDecisionSource,
        sample_index: int,
        run_id: str,
    ) -> CatalogSingleAddTrajectory:
        self._validate_operation_contract(operation)
        pre_hash = state.state_hash()
        precondition_failure = self._precondition_failure(state, operation)
        if precondition_failure is not None:
            return self._no_transition_trajectory(
                state, operation, sample_index, precondition_failure
            )

        pool = self.build_pool(state, operation)
        if not pool.candidates:
            return self._no_transition_trajectory(
                state,
                operation,
                sample_index,
                pool.empty_reason or "ordinary_add_pool_exhausted",
                candidate_digest=pool.candidate_digest,
            )

        decision_id = (
            f"{run_id}.sample_{sample_index}.step_0."
            f"{operation.operation_id}.{operation.mode_id}"
        )
        decision = decision_source.choose_one(decision_id, pool.candidates)
        terminal_state = _append_ordinary_modifier(
            self._working_state(state, operation), decision.selected.key
        )
        self._assert_applied_transition(state, terminal_state, operation)
        return CatalogSingleAddTrajectory(
            sample_index=sample_index,
            outcome="applied",
            operation_id=operation.operation_id,
            pre_state_hash=pre_hash,
            post_state_hash=terminal_state.state_hash(),
            source_rarity=state.rarity.value,
            pool_build_rarity=operation.pool_build_rarity.value,
            output_rarity=operation.output_rarity.value,
            decision_id=decision.record.decision_id,
            selected_mod_id=decision.selected.key,
            candidate_count=decision.record.candidate_count,
            candidate_digest=decision.record.candidate_digest,
            no_transition_reason=None,
        )

    def run(
        self,
        *,
        initial_state: ItemState,
        operation: CatalogSingleAddOperation,
        seed: int,
        sample_count: int,
        run_id: str,
    ) -> CatalogSingleAddRunResult:
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
            "schema_version": M40A_SCHEMA_VERSION,
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
            "trajectories": [trajectory.public_payload() for trajectory in trajectories],
            "decisions": list(source.records),
        }
        return CatalogSingleAddRunResult(
            schema_version=M40A_SCHEMA_VERSION,
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
            result_hash=sha256_canonical(payload, schema_version=1),
        )

    def _working_state(
        self, state: ItemState, operation: CatalogSingleAddOperation
    ) -> ItemState:
        return replace(state, rarity=operation.pool_build_rarity)

    def _precondition_failure(
        self, state: ItemState, operation: CatalogSingleAddOperation
    ) -> str | None:
        if state.item_class != operation.item_class:
            return "item_class_mismatch"
        _assert_known_installed_modifiers(state, self.static)
        if state.rarity not in operation.input_rarities:
            return "invalid_source_rarity"
        capacity = capacity_snapshot(state, self.static)
        if (
            capacity.prefix_used > capacity.prefix_capacity
            or capacity.suffix_used > capacity.suffix_capacity
            or capacity.total_used > capacity.total_capacity
        ):
            return "source_capacity_invalid"
        for precondition in operation.preconditions:
            if precondition.kind == "occupied_explicit_slots":
                if not (
                    precondition.operator == "<"
                    and isinstance(precondition.value, int)
                    and capacity.total_used < precondition.value
                ):
                    return "occupied_explicit_slots_precondition_failed"
            elif precondition.kind == "free_explicit_slots_after_side_filter":
                required = (
                    operation.add_count
                    if precondition.value == "resolved_add_count"
                    else None
                )
                if operation.side_filter == Side.PREFIX:
                    free_total = capacity.prefix_capacity - capacity.prefix_used
                elif operation.side_filter == Side.SUFFIX:
                    free_total = capacity.suffix_capacity - capacity.suffix_used
                else:
                    free_total = capacity.total_capacity - capacity.total_used
                if not (
                    precondition.operator == ">="
                    and required is not None
                    and free_total >= required
                ):
                    return "free_explicit_slots_precondition_failed"
            else:
                raise M40ARarityProgressionInvariantViolation(
                    f"unsupported compiled precondition: {precondition.kind}"
                )
        return None

    def _validate_operation_contract(self, operation: CatalogSingleAddOperation) -> None:
        if operation.semantics_version != M40A_SEMANTICS_VERSION:
            raise M40ARarityProgressionInvariantViolation(
                "M40-A catalog single-add semantics version mismatch"
            )
        if operation.add_count not in {1, 2}:
            raise M40ARarityProgressionInvariantViolation(
                "catalog add_count must be one or two"
            )
        if operation.operation_id not in M40A_OPERATION_IDS:
            raise M40ARarityProgressionInvariantViolation(
                f"unsupported M40-A operation_id: {operation.operation_id}"
            )
        row = _operation_row(self.static.operations, operation.operation_id)
        if row is None:
            raise M40ARarityProgressionInvariantViolation(
                f"missing admitted operation row: {operation.operation_id}"
            )
        if row.get("runtime_admission_status") != ACCEPTED_RUNTIME_STATUS:
            raise M40ARarityProgressionInvariantViolation(
                f"operation is not executable-admitted: {operation.operation_id}"
            )
        if row.get("group") != M40A_OPERATION_GROUPS[operation.operation_id]:
            raise M40ARarityProgressionInvariantViolation(
                f"M40-A operation group mismatch: {operation.operation_id}"
            )

        transition = row.get("transition")
        remove = transition.get("remove") if isinstance(transition, Mapping) else None
        add = transition.get("add") if isinstance(transition, Mapping) else None
        if (
            not isinstance(transition, Mapping)
            or transition.get("atomic") is not True
            or not isinstance(remove, Mapping)
            or remove.get("kind") != "none"
            or not isinstance(add, Mapping)
            or add.get("kind") != "ordinary_weighted"
            or add.get("count") != 1
            or add.get("side_filter") not in (None,)
        ):
            raise M40ARarityProgressionInvariantViolation(
                f"unsupported M40-A transition shape: {operation.operation_id}"
            )

        expected_inputs = _rarity_tuple(row.get("input_rarity"), operation.operation_id)
        expected_output = _rarity(transition.get("output_rarity"), operation.operation_id)
        expected_pool = _rarity(
            transition.get("pool_build_rarity", expected_output.value),
            operation.operation_id,
        )
        expected_mml = _mml(add.get("mml"), operation.operation_id)
        expected_preconditions = _precondition_tuple(
            transition.get("preconditions"), operation.operation_id
        )
        if (
            operation.input_rarities != expected_inputs
            or operation.output_rarity != expected_output
            or operation.pool_build_rarity != expected_pool
            or operation.preconditions != expected_preconditions
            or operation.mml != expected_mml
        ):
            raise M40ARarityProgressionInvariantViolation(
                f"operation plan does not match admitted catalog row: {operation.operation_id}"
            )
        from p2c_engine.operations.omen import M45AOmenAdmissionError, compile_omen_effects

        try:
            effects = compile_omen_effects(
                self.static.omens,
                operation_group=M40A_OPERATION_GROUPS[operation.operation_id],
                active_modifier_ids=operation.active_modifier_ids,
            )
        except M45AOmenAdmissionError as exc:
            raise M40ARarityProgressionInvariantViolation(str(exc)) from exc
        if (
            effects.add_count != operation.add_count
            or effects.add_side_filter != operation.side_filter
        ):
            raise M40ARarityProgressionInvariantViolation(
                "catalog single-add Omen effect plan mismatch"
            )
        if operation.add_count != 1:
            raise M40ARarityProgressionInvariantViolation(
                "multi-add modifier plans require the accepted M45-A atomic harness"
            )

    def _assert_applied_transition(
        self,
        pre_state: ItemState,
        terminal_state: ItemState,
        operation: CatalogSingleAddOperation,
    ) -> None:
        if terminal_state.rarity != operation.output_rarity:
            raise M40ARarityProgressionInvariantViolation(
                "M40-A terminal rarity does not match operation output rarity"
            )
        if len(terminal_state.modifiers) != len(pre_state.modifiers) + 1:
            raise M40ARarityProgressionInvariantViolation(
                "M40-A applied transition must add exactly one modifier"
            )
        _assert_fractured_modifiers_unchanged(
            pre_state, terminal_state, self.static.modifier_index
        )
        _assert_capacity(terminal_state, self.static.modifier_index)
        _assert_duplicate_family_and_groups(terminal_state, self.static.modifier_index)

    def _no_transition_path(
        self,
        state: ItemState,
        reason: str,
        *,
        candidate_digest: str | None = None,
    ) -> CatalogSingleAddExactPath:
        return CatalogSingleAddExactPath(
            path_key=None,
            outcome="no_transition_no_consumption",
            terminal_state_hash=state.state_hash(),
            selected_mod_id=None,
            candidate_count=0,
            candidate_digest=candidate_digest,
            no_transition_reason=reason,
            probability_numerator=1,
            probability_denominator=1,
        )

    def _no_transition_trajectory(
        self,
        state: ItemState,
        operation: CatalogSingleAddOperation,
        sample_index: int,
        reason: str,
        *,
        candidate_digest: str | None = None,
    ) -> CatalogSingleAddTrajectory:
        state_hash = state.state_hash()
        return CatalogSingleAddTrajectory(
            sample_index=sample_index,
            outcome="no_transition_no_consumption",
            operation_id=operation.operation_id,
            pre_state_hash=state_hash,
            post_state_hash=state_hash,
            source_rarity=state.rarity.value,
            pool_build_rarity=operation.pool_build_rarity.value,
            output_rarity=operation.output_rarity.value,
            decision_id=None,
            selected_mod_id=None,
            candidate_count=0,
            candidate_digest=candidate_digest,
            no_transition_reason=reason,
        )


def _operation_row(operations: Any, operation_id: str) -> Mapping[str, Any] | None:
    if not isinstance(operations, Mapping):
        return None
    for row in operations.get("operations") or ():
        if isinstance(row, Mapping) and row.get("operation_id") == operation_id:
            return row
    return None


def _rarity(value: Any, operation_id: str) -> Rarity:
    try:
        return Rarity(value)
    except (TypeError, ValueError) as exc:
        raise M40ARarityProgressionInvariantViolation(
            f"invalid rarity in admitted row {operation_id}: {value!r}"
        ) from exc


def _rarity_tuple(value: Any, operation_id: str) -> tuple[Rarity, ...]:
    if not isinstance(value, (list, tuple)) or not value:
        raise M40ARarityProgressionInvariantViolation(
            f"invalid input_rarity in admitted row: {operation_id}"
        )
    return tuple(_rarity(entry, operation_id) for entry in value)


def _mml(value: Any, operation_id: str) -> int | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise M40ARarityProgressionInvariantViolation(
            f"invalid MML in admitted row {operation_id}: {value!r}"
        )
    return value


def _precondition_tuple(
    value: Any, operation_id: str
) -> tuple[CatalogSingleAddPrecondition, ...]:
    if value is None:
        return ()
    if not isinstance(value, (list, tuple)):
        raise M40ARarityProgressionInvariantViolation(
            f"invalid preconditions in admitted row: {operation_id}"
        )
    output: list[CatalogSingleAddPrecondition] = []
    for row in value:
        if not isinstance(row, Mapping):
            raise M40ARarityProgressionInvariantViolation(
                f"invalid precondition in admitted row: {operation_id}"
            )
        precondition = CatalogSingleAddPrecondition(
            kind=row.get("type"),
            operator=row.get("operator"),
            value=row.get("value"),
        )
        if (
            precondition.kind == "occupied_explicit_slots"
            and precondition.operator == "<"
            and isinstance(precondition.value, int)
            and not isinstance(precondition.value, bool)
            and precondition.value > 0
        ):
            output.append(precondition)
            continue
        if (
            precondition.kind == "free_explicit_slots_after_side_filter"
            and precondition.operator == ">="
            and precondition.value == "resolved_add_count"
        ):
            output.append(precondition)
            continue
        raise M40ARarityProgressionInvariantViolation(
            f"unsupported precondition in admitted row: {operation_id} ({precondition!r})"
        )
    return tuple(output)


def _assert_known_installed_modifiers(state: ItemState, static: StaticGameData) -> None:
    for instance in state.modifiers:
        if instance.mod_id not in static.modifier_index:
            raise M40ARarityProgressionInvariantViolation(
                f"unknown installed mod_id: {instance.mod_id}"
            )


def _assert_exact_mass_one(paths: list[CatalogSingleAddExactPath]) -> None:
    mass = sum(
        (Fraction(path.probability_numerator, path.probability_denominator) for path in paths),
        Fraction(0, 1),
    )
    if mass != Fraction(1, 1):
        raise M40ARarityProgressionInvariantViolation(
            "M40-A exact path mass does not sum to one"
        )


__all__ = [
    "M40A_OPERATION_IDS",
    "M40A_SCHEMA_VERSION",
    "M40A_SEMANTICS_VERSION",
    "CatalogSingleAddExactPath",
    "CatalogSingleAddExactTerminal",
    "CatalogSingleAddHarness",
    "CatalogSingleAddOperation",
    "CatalogSingleAddPrecondition",
    "CatalogSingleAddRunResult",
    "CatalogSingleAddTrajectory",
    "M40ARarityProgressionError",
    "M40ARarityProgressionInvariantViolation",
]
