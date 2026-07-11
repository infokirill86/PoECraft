from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
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
    OrdinaryAddOperation,
    _append_ordinary_modifier,
    _assert_capacity,
    _assert_duplicate_family_and_groups,
    _assert_fractured_modifiers_unchanged,
)
from .rarity_progression import CatalogSingleAddOperation


M45A_GREATER_EXALTATION_SCHEMA_VERSION = "p2c.m45a.greater_exaltation_atomic_two_add.v1"
M45A_GREATER_EXALTATION_SEMANTICS_VERSION = (
    "p2c.m45a.greater_exaltation.sequential_atomic.project_model.v1"
)
M45A_GREATER_EXALTATION_OMEN_ID = "greater_exaltation"
M45A_GREATER_EXALTATION_ADD_COUNT = 2
M45A_MAX_CANDIDATES_PER_POOL = 256
M45A_MAX_EXACT_PATHS = 65_536


class M45AGreaterExaltationError(M32MonteCarloError):
    pass


class M45AGreaterExaltationInvariantViolation(
    M45AGreaterExaltationError, M32InvariantViolation
):
    pass


class M45AGreaterExaltationCeilingExceeded(M45AGreaterExaltationError):
    def __init__(self, ceiling_name: str, limit: int, observed: int) -> None:
        super().__init__(
            f"M45-A Greater Exaltation ceiling exceeded: {ceiling_name} "
            f"limit={limit} observed={observed}"
        )
        self.ceiling_name = ceiling_name
        self.limit = limit
        self.observed = observed


GreaterExaltationOperation = OrdinaryAddOperation | CatalogSingleAddOperation
PoolBuilder = Callable[[OrdinaryAddPoolRequest, StaticGameData], PoolBuildResult]


@dataclass(frozen=True, slots=True)
class GreaterExaltationAddTrace:
    add_index: int
    pre_state_hash: str
    post_state_hash: str
    decision_id: str | None
    selected_mod_id: str | None
    candidate_count: int
    candidate_digest: str | None
    pool_fingerprint: str | None
    no_transition_reason: str | None

    def public_payload(self) -> dict[str, object]:
        return {
            "add_index": self.add_index,
            "pre_state_hash": self.pre_state_hash,
            "post_state_hash": self.post_state_hash,
            "decision_id": self.decision_id,
            "selected_mod_id": self.selected_mod_id,
            "candidate_count": self.candidate_count,
            "candidate_digest": self.candidate_digest,
            "pool_fingerprint": self.pool_fingerprint,
            "no_transition_reason": self.no_transition_reason,
        }


@dataclass(frozen=True, slots=True)
class GreaterExaltationExactPath:
    path_key: tuple[str, ...]
    terminal_state: ItemState
    terminal_state_hash: str
    outcome: str
    selected_mod_ids: tuple[str, ...]
    traces: tuple[GreaterExaltationAddTrace, ...]
    no_transition_reason: str | None
    probability_numerator: int
    probability_denominator: int


@dataclass(frozen=True, slots=True)
class GreaterExaltationExactTerminal:
    terminal_state_hash: str
    probability_numerator: int
    probability_denominator: int
    path_count: int
    path_keys: tuple[tuple[str, ...], ...]


@dataclass(frozen=True, slots=True)
class GreaterExaltationTrajectory:
    sample_index: int
    outcome: str
    initial_state_hash: str
    terminal_state_hash: str
    selected_mod_ids: tuple[str, ...]
    traces: tuple[GreaterExaltationAddTrace, ...]
    no_transition_reason: str | None

    def public_payload(self) -> dict[str, object]:
        return {
            "sample_index": self.sample_index,
            "outcome": self.outcome,
            "initial_state_hash": self.initial_state_hash,
            "terminal_state_hash": self.terminal_state_hash,
            "selected_mod_ids": self.selected_mod_ids,
            "traces": [trace.public_payload() for trace in self.traces],
            "no_transition_reason": self.no_transition_reason,
        }


