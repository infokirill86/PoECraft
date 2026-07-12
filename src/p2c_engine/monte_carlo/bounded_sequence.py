from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction
from types import MappingProxyType
from typing import Literal, Mapping

from p2c_engine.canonical.hashes import sha256_canonical
from p2c_engine.decisions import RecordingDecisionSource, SeededDecisionSource
from p2c_engine.domain.decision import DecisionRecord
from p2c_engine.domain.defects import SamplingContractDefect
from p2c_engine.domain.item_state import ItemState
from p2c_engine.domain.versions import RNG_STREAM_VERSION, SAMPLING_ALGORITHM_ID
from p2c_engine.operations.resolver import (
    M38AResolverAdmissionError,
    OperationResolver,
    OperationResolverRequest,
    ResolvedOperationPlan,
)
from p2c_engine.sampling.exact import branch_options
from p2c_engine.static_data.game_data import StaticGameData

from .annulment import (
    ANNULMENT_OPERATION_ID,
    AnnulmentMonteCarloHarness,
    AnnulmentOperation,
    _assert_annulment_runtime_invariants,
    _metadata_by_candidate_key,
    _remove_modifier_instance,
)
from .chaos_like import (
    M39B_CHAOS_OPERATION_IDS,
    ChaosLikeMonteCarloHarness,
    ChaosLikeOperation,
)
from .greater_essence import (
    M41A_OPERATION_IDS,
    GreaterEssenceHarness,
    GreaterEssenceOperation,
)
from .ordinary_add import (
    MC_OPERATION_ID,
    M32_VALUE_POLICY,
    M32InvariantViolation,
    M32MonteCarloError,
    OrdinaryAddMonteCarloHarness,
    OrdinaryAddOperation,
    _append_ordinary_modifier,
)
from .perfect_essence import (
    M42A_OPERATION_IDS,
    PerfectEssenceHarness,
    PerfectEssenceOperation,
)
from .rarity_progression import (
    M40A_OPERATION_IDS,
    CatalogSingleAddHarness,
    CatalogSingleAddOperation,
)
from .alchemy import (
    M44A_ALCHEMY_OPERATION_ID,
    M44A_MAX_EXACT_PATHS,
    AlchemyHarness,
    AlchemyOperation,
    M44AExactCeilingExceeded,
)
from .greater_exaltation import (
    GreaterExaltationHarness,
    M45AGreaterExaltationCeilingExceeded,
)
from .fracture import (
    FRACTURING_ORB_OPERATION_ID,
    FractureHarness,
    FractureOperation,
    _fracture_modifier_instance,
    _metadata_by_candidate_key as _fracture_metadata_by_candidate_key,
    _assert_fracture_transition,
)


M43A_SCHEMA_VERSION = "p2c.m43a.bounded_accepted_operation_sequence.v1"
M43A_SEMANTICS_VERSION = "p2c.m43a.accepted_composition.project_model.v1"
M43A_MIN_STEPS = 1
M43A_MAX_STEPS = 8
M43A_MAX_CANDIDATES_PER_POOL = 256
M43A_MAX_EXACT_PATHS = 65_536
M43A_MAX_EXACT_TERMINALS = 65_536
M43A_FIXED_SEEDS = (43_001, 43_002, 43_003)
M43A_SAMPLE_TIERS = (512, 2_048, 8_192)

ExecutorId = Literal[
    "ordinary_add",
    "annulment",
    "chaos_like",
    "catalog_single_add",
    "greater_essence",
    "perfect_essence",
    "alchemy",
    "fracture",
]


class M43ASequenceError(M32MonteCarloError):
    """Base error for the bounded accepted-operation sequence runtime."""


class M43ASequenceAdmissionError(M43ASequenceError):
    """Fail-closed request, admission, or executor-registry error."""


class M43ASequenceInvariantViolation(M43ASequenceError, M32InvariantViolation):
    """Raised when accepted composition invariants fail."""


@dataclass(frozen=True, slots=True)
class BoundedSequenceStep:
    step_id: str
    currency_id: str
    mode_id: str
    variant_id: str | None = None
    active_modifier_ids: tuple[str, ...] = ()
    mml: int | None = None


@dataclass(frozen=True, slots=True)
class BoundedSequenceRequest:
    sequence_id: str
    steps: tuple[BoundedSequenceStep, ...]
    stop_on_no_transition: bool = True


@dataclass(frozen=True, slots=True)
class SequenceStepTrace:
    step_index: int
    step_id: str
    currency_id: str
    operation_id: str
    mode_id: str
    executor_id: ExecutorId
    outcome: str
    pre_state_hash: str
    post_state_hash: str
    resolver_plan_digest: str
    transition_key: str
    decision_ids: tuple[str, ...]
    selected_keys: tuple[str, ...]
    candidate_count: int
    pool_digest: str | None
    no_transition_reason: str | None
    probability_numerator: int | None = None
    probability_denominator: int | None = None

    def public_payload(self) -> dict[str, object]:
        return {
            "step_index": self.step_index,
            "step_id": self.step_id,
            "currency_id": self.currency_id,
            "operation_id": self.operation_id,
            "mode_id": self.mode_id,
            "executor_id": self.executor_id,
            "outcome": self.outcome,
            "pre_state_hash": self.pre_state_hash,
            "post_state_hash": self.post_state_hash,
            "resolver_plan_digest": self.resolver_plan_digest,
            "transition_key": self.transition_key,
            "decision_ids": self.decision_ids,
            "selected_keys": self.selected_keys,
            "candidate_count": self.candidate_count,
            "pool_digest": self.pool_digest,
            "no_transition_reason": self.no_transition_reason,
        }


@dataclass(frozen=True, slots=True)
class ExactCeilingStop:
    stop_code: Literal[
        "candidate_branch_ceiling_exceeded",
        "exact_path_ceiling_exceeded",
        "exact_terminal_ceiling_exceeded",
    ]
    ceiling_name: str
    ceiling_limit: int
    observed_count: int
    step_index: int
    step_id: str
    currency_id: str
    message: str


@dataclass(frozen=True, slots=True)
class ExactSequencePath:
    path_key: tuple[str, ...]
    terminal_state: ItemState
    terminal_state_hash: str
    execution_terminal_key: str
    outcome: str
    completed_step_count: int
    terminal_step_index: int | None
    steps: tuple[SequenceStepTrace, ...]
    probability_numerator: int
    probability_denominator: int


@dataclass(frozen=True, slots=True)
class ExactExecutionTerminal:
    execution_terminal_key: str
    terminal_state: ItemState
    terminal_state_hash: str
    outcome: str
    completed_step_count: int
    terminal_step_index: int | None
    path_count: int
    path_keys: tuple[tuple[str, ...], ...]
    probability_numerator: int
    probability_denominator: int


@dataclass(frozen=True, slots=True)
class ExactStateProjection:
    terminal_state: ItemState
    terminal_state_hash: str
    execution_terminal_count: int
    path_count: int
    probability_numerator: int
    probability_denominator: int


@dataclass(frozen=True, slots=True)
class ExactStepMarginal:
    step_index: int
    step_id: str
    post_state_hash: str
    outcome: str
    probability_numerator: int
    probability_denominator: int


