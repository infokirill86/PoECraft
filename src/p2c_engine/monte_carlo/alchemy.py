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
from p2c_engine.domain.enums import Rarity
from p2c_engine.domain.item_state import ItemState
from p2c_engine.domain.pool_building import PoolBuildResult
from p2c_engine.domain.versions import RNG_STREAM_VERSION, SAMPLING_ALGORITHM_ID
from p2c_engine.legality.pool_builders import (
    OrdinaryAddPoolRequest,
    build_ordinary_add_pool,
)
from p2c_engine.legality.state_validation import validate_item_state
from p2c_engine.sampling.exact import branch_options
from p2c_engine.static_data.game_data import StaticGameData

from .ordinary_add import (
    M32_VALUE_POLICY,
    M32InvariantViolation,
    M32MonteCarloError,
    _append_ordinary_modifier,
)


M44A_ALCHEMY_OPERATION_ID = "alchemy"
M44A_ADD_COUNT = 4
M44A_SCHEMA_VERSION = "p2c.m44a.alchemy_runtime.v1"
M44A_SEMANTICS_VERSION = "p2c.m44a.alchemy_sequential_add.project_model.v1"
M44A_MAX_CANDIDATES_PER_POOL = 256
M44A_MAX_EXACT_PATHS = 65_536
M44A_MAX_EXACT_TERMINALS = 65_536
M44A_FIXED_SEEDS = (44_001, 44_002, 44_003)
M44A_SAMPLE_TIERS = (512, 2_048, 8_192)
ACCEPTED_RUNTIME_STATUS = "accepted_executable_runtime"


class M44AAlchemyError(M32MonteCarloError):
    """Base class for M44-A Alchemy runtime failures."""


class M44AAlchemyInvariantViolation(M44AAlchemyError, M32InvariantViolation):
    """Raised when the admitted atomic Alchemy contract is violated."""


class M44AExactCeilingExceeded(M44AAlchemyError):
    """Fail-closed exact stop; never a request to approximate silently."""

    def __init__(
        self,
        *,
        ceiling_name: str,
        ceiling_limit: int,
        observed_count: int,
        add_index: int,
    ) -> None:
        self.ceiling_name = ceiling_name
        self.ceiling_limit = ceiling_limit
        self.observed_count = observed_count
        self.add_index = add_index
        super().__init__(
            "M44-A exact ceiling exceeded: "
            f"{ceiling_name} limit={ceiling_limit} observed={observed_count} "
            f"add_index={add_index}"
        )


@dataclass(frozen=True, slots=True)
class AlchemyOperation:
    mode_id: str
    operation_id: str = M44A_ALCHEMY_OPERATION_ID
    item_class: str = "quarterstaff"
    input_rarities: tuple[Rarity, ...] = (Rarity.NORMAL, Rarity.MAGIC)
    output_rarity: Rarity = Rarity.RARE
    add_count: int = M44A_ADD_COUNT
    semantics_version: str = M44A_SEMANTICS_VERSION


@dataclass(frozen=True, slots=True)
class AlchemyAddTrace:
    add_index: int
    outcome: str
    working_pre_state_hash: str
    working_post_state_hash: str
    decision_id: str | None
    selected_mod_id: str | None
    candidate_count: int
    candidate_digest: str | None
    no_transition_reason: str | None

    def public_payload(self) -> dict[str, object]:
        return {
            "add_index": self.add_index,
            "outcome": self.outcome,
            "working_pre_state_hash": self.working_pre_state_hash,
            "working_post_state_hash": self.working_post_state_hash,
            "decision_id": self.decision_id,
            "selected_mod_id": self.selected_mod_id,
            "candidate_count": self.candidate_count,
            "candidate_digest": self.candidate_digest,
            "no_transition_reason": self.no_transition_reason,
        }


@dataclass(frozen=True, slots=True)
class AlchemyExactPath:
    path_key: tuple[str | None, ...]
    outcome: str
    terminal_state: ItemState
    terminal_state_hash: str
    selected_mod_ids: tuple[str, ...]
    traces: tuple[AlchemyAddTrace, ...]
    candidate_count_total: int
    pool_digest: str | None
    no_transition_reason: str | None
    probability_numerator: int
    probability_denominator: int