@dataclass(frozen=True, slots=True)
class GreaterExaltationRunResult:
    schema_version: str
    run_id: str
    seed: int
    sample_count: int
    currency_id: str
    mode_id: str
    source_fingerprint: str
    semantic_fingerprint: str
    code_version: str
    trajectories: tuple[GreaterExaltationTrajectory, ...]
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
            "currency_id": self.currency_id,
            "mode_id": self.mode_id,
            "trajectory_count": len(self.trajectories),
            "decision_count": len(self.decisions),
            "terminal_state_hash_count": len(
                {trajectory.terminal_state_hash for trajectory in self.trajectories}
            ),
            "source_fingerprint": self.source_fingerprint,
            "semantic_fingerprint": self.semantic_fingerprint,
            "code_version": self.code_version,
            "result_hash": self.result_hash,
        }


class GreaterExaltationHarness:
    """Atomic two-add Omen runtime over the accepted ordinary weighted pool."""

    def __init__(
        self,
        *,
        static: StaticGameData,
        pool_builder: PoolBuilder = build_ordinary_add_pool,
        code_version: str = "p2c.m45a.dev",
    ) -> None:
        self.static = static
        self.pool_builder = pool_builder
        self.code_version = code_version

    def validate_operation_contract(
        self, state: ItemState, operation: GreaterExaltationOperation
    ) -> None:
        currency_id, item_class, side_filter, mml, active_ids, add_count = _fields(
            operation
        )
        if state.item_class != item_class or state.rarity != Rarity.RARE:
            raise M45AGreaterExaltationInvariantViolation(
                "Greater Exaltation requires a Rare item of the compiled item class"
            )
        row = _operation_row(self.static.operations, currency_id)
        if row is None or row.get("runtime_admission_status") != "accepted_executable_runtime":
            raise M45AGreaterExaltationInvariantViolation(
                f"Greater Exaltation base currency is not admitted: {currency_id}"
            )
        if row.get("group") != "exalted":
            raise M45AGreaterExaltationInvariantViolation(
                f"Greater Exaltation requires Exalted operation group: {currency_id}"
            )
        from p2c_engine.operations.omen import M45AOmenAdmissionError, compile_omen_effects

        try:
            effects = compile_omen_effects(
                self.static.omens,
                operation_group="exalted",
                active_modifier_ids=active_ids,
            )
        except M45AOmenAdmissionError as exc:
            raise M45AGreaterExaltationInvariantViolation(str(exc)) from exc
        if (
            M45A_GREATER_EXALTATION_OMEN_ID not in effects.omen_ids
            or effects.add_count != M45A_GREATER_EXALTATION_ADD_COUNT
            or add_count != effects.add_count
            or side_filter != effects.add_side_filter
        ):
            raise M45AGreaterExaltationInvariantViolation(
                "Greater Exaltation resolved effect mismatch"
            )
        transition = row.get("transition")
        add = transition.get("add") if isinstance(transition, Mapping) else None
        omen_resolution = (
            transition.get("omen_resolution") if isinstance(transition, Mapping) else None
        )
        greater = (
            omen_resolution.get("greater_exaltation")
            if isinstance(omen_resolution, Mapping)
            else None
        )
        if (
            not isinstance(transition, Mapping)
            or transition.get("atomic") is not True
            or not isinstance(add, Mapping)
            or add.get("kind") != "ordinary_weighted"
            or add.get("count") != 1
            or add.get("mml") != mml
            or not isinstance(greater, Mapping)
            or greater.get("resolved_add_count") != 2
            or greater.get("partial_execution") is not False
            or greater.get("on_insufficient_slots") != "NO_TRANSITION_NO_CONSUMPTION"
        ):
            raise M45AGreaterExaltationInvariantViolation(
                f"Greater Exaltation data contract drift: {currency_id}"
            )

    def build_pool(
        self, state: ItemState, operation: GreaterExaltationOperation
    ) -> PoolBuildResult:
        self.validate_operation_contract(state, operation)
        _currency_id, item_class, side_filter, mml, _active_ids, _add_count = _fields(
            operation
        )
        return self.pool_builder(
            OrdinaryAddPoolRequest(
                item_class=item_class,
                state=state,
                side_filter=side_filter,
                mml=mml,
            ),
            self.static,
        )

    def enumerate_paths(
        self,
        *,
        initial_state: ItemState,
        operation: GreaterExaltationOperation,
        decision_id_prefix: str,
        max_candidates_per_pool: int = M45A_MAX_CANDIDATES_PER_POOL,
        max_exact_paths: int = M45A_MAX_EXACT_PATHS,
    ) -> tuple[GreaterExaltationExactPath, ...]:
        self._validate_ceiling("max_candidates_per_pool", max_candidates_per_pool)
        self._validate_ceiling("max_exact_paths", max_exact_paths)
        self.validate_operation_contract(initial_state, operation)
        reason = self._precondition_failure(initial_state, operation)
        if reason is not None:
            return (self._no_transition_path(initial_state, reason),)

        first_pool = self.build_pool(initial_state, operation)
        self._candidate_ceiling(first_pool, max_candidates_per_pool)
        if not first_pool.candidates:
            return (
                self._no_transition_path(
                    initial_state,
                    first_pool.empty_reason or "ordinary_add_pool_exhausted",
                ),
            )

        paths: list[GreaterExaltationExactPath] = []
        for first in branch_options(f"{decision_id_prefix}.add_0", first_pool.candidates):
            after_first = _append_ordinary_modifier(initial_state, first.selected_key)
            self._assert_intermediate(initial_state, after_first)
            first_trace = self._trace(0, initial_state, after_first, first, first_pool)
            first_mass = Fraction(first.probability_numerator, first.probability_denominator)
            second_pool = self.build_pool(after_first, operation)
            self._candidate_ceiling(second_pool, max_candidates_per_pool)
            if not second_pool.candidates:
                paths.append(
                    GreaterExaltationExactPath(
                        path_key=(f"add:{first.selected_key}", "add:NO_TRANSITION"),
                        terminal_state=initial_state,
                        terminal_state_hash=initial_state.state_hash(),
                        outcome="no_transition_no_consumption",
                        selected_mod_ids=(),
                        traces=(
                            first_trace,
                            GreaterExaltationAddTrace(
                                add_index=1,
                                pre_state_hash=after_first.state_hash(),
                                post_state_hash=initial_state.state_hash(),
                                decision_id=None,
                                selected_mod_id=None,
                                candidate_count=0,
                                candidate_digest=None,
                                pool_fingerprint=second_pool.result_fingerprint,
                                no_transition_reason=second_pool.empty_reason
                                or "ordinary_add_pool_exhausted",
                            ),
                        ),
                        no_transition_reason=second_pool.empty_reason
                        or "ordinary_add_pool_exhausted",
                        probability_numerator=first_mass.numerator,
                        probability_denominator=first_mass.denominator,
                    )
                )
                continue
            for second in branch_options(
                f"{decision_id_prefix}.add_1.{first.selected_key}",
                second_pool.candidates,
            ):
                terminal = _append_ordinary_modifier(after_first, second.selected_key)
                self._assert_terminal(initial_state, terminal)
                second_mass = Fraction(
                    second.probability_numerator, second.probability_denominator
                )
                mass = first_mass * second_mass
                paths.append(
                    GreaterExaltationExactPath(
                        path_key=(
                            f"add:{first.selected_key}",
                            f"add:{second.selected_key}",
                        ),
                        terminal_state=terminal,
                        terminal_state_hash=terminal.state_hash(),
                        outcome="completed",
                        selected_mod_ids=(first.selected_key, second.selected_key),
                        traces=(
                            first_trace,
                            self._trace(1, after_first, terminal, second, second_pool),
                        ),
                        no_transition_reason=None,
                        probability_numerator=mass.numerator,
                        probability_denominator=mass.denominator,
                    )
                )
                if len(paths) > max_exact_paths:
                    raise M45AGreaterExaltationCeilingExceeded(
                        "max_exact_paths", max_exact_paths, len(paths)
                    )
        self._assert_mass(paths)
        return tuple(paths)

    def enumerate_terminal_distribution(
        self, **kwargs: Any
    ) -> tuple[GreaterExaltationExactTerminal, ...]:
        paths = self.enumerate_paths(**kwargs)
        masses: dict[str, Fraction] = {}
        keys: dict[str, list[tuple[str, ...]]] = {}
        for path in paths:
            masses[path.terminal_state_hash] = masses.get(
                path.terminal_state_hash, Fraction(0, 1)
            ) + Fraction(path.probability_numerator, path.probability_denominator)
            keys.setdefault(path.terminal_state_hash, []).append(path.path_key)
        terminals = tuple(
            GreaterExaltationExactTerminal(
                terminal_state_hash=state_hash,
                probability_numerator=mass.numerator,
                probability_denominator=mass.denominator,
                path_count=len(keys[state_hash]),
                path_keys=tuple(sorted(keys[state_hash])),
            )
            for state_hash, mass in sorted(masses.items())
        )
        if sum(
            (
                Fraction(row.probability_numerator, row.probability_denominator)
                for row in terminals
            ),
            Fraction(0, 1),
        ) != Fraction(1, 1):
            raise M45AGreaterExaltationInvariantViolation(
                "Greater Exaltation terminal mass does not sum to one"
            )
        return terminals

    def sample_once(
        self,
        *,
        initial_state: ItemState,
        operation: GreaterExaltationOperation,
        decision_source: RecordingDecisionSource,
        sample_index: int,
        run_id: str,
        decision_id_prefix: str | None = None,
    ) -> GreaterExaltationTrajectory:
        self.validate_operation_contract(initial_state, operation)
        reason = self._precondition_failure(initial_state, operation)
        if reason is not None:
            return self._no_transition_trajectory(initial_state, sample_index, reason)
        prefix = decision_id_prefix or f"{run_id}.sample_{sample_index}.greater_exaltation"
        first_pool = self.build_pool(initial_state, operation)
        if not first_pool.candidates:
            return self._no_transition_trajectory(
                initial_state,
                sample_index,
                first_pool.empty_reason or "ordinary_add_pool_exhausted",
            )
        first = decision_source.choose_one(f"{prefix}.add_0", first_pool.candidates)
        after_first = _append_ordinary_modifier(initial_state, first.selected.key)
        self._assert_intermediate(initial_state, after_first)
        first_trace = self._trace(0, initial_state, after_first, first, first_pool)
        second_pool = self.build_pool(after_first, operation)
        if not second_pool.candidates:
            return GreaterExaltationTrajectory(
                sample_index=sample_index,
                outcome="no_transition_no_consumption",
                initial_state_hash=initial_state.state_hash(),
                terminal_state_hash=initial_state.state_hash(),
                selected_mod_ids=(),
                traces=(
                    first_trace,
                    GreaterExaltationAddTrace(
                        add_index=1,
                        pre_state_hash=after_first.state_hash(),
                        post_state_hash=initial_state.state_hash(),
                        decision_id=None,
                        selected_mod_id=None,
                        candidate_count=0,
                        candidate_digest=None,
                        pool_fingerprint=second_pool.result_fingerprint,
                        no_transition_reason=second_pool.empty_reason
                        or "ordinary_add_pool_exhausted",
                    ),
                ),
                no_transition_reason=second_pool.empty_reason
                or "ordinary_add_pool_exhausted",
            )
        second = decision_source.choose_one(
            f"{prefix}.add_1.{first.selected.key}", second_pool.candidates
        )
        terminal = _append_ordinary_modifier(after_first, second.selected.key)
        self._assert_terminal(initial_state, terminal)
        return GreaterExaltationTrajectory(
            sample_index=sample_index,
            outcome="completed",
            initial_state_hash=initial_state.state_hash(),
            terminal_state_hash=terminal.state_hash(),
            selected_mod_ids=(first.selected.key, second.selected.key),
            traces=(
                first_trace,
                self._trace(1, after_first, terminal, second, second_pool),
            ),
            no_transition_reason=None,
        )

    def run(
        self,
        *,
        initial_state: ItemState,
        operation: GreaterExaltationOperation,
        seed: int,
        sample_count: int,
        run_id: str,
    ) -> GreaterExaltationRunResult:
        if isinstance(sample_count, bool) or not isinstance(sample_count, int) or sample_count < 0:
            raise SamplingContractDefect("sample_count must be a non-negative integer")
        source = RecordingDecisionSource(SeededDecisionSource(seed))
        trajectories = tuple(
            self.sample_once(
                initial_state=initial_state,
                operation=operation,
                decision_source=source,
                sample_index=index,
                run_id=run_id,
            )
            for index in range(sample_count)
        )
        currency_id, _item_class, _side, _mml, _omens, _count = _fields(operation)
        payload = {
            "schema_version": M45A_GREATER_EXALTATION_SCHEMA_VERSION,
            "semantics_version": M45A_GREATER_EXALTATION_SEMANTICS_VERSION,
            "run_id": run_id,
            "seed": seed,
            "sample_count": sample_count,
            "currency_id": currency_id,
            "mode_id": operation.mode_id,
            "rng_stream_version": RNG_STREAM_VERSION,
            "sampling_algorithm_id": SAMPLING_ALGORITHM_ID,
            "source_fingerprint": self.static.source_fingerprint,
            "semantic_fingerprint": self.static.semantic_fingerprint,
            "code_version": self.code_version,
            "trajectories": [row.public_payload() for row in trajectories],
            "decisions": list(source.records),
        }
        return GreaterExaltationRunResult(
            schema_version=M45A_GREATER_EXALTATION_SCHEMA_VERSION,
            run_id=run_id,
            seed=seed,
            sample_count=sample_count,
            currency_id=currency_id,
            mode_id=operation.mode_id,
            source_fingerprint=self.static.source_fingerprint,
            semantic_fingerprint=self.static.semantic_fingerprint,
            code_version=self.code_version,
            trajectories=trajectories,
            decisions=source.records,
            result_hash=sha256_canonical(payload, schema_version=1),
        )

    def verify_replay(
        self,
        *,
        initial_state: ItemState,
        operation: GreaterExaltationOperation,
        expected: GreaterExaltationRunResult,
    ) -> GreaterExaltationRunResult:
        replay = self.run(
            initial_state=initial_state,
            operation=operation,
            seed=expected.seed,
            sample_count=expected.sample_count,
            run_id=expected.run_id,
        )
        if replay != expected:
            raise M45AGreaterExaltationInvariantViolation(
                "Greater Exaltation deterministic replay mismatch"
            )
        return replay

    def _precondition_failure(
        self, state: ItemState, operation: GreaterExaltationOperation
    ) -> str | None:
        _currency_id, _item_class, side, _mml, _omens, _count = _fields(operation)
        capacity = capacity_snapshot(state, self.static)
        if side == Side.PREFIX:
            free = capacity.prefix_capacity - capacity.prefix_used
        elif side == Side.SUFFIX:
            free = capacity.suffix_capacity - capacity.suffix_used
        else:
            free = capacity.total_capacity - capacity.total_used
        if free < 2:
            return "insufficient_capacity_for_atomic_two_add"
        return None

    def _assert_intermediate(self, initial: ItemState, state: ItemState) -> None:
        if len(state.modifiers) != len(initial.modifiers) + 1:
            raise M45AGreaterExaltationInvariantViolation(
                "Greater Exaltation first branch add did not add exactly one modifier"
            )
        _assert_fractured_modifiers_unchanged(initial, state, self.static.modifier_index)
        _assert_capacity(state, self.static.modifier_index)
        _assert_duplicate_family_and_groups(state, self.static.modifier_index)

    def _assert_terminal(self, initial: ItemState, terminal: ItemState) -> None:
        if len(terminal.modifiers) != len(initial.modifiers) + 2:
            raise M45AGreaterExaltationInvariantViolation(
                "Greater Exaltation must add exactly two modifiers"
            )
        _assert_fractured_modifiers_unchanged(
            initial, terminal, self.static.modifier_index
        )
        _assert_capacity(terminal, self.static.modifier_index)
        _assert_duplicate_family_and_groups(terminal, self.static.modifier_index)

    @staticmethod
    def _trace(add_index, pre, post, option, pool):
        return GreaterExaltationAddTrace(
            add_index=add_index,
            pre_state_hash=pre.state_hash(),
            post_state_hash=post.state_hash(),
            decision_id=option.decision_id
            if hasattr(option, "decision_id")
            else option.record.decision_id,
            selected_mod_id=option.selected_key
            if hasattr(option, "selected_key")
            else option.selected.key,
            candidate_count=len(pool.candidates),
            candidate_digest=option.candidate_digest
            if hasattr(option, "candidate_digest")
            else option.record.candidate_digest,
            pool_fingerprint=pool.result_fingerprint,
            no_transition_reason=None,
        )

    @staticmethod
    def _candidate_ceiling(pool: PoolBuildResult, limit: int) -> None:
        if len(pool.candidates) > limit:
            raise M45AGreaterExaltationCeilingExceeded(
                "max_candidates_per_pool", limit, len(pool.candidates)
            )

    @staticmethod
    def _validate_ceiling(name: str, value: int) -> None:
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise SamplingContractDefect(f"{name} must be a positive integer")

    @staticmethod
    def _assert_mass(paths: list[GreaterExaltationExactPath]) -> None:
        total = sum(
            (
                Fraction(path.probability_numerator, path.probability_denominator)
                for path in paths
            ),
            Fraction(0, 1),
        )
        if total != Fraction(1, 1):
            raise M45AGreaterExaltationInvariantViolation(
                "Greater Exaltation exact path mass does not sum to one"
            )

    @staticmethod
    def _no_transition_path(state: ItemState, reason: str) -> GreaterExaltationExactPath:
        return GreaterExaltationExactPath(
            path_key=(f"NO_TRANSITION:{reason}",),
            terminal_state=state,
            terminal_state_hash=state.state_hash(),
            outcome="no_transition_no_consumption",
            selected_mod_ids=(),
            traces=(),
            no_transition_reason=reason,
            probability_numerator=1,
            probability_denominator=1,
        )

    @staticmethod
    def _no_transition_trajectory(
        state: ItemState, sample_index: int, reason: str
    ) -> GreaterExaltationTrajectory:
        return GreaterExaltationTrajectory(
            sample_index=sample_index,
            outcome="no_transition_no_consumption",
            initial_state_hash=state.state_hash(),
            terminal_state_hash=state.state_hash(),
            selected_mod_ids=(),
            traces=(),
            no_transition_reason=reason,
        )


