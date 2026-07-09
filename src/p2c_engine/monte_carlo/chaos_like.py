from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from p2c_engine.canonical.hashes import sha256_canonical
from p2c_engine.decisions import RecordingDecisionSource, SeededDecisionSource
from p2c_engine.domain.candidate import BranchOption
from p2c_engine.domain.decision import DecisionRecord
from p2c_engine.domain.defects import SamplingContractDefect
from p2c_engine.domain.enums import Rarity
from p2c_engine.domain.item_state import ItemState
from p2c_engine.domain.pool_building import RemovalInstanceMetadata
from p2c_engine.domain.versions import RNG_STREAM_VERSION, SAMPLING_ALGORITHM_ID
from p2c_engine.legality.pool_builders import (
    OrdinaryAddPoolRequest,
    RemovalPoolRequest,
    build_ordinary_add_pool,
    build_removal_pool,
)
from p2c_engine.sampling.exact import branch_options
from p2c_engine.static_data.game_data import StaticGameData

from .annulment import (
    RemovalPoolBuilder,
    _metadata_by_candidate_key,
    _remove_modifier_instance,
    _validate_annulment_pool,
)
from .heterogeneous_chain import ACCEPTED_RUNTIME_STATUS, _operation_row
from .ordinary_add import (
    M32_VALUE_POLICY,
    M32InvariantViolation,
    M32MonteCarloError,
    PoolBuilder,
    _append_ordinary_modifier,
    _assert_capacity,
    _assert_duplicate_family_and_groups,
    _assert_fractured_suffix_unchanged,
)


M37A_CHAOSLIKE_SCHEMA_VERSION = "p2c.m37a.chaoslike_remove_then_add.v1"
M37A_CHAOSLIKE_SEMANTICS_VERSION = "p2c.m37a.base_chaos.project_model.v1"
CHAOS_OPERATION_ID = "chaos"
M37A_PROJECT_MODEL_POLICY = (
    "base chaos removes uniformly over eligible removable non-fractured installed "
    "modifier instances, then adds from the accepted combined generation_weight "
    "ordinary-add pool; Whittling and side Omens are not base behavior"
)


class M37AChaosLikeError(M32MonteCarloError):
    """Base class for M37-A base Chaos-like runtime failures."""


class M37AChaosLikeInvariantViolation(M37AChaosLikeError, M32InvariantViolation):
    """Raised when base Chaos-like runtime invariants fail."""


@dataclass(frozen=True, slots=True)
class ChaosLikeOperation:
    """One M37-A base Chaos-like operation invocation.

    M37-A admits only base `chaos`. Whittling, side Omens, Greater/Perfect
    Chaos, MML, and every other Chaos-like variant remain out of scope.
    """

    mode_id: str
    operation_id: str = CHAOS_OPERATION_ID
    item_class: str = "quarterstaff"
    semantics_version: str = M37A_CHAOSLIKE_SEMANTICS_VERSION


@dataclass(frozen=True, slots=True)
class ChaosLikeStepTrace:
    step_index: int
    stage: str
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
            "stage": self.stage,
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
class ExactChaosLikePath:
    path_key: tuple[str, ...]
    terminal_state_hash: str
    outcome: str
    steps: tuple[ChaosLikeStepTrace, ...]
    probability_numerator: int
    probability_denominator: int


@dataclass(frozen=True, slots=True)
class ExactChaosLikeTerminalOption:
    terminal_state_hash: str
    probability_numerator: int
    probability_denominator: int
    path_count: int
    path_keys: tuple[tuple[str, ...], ...]


@dataclass(frozen=True, slots=True)
class ChaosLikeTrajectory:
    sample_index: int
    outcome: str
    initial_state_hash: str
    terminal_state_hash: str
    steps: tuple[ChaosLikeStepTrace, ...]

    def public_payload(self) -> dict[str, object]:
        return {
            "sample_index": self.sample_index,
            "outcome": self.outcome,
            "initial_state_hash": self.initial_state_hash,
            "terminal_state_hash": self.terminal_state_hash,
            "steps": [step.public_payload() for step in self.steps],
        }


@dataclass(frozen=True, slots=True)
class ChaosLikeRunResult:
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
    trajectories: tuple[ChaosLikeTrajectory, ...]
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
            "mode_id": self.mode_id,
            "operation_id": self.operation_id,
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