@dataclass(frozen=True, slots=True)
class AlchemyExactTerminal:
    terminal_state_hash: str
    outcome: str
    path_count: int
    path_keys: tuple[tuple[str | None, ...], ...]
    probability_numerator: int
    probability_denominator: int


@dataclass(frozen=True, slots=True)
class AlchemyTrajectory:
    sample_index: int
    outcome: str
    operation_id: str
    pre_state_hash: str
    post_state_hash: str
    selected_mod_ids: tuple[str, ...]
    traces: tuple[AlchemyAddTrace, ...]
    candidate_count_total: int
    pool_digest: str | None
    no_transition_reason: str | None

    def public_payload(self) -> dict[str, object]:
        return {
            "sample_index": self.sample_index,
            "outcome": self.outcome,
            "operation_id": self.operation_id,
            "pre_state_hash": self.pre_state_hash,
            "post_state_hash": self.post_state_hash,
            "selected_mod_ids": self.selected_mod_ids,
            "traces": [trace.public_payload() for trace in self.traces],
            "candidate_count_total": self.candidate_count_total,
            "pool_digest": self.pool_digest,
            "no_transition_reason": self.no_transition_reason,
        }


@dataclass(frozen=True, slots=True)
class AlchemyRunResult:
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
    trajectories: tuple[AlchemyTrajectory, ...]
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