@dataclass(frozen=True, slots=True)
class ExactSequenceEvaluation:
    schema_version: str
    status: Literal["completed", "ceiling_exceeded"]
    sequence_id: str
    path_count: int
    terminal_count: int
    mass_sum_exactly_one: bool
    paths: tuple[ExactSequencePath, ...]
    terminals: tuple[ExactExecutionTerminal, ...]
    ceiling_stop: ExactCeilingStop | None

    def public_summary(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "status": self.status,
            "numeric_probability_free": True,
            "public_numeric_release": False,
            "probability_values_printed": False,
            "value_policy": M32_VALUE_POLICY,
            "sequence_id": self.sequence_id,
            "path_count": self.path_count,
            "terminal_count": self.terminal_count,
            "mass_sum_exactly_one": self.mass_sum_exactly_one,
            "ceiling_hit": self.ceiling_stop is not None,
            "ceiling_stop_code": (
                self.ceiling_stop.stop_code if self.ceiling_stop else None
            ),
        }

    def state_only_projection(self) -> tuple[ExactStateProjection, ...]:
        if self.status != "completed":
            return ()
        masses: dict[str, Fraction] = defaultdict(Fraction)
        states: dict[str, ItemState] = {}
        terminal_counts: dict[str, int] = defaultdict(int)
        path_counts: dict[str, int] = defaultdict(int)
        for terminal in self.terminals:
            key = terminal.terminal_state_hash
            masses[key] += Fraction(
                terminal.probability_numerator, terminal.probability_denominator
            )
            states[key] = terminal.terminal_state
            terminal_counts[key] += 1
            path_counts[key] += terminal.path_count
        return tuple(
            ExactStateProjection(
                terminal_state=states[state_hash],
                terminal_state_hash=state_hash,
                execution_terminal_count=terminal_counts[state_hash],
                path_count=path_counts[state_hash],
                probability_numerator=mass.numerator,
                probability_denominator=mass.denominator,
            )
            for state_hash, mass in sorted(masses.items())
        )

    def step_marginals(self) -> tuple[ExactStepMarginal, ...]:
        if self.status != "completed":
            return ()
        masses: dict[tuple[int, str, str, str], Fraction] = defaultdict(Fraction)
        for path in self.paths:
            path_mass = Fraction(
                path.probability_numerator, path.probability_denominator
            )
            for trace in path.steps:
                key = (
                    trace.step_index,
                    trace.step_id,
                    trace.post_state_hash,
                    trace.outcome,
                )
                masses[key] += path_mass
        return tuple(
            ExactStepMarginal(
                step_index=key[0],
                step_id=key[1],
                post_state_hash=key[2],
                outcome=key[3],
                probability_numerator=mass.numerator,
                probability_denominator=mass.denominator,
            )
            for key, mass in sorted(masses.items())
        )


@dataclass(frozen=True, slots=True)
class SequenceTrajectory:
    sample_index: int
    outcome: str
    initial_state_hash: str
    terminal_state: ItemState
    terminal_state_hash: str
    execution_terminal_key: str
    completed_step_count: int
    terminal_step_index: int | None
    steps: tuple[SequenceStepTrace, ...]

    def public_payload(self) -> dict[str, object]:
        return {
            "sample_index": self.sample_index,
            "outcome": self.outcome,
            "initial_state_hash": self.initial_state_hash,
            "terminal_state_hash": self.terminal_state_hash,
            "execution_terminal_key": self.execution_terminal_key,
            "completed_step_count": self.completed_step_count,
            "terminal_step_index": self.terminal_step_index,
            "steps": [step.public_payload() for step in self.steps],
        }


@dataclass(frozen=True, slots=True)
class SequenceRunResult:
    schema_version: str
    semantics_version: str
    run_id: str
    seed: int
    sample_count: int
    sequence_id: str
    currency_ids: tuple[str, ...]
    rng_stream_version: int
    sampling_algorithm_id: str
    source_fingerprint: str
    semantic_fingerprint: str
    code_version: str
    trajectories: tuple[SequenceTrajectory, ...]
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
            "sequence_id": self.sequence_id,
            "currency_ids": self.currency_ids,
            "source_fingerprint": self.source_fingerprint,
            "semantic_fingerprint": self.semantic_fingerprint,
            "trajectory_count": len(self.trajectories),
            "decision_count": len(self.decisions),
            "execution_terminal_count": len(
                {row.execution_terminal_key for row in self.trajectories}
            ),
            "result_hash": self.result_hash,
        }


@dataclass(frozen=True, slots=True)
class _StepTransition:
    state: ItemState
    trace: SequenceStepTrace
    path_component: str
    probability: Fraction
    terminal: bool


class _ExactCeilingExceeded(RuntimeError):
    def __init__(self, stop: ExactCeilingStop) -> None:
        super().__init__(stop.message)
        self.stop = stop


class AcceptedOperationExecutorRegistry:
    """Explicit currency-id to accepted executor mapping.

    Runtime admission is necessary but not sufficient. A future admitted row is
    rejected until its currency id is deliberately added to this registry.
    """

    def __init__(self, mapping: Mapping[str, ExecutorId] | None = None) -> None:
        selected = _default_executor_mapping() if mapping is None else mapping
        self._mapping = MappingProxyType(dict(selected))

    @property
    def mapping(self) -> Mapping[str, ExecutorId]:
        return self._mapping

    def executor_for(self, currency_id: str, static: StaticGameData) -> ExecutorId:
        executor = self._mapping.get(currency_id)
        if executor is not None:
            return executor
        row = _operation_row(static, currency_id)
        if row is not None and row.get("runtime_admission_status") == "accepted_executable_runtime":
            raise M43ASequenceAdmissionError(
                "operation is executable-admitted but has no M43-A accepted executor: "
                f"{currency_id}"
            )
        raise M43ASequenceAdmissionError(
            f"operation is not admitted in the M43-A executor registry: {currency_id}"
        )


