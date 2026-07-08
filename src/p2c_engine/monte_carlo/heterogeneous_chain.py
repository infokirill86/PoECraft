from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from p2c_engine.canonical.hashes import sha256_canonical
from p2c_engine.decisions import RecordingDecisionSource, SeededDecisionSource
from p2c_engine.domain.candidate import BranchOption
from p2c_engine.domain.decision import DecisionRecord
from p2c_engine.domain.defects import SamplingContractDefect
from p2c_engine.domain.item_state import ItemState
from p2c_engine.domain.pool_building import RemovalInstanceMetadata
from p2c_engine.domain.versions import RNG_STREAM_VERSION, SAMPLING_ALGORITHM_ID
from p2c_engine.legality.pool_builders import build_ordinary_add_pool, build_removal_pool
from p2c_engine.sampling.exact import branch_options
from p2c_engine.static_data.game_data import StaticGameData

from .annulment import (
    ANNULMENT_OPERATION_ID,
    AnnulmentMonteCarloHarness,
    AnnulmentOperation,
    RemovalPoolBuilder,
    _metadata_by_candidate_key,
    _remove_modifier_instance,
)
from .ordinary_add import (
    M32_VALUE_POLICY,
    MC_OPERATION_ID,
    M32InvariantViolation,
    M32MonteCarloError,
    OrdinaryAddMonteCarloHarness,
    OrdinaryAddOperation,
    PoolBuilder,
    _append_ordinary_modifier,
)


M36A_CHAIN_SCHEMA_VERSION = "p2c.m36a.heterogeneous_chain.v1"
M36A_SEMANTICS_VERSION = "p2c.m36a.accepted_two_step_chain.v1"
M36A_SEQUENCE_LENGTH = 2
M36A_CONSTRUCTED_FIXTURE_LABEL = (
    "project-model hardening fixture; not a real crafting route"
)
ACCEPTED_RUNTIME_STATUS = "accepted_executable_runtime"


class M36AChainError(M32MonteCarloError):
    """Base class for M36-A heterogeneous-chain failures."""


class M36AChainInvariantViolation(M36AChainError, M32InvariantViolation):
    """Raised when M36-A chain runtime invariants fail."""


@dataclass(frozen=True, slots=True)
class CatalogOperationInvocation:
    """Catalog operation reference used only for fail-closed validation tests.

    M36-A does not implement catalog wrappers such as Exalted or Chaos. The only
    accepted operation-row invocation is base Annulment through AnnulmentOperation.
    """

    mode_id: str
    operation_id: str
    item_class: str = "quarterstaff"


AcceptedM36AOperation = OrdinaryAddOperation | AnnulmentOperation | CatalogOperationInvocation


@dataclass(frozen=True, slots=True)
class M36AChainStepTrace:
    step_index: int
    operation_id: str
    mode_id: str
    outcome: str
    pre_state_hash: str
    post_state_hash: str
    decision_id: str | None
    selected_key: str | None
    selected_mod_id: str | None
    candidate_count: int
    candidate_digest: str | None
    pool_fingerprint: str | None
    no_transition_reason: str | None
    probability_numerator: int | None = None
    probability_denominator: int | None = None

    def public_payload(self) -> dict[str, object]:
        return {
            "step_index": self.step_index,
            "operation_id": self.operation_id,
            "mode_id": self.mode_id,
            "outcome": self.outcome,
            "pre_state_hash": self.pre_state_hash,
            "post_state_hash": self.post_state_hash,
            "decision_id": self.decision_id,
            "selected_key": self.selected_key,
            "selected_mod_id": self.selected_mod_id,
            "candidate_count": self.candidate_count,
            "candidate_digest": self.candidate_digest,
            "pool_fingerprint": self.pool_fingerprint,
            "no_transition_reason": self.no_transition_reason,
        }


@dataclass(frozen=True, slots=True)
class M36AExactChainPath:
    path_key: tuple[str, ...]
    terminal_state_hash: str
    outcome: str
    steps: tuple[M36AChainStepTrace, ...]
    probability_numerator: int
    probability_denominator: int


