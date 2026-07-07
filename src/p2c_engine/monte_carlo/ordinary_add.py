from __future__ import annotations

from collections import Counter
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any

from p2c_engine.canonical.hashes import sha256_canonical
from p2c_engine.decisions import RecordingDecisionSource, SeededDecisionSource
from p2c_engine.domain.candidate import BranchOption
from p2c_engine.domain.decision import DecisionRecord
from p2c_engine.domain.defects import SamplingContractDefect, StaticDataDefect
from p2c_engine.domain.enums import Rarity, Side
from p2c_engine.domain.item_state import ItemState, ModifierInstance
from p2c_engine.domain.versions import RNG_STREAM_VERSION, SAMPLING_ALGORITHM_ID
from p2c_engine.legality.pool_builders import (
    OrdinaryAddPoolRequest,
    build_ordinary_add_pool,
)
from p2c_engine.sampling.exact import branch_options
from p2c_engine.static_data.game_data import StaticGameData


MC_HARNESS_SCHEMA_VERSION = "p2c.m32.seeded_mc_harness.v1"
MC_OPERATION_ID = "ordinary_add"
ORDINARY_ADD_SEMANTICS_VERSION = "p2c.m16.ordinary_add.v1"
M32_VALUE_POLICY = "public_reports_are_numeric_probability_free_counts_hashes_statuses_only"


class M32MonteCarloError(RuntimeError):
    """Base class for M32 Monte Carlo harness failures."""


class M32InvariantViolation(M32MonteCarloError):
    """Raised when a simulated transition violates accepted runtime invariants."""


@dataclass(frozen=True, slots=True)
class OrdinaryAddOperation:
    """One accepted ordinary_add operation invocation.

    The operation_id is fail-closed through the accepted operation semantics
    registry. The side and MML fields are explicit mode parameters passed into
    the shared ordinary-add pool builder; they are not new mechanics.
    """

    mode_id: str
    operation_id: str = MC_OPERATION_ID
    item_class: str = "quarterstaff"
    side_filter: Side | None = None
    mml: int | None = None
    semantics_version: str = ORDINARY_ADD_SEMANTICS_VERSION


@dataclass(frozen=True, slots=True)
class MonteCarloTrajectory:
    sample_index: int
    outcome: str
    pre_state_hash: str
    post_state_hash: str
    decision_id: str | None
    selected_mod_id: str | None
    candidate_count: int
    candidate_digest: str | None

    def public_payload(self) -> dict[str, object]:
        return {
            "sample_index": self.sample_index,
            "outcome": self.outcome,
            "pre_state_hash": self.pre_state_hash,
            "post_state_hash": self.post_state_hash,
            "decision_id": self.decision_id,
            "selected_mod_id": self.selected_mod_id,
            "candidate_count": self.candidate_count,
            "candidate_digest": self.candidate_digest,
        }