class BoundedAcceptedOperationSequenceHarness:
    """One-to-eight-step evaluator over already accepted operations only."""

    def __init__(
        self,
        *,
        static: StaticGameData,
        resolver: OperationResolver | None = None,
        executor_registry: AcceptedOperationExecutorRegistry | None = None,
        code_version: str = "p2c.m43a.dev",
    ) -> None:
        self.static = static
        self.resolver = resolver or OperationResolver(static=static)
        self.executor_registry = executor_registry or AcceptedOperationExecutorRegistry()
        self.ordinary = OrdinaryAddMonteCarloHarness(static=static, code_version=code_version)
        self.annulment = AnnulmentMonteCarloHarness(static=static, code_version=code_version)
        self.chaos = ChaosLikeMonteCarloHarness(static=static, code_version=code_version)
        self.catalog_add = CatalogSingleAddHarness(static=static, code_version=code_version)
        self.greater_essence = GreaterEssenceHarness(static=static, code_version=code_version)
        self.perfect_essence = PerfectEssenceHarness(static=static, code_version=code_version)
        self.alchemy = AlchemyHarness(static=static, code_version=code_version)
        self.greater_exaltation = GreaterExaltationHarness(
            static=static, code_version=code_version
        )
        self.fracture = FractureHarness(static=static, code_version=code_version)
        self.code_version = code_version

    def enumerate_exact(
        self,
        *,
        initial_state: ItemState,
        request: BoundedSequenceRequest,
        decision_id_prefix: str,
        max_candidates_per_pool: int = M43A_MAX_CANDIDATES_PER_POOL,
        max_exact_paths: int = M43A_MAX_EXACT_PATHS,
        max_exact_terminals: int = M43A_MAX_EXACT_TERMINALS,
    ) -> ExactSequenceEvaluation:
        self._validate_request(request)
        self._validate_ceiling("max_candidates_per_pool", max_candidates_per_pool)
        self._validate_ceiling("max_exact_paths", max_exact_paths)
        self._validate_ceiling("max_exact_terminals", max_exact_terminals)
        frontier: list[
            tuple[ItemState, Fraction, tuple[SequenceStepTrace, ...], tuple[str, ...], int]
        ] = [(initial_state, Fraction(1, 1), (), (), 0)]
        terminal_paths: list[ExactSequencePath] = []

        try:
            for step_index, step in enumerate(request.steps):
                next_frontier: list[
                    tuple[ItemState, Fraction, tuple[SequenceStepTrace, ...], tuple[str, ...], int]
                ] = []
                for state, path_mass, traces, path_key, completed_count in frontier:
                    transitions = self._exact_transitions(
                        state=state,
                        step=step,
                        step_index=step_index,
                        decision_id_prefix=decision_id_prefix,
                        max_candidates_per_pool=max_candidates_per_pool,
                    )
                    for transition in transitions:
                        mass = path_mass * transition.probability
                        next_traces = traces + (transition.trace,)
                        next_key = path_key + (transition.path_component,)
                        next_completed = completed_count + (0 if transition.terminal else 1)
                        final_step = step_index == len(request.steps) - 1
                        if transition.terminal or final_step:
                            outcome = (
                                transition.trace.outcome if transition.terminal else "completed"
                            )
                            terminal_index = step_index if transition.terminal else None
                            terminal_paths.append(
                                self._exact_path(
                                    state=transition.state,
                                    path_key=next_key,
                                    traces=next_traces,
                                    outcome=outcome,
                                    completed_step_count=next_completed,
                                    terminal_step_index=terminal_index,
                                    probability=mass,
                                )
                            )
                        else:
                            next_frontier.append(
                                (
                                    transition.state,
                                    mass,
                                    next_traces,
                                    next_key,
                                    next_completed,
                                )
                            )
                        observed_paths = len(terminal_paths) + len(next_frontier)
                        if observed_paths > max_exact_paths:
                            raise _ExactCeilingExceeded(
                                self._ceiling_stop(
                                    "exact_path_ceiling_exceeded",
                                    "max_exact_paths",
                                    max_exact_paths,
                                    observed_paths,
                                    step_index,
                                    step,
                                )
                            )
                        observed_terminals = len(
                            {path.execution_terminal_key for path in terminal_paths}
                        )
                        if observed_terminals > max_exact_terminals:
                            raise _ExactCeilingExceeded(
                                self._ceiling_stop(
                                    "exact_terminal_ceiling_exceeded",
                                    "max_exact_terminals",
                                    max_exact_terminals,
                                    observed_terminals,
                                    step_index,
                                    step,
                                )
                            )
                frontier = next_frontier
        except _ExactCeilingExceeded as exc:
            return ExactSequenceEvaluation(
                schema_version=M43A_SCHEMA_VERSION,
                status="ceiling_exceeded",
                sequence_id=request.sequence_id,
                path_count=0,
                terminal_count=0,
                mass_sum_exactly_one=False,
                paths=(),
                terminals=(),
                ceiling_stop=exc.stop,
            )

        terminals = self._aggregate_execution_terminals(terminal_paths)
        mass = sum(
            (
                Fraction(path.probability_numerator, path.probability_denominator)
                for path in terminal_paths
            ),
            Fraction(0, 1),
        )
        if mass != Fraction(1, 1):
            raise M43ASequenceInvariantViolation(
                f"M43-A exact path mass does not sum to one: {mass}"
            )
        terminal_mass = sum(
            (
                Fraction(row.probability_numerator, row.probability_denominator)
                for row in terminals
            ),
            Fraction(0, 1),
        )
        if terminal_mass != Fraction(1, 1):
            raise M43ASequenceInvariantViolation(
                f"M43-A execution-terminal mass does not sum to one: {terminal_mass}"
            )
        return ExactSequenceEvaluation(
            schema_version=M43A_SCHEMA_VERSION,
            status="completed",
            sequence_id=request.sequence_id,
            path_count=len(terminal_paths),
            terminal_count=len(terminals),
            mass_sum_exactly_one=True,
            paths=tuple(terminal_paths),
            terminals=terminals,
            ceiling_stop=None,
        )

    def sample_once(
        self,
        *,
        initial_state: ItemState,
        request: BoundedSequenceRequest,
        decision_source: RecordingDecisionSource,
        sample_index: int,
        run_id: str,
    ) -> SequenceTrajectory:
        self._validate_request(request)
        state = initial_state
        traces: list[SequenceStepTrace] = []
        completed_count = 0
        outcome = "completed"
        terminal_step_index: int | None = None
        for step_index, step in enumerate(request.steps):
            transition = self._sample_transition(
                state=state,
                step=step,
                step_index=step_index,
                decision_source=decision_source,
                sample_index=sample_index,
                run_id=run_id,
            )
            traces.append(transition.trace)
            state = transition.state
            if transition.terminal:
                outcome = transition.trace.outcome
                terminal_step_index = step_index
                break
            completed_count += 1
        key = _execution_terminal_key(
            state_hash=state.state_hash(),
            outcome=outcome,
            completed_step_count=completed_count,
            terminal_step_index=terminal_step_index,
        )
        return SequenceTrajectory(
            sample_index=sample_index,
            outcome=outcome,
            initial_state_hash=initial_state.state_hash(),
            terminal_state=state,
            terminal_state_hash=state.state_hash(),
            execution_terminal_key=key,
            completed_step_count=completed_count,
            terminal_step_index=terminal_step_index,
            steps=tuple(traces),
        )

    def run(
        self,
        *,
        initial_state: ItemState,
        request: BoundedSequenceRequest,
        seed: int,
        sample_count: int,
        run_id: str,
    ) -> SequenceRunResult:
        self._validate_request(request)
        if isinstance(sample_count, bool) or not isinstance(sample_count, int) or sample_count < 0:
            raise SamplingContractDefect(
                "sample_count must be a non-negative non-bool integer"
            )
        source = RecordingDecisionSource(SeededDecisionSource(seed))
        trajectories = tuple(
            self.sample_once(
                initial_state=initial_state,
                request=request,
                decision_source=source,
                sample_index=index,
                run_id=run_id,
            )
            for index in range(sample_count)
        )
        payload = {
            "schema_version": M43A_SCHEMA_VERSION,
            "semantics_version": M43A_SEMANTICS_VERSION,
            "run_id": run_id,
            "seed": seed,
            "sample_count": sample_count,
            "sequence_id": request.sequence_id,
            "currency_ids": tuple(step.currency_id for step in request.steps),
            "rng_stream_version": RNG_STREAM_VERSION,
            "sampling_algorithm_id": SAMPLING_ALGORITHM_ID,
            "source_fingerprint": self.static.source_fingerprint,
            "semantic_fingerprint": self.static.semantic_fingerprint,
            "code_version": self.code_version,
            "trajectories": [row.public_payload() for row in trajectories],
            "decisions": list(source.records),
        }
        return SequenceRunResult(
            schema_version=M43A_SCHEMA_VERSION,
            semantics_version=M43A_SEMANTICS_VERSION,
            run_id=run_id,
            seed=seed,
            sample_count=sample_count,
            sequence_id=request.sequence_id,
            currency_ids=tuple(step.currency_id for step in request.steps),
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
        expected: SequenceRunResult,
        initial_state: ItemState,
        request: BoundedSequenceRequest,
    ) -> SequenceRunResult:
        replayed = self.run(
            initial_state=initial_state,
            request=request,
            seed=expected.seed,
            sample_count=expected.sample_count,
            run_id=expected.run_id,
        )
        if replayed != expected:
            raise M43ASequenceInvariantViolation(
                "M43-A deterministic replay mismatch"
            )
        return replayed

    def _validate_request(self, request: BoundedSequenceRequest) -> None:
        if not isinstance(request.sequence_id, str) or not request.sequence_id.strip():
            raise M43ASequenceAdmissionError("sequence_id must be a non-empty string")
        if request.stop_on_no_transition is not True:
            raise M43ASequenceAdmissionError(
                "M43-A requires stop_on_no_transition=true"
            )
        if not isinstance(request.steps, tuple) or not (
            M43A_MIN_STEPS <= len(request.steps) <= M43A_MAX_STEPS
        ):
            raise M43ASequenceAdmissionError(
                f"M43-A sequences require {M43A_MIN_STEPS}-{M43A_MAX_STEPS} steps"
            )
        ids: set[str] = set()
        for step in request.steps:
            if not isinstance(step, BoundedSequenceStep):
                raise M43ASequenceAdmissionError(
                    "every M43-A step must be BoundedSequenceStep"
                )
            if not step.step_id or not step.currency_id or not step.mode_id:
                raise M43ASequenceAdmissionError(
                    "step_id, currency_id, and mode_id must be non-empty"
                )
            if step.step_id in ids:
                raise M43ASequenceAdmissionError(
                    f"duplicate M43-A step_id: {step.step_id}"
                )
            ids.add(step.step_id)
            if step.variant_id not in (None, "", "base"):
                raise M43ASequenceAdmissionError(
                    f"unsupported sequence variant: {step.variant_id}"
                )
            if not isinstance(step.active_modifier_ids, tuple) or any(
                not isinstance(value, str) or not value
                for value in step.active_modifier_ids
            ):
                raise M43ASequenceAdmissionError(
                    "active_modifier_ids must be a tuple of non-empty strings"
                )
            self.executor_registry.executor_for(step.currency_id, self.static)

    def _validate_ceiling(self, name: str, value: int) -> None:
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise SamplingContractDefect(f"{name} must be a positive non-bool integer")

    def _resolve(
        self, state: ItemState, step: BoundedSequenceStep
    ) -> ResolvedOperationPlan | None:
        try:
            return self.resolver.resolve(
                OperationResolverRequest(
                    currency_id=step.currency_id,
                    item_state=state,
                    mode_id=step.mode_id,
                    variant_id=step.variant_id,
                    active_modifier_ids=step.active_modifier_ids,
                    mml=step.mml,
                )
            )
        except M38AResolverAdmissionError as exc:
            if "does not accept the current item rarity" in str(exc):
                return None
            raise M43ASequenceAdmissionError(
                f"resolver rejected registered M43-A operation {step.currency_id}: {exc}"
            ) from exc

    def _exact_transitions(
        self,
        *,
        state: ItemState,
        step: BoundedSequenceStep,
        step_index: int,
        decision_id_prefix: str,
        max_candidates_per_pool: int,
    ) -> tuple[_StepTransition, ...]:
        executor_id = self.executor_registry.executor_for(step.currency_id, self.static)
        plan = self._resolve(state, step)
        if plan is None:
            return (
                self._resolver_no_transition(
                    state=state,
                    step=step,
                    step_index=step_index,
                    executor_id=executor_id,
                ),
            )
        self._assert_plan_executor(plan, executor_id)
        decision_id = (
            f"{decision_id_prefix}.step_{step_index}.{plan.operation_id}.{step.mode_id}"
        )
        if plan.filters.add_count == 2:
            return self._greater_exaltation_exact(
                state,
                step,
                step_index,
                plan,
                decision_id,
                max_candidates_per_pool,
                executor_id,
            )
        if executor_id == "ordinary_add":
            return self._ordinary_exact(state, step, step_index, plan, decision_id, max_candidates_per_pool)
        if executor_id == "annulment":
            return self._annulment_exact(state, step, step_index, plan, decision_id, max_candidates_per_pool)
        if executor_id == "chaos_like":
            return self._chaos_exact(state, step, step_index, plan, decision_id, max_candidates_per_pool)
        if executor_id == "catalog_single_add":
            return self._catalog_exact(state, step, step_index, plan, decision_id, max_candidates_per_pool)
        if executor_id == "greater_essence":
            return self._greater_exact(state, step, step_index, plan)
        if executor_id == "perfect_essence":
            return self._perfect_exact(state, step, step_index, plan, decision_id, max_candidates_per_pool)
        if executor_id == "alchemy":
            return self._alchemy_exact(
                state,
                step,
                step_index,
                plan,
                decision_id,
                max_candidates_per_pool,
            )
        if executor_id == "fracture":
            return self._fracture_exact(
                state, step, step_index, plan, decision_id, max_candidates_per_pool
            )
        raise M43ASequenceAdmissionError(f"unsupported executor id: {executor_id}")

    def _sample_transition(
        self,
        *,
        state: ItemState,
        step: BoundedSequenceStep,
        step_index: int,
        decision_source: RecordingDecisionSource,
        sample_index: int,
        run_id: str,
    ) -> _StepTransition:
        executor_id = self.executor_registry.executor_for(step.currency_id, self.static)
        plan = self._resolve(state, step)
        if plan is None:
            return self._resolver_no_transition(
                state=state,
                step=step,
                step_index=step_index,
                executor_id=executor_id,
            )
        self._assert_plan_executor(plan, executor_id)
        if plan.filters.add_count == 2:
            return self._greater_exaltation_sample(
                state,
                step,
                step_index,
                plan,
                decision_source,
                sample_index,
                run_id,
                executor_id,
            )
        if executor_id == "ordinary_add":
            return self._ordinary_sample(state, step, step_index, plan, decision_source, sample_index, run_id)
        if executor_id == "annulment":
            return self._annulment_sample(state, step, step_index, plan, decision_source, sample_index, run_id)
        if executor_id == "chaos_like":
            return self._chaos_sample(state, step, step_index, plan, decision_source, sample_index, run_id)
        if executor_id == "catalog_single_add":
            return self._catalog_sample(state, step, step_index, plan, decision_source, sample_index, run_id)
        if executor_id == "greater_essence":
            return self._greater_sample(state, step, step_index, plan)
        if executor_id == "perfect_essence":
            return self._perfect_sample(state, step, step_index, plan, decision_source, sample_index, run_id)
        if executor_id == "alchemy":
            return self._alchemy_sample(
                state,
                step,
                step_index,
                plan,
                decision_source,
                sample_index,
                run_id,
            )
        if executor_id == "fracture":
            return self._fracture_sample(
                state,
                step,
                step_index,
                plan,
                decision_source,
                sample_index,
                run_id,
            )
        raise M43ASequenceAdmissionError(f"unsupported executor id: {executor_id}")

    def _ordinary_exact(self, state, step, step_index, plan, decision_id, ceiling):
        operation = _expect_operation(plan, OrdinaryAddOperation)
        pool = self.ordinary.build_pool(state, operation)
        self._candidate_ceiling(pool.candidates, ceiling, step_index, step)
        if not pool.candidates:
            return (self._no_transition(state, step, step_index, plan, "ordinary_add", pool.empty_reason or "ordinary_add_pool_exhausted", pool.result_fingerprint),)
        output = []
        for option in branch_options(decision_id, pool.candidates):
            post = _append_ordinary_modifier(state, option.selected_key)
            self.ordinary._assert_runtime_invariants(pre_state=state, post_state=post, expected_mode_id=operation.mode_id, actual_mode_id=operation.mode_id, operation_id=operation.operation_id)
            output.append(self._transition(state, post, step, step_index, plan, "ordinary_add", "applied", f"add:{option.selected_key}", (option.decision_id,), (option.selected_key,), len(pool.candidates), option.candidate_digest, None, Fraction(option.probability_numerator, option.probability_denominator), False))
        return tuple(output)

    def _annulment_exact(self, state, step, step_index, plan, decision_id, ceiling):
        operation = _expect_operation(plan, AnnulmentOperation)
        pool = self.annulment.build_pool(state, operation)
        self._candidate_ceiling(pool.candidates, ceiling, step_index, step)
        metadata = _metadata_by_candidate_key(pool)
        if not pool.candidates:
            return (self._no_transition(state, step, step_index, plan, "annulment", pool.empty_reason or "removal_pool_exhausted", pool.result_fingerprint),)
        output = []
        for option in branch_options(decision_id, pool.candidates):
            selected = metadata[option.selected_key]
            post = _remove_modifier_instance(state, selected)
            _assert_annulment_runtime_invariants(pre_state=state, post_state=post, selected_metadata=selected, operation_id=operation.operation_id, modifier_index=self.static.modifier_index)
            output.append(self._transition(state, post, step, step_index, plan, "annulment", "applied", f"remove:{option.selected_key}", (option.decision_id,), (option.selected_key,), len(pool.candidates), option.candidate_digest, None, Fraction(option.probability_numerator, option.probability_denominator), False))
        return tuple(output)

    def _fracture_exact(self, state, step, step_index, plan, decision_id, ceiling):
        operation = _expect_operation(plan, FractureOperation)
        pool = self.fracture.build_pool(state, operation)
        self._candidate_ceiling(pool.candidates, ceiling, step_index, step)
        if not pool.candidates:
            return (
                self._no_transition(
                    state,
                    step,
                    step_index,
                    plan,
                    "fracture",
                    pool.empty_reason or "fracture_candidate_pool_exhausted",
                    pool.result_fingerprint,
                ),
            )
        metadata = _fracture_metadata_by_candidate_key(pool)
        output = []
        for option in branch_options(decision_id, pool.candidates):
            selected = metadata[option.selected_key]
            post = _fracture_modifier_instance(state, selected)
            _assert_fracture_transition(state, post, selected, self.static)
            output.append(
                self._transition(
                    state,
                    post,
                    step,
                    step_index,
                    plan,
                    "fracture",
                    "applied",
                    f"fracture:{option.selected_key}",
                    (option.decision_id,),
                    (option.selected_key,),
                    len(pool.candidates),
                    option.candidate_digest,
                    None,
                    Fraction(option.probability_numerator, option.probability_denominator),
                    False,
                )
            )
        return tuple(output)

    def _chaos_exact(self, state, step, step_index, plan, decision_id, ceiling):
        operation = _expect_operation(plan, ChaosLikeOperation)
        removal_pool = self.chaos.build_removal_pool(state, operation)
        self._candidate_ceiling(removal_pool.candidates, ceiling, step_index, step)
        metadata = _metadata_by_candidate_key(removal_pool)
        if not removal_pool.candidates:
            return (self._no_transition(state, step, step_index, plan, "chaos_like", removal_pool.empty_reason or "removal_pool_exhausted", removal_pool.result_fingerprint),)
        output = []
        for removal_option in branch_options(f"{decision_id}.remove", removal_pool.candidates):
            selected = metadata[removal_option.selected_key]
            removed = _remove_modifier_instance(state, selected)
            self.chaos._assert_remove_invariants(pre_state=state, post_state=removed, selected=selected)
            add_pool = self.chaos.build_add_pool(removed, operation)
            self._candidate_ceiling(add_pool.candidates, ceiling, step_index, step)
            removal_mass = Fraction(removal_option.probability_numerator, removal_option.probability_denominator)
            if not add_pool.candidates:
                digest = _combined_digest(removal_pool.result_fingerprint, add_pool.result_fingerprint)
                output.append(self._transition(state, state, step, step_index, plan, "chaos_like", "no_transition_no_consumption", f"remove:{removal_option.selected_key}|add:NO_TRANSITION", (removal_option.decision_id,), (removal_option.selected_key,), len(removal_pool.candidates), digest, add_pool.empty_reason or "ordinary_add_pool_exhausted", removal_mass, True))
                continue
            for add_option in branch_options(f"{decision_id}.add.{removal_option.selected_key}", add_pool.candidates):
                post = _append_ordinary_modifier(removed, add_option.selected_key)
                self.chaos._assert_add_invariants(pre_state=state, post_removal_state=removed, terminal_state=post)
                mass = removal_mass * Fraction(add_option.probability_numerator, add_option.probability_denominator)
                digest = _combined_digest(removal_pool.result_fingerprint, add_pool.result_fingerprint)
                output.append(self._transition(state, post, step, step_index, plan, "chaos_like", "completed", f"remove:{removal_option.selected_key}|add:{add_option.selected_key}", (removal_option.decision_id, add_option.decision_id), (removal_option.selected_key, add_option.selected_key), len(removal_pool.candidates) + len(add_pool.candidates), digest, None, mass, False))
        return tuple(output)

    def _catalog_exact(self, state, step, step_index, plan, decision_id, ceiling):
        operation = _expect_operation(plan, CatalogSingleAddOperation)
        reason = self.catalog_add._precondition_failure(state, operation)
        if reason is not None:
            return (self._no_transition(state, step, step_index, plan, "catalog_single_add", reason, None),)
        pool = self.catalog_add.build_pool(state, operation)
        self._candidate_ceiling(pool.candidates, ceiling, step_index, step)
        if not pool.candidates:
            return (self._no_transition(state, step, step_index, plan, "catalog_single_add", pool.empty_reason or "ordinary_add_pool_exhausted", pool.result_fingerprint),)
        working = self.catalog_add._working_state(state, operation)
        output = []
        for option in branch_options(decision_id, pool.candidates):
            post = _append_ordinary_modifier(working, option.selected_key)
            self.catalog_add._assert_applied_transition(state, post, operation)
            output.append(self._transition(state, post, step, step_index, plan, "catalog_single_add", "applied", f"add:{option.selected_key}", (option.decision_id,), (option.selected_key,), len(pool.candidates), option.candidate_digest, None, Fraction(option.probability_numerator, option.probability_denominator), False))
        return tuple(output)

    def _greater_exact(self, state, step, step_index, plan):
        operation = _expect_operation(plan, GreaterEssenceOperation)
        terminal, reason = self.greater_essence._transition(state, operation)
        if terminal is None:
            return (self._no_transition(state, step, step_index, plan, "greater_essence", reason or "greater_essence_precondition_failed", None),)
        return (self._transition(state, terminal, step, step_index, plan, "greater_essence", "applied", f"guaranteed:{operation.guaranteed_mod_id}", (), (operation.guaranteed_mod_id,), 0, None, None, Fraction(1, 1), False),)

    def _perfect_exact(self, state, step, step_index, plan, decision_id, ceiling):
        operation = _expect_operation(plan, PerfectEssenceOperation)
        pool = self.perfect_essence.build_feasible_pool(state, operation)
        self._candidate_ceiling(pool.candidates, ceiling, step_index, step)
        metadata = {row.candidate_key: row for row in pool.removal_metadata}
        if not pool.candidates:
            return (self._no_transition(state, step, step_index, plan, "perfect_essence", pool.empty_reason or "feasible_removal_pool_exhausted", pool.result_fingerprint),)
        output = []
        for option in branch_options(decision_id, pool.candidates):
            selected = metadata[option.selected_key]
            post = self.perfect_essence._terminal_for_candidate(state, operation, selected)
            if post is None:
                raise M43ASequenceInvariantViolation("perfect Essence feasible candidate became invalid")
            self.perfect_essence._assert_terminal_invariants(state, post, operation, selected)
            output.append(self._transition(state, post, step, step_index, plan, "perfect_essence", "completed", f"remove:{option.selected_key}|guaranteed:{operation.guaranteed_mod_id}", (option.decision_id,), (option.selected_key, operation.guaranteed_mod_id), len(pool.candidates), pool.result_fingerprint, None, Fraction(option.probability_numerator, option.probability_denominator), False))
        return tuple(output)

    def _alchemy_exact(self, state, step, step_index, plan, decision_id, ceiling):
        operation = _expect_operation(plan, AlchemyOperation)
        try:
            paths = self.alchemy.enumerate_paths(
                initial_state=state,
                operation=operation,
                decision_id_prefix=decision_id,
                max_candidates_per_pool=ceiling,
                max_exact_paths=M44A_MAX_EXACT_PATHS,
            )
        except M44AExactCeilingExceeded as exc:
            raise _ExactCeilingExceeded(
                self._ceiling_stop(
                    "alchemy_internal_exact_ceiling_exceeded",
                    exc.ceiling_name,
                    exc.ceiling_limit,
                    exc.observed_count,
                    step_index,
                    step,
                )
            ) from exc
        output = []
        for path in paths:
            decision_ids = tuple(
                trace.decision_id for trace in path.traces if trace.decision_id is not None
            )
            key = (
                "alchemy:" + "|".join(path.selected_mod_ids)
                if path.outcome == "completed"
                else f"alchemy:NO_TRANSITION:{path.no_transition_reason}"
            )
            output.append(
                self._transition(
                    state,
                    path.terminal_state,
                    step,
                    step_index,
                    plan,
                    "alchemy",
                    path.outcome,
                    key,
                    decision_ids,
                    path.selected_mod_ids,
                    path.candidate_count_total,
                    path.pool_digest,
                    path.no_transition_reason,
                    Fraction(path.probability_numerator, path.probability_denominator),
                    path.outcome != "completed",
                )
            )
        return tuple(output)

    def _greater_exaltation_exact(
        self,
        state,
        step,
        step_index,
        plan,
        decision_id,
        ceiling,
        executor_id,
    ):
        operation = plan.operation
        if not isinstance(operation, (OrdinaryAddOperation, CatalogSingleAddOperation)):
            raise M43ASequenceAdmissionError(
                "Greater Exaltation plan must wrap an accepted Exalted add executor"
            )
        try:
            paths = self.greater_exaltation.enumerate_paths(
                initial_state=state,
                operation=operation,
                decision_id_prefix=decision_id,
                max_candidates_per_pool=ceiling,
                max_exact_paths=M43A_MAX_EXACT_PATHS,
            )
        except M45AGreaterExaltationCeilingExceeded as exc:
            raise _ExactCeilingExceeded(
                self._ceiling_stop(
                    "greater_exaltation_internal_exact_ceiling_exceeded",
                    exc.ceiling_name,
                    exc.limit,
                    exc.observed,
                    step_index,
                    step,
                )
            ) from exc
        output = []
        for path in paths:
            decision_ids = tuple(
                trace.decision_id for trace in path.traces if trace.decision_id is not None
            )
            pool_digest = _combined_digest(
                *(trace.pool_fingerprint for trace in path.traces)
            )
            key = (
                "greater_exaltation:" + "|".join(path.selected_mod_ids)
                if path.outcome == "completed"
                else f"greater_exaltation:NO_TRANSITION:{path.no_transition_reason}"
            )
            output.append(
                self._transition(
                    state,
                    path.terminal_state,
                    step,
                    step_index,
                    plan,
                    executor_id,
                    path.outcome,
                    key,
                    decision_ids,
                    path.selected_mod_ids,
                    sum(trace.candidate_count for trace in path.traces),
                    pool_digest,
                    path.no_transition_reason,
                    Fraction(path.probability_numerator, path.probability_denominator),
                    path.outcome != "completed",
                )
            )
        return tuple(output)

    def _ordinary_sample(self, state, step, step_index, plan, source, sample_index, run_id):
        operation = _expect_operation(plan, OrdinaryAddOperation)
        pool = self.ordinary.build_pool(state, operation)
        if not pool.candidates:
            return self._no_transition(state, step, step_index, plan, "ordinary_add", pool.empty_reason or "ordinary_add_pool_exhausted", pool.result_fingerprint)
        decision_id = self._sample_decision_id(
            run_id, sample_index, step_index, step, operation.operation_id
        )
        decision = source.choose_one(decision_id, pool.candidates)
        post = _append_ordinary_modifier(state, decision.selected.key)
        self.ordinary._assert_runtime_invariants(pre_state=state, post_state=post, expected_mode_id=operation.mode_id, actual_mode_id=operation.mode_id, operation_id=operation.operation_id)
        return self._transition(state, post, step, step_index, plan, "ordinary_add", "applied", f"add:{decision.selected.key}", (decision.record.decision_id,), (decision.selected.key,), decision.record.candidate_count, decision.record.candidate_digest, None, Fraction(1, 1), False)

    def _annulment_sample(self, state, step, step_index, plan, source, sample_index, run_id):
        operation = _expect_operation(plan, AnnulmentOperation)
        pool = self.annulment.build_pool(state, operation)
        metadata = _metadata_by_candidate_key(pool)
        if not pool.candidates:
            return self._no_transition(state, step, step_index, plan, "annulment", pool.empty_reason or "removal_pool_exhausted", pool.result_fingerprint)
        decision_id = self._sample_decision_id(
            run_id, sample_index, step_index, step, operation.operation_id
        )
        decision = source.choose_one(decision_id, pool.candidates)
        selected = metadata[decision.selected.key]
        post = _remove_modifier_instance(state, selected)
        _assert_annulment_runtime_invariants(pre_state=state, post_state=post, selected_metadata=selected, operation_id=operation.operation_id, modifier_index=self.static.modifier_index)
        return self._transition(state, post, step, step_index, plan, "annulment", "applied", f"remove:{decision.selected.key}", (decision.record.decision_id,), (decision.selected.key,), decision.record.candidate_count, decision.record.candidate_digest, None, Fraction(1, 1), False)

    def _fracture_sample(self, state, step, step_index, plan, source, sample_index, run_id):
        operation = _expect_operation(plan, FractureOperation)
        decision_id = self._sample_decision_id(
            run_id, sample_index, step_index, step, operation.operation_id
        )
        trajectory = self.fracture.sample_once(
            state=state,
            operation=operation,
            decision_source=source,
            sample_index=sample_index,
            run_id=run_id,
            decision_id=decision_id,
        )
        if trajectory.outcome != "applied":
            return self._no_transition(
                state,
                step,
                step_index,
                plan,
                "fracture",
                trajectory.no_transition_reason or "fracture_candidate_pool_exhausted",
                trajectory.pool_fingerprint,
            )
        selected = _fracture_metadata_by_candidate_key(
            self.fracture.build_pool(state, operation)
        )[trajectory.selected_candidate_key]
        post = _fracture_modifier_instance(state, selected)
        _assert_fracture_transition(state, post, selected, self.static)
        return self._transition(
            state,
            post,
            step,
            step_index,
            plan,
            "fracture",
            "applied",
            f"fracture:{trajectory.selected_candidate_key}",
            (trajectory.decision_id,),
            (trajectory.selected_candidate_key,),
            trajectory.candidate_count,
            trajectory.candidate_digest,
            None,
            Fraction(1, 1),
            False,
        )

    def _chaos_sample(self, state, step, step_index, plan, source, sample_index, run_id):
        operation = _expect_operation(plan, ChaosLikeOperation)
        removal_pool = self.chaos.build_removal_pool(state, operation)
        metadata = _metadata_by_candidate_key(removal_pool)
        if not removal_pool.candidates:
            return self._no_transition(state, step, step_index, plan, "chaos_like", removal_pool.empty_reason or "removal_pool_exhausted", removal_pool.result_fingerprint)
        prefix = self._sample_decision_id(
            run_id, sample_index, step_index, step, operation.operation_id
        )
        removal_id = f"{prefix}.remove"
        removal = source.choose_one(removal_id, removal_pool.candidates)
        selected = metadata[removal.selected.key]
        removed = _remove_modifier_instance(state, selected)
        self.chaos._assert_remove_invariants(pre_state=state, post_state=removed, selected=selected)
        add_pool = self.chaos.build_add_pool(removed, operation)
        digest = _combined_digest(removal_pool.result_fingerprint, add_pool.result_fingerprint)
        if not add_pool.candidates:
            return self._transition(state, state, step, step_index, plan, "chaos_like", "no_transition_no_consumption", f"remove:{removal.selected.key}|add:NO_TRANSITION", (removal.record.decision_id,), (removal.selected.key,), removal.record.candidate_count, digest, add_pool.empty_reason or "ordinary_add_pool_exhausted", Fraction(1, 1), True)
        add_id = f"{prefix}.add" if step_index != 0 else f"{run_id}.sample_{sample_index}.step_1.{operation.operation_id}.{operation.mode_id}.add"
        add = source.choose_one(add_id, add_pool.candidates)
        post = _append_ordinary_modifier(removed, add.selected.key)
        self.chaos._assert_add_invariants(pre_state=state, post_removal_state=removed, terminal_state=post)
        return self._transition(state, post, step, step_index, plan, "chaos_like", "completed", f"remove:{removal.selected.key}|add:{add.selected.key}", (removal.record.decision_id, add.record.decision_id), (removal.selected.key, add.selected.key), removal.record.candidate_count + add.record.candidate_count, digest, None, Fraction(1, 1), False)

    def _catalog_sample(self, state, step, step_index, plan, source, sample_index, run_id):
        operation = _expect_operation(plan, CatalogSingleAddOperation)
        reason = self.catalog_add._precondition_failure(state, operation)
        if reason is not None:
            return self._no_transition(state, step, step_index, plan, "catalog_single_add", reason, None)
        pool = self.catalog_add.build_pool(state, operation)
        if not pool.candidates:
            return self._no_transition(state, step, step_index, plan, "catalog_single_add", pool.empty_reason or "ordinary_add_pool_exhausted", pool.result_fingerprint)
        decision_id = self._sample_decision_id(
            run_id, sample_index, step_index, step, operation.operation_id
        )
        decision = source.choose_one(decision_id, pool.candidates)
        post = _append_ordinary_modifier(self.catalog_add._working_state(state, operation), decision.selected.key)
        self.catalog_add._assert_applied_transition(state, post, operation)
        return self._transition(state, post, step, step_index, plan, "catalog_single_add", "applied", f"add:{decision.selected.key}", (decision.record.decision_id,), (decision.selected.key,), decision.record.candidate_count, decision.record.candidate_digest, None, Fraction(1, 1), False)

    def _greater_sample(self, state, step, step_index, plan):
        operation = _expect_operation(plan, GreaterEssenceOperation)
        terminal, reason = self.greater_essence._transition(state, operation)
        if terminal is None:
            return self._no_transition(state, step, step_index, plan, "greater_essence", reason or "greater_essence_precondition_failed", None)
        return self._transition(state, terminal, step, step_index, plan, "greater_essence", "applied", f"guaranteed:{operation.guaranteed_mod_id}", (), (operation.guaranteed_mod_id,), 0, None, None, Fraction(1, 1), False)

    def _perfect_sample(self, state, step, step_index, plan, source, sample_index, run_id):
        operation = _expect_operation(plan, PerfectEssenceOperation)
        pool = self.perfect_essence.build_feasible_pool(state, operation)
        if not pool.candidates:
            return self._no_transition(state, step, step_index, plan, "perfect_essence", pool.empty_reason or "feasible_removal_pool_exhausted", pool.result_fingerprint)
        decision_id = self._sample_decision_id(
            run_id,
            sample_index,
            step_index,
            step,
            operation.operation_id,
            suffix=".remove",
        )
        decision = source.choose_one(decision_id, pool.candidates)
        metadata = {row.candidate_key: row for row in pool.removal_metadata}
        selected = metadata[decision.selected.key]
        post = self.perfect_essence._terminal_for_candidate(state, operation, selected)
        if post is None:
            raise M43ASequenceInvariantViolation("perfect Essence feasible candidate became invalid")
        self.perfect_essence._assert_terminal_invariants(state, post, operation, selected)
        return self._transition(state, post, step, step_index, plan, "perfect_essence", "completed", f"remove:{decision.selected.key}|guaranteed:{operation.guaranteed_mod_id}", (decision.record.decision_id,), (decision.selected.key, operation.guaranteed_mod_id), decision.record.candidate_count, pool.result_fingerprint, None, Fraction(1, 1), False)

    def _alchemy_sample(self, state, step, step_index, plan, source, sample_index, run_id):
        operation = _expect_operation(plan, AlchemyOperation)
        prefix = self._sample_decision_id(
            run_id, sample_index, step_index, step, operation.operation_id
        )
        trajectory = self.alchemy.sample_once(
            initial_state=state,
            operation=operation,
            decision_source=source,
            sample_index=sample_index,
            run_id=run_id,
            decision_id_prefix=prefix,
        )
        decision_ids = tuple(
            trace.decision_id
            for trace in trajectory.traces
            if trace.decision_id is not None
        )
        key = (
            "alchemy:" + "|".join(trajectory.selected_mod_ids)
            if trajectory.outcome == "completed"
            else f"alchemy:NO_TRANSITION:{trajectory.no_transition_reason}"
        )
        terminal_state = state
        if trajectory.outcome == "completed":
            terminal_state = self.alchemy._working_state(state, operation)
            for selected_mod_id in trajectory.selected_mod_ids:
                terminal_state = _append_ordinary_modifier(
                    terminal_state, selected_mod_id
                )
            self.alchemy._assert_terminal(state, terminal_state, operation)
        return self._transition(
            state,
            terminal_state,
            step,
            step_index,
            plan,
            "alchemy",
            trajectory.outcome,
            key,
            decision_ids,
            trajectory.selected_mod_ids,
            trajectory.candidate_count_total,
            trajectory.pool_digest,
            trajectory.no_transition_reason,
            Fraction(1, 1),
            trajectory.outcome != "completed",
        )

    def _greater_exaltation_sample(
        self,
        state,
        step,
        step_index,
        plan,
        source,
        sample_index,
        run_id,
        executor_id,
    ):
        operation = plan.operation
        if not isinstance(operation, (OrdinaryAddOperation, CatalogSingleAddOperation)):
            raise M43ASequenceAdmissionError(
                "Greater Exaltation plan must wrap an accepted Exalted add executor"
            )
        prefix = self._sample_decision_id(
            run_id, sample_index, step_index, step, plan.operation_id
        )
        trajectory = self.greater_exaltation.sample_once(
            initial_state=state,
            operation=operation,
            decision_source=source,
            sample_index=sample_index,
            run_id=run_id,
            decision_id_prefix=prefix,
        )
        terminal = state
        if trajectory.outcome == "completed":
            for selected_mod_id in trajectory.selected_mod_ids:
                terminal = _append_ordinary_modifier(terminal, selected_mod_id)
            self.greater_exaltation._assert_terminal(state, terminal)
        decision_ids = tuple(
            trace.decision_id for trace in trajectory.traces if trace.decision_id is not None
        )
        pool_digest = _combined_digest(
            *(trace.pool_fingerprint for trace in trajectory.traces)
        )
        key = (
            "greater_exaltation:" + "|".join(trajectory.selected_mod_ids)
            if trajectory.outcome == "completed"
            else f"greater_exaltation:NO_TRANSITION:{trajectory.no_transition_reason}"
        )
        return self._transition(
            state,
            terminal,
            step,
            step_index,
            plan,
            executor_id,
            trajectory.outcome,
            key,
            decision_ids,
            trajectory.selected_mod_ids,
            sum(trace.candidate_count for trace in trajectory.traces),
            pool_digest,
            trajectory.no_transition_reason,
            Fraction(1, 1),
            trajectory.outcome != "completed",
        )

    def _sample_decision_id(
        self, run_id, sample_index, step_index, step, operation_id, suffix=""
    ):
        return (
            f"{run_id}.sample_{sample_index}.step_{step_index}."
            f"{operation_id}.{step.mode_id}{suffix}"
        )

    def _resolver_no_transition(self, *, state, step, step_index, executor_id):
        digest = sha256_canonical({"state_hash": state.state_hash(), "currency_id": step.currency_id, "mode_id": step.mode_id, "outcome": "resolver_rejected_current_state"}, schema_version=1)
        trace = SequenceStepTrace(step_index=step_index, step_id=step.step_id, currency_id=step.currency_id, operation_id=step.currency_id, mode_id=step.mode_id, executor_id=executor_id, outcome="no_transition_no_consumption", pre_state_hash=state.state_hash(), post_state_hash=state.state_hash(), resolver_plan_digest=digest, transition_key=f"{step.currency_id}:NO_TRANSITION:rarity", decision_ids=(), selected_keys=(), candidate_count=0, pool_digest=None, no_transition_reason="resolver_rejected_current_state", probability_numerator=1, probability_denominator=1)
        return _StepTransition(state=state, trace=trace, path_component=trace.transition_key, probability=Fraction(1, 1), terminal=True)

    def _no_transition(self, state, step, step_index, plan, executor_id, reason, pool_digest):
        return self._transition(state, state, step, step_index, plan, executor_id, "no_transition_no_consumption", f"{step.currency_id}:NO_TRANSITION:{reason}", (), (), 0, pool_digest, reason, Fraction(1, 1), True)

    def _transition(self, pre, post, step, step_index, plan, executor_id, outcome, key, decision_ids, selected_keys, candidate_count, pool_digest, reason, probability, terminal):
        trace = SequenceStepTrace(step_index=step_index, step_id=step.step_id, currency_id=step.currency_id, operation_id=plan.operation_id, mode_id=step.mode_id, executor_id=executor_id, outcome=outcome, pre_state_hash=pre.state_hash(), post_state_hash=post.state_hash(), resolver_plan_digest=_plan_digest(plan, pre), transition_key=key, decision_ids=tuple(decision_ids), selected_keys=tuple(selected_keys), candidate_count=candidate_count, pool_digest=pool_digest, no_transition_reason=reason, probability_numerator=probability.numerator, probability_denominator=probability.denominator)
        return _StepTransition(state=post, trace=trace, path_component=key, probability=probability, terminal=terminal)

    def _candidate_ceiling(self, candidates, ceiling, step_index, step):
        if len(candidates) > ceiling:
            raise _ExactCeilingExceeded(self._ceiling_stop("candidate_branch_ceiling_exceeded", "max_candidates_per_pool", ceiling, len(candidates), step_index, step))

    def _ceiling_stop(self, code, name, limit, observed, step_index, step):
        return ExactCeilingStop(stop_code=code, ceiling_name=name, ceiling_limit=limit, observed_count=observed, step_index=step_index, step_id=step.step_id, currency_id=step.currency_id, message=f"M43-A exact ceiling exceeded: {name} limit={limit} observed={observed} step={step.step_id}")

    def _exact_path(self, *, state, path_key, traces, outcome, completed_step_count, terminal_step_index, probability):
        key = _execution_terminal_key(state_hash=state.state_hash(), outcome=outcome, completed_step_count=completed_step_count, terminal_step_index=terminal_step_index)
        return ExactSequencePath(path_key=path_key, terminal_state=state, terminal_state_hash=state.state_hash(), execution_terminal_key=key, outcome=outcome, completed_step_count=completed_step_count, terminal_step_index=terminal_step_index, steps=traces, probability_numerator=probability.numerator, probability_denominator=probability.denominator)

    def _aggregate_execution_terminals(self, paths):
        masses = defaultdict(Fraction)
        grouped_paths = defaultdict(list)
        representative = {}
        for path in paths:
            masses[path.execution_terminal_key] += Fraction(path.probability_numerator, path.probability_denominator)
            grouped_paths[path.execution_terminal_key].append(path.path_key)
            representative[path.execution_terminal_key] = path
        return tuple(ExactExecutionTerminal(execution_terminal_key=key, terminal_state=representative[key].terminal_state, terminal_state_hash=representative[key].terminal_state_hash, outcome=representative[key].outcome, completed_step_count=representative[key].completed_step_count, terminal_step_index=representative[key].terminal_step_index, path_count=len(grouped_paths[key]), path_keys=tuple(sorted(grouped_paths[key])), probability_numerator=masses[key].numerator, probability_denominator=masses[key].denominator) for key in sorted(masses))

    def _assert_plan_executor(self, plan, executor_id):
        expected = {"ordinary_add": OrdinaryAddOperation, "annulment": AnnulmentOperation, "chaos_like": ChaosLikeOperation, "catalog_single_add": CatalogSingleAddOperation, "greater_essence": GreaterEssenceOperation, "perfect_essence": PerfectEssenceOperation, "alchemy": AlchemyOperation, "fracture": FractureOperation}[executor_id]
        if not isinstance(plan.operation, expected):
            raise M43ASequenceAdmissionError(f"executor registry/plan mismatch for {plan.currency_id}: expected {executor_id}, got {type(plan.operation).__name__}")