class AlchemyHarness:
    """Atomic four-add runtime over the accepted ordinary weighted-add kernel.

    Intermediate adds mutate only an isolated empty-Rare working state. The
    caller-visible item changes once, after the fourth successful add. The
    sequential model is accepted project-model behavior and is not a server-
    truth claim about the game's internal roll implementation.
    """

    def __init__(
        self,
        *,
        static: StaticGameData,
        pool_builder: PoolBuilder = build_ordinary_add_pool,
        code_version: str = "p2c.m44a.dev",
    ) -> None:
        self.static = static
        self.pool_builder = pool_builder
        self.code_version = code_version

    def build_pool(
        self, working_state: ItemState, operation: AlchemyOperation
    ) -> PoolBuildResult:
        self._validate_operation_contract(operation)
        if working_state.rarity != Rarity.RARE:
            raise M44AAlchemyInvariantViolation(
                "M44-A pool must be built from the isolated Rare working state"
            )
        if len(working_state.modifiers) >= operation.add_count:
            raise M44AAlchemyInvariantViolation(
                "M44-A pool requested after the declared add count was reached"
            )
        return self.pool_builder(
            OrdinaryAddPoolRequest(
                item_class=operation.item_class,
                state=working_state,
                mml=None,
            ),
            self.static,
        )

    def enumerate_paths(
        self,
        *,
        initial_state: ItemState,
        operation: AlchemyOperation,
        decision_id_prefix: str,
        max_candidates_per_pool: int = M44A_MAX_CANDIDATES_PER_POOL,
        max_exact_paths: int = M44A_MAX_EXACT_PATHS,
    ) -> tuple[AlchemyExactPath, ...]:
        self._validate_operation_contract(operation)
        self._validate_ceiling("max_candidates_per_pool", max_candidates_per_pool)
        self._validate_ceiling("max_exact_paths", max_exact_paths)
        reason = self._precondition_failure(initial_state, operation)
        if reason is not None:
            return (self._no_transition_path(initial_state, reason),)

        frontier: list[
            tuple[
                ItemState,
                Fraction,
                tuple[str | None, ...],
                tuple[str, ...],
                tuple[AlchemyAddTrace, ...],
                int,
                tuple[str, ...],
            ]
        ] = [
            (
                self._working_state(initial_state, operation),
                Fraction(1, 1),
                (),
                (),
                (),
                0,
                (),
            )
        ]
        completed: list[AlchemyExactPath] = []

        for add_index in range(operation.add_count):
            next_frontier: list[
                tuple[
                    ItemState,
                    Fraction,
                    tuple[str | None, ...],
                    tuple[str, ...],
                    tuple[AlchemyAddTrace, ...],
                    int,
                    tuple[str, ...],
                ]
            ] = []
            for (
                working_state,
                path_mass,
                path_key,
                selected_ids,
                traces,
                candidate_total,
                pool_digests,
            ) in frontier:
                pool = self.build_pool(working_state, operation)
                self._candidate_ceiling(pool, max_candidates_per_pool, add_index)
                if not pool.candidates:
                    reason = pool.empty_reason or "ordinary_add_pool_exhausted"
                    trace = AlchemyAddTrace(
                        add_index=add_index,
                        outcome="failed_atomic_rollback",
                        working_pre_state_hash=working_state.state_hash(),
                        working_post_state_hash=working_state.state_hash(),
                        decision_id=None,
                        selected_mod_id=None,
                        candidate_count=0,
                        candidate_digest=pool.candidate_digest,
                        no_transition_reason=reason,
                    )
                    completed.append(
                        self._path(
                            terminal_state=initial_state,
                            outcome="no_transition_no_consumption",
                            path_key=path_key + (None,),
                            selected_mod_ids=selected_ids,
                            traces=traces + (trace,),
                            candidate_count_total=candidate_total,
                            pool_digests=pool_digests + (pool.result_fingerprint,),
                            no_transition_reason=reason,
                            probability=path_mass,
                        )
                    )
                    continue

                decision_id = f"{decision_id_prefix}.add_{add_index}"
                for option in branch_options(decision_id, pool.candidates):
                    post_state = _append_ordinary_modifier(
                        working_state, option.selected_key
                    )
                    self._assert_working_add(
                        pre_state=working_state,
                        post_state=post_state,
                        add_index=add_index,
                    )
                    option_mass = Fraction(
                        option.probability_numerator,
                        option.probability_denominator,
                    )
                    trace = AlchemyAddTrace(
                        add_index=add_index,
                        outcome="applied_internal_add",
                        working_pre_state_hash=working_state.state_hash(),
                        working_post_state_hash=post_state.state_hash(),
                        decision_id=option.decision_id,
                        selected_mod_id=option.selected_key,
                        candidate_count=len(pool.candidates),
                        candidate_digest=option.candidate_digest,
                        no_transition_reason=None,
                    )
                    next_frontier.append(
                        (
                            post_state,
                            path_mass * option_mass,
                            path_key + (option.selected_key,),
                            selected_ids + (option.selected_key,),
                            traces + (trace,),
                            candidate_total + len(pool.candidates),
                            pool_digests + (pool.result_fingerprint,),
                        )
                    )
                    observed = len(completed) + len(next_frontier)
                    if observed > max_exact_paths:
                        raise M44AExactCeilingExceeded(
                            ceiling_name="max_exact_paths",
                            ceiling_limit=max_exact_paths,
                            observed_count=observed,
                            add_index=add_index,
                        )
            frontier = next_frontier

        for (
            terminal_state,
            path_mass,
            path_key,
            selected_ids,
            traces,
            candidate_total,
            pool_digests,
        ) in frontier:
            self._assert_terminal(initial_state, terminal_state, operation)
            completed.append(
                self._path(
                    terminal_state=terminal_state,
                    outcome="completed",
                    path_key=path_key,
                    selected_mod_ids=selected_ids,
                    traces=traces,
                    candidate_count_total=candidate_total,
                    pool_digests=pool_digests,
                    no_transition_reason=None,
                    probability=path_mass,
                )
            )
        self._assert_exact_mass_one(completed)
        return tuple(completed)

    def enumerate_terminal_distribution(
        self,
        *,
        initial_state: ItemState,
        operation: AlchemyOperation,
        decision_id_prefix: str,
        max_candidates_per_pool: int = M44A_MAX_CANDIDATES_PER_POOL,
        max_exact_paths: int = M44A_MAX_EXACT_PATHS,
        max_exact_terminals: int = M44A_MAX_EXACT_TERMINALS,
    ) -> tuple[AlchemyExactTerminal, ...]:
        self._validate_ceiling("max_exact_terminals", max_exact_terminals)
        paths = self.enumerate_paths(
            initial_state=initial_state,
            operation=operation,
            decision_id_prefix=decision_id_prefix,
            max_candidates_per_pool=max_candidates_per_pool,
            max_exact_paths=max_exact_paths,
        )
        masses: dict[tuple[str, str], Fraction] = defaultdict(Fraction)
        path_keys: dict[tuple[str, str], list[tuple[str | None, ...]]] = defaultdict(list)
        for path in paths:
            key = (path.terminal_state_hash, path.outcome)
            masses[key] += Fraction(
                path.probability_numerator, path.probability_denominator
            )
            path_keys[key].append(path.path_key)
        if len(masses) > max_exact_terminals:
            raise M44AExactCeilingExceeded(
                ceiling_name="max_exact_terminals",
                ceiling_limit=max_exact_terminals,
                observed_count=len(masses),
                add_index=operation.add_count - 1,
            )
        terminals = tuple(
            AlchemyExactTerminal(
                terminal_state_hash=key[0],
                outcome=key[1],
                path_count=len(path_keys[key]),
                path_keys=tuple(sorted(path_keys[key])),
                probability_numerator=masses[key].numerator,
                probability_denominator=masses[key].denominator,
            )
            for key in sorted(masses)
        )
        if sum(
            (
                Fraction(row.probability_numerator, row.probability_denominator)
                for row in terminals
            ),
            Fraction(0, 1),
        ) != Fraction(1, 1):
            raise M44AAlchemyInvariantViolation(
                "M44-A exact terminal mass does not sum to one"
            )
        return terminals

    def sample_once(
        self,
        *,
        initial_state: ItemState,
        operation: AlchemyOperation,
        decision_source: RecordingDecisionSource,
        sample_index: int,
        run_id: str,
        decision_id_prefix: str | None = None,
    ) -> AlchemyTrajectory:
        self._validate_operation_contract(operation)
        pre_hash = initial_state.state_hash()
        reason = self._precondition_failure(initial_state, operation)
        if reason is not None:
            return self._no_transition_trajectory(
                initial_state, operation, sample_index, reason
            )

        working_state = self._working_state(initial_state, operation)
        selected_ids: list[str] = []
        traces: list[AlchemyAddTrace] = []
        candidate_total = 0
        pool_digests: list[str] = []
        prefix = decision_id_prefix or (
            f"{run_id}.sample_{sample_index}.step_0."
            f"{operation.operation_id}.{operation.mode_id}"
        )

        for add_index in range(operation.add_count):
            pool = self.build_pool(working_state, operation)
            pool_digests.append(pool.result_fingerprint)
            if not pool.candidates:
                reason = pool.empty_reason or "ordinary_add_pool_exhausted"
                traces.append(
                    AlchemyAddTrace(
                        add_index=add_index,
                        outcome="failed_atomic_rollback",
                        working_pre_state_hash=working_state.state_hash(),
                        working_post_state_hash=working_state.state_hash(),
                        decision_id=None,
                        selected_mod_id=None,
                        candidate_count=0,
                        candidate_digest=pool.candidate_digest,
                        no_transition_reason=reason,
                    )
                )
                return AlchemyTrajectory(
                    sample_index=sample_index,
                    outcome="no_transition_no_consumption",
                    operation_id=operation.operation_id,
                    pre_state_hash=pre_hash,
                    post_state_hash=pre_hash,
                    selected_mod_ids=tuple(selected_ids),
                    traces=tuple(traces),
                    candidate_count_total=candidate_total,
                    pool_digest=self._combined_pool_digest(pool_digests),
                    no_transition_reason=reason,
                )
            decision = decision_source.choose_one(
                f"{prefix}.add_{add_index}", pool.candidates
            )
            post_state = _append_ordinary_modifier(
                working_state, decision.selected.key
            )
            self._assert_working_add(
                pre_state=working_state,
                post_state=post_state,
                add_index=add_index,
            )
            selected_ids.append(decision.selected.key)
            candidate_total += decision.record.candidate_count
            traces.append(
                AlchemyAddTrace(
                    add_index=add_index,
                    outcome="applied_internal_add",
                    working_pre_state_hash=working_state.state_hash(),
                    working_post_state_hash=post_state.state_hash(),
                    decision_id=decision.record.decision_id,
                    selected_mod_id=decision.selected.key,
                    candidate_count=decision.record.candidate_count,
                    candidate_digest=decision.record.candidate_digest,
                    no_transition_reason=None,
                )
            )
            working_state = post_state

        self._assert_terminal(initial_state, working_state, operation)
        return AlchemyTrajectory(
            sample_index=sample_index,
            outcome="completed",
            operation_id=operation.operation_id,
            pre_state_hash=pre_hash,
            post_state_hash=working_state.state_hash(),
            selected_mod_ids=tuple(selected_ids),
            traces=tuple(traces),
            candidate_count_total=candidate_total,
            pool_digest=self._combined_pool_digest(pool_digests),
            no_transition_reason=None,
        )

    def run(
        self,
        *,
        initial_state: ItemState,
        operation: AlchemyOperation,
        seed: int,
        sample_count: int,
        run_id: str,
    ) -> AlchemyRunResult:
        if (
            isinstance(sample_count, bool)
            or not isinstance(sample_count, int)
            or sample_count < 0
        ):
            raise SamplingContractDefect(
                "sample_count must be a non-negative non-bool integer"
            )
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
        payload = {
            "schema_version": M44A_SCHEMA_VERSION,
            "semantics_version": M44A_SEMANTICS_VERSION,
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
        return AlchemyRunResult(
            schema_version=M44A_SCHEMA_VERSION,
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

    def verify_replay(
        self,
        *,
        expected: AlchemyRunResult,
        initial_state: ItemState,
        operation: AlchemyOperation,
    ) -> AlchemyRunResult:
        replayed = self.run(
            initial_state=initial_state,
            operation=operation,
            seed=expected.seed,
            sample_count=expected.sample_count,
            run_id=expected.run_id,
        )
        if replayed != expected:
            raise M44AAlchemyInvariantViolation("M44-A deterministic replay mismatch")
        return replayed

    def _working_state(
        self, state: ItemState, operation: AlchemyOperation
    ) -> ItemState:
        return replace(
            state,
            rarity=operation.output_rarity,
            modifiers=(),
            unrevealed_desecrated=None,
        )

    def _precondition_failure(
        self, state: ItemState, operation: AlchemyOperation
    ) -> str | None:
        if state.item_class != operation.item_class:
            return "item_class_mismatch"
        for instance in state.modifiers:
            if instance.mod_id not in self.static.modifier_index:
                return "unknown_installed_modifier"
        if state.rarity not in operation.input_rarities:
            return "invalid_source_rarity"
        validation = validate_item_state(state, self.static)
        if not validation.ok:
            return "invalid_source_state"
        if any(instance.fractured for instance in state.modifiers):
            return "fractured_input_not_admitted"
        if state.unrevealed_desecrated is not None:
            return "unrevealed_desecrated_input_not_admitted"
        return None

    def _validate_operation_contract(self, operation: AlchemyOperation) -> None:
        if operation.semantics_version != M44A_SEMANTICS_VERSION:
            raise M44AAlchemyInvariantViolation(
                "M44-A Alchemy semantics version mismatch"
            )
        if operation.operation_id != M44A_ALCHEMY_OPERATION_ID:
            raise M44AAlchemyInvariantViolation(
                f"unsupported M44-A operation id: {operation.operation_id}"
            )
        row = self._operation_row(operation.operation_id)
        if row is None:
            raise M44AAlchemyInvariantViolation("missing admitted Alchemy row")
        if row.get("runtime_admission_status") != ACCEPTED_RUNTIME_STATUS:
            raise M44AAlchemyInvariantViolation("Alchemy is not executable-admitted")
        if row.get("group") != "alchemy":
            raise M44AAlchemyInvariantViolation("Alchemy operation group mismatch")
        transition = row.get("transition")
        remove = transition.get("remove") if isinstance(transition, Mapping) else None
        add = transition.get("add") if isinstance(transition, Mapping) else None
        sequence = transition.get("sequence") if isinstance(transition, Mapping) else None
        expected_sequence = (
            "discard_all_explicit",
            "create_empty_rare_shell",
            "add_ordinary_x4",
            "commit",
        )
        if (
            not isinstance(transition, Mapping)
            or transition.get("atomic") is not True
            or transition.get("output_rarity") != "rare"
            or tuple(sequence or ()) != expected_sequence
            or not isinstance(remove, Mapping)
            or remove.get("kind") != "all_explicit"
            or not isinstance(add, Mapping)
            or add.get("kind") != "ordinary_weighted_sequential"
            or add.get("count") != M44A_ADD_COUNT
            or add.get("mml") is not None
        ):
            raise M44AAlchemyInvariantViolation(
                "unsupported admitted M44-A Alchemy transition shape"
            )
        raw_inputs = row.get("input_rarity")
        if not isinstance(raw_inputs, (list, tuple)):
            raise M44AAlchemyInvariantViolation("invalid Alchemy input_rarity")
        try:
            expected_inputs = tuple(Rarity(value) for value in raw_inputs)
        except (TypeError, ValueError) as exc:
            raise M44AAlchemyInvariantViolation(
                "invalid Alchemy input_rarity"
            ) from exc
        if (
            operation.input_rarities != expected_inputs
            or operation.output_rarity != Rarity.RARE
            or operation.add_count != M44A_ADD_COUNT
        ):
            raise M44AAlchemyInvariantViolation(
                "Alchemy operation plan does not match admitted catalog row"
            )

    def _assert_working_add(
        self, *, pre_state: ItemState, post_state: ItemState, add_index: int
    ) -> None:
        if pre_state.rarity != Rarity.RARE or post_state.rarity != Rarity.RARE:
            raise M44AAlchemyInvariantViolation(
                "M44-A internal add left the Rare working state"
            )
        if len(post_state.modifiers) != len(pre_state.modifiers) + 1:
            raise M44AAlchemyInvariantViolation(
                "M44-A internal step did not add exactly one modifier"
            )
        validation = validate_item_state(post_state, self.static)
        if not validation.ok:
            raise M44AAlchemyInvariantViolation(
                f"M44-A internal add produced invalid state at add_index={add_index}"
            )

    def _assert_terminal(
        self,
        initial_state: ItemState,
        terminal_state: ItemState,
        operation: AlchemyOperation,
    ) -> None:
        if terminal_state.rarity != Rarity.RARE:
            raise M44AAlchemyInvariantViolation("Alchemy terminal must be Rare")
        if len(terminal_state.modifiers) != operation.add_count:
            raise M44AAlchemyInvariantViolation(
                "Alchemy terminal must contain exactly four generated modifiers"
            )
        if any(
            modifier.crafted or modifier.desecrated or modifier.fractured
            for modifier in terminal_state.modifiers
        ):
            raise M44AAlchemyInvariantViolation(
                "Alchemy generated modifier flags must be ordinary"
            )
        if (
            terminal_state.item_class != initial_state.item_class
            or terminal_state.item_level != initial_state.item_level
            or terminal_state.augment_socket_capacity
            != initial_state.augment_socket_capacity
            or terminal_state.augment_socket_used != initial_state.augment_socket_used
            or terminal_state.astrid_installed != initial_state.astrid_installed
        ):
            raise M44AAlchemyInvariantViolation(
                "Alchemy changed non-explicit item identity or support metadata"
            )
        validation = validate_item_state(terminal_state, self.static)
        if not validation.ok:
            raise M44AAlchemyInvariantViolation(
                "Alchemy terminal violates accepted item-state legality"
            )

    def _path(
        self,
        *,
        terminal_state: ItemState,
        outcome: str,
        path_key: tuple[str | None, ...],
        selected_mod_ids: tuple[str, ...],
        traces: tuple[AlchemyAddTrace, ...],
        candidate_count_total: int,
        pool_digests: tuple[str, ...],
        no_transition_reason: str | None,
        probability: Fraction,
    ) -> AlchemyExactPath:
        return AlchemyExactPath(
            path_key=path_key,
            outcome=outcome,
            terminal_state=terminal_state,
            terminal_state_hash=terminal_state.state_hash(),
            selected_mod_ids=selected_mod_ids,
            traces=traces,
            candidate_count_total=candidate_count_total,
            pool_digest=self._combined_pool_digest(pool_digests),
            no_transition_reason=no_transition_reason,
            probability_numerator=probability.numerator,
            probability_denominator=probability.denominator,
        )

    def _no_transition_path(
        self, state: ItemState, reason: str
    ) -> AlchemyExactPath:
        return self._path(
            terminal_state=state,
            outcome="no_transition_no_consumption",
            path_key=(None,),
            selected_mod_ids=(),
            traces=(),
            candidate_count_total=0,
            pool_digests=(),
            no_transition_reason=reason,
            probability=Fraction(1, 1),
        )

    def _no_transition_trajectory(
        self,
        state: ItemState,
        operation: AlchemyOperation,
        sample_index: int,
        reason: str,
    ) -> AlchemyTrajectory:
        state_hash = state.state_hash()
        return AlchemyTrajectory(
            sample_index=sample_index,
            outcome="no_transition_no_consumption",
            operation_id=operation.operation_id,
            pre_state_hash=state_hash,
            post_state_hash=state_hash,
            selected_mod_ids=(),
            traces=(),
            candidate_count_total=0,
            pool_digest=None,
            no_transition_reason=reason,
        )

    def _candidate_ceiling(
        self, pool: PoolBuildResult, limit: int, add_index: int
    ) -> None:
        if len(pool.candidates) > limit:
            raise M44AExactCeilingExceeded(
                ceiling_name="max_candidates_per_pool",
                ceiling_limit=limit,
                observed_count=len(pool.candidates),
                add_index=add_index,
            )

    def _validate_ceiling(self, name: str, value: int) -> None:
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise SamplingContractDefect(f"{name} must be a positive non-bool integer")

    def _assert_exact_mass_one(self, paths: list[AlchemyExactPath]) -> None:
        total = sum(
            (
                Fraction(path.probability_numerator, path.probability_denominator)
                for path in paths
            ),
            Fraction(0, 1),
        )
        if total != Fraction(1, 1):
            raise M44AAlchemyInvariantViolation(
                "M44-A exact path mass does not sum to one"
            )

    def _operation_row(self, operation_id: str) -> Mapping[str, Any] | None:
        if not isinstance(self.static.operations, Mapping):
            return None
        for row in self.static.operations.get("operations") or ():
            if isinstance(row, Mapping) and row.get("operation_id") == operation_id:
                return row
        return None

    def _combined_pool_digest(self, digests: list[str] | tuple[str, ...]) -> str | None:
        if not digests:
            return None
        return sha256_canonical(
            {"ordered_pool_result_fingerprints": tuple(digests)}, schema_version=1
        )


__all__ = [
    "AlchemyAddTrace",
    "AlchemyExactPath",
    "AlchemyExactTerminal",
    "AlchemyHarness",
    "AlchemyOperation",
    "AlchemyRunResult",
    "AlchemyTrajectory",
    "M44A_ADD_COUNT",
    "M44A_ALCHEMY_OPERATION_ID",
    "M44A_FIXED_SEEDS",
    "M44A_MAX_CANDIDATES_PER_POOL",
    "M44A_MAX_EXACT_PATHS",
    "M44A_MAX_EXACT_TERMINALS",
    "M44A_SAMPLE_TIERS",
    "M44A_SCHEMA_VERSION",
    "M44A_SEMANTICS_VERSION",
    "M44AAlchemyError",
    "M44AAlchemyInvariantViolation",
    "M44AExactCeilingExceeded",
]