@dataclass(frozen=True, slots=True)
class MonteCarloRunResult:
    schema_version: str
    run_id: str
    seed: int
    sample_count: int
    mode_id: str
    operation_sequence_id: str
    operation_id: str
    rng_stream_version: int
    sampling_algorithm_id: str
    source_fingerprint: str
    semantic_fingerprint: str
    code_version: str
    trajectories: tuple[MonteCarloTrajectory, ...]
    decisions: tuple[DecisionRecord, ...]
    result_hash: str

    def public_summary(self) -> dict[str, object]:
        terminal_state_hashes = {
            trajectory.post_state_hash for trajectory in self.trajectories
        }
        payload: dict[str, object] = {
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
            "operation_sequence_id": self.operation_sequence_id,
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
        return payload


PoolBuilder = Callable[[OrdinaryAddPoolRequest, StaticGameData], Any]


class OrdinaryAddMonteCarloHarness:
    """Seeded MC harness over accepted ordinary_add only.

    Exact enumeration and MC sampling both call build_pool(), which delegates to
    the injected ordinary-add pool builder. The default builder is the accepted
    p2c_engine.legality.pool_builders.build_ordinary_add_pool path.
    """

    def __init__(
        self,
        *,
        static: StaticGameData,
        pool_builder: PoolBuilder = build_ordinary_add_pool,
        code_version: str = "p2c.m32.dev",
    ) -> None:
        self.static = static
        self.pool_builder = pool_builder
        self.code_version = code_version

    def build_pool(self, state: ItemState, operation: OrdinaryAddOperation):
        self._validate_operation(operation)
        request = OrdinaryAddPoolRequest(
            item_class=operation.item_class,
            state=state,
            side_filter=operation.side_filter,
            mml=operation.mml,
        )
        return self.pool_builder(request, self.static)

    def enumerate_outcomes(
        self,
        *,
        state: ItemState,
        operation: OrdinaryAddOperation,
        decision_id: str,
    ) -> tuple[BranchOption, ...]:
        pool = self.build_pool(state, operation)
        if not pool.candidates:
            return ()
        return branch_options(decision_id, pool.candidates)

    def sample_once(
        self,
        *,
        state: ItemState,
        operation: OrdinaryAddOperation,
        decision_source: RecordingDecisionSource,
        sample_index: int,
        run_id: str,
    ) -> MonteCarloTrajectory:
        self._validate_operation(operation)
        pre_hash = state.state_hash()
        pool = self.build_pool(state, operation)
        if not pool.candidates:
            self._assert_runtime_invariants(
                pre_state=state,
                post_state=state,
                expected_mode_id=operation.mode_id,
                actual_mode_id=operation.mode_id,
                operation_id=operation.operation_id,
            )
            return MonteCarloTrajectory(
                sample_index=sample_index,
                outcome="no_transition",
                pre_state_hash=pre_hash,
                post_state_hash=pre_hash,
                decision_id=None,
                selected_mod_id=None,
                candidate_count=0,
                candidate_digest=None,
            )

        decision_id = (
            f"{run_id}.sample_{sample_index}.step_0.{operation.operation_id}.{operation.mode_id}"
        )
        decision = decision_source.choose_one(decision_id, pool.candidates)
        post_state = _append_ordinary_modifier(state, decision.selected.key)
        self._assert_runtime_invariants(
            pre_state=state,
            post_state=post_state,
            expected_mode_id=operation.mode_id,
            actual_mode_id=operation.mode_id,
            operation_id=operation.operation_id,
        )
        return MonteCarloTrajectory(
            sample_index=sample_index,
            outcome="applied",
            pre_state_hash=pre_hash,
            post_state_hash=post_state.state_hash(),
            decision_id=decision.record.decision_id,
            selected_mod_id=decision.selected.key,
            candidate_count=decision.record.candidate_count,
            candidate_digest=decision.record.candidate_digest,
        )

    def run(
        self,
        *,
        initial_state: ItemState,
        operation: OrdinaryAddOperation,
        seed: int,
        sample_count: int,
        run_id: str,
        operation_sequence_id: str = "m32_single_ordinary_add",
    ) -> MonteCarloRunResult:
        if not isinstance(sample_count, int) or isinstance(sample_count, bool) or sample_count < 0:
            raise SamplingContractDefect("sample_count must be a non-negative non-bool integer")
        decision_source = RecordingDecisionSource(SeededDecisionSource(seed))
        trajectories = tuple(
            self.sample_once(
                state=initial_state,
                operation=operation,
                decision_source=decision_source,
                sample_index=index,
                run_id=run_id,
            )
            for index in range(sample_count)
        )
        payload = {
            "schema_version": MC_HARNESS_SCHEMA_VERSION,
            "run_id": run_id,
            "seed": seed,
            "sample_count": sample_count,
            "mode_id": operation.mode_id,
            "operation_sequence_id": operation_sequence_id,
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
        return MonteCarloRunResult(
            schema_version=MC_HARNESS_SCHEMA_VERSION,
            run_id=run_id,
            seed=seed,
            sample_count=sample_count,
            mode_id=operation.mode_id,
            operation_sequence_id=operation_sequence_id,
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

    def _validate_operation(self, operation: OrdinaryAddOperation) -> None:
        if operation.operation_id != MC_OPERATION_ID:
            raise M32InvariantViolation(f"unsupported operation_id: {operation.operation_id}")
        if operation.semantics_version != ORDINARY_ADD_SEMANTICS_VERSION:
            raise M32InvariantViolation("ordinary_add semantics version mismatch")

    def _assert_runtime_invariants(
        self,
        *,
        pre_state: ItemState,
        post_state: ItemState,
        expected_mode_id: str,
        actual_mode_id: str,
        operation_id: str,
    ) -> None:
        if operation_id != MC_OPERATION_ID:
            raise M32InvariantViolation(f"unsupported operation_id: {operation_id}")
        if actual_mode_id != expected_mode_id:
            raise M32InvariantViolation("mode changed during MC trajectory")
        _assert_fractured_suffix_unchanged(pre_state, post_state, self.static.modifier_index)
        _assert_capacity(post_state, self.static.modifier_index)
        _assert_duplicate_family_and_groups(post_state, self.static.modifier_index)


def _append_ordinary_modifier(state: ItemState, mod_id: str) -> ItemState:
    return state.with_modifiers(
        state.modifiers
        + (
            ModifierInstance(
                mod_id=mod_id,
                crafted=False,
                desecrated=False,
                fractured=False,
            ),
        )
    )


def _assert_fractured_suffix_unchanged(
    pre_state: ItemState,
    post_state: ItemState,
    modifier_index: Mapping[str, Any],
) -> None:
    pre_fractured = tuple(m for m in pre_state.modifiers if m.fractured)
    post_fractured = tuple(m for m in post_state.modifiers if m.fractured)
    if pre_fractured != post_fractured:
        raise M32InvariantViolation("fractured modifier changed during trajectory")
    for instance in post_fractured:
        static = modifier_index.get(instance.mod_id)
        if static is None:
            raise M32InvariantViolation(f"unknown fractured mod_id: {instance.mod_id}")
        if static.side != Side.SUFFIX:
            raise M32InvariantViolation("fractured modifier is not a suffix")


def _assert_capacity(state: ItemState, modifier_index: Mapping[str, Any]) -> None:
    rarity_capacity = {
        Rarity.NORMAL.value: {Side.PREFIX.value: 0, Side.SUFFIX.value: 0},
        Rarity.MAGIC.value: {Side.PREFIX.value: 1, Side.SUFFIX.value: 1},
        Rarity.RARE.value: {Side.PREFIX.value: 3, Side.SUFFIX.value: 3},
    }
    capacity = rarity_capacity[state.rarity.value]
    used: Counter[str] = Counter()
    for instance in state.modifiers:
        static = modifier_index.get(instance.mod_id)
        if static is None:
            raise M32InvariantViolation(f"unknown installed mod_id: {instance.mod_id}")
        used[static.side.value] += 1
    if state.unrevealed_desecrated is not None:
        used[state.unrevealed_desecrated.side.value] += 1
    for side, count in used.items():
        if count > capacity[side]:
            raise M32InvariantViolation(f"{side} capacity exceeded")
    if sum(used.values()) > sum(capacity.values()):
        raise M32InvariantViolation("total affix capacity exceeded")


def _assert_duplicate_family_and_groups(
    state: ItemState,
    modifier_index: Mapping[str, Any],
) -> None:
    family_counts: Counter[str] = Counter()
    group_counts: Counter[str] = Counter()
    for instance in state.modifiers:
        static = modifier_index.get(instance.mod_id)
        if static is None:
            raise M32InvariantViolation(f"unknown installed mod_id: {instance.mod_id}")
        family_counts[static.family_id] += 1
        group_counts.update(static.group_ids)
    duplicate_families = [family for family, count in family_counts.items() if count > 1]
    if duplicate_families:
        raise M32InvariantViolation(f"duplicate family installed: {sorted(duplicate_families)}")
    duplicate_groups = [group for group, count in group_counts.items() if count > 1]
    if duplicate_groups:
        raise M32InvariantViolation(f"group conflict installed: {sorted(duplicate_groups)}")


def build_public_smoke_summary(
    *,
    static: StaticGameData,
    initial_state: ItemState,
    seed: int,
    sample_count: int,
    mode_id: str,
    run_id: str,
    mml: int | None = None,
) -> dict[str, object]:
    harness = OrdinaryAddMonteCarloHarness(static=static)
    result = harness.run(
        initial_state=initial_state,
        operation=OrdinaryAddOperation(mode_id=mode_id, mml=mml),
        seed=seed,
        sample_count=sample_count,
        run_id=run_id,
    )
    return result.public_summary()