def _default_executor_mapping() -> dict[str, ExecutorId]:
    mapping: dict[str, ExecutorId] = {
        MC_OPERATION_ID: "ordinary_add",
        ANNULMENT_OPERATION_ID: "annulment",
    }
    mapping.update({operation_id: "chaos_like" for operation_id in M39B_CHAOS_OPERATION_IDS})
    mapping.update({operation_id: "catalog_single_add" for operation_id in M40A_OPERATION_IDS})
    mapping.update({"greater_exalted": "ordinary_add", "perfect_exalted": "ordinary_add"})
    mapping.update({operation_id: "greater_essence" for operation_id in M41A_OPERATION_IDS})
    mapping.update({operation_id: "perfect_essence" for operation_id in M42A_OPERATION_IDS})
    mapping[M44A_ALCHEMY_OPERATION_ID] = "alchemy"
    mapping[FRACTURING_ORB_OPERATION_ID] = "fracture"
    return mapping


def _operation_row(static: StaticGameData, operation_id: str):
    for row in static.operations.get("operations") or ():
        if row.get("operation_id") == operation_id:
            return row
    return None


def _expect_operation(plan: ResolvedOperationPlan, expected_type):
    if not isinstance(plan.operation, expected_type):
        raise M43ASequenceAdmissionError(
            f"resolved operation type mismatch: {plan.currency_id} -> {type(plan.operation).__name__}"
        )
    return plan.operation