@dataclass(frozen=True, slots=True)
class M36AExactTerminalOption:
    terminal_state_hash: str
    probability_numerator: int
    probability_denominator: int
    path_count: int
    path_keys: tuple[tuple[str, ...], ...]


@dataclass(frozen=True, slots=True)
class M36AChainTrajectory:
    sample_index: int
    outcome: str
    initial_state_hash: str
    terminal_state_hash: str
    steps: tuple[M36AChainStepTrace, ...]

    def public_payload(self) -> dict[str, object]:
        return {
            "sample_index": self.sample_index,
            "outcome": self.outcome,
            "initial_state_hash": self.initial_state_hash,
            "terminal_state_hash": self.terminal_state_hash,
            "steps": [step.public_payload() for step in self.steps],
        }


@dataclass(frozen=True, slots=True)
class M36AChainRunResult:
    schema_version: str
    run_id: str
    seed: int
    sample_count: int
    chain_id: str
    operation_ids: tuple[str, str]
    rng_stream_version: int
    sampling_algorithm_id: str
    source_fingerprint: str
    semantic_fingerprint: str
    code_version: str
    trajectories: tuple[M36AChainTrajectory, ...]
    decisions: tuple[DecisionRecord, ...]
    result_hash: str

    def public_summary(self) -> dict[str, object]:
        terminal_state_hashes = {
            trajectory.terminal_state_hash for trajectory in self.trajectories
        }
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
            "chain_id": self.chain_id,
            "operation_ids": self.operation_ids,
            "rng_stream_version": self.rng_stream_version,
            "sampling_algorithm_id": self.sampling_algorithm_id,
            "source_fingerprint": self.source_fingerprint,
            "semantic_fingerprint": self.semantic_fingerprint,
            "code_version": self.code_version,
            "trajectory_count": len(self.trajectories),
            "decision_count": len(self.decisions),
            "terminal_state_hash_count": len(terminal_state_hashes),
            "result_hash": self.result_hash,
        }


@dataclass(frozen=True, slots=True)
class _ExactTransition:
    state: ItemState
    step: M36AChainStepTrace
    path_component: str
    probability: Fraction
    terminal: bool