def _fields(operation: GreaterExaltationOperation):
    if isinstance(operation, OrdinaryAddOperation):
        currency_id = operation.source_currency_id
        if currency_id is None:
            raise M45AGreaterExaltationInvariantViolation(
                "compiled ordinary-add plan is missing source currency"
            )
        return (
            currency_id,
            operation.item_class,
            operation.side_filter,
            operation.mml,
            operation.active_modifier_ids,
            operation.add_count,
        )
    return (
        operation.operation_id,
        operation.item_class,
        operation.side_filter,
        operation.mml,
        operation.active_modifier_ids,
        operation.add_count,
    )


def _operation_row(operations: Any, operation_id: str) -> Mapping[str, Any] | None:
    if not isinstance(operations, Mapping):
        return None
    for row in operations.get("operations") or ():
        if isinstance(row, Mapping) and row.get("operation_id") == operation_id:
            return row
    return None


__all__ = [
    "GreaterExaltationAddTrace",
    "GreaterExaltationExactPath",
    "GreaterExaltationExactTerminal",
    "GreaterExaltationHarness",
    "GreaterExaltationOperation",
    "GreaterExaltationRunResult",
    "GreaterExaltationTrajectory",
    "M45AGreaterExaltationCeilingExceeded",
    "M45AGreaterExaltationError",
    "M45AGreaterExaltationInvariantViolation",
    "M45A_GREATER_EXALTATION_ADD_COUNT",
    "M45A_GREATER_EXALTATION_OMEN_ID",
    "M45A_GREATER_EXALTATION_SCHEMA_VERSION",
    "M45A_GREATER_EXALTATION_SEMANTICS_VERSION",
]