def _plan_digest(plan: ResolvedOperationPlan, state: ItemState) -> str:
    return sha256_canonical(
        {"state_hash": state.state_hash(), "plan": plan.public_summary()},
        schema_version=1,
    )


def _combined_digest(*values: str | None) -> str:
    return sha256_canonical({"component_digests": values}, schema_version=1)


def _execution_terminal_key(*, state_hash, outcome, completed_step_count, terminal_step_index):
    return sha256_canonical(
        {
            "state_hash": state_hash,
            "outcome": outcome,
            "completed_step_count": completed_step_count,
            "terminal_step_index": terminal_step_index,
        },
        schema_version=1,
    )


__all__ = [
    "AcceptedOperationExecutorRegistry",
    "BoundedAcceptedOperationSequenceHarness",
    "BoundedSequenceRequest",
    "BoundedSequenceStep",
    "ExactCeilingStop",
    "ExactExecutionTerminal",
    "ExactSequenceEvaluation",
    "ExactSequencePath",
    "ExactStateProjection",
    "ExactStepMarginal",
    "M43A_FIXED_SEEDS",
    "M43A_MAX_CANDIDATES_PER_POOL",
    "M43A_MAX_EXACT_PATHS",
    "M43A_MAX_EXACT_TERMINALS",
    "M43A_MAX_STEPS",
    "M43A_MIN_STEPS",
    "M43A_SAMPLE_TIERS",
    "M43A_SCHEMA_VERSION",
    "M43A_SEMANTICS_VERSION",
    "M43ASequenceAdmissionError",
    "M43ASequenceError",
    "M43ASequenceInvariantViolation",
    "SequenceRunResult",
    "SequenceStepTrace",
    "SequenceTrajectory",
]