class ChaosLikeMonteCarloHarness:
    """Exact/oracle and seeded MC harness for M37-A base Chaos-like runtime only."""

    def __init__(
        self,
        *,
        static: StaticGameData,
        ordinary_add_pool_builder: PoolBuilder = build_ordinary_add_pool,
        removal_pool_builder: RemovalPoolBuilder = build_removal_pool,
        code_version: str = "p2c.m37a.dev",
    ) -> None:
        self.static = static
        self.ordinary_add_pool_builder = ordinary_add_pool_builder
        self.removal_pool_builder = removal_pool_builder
        self.code_version = code_version

    def build_removal_pool(self, state: ItemState, operation: ChaosLikeOperation):
        self._validate_operation(operation, state)
        request = RemovalPoolRequest(
            item_class=operation.item_class,
            state=state,
        )
        pool = self.removal_pool_builder(request, self.static)
        _validate_annulment_pool(pool)
        return pool

    def build_add_pool(self, state: ItemState, operation: ChaosLikeOperation):
        self._validate_operation(operation, state)
        request = OrdinaryAddPoolRequest(
            item_class=operation.item_class,
            state=state,
            side_filter=None,
            mml=None,
        )
        return self.ordinary_add_pool_builder(request, self.static)

    def enumerate_paths(
        self,
        *,
        initial_state: ItemState,
        operation: ChaosLikeOperation,
        decision_id_prefix: str,
        max_exact_paths: int,
    ) -> tuple[ExactChaosLikePath, ...]:
        self._validate_operation(operation, initial_state)
        if not isinstance(max_exact_paths, int) or isinstance(max_exact_paths, bool) or max_exact_paths <= 0:
            raise SamplingContractDefect("max_exact_paths must be a positive integer")

        initial_hash = initial_state.state_hash()
        removal_pool = self.build_removal_pool(initial_state, operation)
        removal_metadata = _metadata_by_candidate_key(removal_pool)
        if not removal_pool.candidates:
            paths = [
                ExactChaosLikePath(
                    path_key=("remove:NO_TRANSITION",),
                    terminal_state_hash=initial_hash,
                    outcome="no_transition_no_consumption",
                    steps=(
                        ChaosLikeStepTrace(
                            step_index=0,
                            stage="remove",
                            outcome="no_transition_no_consumption",
                            pre_state_hash=initial_hash,
                            post_state_hash=initial_hash,
                            decision_id=None,
                            selected_key=None,
                            selected_mod_id=None,
                            candidate_count=0,
                            candidate_digest=None,
                            pool_fingerprint=removal_pool.result_fingerprint,
                            no_transition_reason=removal_pool.empty_reason
                            or "removal_pool_exhausted",
                            probability_numerator=1,
                            probability_denominator=1,
                        ),
                    ),
                    probability_numerator=1,
                    probability_denominator=1,
                )
            ]
            self._assert_mass_conservation(paths)
            return tuple(paths)

        paths: list[ExactChaosLikePath] = []
        for removal_option in branch_options(
            f"{decision_id_prefix}.step_0.{operation.operation_id}.{operation.mode_id}.remove",
            removal_pool.candidates,
        ):
            selected = removal_metadata[removal_option.selected_key]
            post_removal_state = _remove_modifier_instance(initial_state, selected)
            self._assert_remove_invariants(
                pre_state=initial_state,
                post_state=post_removal_state,
                selected=selected,
            )
            remove_step = self._remove_step(
                operation=operation,
                state=initial_state,
                post_state=post_removal_state,
                option=removal_option,
                selected=selected,
                candidate_count=len(removal_pool.candidates),
                pool_fingerprint=removal_pool.result_fingerprint,
            )
            add_pool = self.build_add_pool(post_removal_state, operation)
            removal_probability = Fraction(
                removal_option.probability_numerator,
                removal_option.probability_denominator,
            )
            if not add_pool.candidates:
                add_step = ChaosLikeStepTrace(
                    step_index=1,
                    stage="add",
                    outcome="no_transition_no_consumption",
                    pre_state_hash=post_removal_state.state_hash(),
                    post_state_hash=initial_hash,
                    decision_id=None,
                    selected_key=None,
                    selected_mod_id=None,
                    candidate_count=0,
                    candidate_digest=None,
                    pool_fingerprint=add_pool.result_fingerprint,
                    no_transition_reason=add_pool.empty_reason or "ordinary_add_pool_exhausted",
                    probability_numerator=1,
                    probability_denominator=1,
                )
                paths.append(
                    ExactChaosLikePath(
                        path_key=(
                            f"remove:{removal_option.selected_key}",
                            "add:NO_TRANSITION",
                        ),
                        terminal_state_hash=initial_hash,
                        outcome="no_transition_no_consumption",
                        steps=(remove_step, add_step),
                        probability_numerator=removal_probability.numerator,
                        probability_denominator=removal_probability.denominator,
                    )
                )
                if len(paths) > max_exact_paths:
                    raise SamplingContractDefect("M37-A exact path ceiling exceeded")
                continue

            for add_option in branch_options(
                f"{decision_id_prefix}.step_1.{operation.operation_id}.{operation.mode_id}.add.{removal_option.selected_key}",
                add_pool.candidates,
            ):
                terminal_state = _append_ordinary_modifier(
                    post_removal_state,
                    add_option.selected_key,
                )
                self._assert_add_invariants(
                    pre_state=initial_state,
                    post_removal_state=post_removal_state,
                    terminal_state=terminal_state,
                )
                add_probability = Fraction(
                    add_option.probability_numerator,
                    add_option.probability_denominator,
                )
                path_probability = removal_probability * add_probability
                paths.append(
                    ExactChaosLikePath(
                        path_key=(
                            f"remove:{removal_option.selected_key}",
                            f"add:{add_option.selected_key}",
                        ),
                        terminal_state_hash=terminal_state.state_hash(),
                        outcome="completed",
                        steps=(
                            remove_step,
                            self._add_step(
                                state=post_removal_state,
                                post_state=terminal_state,
                                option=add_option,
                                candidate_count=len(add_pool.candidates),
                                pool_fingerprint=add_pool.result_fingerprint,
                            ),
                        ),
                        probability_numerator=path_probability.numerator,
                        probability_denominator=path_probability.denominator,
                    )
                )
                if len(paths) > max_exact_paths:
                    raise SamplingContractDefect("M37-A exact path ceiling exceeded")
        self._assert_mass_conservation(paths)
        return tuple(paths)

    def enumerate_terminal_distribution(
        self,
        *,
        initial_state: ItemState,
        operation: ChaosLikeOperation,
        decision_id_prefix: str,
        max_exact_paths: int,
    ) -> tuple[ExactChaosLikeTerminalOption, ...]:
        paths = self.enumerate_paths(
            initial_state=initial_state,
            operation=operation,
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
            ExactChaosLikeTerminalOption(
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
            raise M37AChaosLikeInvariantViolation("M37-A terminal mass does not sum to 1")
        return terminals

    def sample_once(
        self,
        *,
        initial_state: ItemState,
        operation: ChaosLikeOperation,
        decision_source: RecordingDecisionSource,
        sample_index: int,
        run_id: str,
    ) -> ChaosLikeTrajectory:
        self._validate_operation(operation, initial_state)
        initial_hash = initial_state.state_hash()
        removal_pool = self.build_removal_pool(initial_state, operation)
        removal_metadata = _metadata_by_candidate_key(removal_pool)
        if not removal_pool.candidates:
            return ChaosLikeTrajectory(
                sample_index=sample_index,
                outcome="no_transition_no_consumption",
                initial_state_hash=initial_hash,
                terminal_state_hash=initial_hash,
                steps=(
                    ChaosLikeStepTrace(
                        step_index=0,
                        stage="remove",
                        outcome="no_transition_no_consumption",
                        pre_state_hash=initial_hash,
                        post_state_hash=initial_hash,
                        decision_id=None,
                        selected_key=None,
                        selected_mod_id=None,
                        candidate_count=0,
                        candidate_digest=None,
                        pool_fingerprint=removal_pool.result_fingerprint,
                        no_transition_reason=removal_pool.empty_reason
                        or "removal_pool_exhausted",
                    ),
                ),
            )

        removal_decision_id = (
            f"{run_id}.sample_{sample_index}.step_0."
            f"{operation.operation_id}.{operation.mode_id}.remove"
        )
        removal_decision = decision_source.choose_one(
            removal_decision_id,
            removal_pool.candidates,
        )
        selected = removal_metadata[removal_decision.selected.key]
        post_removal_state = _remove_modifier_instance(initial_state, selected)
        self._assert_remove_invariants(
            pre_state=initial_state,
            post_state=post_removal_state,
            selected=selected,
        )
        remove_step = ChaosLikeStepTrace(
            step_index=0,
            stage="remove",
            outcome="applied_on_branch_copy",
            pre_state_hash=initial_hash,
            post_state_hash=post_removal_state.state_hash(),
            decision_id=removal_decision.record.decision_id,
            selected_key=removal_decision.selected.key,
            selected_mod_id=selected.mod_id,
            candidate_count=removal_decision.record.candidate_count,
            candidate_digest=removal_decision.record.candidate_digest,
            pool_fingerprint=removal_pool.result_fingerprint,
            no_transition_reason=None,
        )

        add_pool = self.build_add_pool(post_removal_state, operation)
        if not add_pool.candidates:
            add_step = ChaosLikeStepTrace(
                step_index=1,
                stage="add",
                outcome="no_transition_no_consumption",
                pre_state_hash=post_removal_state.state_hash(),
                post_state_hash=initial_hash,
                decision_id=None,
                selected_key=None,
                selected_mod_id=None,
                candidate_count=0,
                candidate_digest=None,
                pool_fingerprint=add_pool.result_fingerprint,
                no_transition_reason=add_pool.empty_reason or "ordinary_add_pool_exhausted",
            )
            return ChaosLikeTrajectory(
                sample_index=sample_index,
                outcome="no_transition_no_consumption",
                initial_state_hash=initial_hash,
                terminal_state_hash=initial_hash,
                steps=(remove_step, add_step),
            )

        add_decision_id = (
            f"{run_id}.sample_{sample_index}.step_1."
            f"{operation.operation_id}.{operation.mode_id}.add"
        )
        add_decision = decision_source.choose_one(add_decision_id, add_pool.candidates)
        terminal_state = _append_ordinary_modifier(
            post_removal_state,
            add_decision.selected.key,
        )
        self._assert_add_invariants(
            pre_state=initial_state,
            post_removal_state=post_removal_state,
            terminal_state=terminal_state,
        )
        add_step = ChaosLikeStepTrace(
            step_index=1,
            stage="add",
            outcome="applied",
            pre_state_hash=post_removal_state.state_hash(),
            post_state_hash=terminal_state.state_hash(),
            decision_id=add_decision.record.decision_id,
            selected_key=add_decision.selected.key,
            selected_mod_id=add_decision.selected.key,
            candidate_count=add_decision.record.candidate_count,
            candidate_digest=add_decision.record.candidate_digest,
            pool_fingerprint=add_pool.result_fingerprint,
            no_transition_reason=None,
        )
        return ChaosLikeTrajectory(
            sample_index=sample_index,
            outcome="completed",
            initial_state_hash=initial_hash,
            terminal_state_hash=terminal_state.state_hash(),
            steps=(remove_step, add_step),
        )

    def run(
        self,
        *,
        initial_state: ItemState,
        operation: ChaosLikeOperation,
        seed: int,
        sample_count: int,
        run_id: str,
    ) -> ChaosLikeRunResult:
        self._validate_operation(operation, initial_state)
        if not isinstance(sample_count, int) or isinstance(sample_count, bool) or sample_count < 0:
            raise SamplingContractDefect("sample_count must be a non-negative non-bool integer")
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
            "schema_version": M37A_CHAOSLIKE_SCHEMA_VERSION,
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
            "decisions": [record for record in decision_source.records],
        }
        result_hash = sha256_canonical(payload, schema_version=1)
        return ChaosLikeRunResult(
            schema_version=M37A_CHAOSLIKE_SCHEMA_VERSION,
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
            decisions=decision_source.records,
            result_hash=result_hash,
        )

    def _validate_operation(self, operation: ChaosLikeOperation, state: ItemState) -> None:
        if operation.operation_id != CHAOS_OPERATION_ID:
            raise M37AChaosLikeInvariantViolation(
                f"unsupported M37-A operation_id: {operation.operation_id}"
            )
        if operation.semantics_version != M37A_CHAOSLIKE_SEMANTICS_VERSION:
            raise M37AChaosLikeInvariantViolation("chaos-like semantics version mismatch")
        if operation.item_class != state.item_class:
            raise M37AChaosLikeInvariantViolation("operation item_class does not match state")
        if state.rarity != Rarity.RARE:
            raise M37AChaosLikeInvariantViolation("base Chaos-like runtime supports rare states only")
        row = _operation_row(self.static.operations, operation.operation_id)
        if row is None:
            raise M37AChaosLikeInvariantViolation(
                f"operation row missing from data/operations.yaml: {operation.operation_id}"
            )
        if row.get("runtime_admission_status") != ACCEPTED_RUNTIME_STATUS:
            raise M37AChaosLikeInvariantViolation(
                f"operation row is not executable-admitted: {operation.operation_id}"
            )
        transition = row.get("transition") if isinstance(row, dict) else None
        add = transition.get("add") if isinstance(transition, dict) else None
        if isinstance(add, dict) and add.get("mml") is not None:
            raise M37AChaosLikeInvariantViolation("M37-A base Chaos must not use MML")

    def _remove_step(
        self,
        *,
        operation: ChaosLikeOperation,
        state: ItemState,
        post_state: ItemState,
        option: BranchOption,
        selected: RemovalInstanceMetadata,
        candidate_count: int,
        pool_fingerprint: str,
    ) -> ChaosLikeStepTrace:
        return ChaosLikeStepTrace(
            step_index=0,
            stage="remove",
            outcome="applied_on_branch_copy",
            pre_state_hash=state.state_hash(),
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
        )

    @staticmethod
    def _add_step(
        *,
        state: ItemState,
        post_state: ItemState,
        option: BranchOption,
        candidate_count: int,
        pool_fingerprint: str,
    ) -> ChaosLikeStepTrace:
        return ChaosLikeStepTrace(
            step_index=1,
            stage="add",
            outcome="applied",
            pre_state_hash=state.state_hash(),
            post_state_hash=post_state.state_hash(),
            decision_id=option.decision_id,
            selected_key=option.selected_key,
            selected_mod_id=option.selected_key,
            candidate_count=candidate_count,
            candidate_digest=option.candidate_digest,
            pool_fingerprint=pool_fingerprint,
            no_transition_reason=None,
            probability_numerator=option.probability_numerator,
            probability_denominator=option.probability_denominator,
        )

    def _assert_remove_invariants(
        self,
        *,
        pre_state: ItemState,
        post_state: ItemState,
        selected: RemovalInstanceMetadata,
    ) -> None:
        if selected.fractured:
            raise M37AChaosLikeInvariantViolation("fractured modifier selected for Chaos removal")
        if len(post_state.modifiers) != len(pre_state.modifiers) - 1:
            raise M37AChaosLikeInvariantViolation("Chaos remove stage must remove exactly one modifier")
        if tuple(mod for mod in pre_state.modifiers if mod.fractured) != tuple(
            mod for mod in post_state.modifiers if mod.fractured
        ):
            raise M37AChaosLikeInvariantViolation("fractured modifier changed during Chaos removal")

    def _assert_add_invariants(
        self,
        *,
        pre_state: ItemState,
        post_removal_state: ItemState,
        terminal_state: ItemState,
    ) -> None:
        if len(terminal_state.modifiers) != len(pre_state.modifiers):
            raise M37AChaosLikeInvariantViolation(
                "completed Chaos-like operation must remove one and add one modifier"
            )
        if len(terminal_state.modifiers) != len(post_removal_state.modifiers) + 1:
            raise M37AChaosLikeInvariantViolation("Chaos add stage must add exactly one modifier")
        if tuple(mod for mod in pre_state.modifiers if mod.fractured) != tuple(
            mod for mod in terminal_state.modifiers if mod.fractured
        ):
            raise M37AChaosLikeInvariantViolation("fractured modifier changed during Chaos add")
        _assert_fractured_suffix_unchanged(
            pre_state,
            terminal_state,
            self.static.modifier_index,
        )
        _assert_capacity(terminal_state, self.static.modifier_index)
        _assert_duplicate_family_and_groups(terminal_state, self.static.modifier_index)

    @staticmethod
    def _assert_mass_conservation(paths: list[ExactChaosLikePath]) -> None:
        total = sum(
            Fraction(path.probability_numerator, path.probability_denominator)
            for path in paths
        )
        if total != Fraction(1, 1):
            raise M37AChaosLikeInvariantViolation("M37-A exact path mass does not sum to 1")


__all__ = [
    "CHAOS_OPERATION_ID",
    "M37A_CHAOSLIKE_SCHEMA_VERSION",
    "M37A_CHAOSLIKE_SEMANTICS_VERSION",
    "M37A_PROJECT_MODEL_POLICY",
    "ChaosLikeMonteCarloHarness",
    "ChaosLikeOperation",
    "ChaosLikeRunResult",
    "ChaosLikeStepTrace",
    "ChaosLikeTrajectory",
    "ExactChaosLikePath",
    "ExactChaosLikeTerminalOption",
    "M37AChaosLikeError",
    "M37AChaosLikeInvariantViolation",
]