class M36AHeterogeneousChainHarness:
    """M36-A two-step chain over accepted ordinary_add and base Annulment only."""

    def __init__(
        self,
        *,
        static: StaticGameData,
        ordinary_add_pool_builder: PoolBuilder = build_ordinary_add_pool,
        removal_pool_builder: RemovalPoolBuilder = build_removal_pool,
        code_version: str = "p2c.m36a.dev",
    ) -> None:
        self.static = static
        self.ordinary_add = OrdinaryAddMonteCarloHarness(
            static=static,
            pool_builder=ordinary_add_pool_builder,
            code_version=code_version,
        )
        self.annulment = AnnulmentMonteCarloHarness(
            static=static,
            removal_pool_builder=removal_pool_builder,
            code_version=code_version,
        )
        self.code_version = code_version

    def enumerate_paths(
        self,
        *,
        initial_state: ItemState,
        operations: tuple[AcceptedM36AOperation, AcceptedM36AOperation],
        decision_id_prefix: str,
        max_exact_paths: int,
    ) -> tuple[M36AExactChainPath, ...]:
        self._validate_chain(operations)
        if not isinstance(max_exact_paths, int) or isinstance(max_exact_paths, bool) or max_exact_paths <= 0:
            raise SamplingContractDefect("max_exact_paths must be a positive integer")

        frontier: tuple[tuple[ItemState, Fraction, tuple[M36AChainStepTrace, ...], tuple[str, ...]], ...] = (
            (initial_state, Fraction(1, 1), (), ()),
        )
        terminal_paths: list[M36AExactChainPath] = []

        for step_index, operation in enumerate(operations):
            next_frontier: list[
                tuple[ItemState, Fraction, tuple[M36AChainStepTrace, ...], tuple[str, ...]]
            ] = []
            for state, path_probability, steps, path_key in frontier:
                transitions = self._exact_transitions_for_step(
                    state=state,
                    operation=operation,
                    step_index=step_index,
                    decision_id=f"{decision_id_prefix}.step_{step_index}.{_operation_id(operation)}.{operation.mode_id}",
                )
                for transition in transitions:
                    probability = path_probability * transition.probability
                    next_steps = steps + (transition.step,)
                    next_path_key = path_key + (transition.path_component,)
                    is_terminal = transition.terminal or step_index == M36A_SEQUENCE_LENGTH - 1
                    if is_terminal:
                        terminal_paths.append(
                            M36AExactChainPath(
                                path_key=next_path_key,
                                terminal_state_hash=transition.state.state_hash(),
                                outcome=(
                                    "no_transition_terminal"
                                    if transition.terminal
                                    else "completed"
                                ),
                                steps=next_steps,
                                probability_numerator=probability.numerator,
                                probability_denominator=probability.denominator,
                            )
                        )
                    else:
                        next_frontier.append(
                            (transition.state, probability, next_steps, next_path_key)
                        )
                    if len(terminal_paths) + len(next_frontier) > max_exact_paths:
                        raise SamplingContractDefect("M36-A exact path ceiling exceeded")
            frontier = tuple(next_frontier)

        self._assert_mass_conservation(terminal_paths)
        return tuple(terminal_paths)

    def enumerate_terminal_distribution(
        self,
        *,
        initial_state: ItemState,
        operations: tuple[AcceptedM36AOperation, AcceptedM36AOperation],
        decision_id_prefix: str,
        max_exact_paths: int,
    ) -> tuple[M36AExactTerminalOption, ...]:
        paths = self.enumerate_paths(
            initial_state=initial_state,
            operations=operations,
            decision_id_prefix=decision_id_prefix,
            max_exact_paths=max_exact_paths,
        )
        grouped: dict[str, Fraction] = {}
        path_keys: dict[str, list[tuple[str, ...]]] = {}
        for path in paths:
            grouped[path.terminal_state_hash] = grouped.get(
                path.terminal_state_hash, Fraction(0, 1)
            ) + Fraction(path.probability_numerator, path.probability_denominator)
            path_keys.setdefault(path.terminal_state_hash, []).append(path.path_key)
        terminals = tuple(
            M36AExactTerminalOption(
                terminal_state_hash=terminal_hash,
                probability_numerator=probability.numerator,
                probability_denominator=probability.denominator,
                path_count=len(path_keys[terminal_hash]),
                path_keys=tuple(sorted(path_keys[terminal_hash])),
            )
            for terminal_hash, probability in sorted(grouped.items())
        )
        if sum(
            Fraction(option.probability_numerator, option.probability_denominator)
            for option in terminals
        ) != Fraction(1, 1):
            raise M36AChainInvariantViolation("M36-A terminal mass does not sum to 1")
        return terminals

    def sample_once(
        self,
        *,
        initial_state: ItemState,
        operations: tuple[AcceptedM36AOperation, AcceptedM36AOperation],
        decision_source: RecordingDecisionSource,
        sample_index: int,
        run_id: str,
    ) -> M36AChainTrajectory:
        self._validate_chain(operations)
        state = initial_state
        initial_hash = initial_state.state_hash()
        steps: list[M36AChainStepTrace] = []
        outcome = "completed"
        for step_index, operation in enumerate(operations):
            transition = self._sample_transition_for_step(
                state=state,
                operation=operation,
                decision_source=decision_source,
                sample_index=sample_index,
                step_index=step_index,
                run_id=run_id,
            )
            steps.append(transition.step)
            state = transition.state
            if transition.terminal:
                outcome = "no_transition_terminal"
                break
        return M36AChainTrajectory(
            sample_index=sample_index,
            outcome=outcome,
            initial_state_hash=initial_hash,
            terminal_state_hash=state.state_hash(),
            steps=tuple(steps),
        )

    def run(
        self,
        *,
        initial_state: ItemState,
        operations: tuple[AcceptedM36AOperation, AcceptedM36AOperation],
        seed: int,
        sample_count: int,
        run_id: str,
        chain_id: str = "m36a_two_step_heterogeneous_chain",
    ) -> M36AChainRunResult:
        self._validate_chain(operations)
        if not isinstance(sample_count, int) or isinstance(sample_count, bool) or sample_count < 0:
            raise SamplingContractDefect("sample_count must be a non-negative non-bool integer")
        decision_source = RecordingDecisionSource(SeededDecisionSource(seed))
        trajectories = tuple(
            self.sample_once(
                initial_state=initial_state,
                operations=operations,
                decision_source=decision_source,
                sample_index=index,
                run_id=run_id,
            )
            for index in range(sample_count)
        )
        payload = {
            "schema_version": M36A_CHAIN_SCHEMA_VERSION,
            "run_id": run_id,
            "seed": seed,
            "sample_count": sample_count,
            "chain_id": chain_id,
            "operation_ids": tuple(_operation_id(operation) for operation in operations),
            "rng_stream_version": RNG_STREAM_VERSION,
            "sampling_algorithm_id": SAMPLING_ALGORITHM_ID,
            "source_fingerprint": self.static.source_fingerprint,
            "semantic_fingerprint": self.static.semantic_fingerprint,
            "code_version": self.code_version,
            "trajectories": [trajectory.public_payload() for trajectory in trajectories],
            "decisions": [record for record in decision_source.records],
        }
        result_hash = sha256_canonical(payload, schema_version=1)
        return M36AChainRunResult(
            schema_version=M36A_CHAIN_SCHEMA_VERSION,
            run_id=run_id,
            seed=seed,
            sample_count=sample_count,
            chain_id=chain_id,
            operation_ids=tuple(_operation_id(operation) for operation in operations),  # type: ignore[arg-type]
            rng_stream_version=RNG_STREAM_VERSION,
            sampling_algorithm_id=SAMPLING_ALGORITHM_ID,
            source_fingerprint=self.static.source_fingerprint,
            semantic_fingerprint=self.static.semantic_fingerprint,
            code_version=self.code_version,
            trajectories=trajectories,
            decisions=decision_source.records,
            result_hash=result_hash,
        )

    def _exact_transitions_for_step(
        self,
        *,
        state: ItemState,
        operation: AcceptedM36AOperation,
        step_index: int,
        decision_id: str,
    ) -> tuple[_ExactTransition, ...]:
        if isinstance(operation, OrdinaryAddOperation):
            pool = self.ordinary_add.build_pool(state, operation)
            pre_hash = state.state_hash()
            if not pool.candidates:
                return (
                    _ExactTransition(
                        state=state,
                        step=M36AChainStepTrace(
                            step_index=step_index,
                            operation_id=operation.operation_id,
                            mode_id=operation.mode_id,
                            outcome="no_transition",
                            pre_state_hash=pre_hash,
                            post_state_hash=pre_hash,
                            decision_id=None,
                            selected_key=None,
                            selected_mod_id=None,
                            candidate_count=0,
                            candidate_digest=None,
                            pool_fingerprint=pool.result_fingerprint,
                            no_transition_reason=pool.empty_reason or "ordinary_add_pool_exhausted",
                            probability_numerator=1,
                            probability_denominator=1,
                        ),
                        path_component=f"{operation.operation_id}:NO_TRANSITION",
                        probability=Fraction(1, 1),
                        terminal=True,
                    ),
                )
            return tuple(
                self._ordinary_add_exact_transition(
                    state=state,
                    operation=operation,
                    option=option,
                    step_index=step_index,
                    candidate_count=len(pool.candidates),
                )
                for option in branch_options(decision_id, pool.candidates)
            )

        if isinstance(operation, AnnulmentOperation):
            pool = self.annulment.build_pool(state, operation)
            pre_hash = state.state_hash()
            metadata_by_key = _metadata_by_candidate_key(pool)
            if not pool.candidates:
                return (
                    _ExactTransition(
                        state=state,
                        step=M36AChainStepTrace(
                            step_index=step_index,
                            operation_id=operation.operation_id,
                            mode_id=operation.mode_id,
                            outcome="no_transition_no_consumption",
                            pre_state_hash=pre_hash,
                            post_state_hash=pre_hash,
                            decision_id=None,
                            selected_key=None,
                            selected_mod_id=None,
                            candidate_count=0,
                            candidate_digest=None,
                            pool_fingerprint=pool.result_fingerprint,
                            no_transition_reason=pool.empty_reason or "removal_pool_exhausted",
                            probability_numerator=1,
                            probability_denominator=1,
                        ),
                        path_component=f"{operation.operation_id}:NO_TRANSITION",
                        probability=Fraction(1, 1),
                        terminal=True,
                    ),
                )
            return tuple(
                self._annulment_exact_transition(
                    state=state,
                    operation=operation,
                    option=option,
                    selected=metadata_by_key[option.selected_key],
                    step_index=step_index,
                    candidate_count=len(pool.candidates),
                    pool_fingerprint=pool.result_fingerprint,
                )
                for option in branch_options(decision_id, pool.candidates)
            )

        raise M36AChainInvariantViolation(
            f"unsupported M36-A operation invocation: {_operation_id(operation)}"
        )

    def _sample_transition_for_step(
        self,
        *,
        state: ItemState,
        operation: AcceptedM36AOperation,
        decision_source: RecordingDecisionSource,
        sample_index: int,
        step_index: int,
        run_id: str,
    ) -> _ExactTransition:
        if isinstance(operation, OrdinaryAddOperation):
            pool = self.ordinary_add.build_pool(state, operation)
            pre_hash = state.state_hash()
            if not pool.candidates:
                return _ExactTransition(
                    state=state,
                    step=M36AChainStepTrace(
                        step_index=step_index,
                        operation_id=operation.operation_id,
                        mode_id=operation.mode_id,
                        outcome="no_transition",
                        pre_state_hash=pre_hash,
                        post_state_hash=pre_hash,
                        decision_id=None,
                        selected_key=None,
                        selected_mod_id=None,
                        candidate_count=0,
                        candidate_digest=None,
                        pool_fingerprint=pool.result_fingerprint,
                        no_transition_reason=pool.empty_reason or "ordinary_add_pool_exhausted",
                    ),
                    path_component=f"{operation.operation_id}:NO_TRANSITION",
                    probability=Fraction(1, 1),
                    terminal=True,
                )
            decision_id = (
                f"{run_id}.sample_{sample_index}.step_{step_index}."
                f"{operation.operation_id}.{operation.mode_id}"
            )
            decision = decision_source.choose_one(decision_id, pool.candidates)
            post_state = _append_ordinary_modifier(state, decision.selected.key)
            self.ordinary_add._assert_runtime_invariants(
                pre_state=state,
                post_state=post_state,
                expected_mode_id=operation.mode_id,
                actual_mode_id=operation.mode_id,
                operation_id=operation.operation_id,
            )
            return _ExactTransition(
                state=post_state,
                step=M36AChainStepTrace(
                    step_index=step_index,
                    operation_id=operation.operation_id,
                    mode_id=operation.mode_id,
                    outcome="applied",
                    pre_state_hash=pre_hash,
                    post_state_hash=post_state.state_hash(),
                    decision_id=decision.record.decision_id,
                    selected_key=decision.selected.key,
                    selected_mod_id=decision.selected.key,
                    candidate_count=decision.record.candidate_count,
                    candidate_digest=decision.record.candidate_digest,
                    pool_fingerprint=pool.result_fingerprint,
                    no_transition_reason=None,
                ),
                path_component=f"{operation.operation_id}:{decision.selected.key}",
                probability=Fraction(1, 1),
                terminal=False,
            )

        if isinstance(operation, AnnulmentOperation):
            pool = self.annulment.build_pool(state, operation)
            pre_hash = state.state_hash()
            metadata_by_key = _metadata_by_candidate_key(pool)
            if not pool.candidates:
                return _ExactTransition(
                    state=state,
                    step=M36AChainStepTrace(
                        step_index=step_index,
                        operation_id=operation.operation_id,
                        mode_id=operation.mode_id,
                        outcome="no_transition_no_consumption",
                        pre_state_hash=pre_hash,
                        post_state_hash=pre_hash,
                        decision_id=None,
                        selected_key=None,
                        selected_mod_id=None,
                        candidate_count=0,
                        candidate_digest=None,
                        pool_fingerprint=pool.result_fingerprint,
                        no_transition_reason=pool.empty_reason or "removal_pool_exhausted",
                    ),
                    path_component=f"{operation.operation_id}:NO_TRANSITION",
                    probability=Fraction(1, 1),
                    terminal=True,
                )
            decision_id = (
                f"{run_id}.sample_{sample_index}.step_{step_index}."
                f"{operation.operation_id}.{operation.mode_id}"
            )
            decision = decision_source.choose_one(decision_id, pool.candidates)
            selected = metadata_by_key[decision.selected.key]
            post_state = _remove_modifier_instance(state, selected)
            exact = self._annulment_exact_transition(
                state=state,
                operation=operation,
                option=BranchOption(
                    decision_id=decision.record.decision_id,
                    candidate_digest=decision.record.candidate_digest,
                    selected_rank=decision.record.selected_rank,
                    selected_key=decision.selected.key,
                    weight=decision.selected.weight,
                    total_weight=decision.record.total_weight or 0,
                    probability_numerator=1,
                    probability_denominator=1,
                ),
                selected=selected,
                step_index=step_index,
                candidate_count=decision.record.candidate_count,
                pool_fingerprint=pool.result_fingerprint,
            )
            return _ExactTransition(
                state=post_state,
                step=M36AChainStepTrace(
                    step_index=exact.step.step_index,
                    operation_id=exact.step.operation_id,
                    mode_id=exact.step.mode_id,
                    outcome=exact.step.outcome,
                    pre_state_hash=exact.step.pre_state_hash,
                    post_state_hash=exact.step.post_state_hash,
                    decision_id=decision.record.decision_id,
                    selected_key=decision.selected.key,
                    selected_mod_id=exact.step.selected_mod_id,
                    candidate_count=decision.record.candidate_count,
                    candidate_digest=decision.record.candidate_digest,
                    pool_fingerprint=pool.result_fingerprint,
                    no_transition_reason=None,
                ),
                path_component=f"{operation.operation_id}:{decision.selected.key}",
                probability=Fraction(1, 1),
                terminal=False,
            )

        raise M36AChainInvariantViolation(
            f"unsupported M36-A operation invocation: {_operation_id(operation)}"
        )

    def _ordinary_add_exact_transition(
        self,
        *,
        state: ItemState,
        operation: OrdinaryAddOperation,
        option: BranchOption,
        step_index: int,
        candidate_count: int,
    ) -> _ExactTransition:
        pre_hash = state.state_hash()
        post_state = _append_ordinary_modifier(state, option.selected_key)
        self.ordinary_add._assert_runtime_invariants(
            pre_state=state,
            post_state=post_state,
            expected_mode_id=operation.mode_id,
            actual_mode_id=operation.mode_id,
            operation_id=operation.operation_id,
        )
        return _ExactTransition(
            state=post_state,
            step=M36AChainStepTrace(
                step_index=step_index,
                operation_id=operation.operation_id,
                mode_id=operation.mode_id,
                outcome="applied",
                pre_state_hash=pre_hash,
                post_state_hash=post_state.state_hash(),
                decision_id=option.decision_id,
                selected_key=option.selected_key,
                selected_mod_id=option.selected_key,
                candidate_count=candidate_count,
                candidate_digest=option.candidate_digest,
                pool_fingerprint=option.candidate_digest,
                no_transition_reason=None,
                probability_numerator=option.probability_numerator,
                probability_denominator=option.probability_denominator,
            ),
            path_component=f"{operation.operation_id}:{option.selected_key}",
            probability=Fraction(option.probability_numerator, option.probability_denominator),
            terminal=False,
        )

    def _annulment_exact_transition(
        self,
        *,
        state: ItemState,
        operation: AnnulmentOperation,
        option: BranchOption,
        selected: RemovalInstanceMetadata,
        step_index: int,
        candidate_count: int,
        pool_fingerprint: str,
    ) -> _ExactTransition:
        pre_hash = state.state_hash()
        post_state = _remove_modifier_instance(state, selected)
        # _remove_modifier_instance and annulment pool validation preserve fractured protection.
        if tuple(mod for mod in state.modifiers if mod.fractured) != tuple(
            mod for mod in post_state.modifiers if mod.fractured
        ):
            raise M36AChainInvariantViolation("fractured modifier changed in M36-A chain")
        return _ExactTransition(
            state=post_state,
            step=M36AChainStepTrace(
                step_index=step_index,
                operation_id=operation.operation_id,
                mode_id=operation.mode_id,
                outcome="applied",
                pre_state_hash=pre_hash,
                post_state_hash=post_state.state_hash(),
                decision_id=option.decision_id,
                selected_key=option.selected_key,
                selected_mod_id=selected.mod_id,
                candidate_count=candidate_count,
                candidate_digest=option.candidate_digest,
                pool_fingerprint=pool_fingerprint,
                no_transition_reason=None,
                probability_numerator=option.probability_numerator,
                probability_denominator=option.probability_denominator,
            ),
            path_component=f"{operation.operation_id}:{option.selected_key}",
            probability=Fraction(option.probability_numerator, option.probability_denominator),
            terminal=False,
        )

    def _validate_chain(
        self,
        operations: tuple[AcceptedM36AOperation, AcceptedM36AOperation],
    ) -> None:
        if not isinstance(operations, tuple) or len(operations) != M36A_SEQUENCE_LENGTH:
            raise M36AChainInvariantViolation("M36-A requires exactly two fixed steps")
        for operation in operations:
            self._validate_operation_admission(operation)
        operation_ids = tuple(_operation_id(operation) for operation in operations)
        if Counter(operation_ids) != Counter({MC_OPERATION_ID: 1, ANNULMENT_OPERATION_ID: 1}):
            raise M36AChainInvariantViolation(
                "M36-A requires one ordinary_add step and one base annulment step"
            )

    def _validate_operation_admission(self, operation: AcceptedM36AOperation) -> None:
        if isinstance(operation, OrdinaryAddOperation):
            self.ordinary_add._validate_operation(operation)
            return
        if isinstance(operation, AnnulmentOperation):
            row = _operation_row(self.static.operations, operation.operation_id)
            if row is None:
                raise M36AChainInvariantViolation(
                    f"operation row missing from data/operations.yaml: {operation.operation_id}"
                )
            if row.get("runtime_admission_status") != ACCEPTED_RUNTIME_STATUS:
                raise M36AChainInvariantViolation(
                    f"operation row is not executable-admitted: {operation.operation_id}"
                )
            if operation.operation_id != ANNULMENT_OPERATION_ID:
                raise M36AChainInvariantViolation(
                    f"unsupported admitted operation row for M36-A: {operation.operation_id}"
                )
            return
        if isinstance(operation, CatalogOperationInvocation):
            row = _operation_row(self.static.operations, operation.operation_id)
            if row is None:
                raise M36AChainInvariantViolation(
                    f"unknown operation row: {operation.operation_id}"
                )
            raise M36AChainInvariantViolation(
                "catalog operation is not executable in M36-A: "
                f"{operation.operation_id} "
                f"(runtime_admission_status={row.get('runtime_admission_status')!r})"
            )
        raise M36AChainInvariantViolation("unsupported M36-A operation object")

    @staticmethod
    def _assert_mass_conservation(paths: list[M36AExactChainPath]) -> None:
        total = sum(
            Fraction(path.probability_numerator, path.probability_denominator)
            for path in paths
        )
        if total != Fraction(1, 1):
            raise M36AChainInvariantViolation("M36-A exact path mass does not sum to 1")


def _operation_id(operation: AcceptedM36AOperation) -> str:
    return operation.operation_id


def _operation_row(operations: Any, operation_id: str) -> dict[str, Any] | None:
    if not isinstance(operations, dict):
        return None
    for row in operations.get("operations") or ():
        if isinstance(row, dict) and row.get("operation_id") == operation_id:
            return row
    return None


__all__ = [
    "ACCEPTED_RUNTIME_STATUS",
    "CatalogOperationInvocation",
    "M36A_CHAIN_SCHEMA_VERSION",
    "M36A_CONSTRUCTED_FIXTURE_LABEL",
    "M36A_SEMANTICS_VERSION",
    "M36A_SEQUENCE_LENGTH",
    "M36AChainError",
    "M36AChainInvariantViolation",
    "M36AChainRunResult",
    "M36AChainStepTrace",
    "M36AChainTrajectory",
    "M36AExactChainPath",
    "M36AExactTerminalOption",
    "M36AHeterogeneousChainHarness",
]
