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
from p2c_engine.domain.item_state import ItemState, ModifierInstance
from p2c_engine.domain.pool_building import PoolBuildResult, RemovalInstanceMetadata
from p2c_engine.domain.versions import RNG_STREAM_VERSION, SAMPLING_ALGORITHM_ID
from p2c_engine.legality.pool_builders import RemovalPoolRequest, build_removal_pool
from p2c_engine.sampling.exact import branch_options
from p2c_engine.static_data.game_data import StaticGameData

from .ordinary_add import M32_VALUE_POLICY, M32InvariantViolation, M32MonteCarloError


M35A_ANNULMENT_SCHEMA_VERSION = "p2c.m35a.annulment_runtime.v1"
ANNULMENT_OPERATION_ID = "annulment"
ANNULMENT_SEMANTICS_VERSION = "p2c.m35.annulment.project_model.v1"


class M35AAnnulmentError(M32MonteCarloError):
    """Base class for M35-A Annulment runtime failures."""


class M35AAnnulmentInvariantViolation(M35AAnnulmentError, M32InvariantViolation):
    """Raised when Annulment violates its accepted project-model invariants."""


@dataclass(frozen=True, slots=True)
class AnnulmentOperation:
    """One M35-A base Annulment operation invocation.

    M35-A intentionally admits only base Annulment. Omen side filters,
    desecrated-only selectors, Chaos composition, and every other operation
    variant remain out of scope.
    """

    mode_id: str
    operation_id: str = ANNULMENT_OPERATION_ID
    item_class: str = "quarterstaff"
    semantics_version: str = ANNULMENT_SEMANTICS_VERSION


@dataclass(frozen=True, slots=True)
class AnnulmentTrajectory:
    sample_index: int
    outcome: str
    pre_state_hash: str
    post_state_hash: str
    decision_id: str | None
    selected_removal_candidate_key: str | None
    selected_mod_id: str | None
    selected_duplicate_ordinal: int | None
    candidate_count: int
    candidate_digest: str | None
    removal_pool_fingerprint: str
    no_transition_reason: str | None

    def public_payload(self) -> dict[str, object]:
        return {
            "sample_index": self.sample_index,
            "outcome": self.outcome,
            "pre_state_hash": self.pre_state_hash,
            "post_state_hash": self.post_state_hash,
            "decision_id": self.decision_id,
            "selected_removal_candidate_key": self.selected_removal_candidate_key,
            "selected_mod_id": self.selected_mod_id,
            "selected_duplicate_ordinal": self.selected_duplicate_ordinal,
            "candidate_count": self.candidate_count,
            "candidate_digest": self.candidate_digest,
            "removal_pool_fingerprint": self.removal_pool_fingerprint,
            "no_transition_reason": self.no_transition_reason,
        }


@dataclass(frozen=True, slots=True)
class AnnulmentRunResult:
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
    trajectories: tuple[AnnulmentTrajectory, ...]
    decisions: tuple[DecisionRecord, ...]
    result_hash: str

    def public_summary(self) -> dict[str, object]:
        terminal_state_hashes = {
            trajectory.post_state_hash for trajectory in self.trajectories
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


@dataclass(frozen=True, slots=True)
class ExactAnnulmentPath:
    path_key: str | None
    terminal_state_hash: str
    outcome: str
    pre_state_hash: str
    post_state_hash: str
    decision_id: str | None
    selected_removal_candidate_key: str | None
    selected_mod_id: str | None
    selected_duplicate_ordinal: int | None
    candidate_count: int
    candidate_digest: str | None
    removal_pool_fingerprint: str
    no_transition_reason: str | None
    probability_numerator: int
    probability_denominator: int


@dataclass(frozen=True, slots=True)
class ExactAnnulmentTerminalOption:
    terminal_state_hash: str
    probability_numerator: int
    probability_denominator: int
    path_count: int
    path_keys: tuple[str | None, ...]


RemovalPoolBuilder = Callable[[RemovalPoolRequest, StaticGameData], PoolBuildResult]


class AnnulmentMonteCarloHarness:
    """Seeded MC and exact/oracle harness for M35-A base Annulment only."""

    def __init__(
        self,
        *,
        static: StaticGameData,
        removal_pool_builder: RemovalPoolBuilder = build_removal_pool,
        code_version: str = "p2c.m35a.dev",
    ) -> None:
        self.static = static
        self.removal_pool_builder = removal_pool_builder
        self.code_version = code_version

    def build_pool(self, state: ItemState, operation: AnnulmentOperation) -> PoolBuildResult:
        self._validate_operation(operation, state)
        request = RemovalPoolRequest(
            item_class=operation.item_class,
            state=state,
        )
        pool = self.removal_pool_builder(request, self.static)
        _validate_annulment_pool(pool)
        return pool

    def enumerate_paths(
        self,
        *,
        state: ItemState,
        operation: AnnulmentOperation,
        decision_id: str,
    ) -> tuple[ExactAnnulmentPath, ...]:
        pool = self.build_pool(state, operation)
        pre_hash = state.state_hash()
        metadata_by_key = _metadata_by_candidate_key(pool)

        if not pool.candidates:
            return (
                ExactAnnulmentPath(
                    path_key=None,
                    terminal_state_hash=pre_hash,
                    outcome="no_transition_no_consumption",
                    pre_state_hash=pre_hash,
                    post_state_hash=pre_hash,
                    decision_id=None,
                    selected_removal_candidate_key=None,
                    selected_mod_id=None,
                    selected_duplicate_ordinal=None,
                    candidate_count=0,
                    candidate_digest=None,
                    removal_pool_fingerprint=pool.result_fingerprint,
                    no_transition_reason=pool.empty_reason or "removal_pool_exhausted",
                    probability_numerator=1,
                    probability_denominator=1,
                ),
            )

        paths: list[ExactAnnulmentPath] = []
        for option in branch_options(decision_id, pool.candidates):
            metadata = metadata_by_key[option.selected_key]
            post_state = _remove_modifier_instance(state, metadata)
            _assert_annulment_runtime_invariants(
                pre_state=state,
                post_state=post_state,
                selected_metadata=metadata,
                operation_id=operation.operation_id,
                modifier_index=self.static.modifier_index,
            )
            paths.append(
                ExactAnnulmentPath(
                    path_key=option.selected_key,
                    terminal_state_hash=post_state.state_hash(),
                    outcome="applied",
                    pre_state_hash=pre_hash,
                    post_state_hash=post_state.state_hash(),
                    decision_id=option.decision_id,
                    selected_removal_candidate_key=option.selected_key,
                    selected_mod_id=metadata.mod_id,
                    selected_duplicate_ordinal=metadata.duplicate_ordinal,
                    candidate_count=len(pool.candidates),
                    candidate_digest=option.candidate_digest,
                    removal_pool_fingerprint=pool.result_fingerprint,
                    no_transition_reason=None,
                    probability_numerator=option.probability_numerator,
                    probability_denominator=option.probability_denominator,
                )
            )
        return tuple(paths)

    def enumerate_terminal_distribution(
        self,
        *,
        state: ItemState,
        operation: AnnulmentOperation,
        decision_id: str,
    ) -> tuple[ExactAnnulmentTerminalOption, ...]:
        paths = self.enumerate_paths(
            state=state,
            operation=operation,
            decision_id=decision_id,
        )
        grouped: dict[str, Fraction] = {}
        path_keys: dict[str, list[str | None]] = {}
        for path in paths:
            grouped[path.terminal_state_hash] = grouped.get(
                path.terminal_state_hash, Fraction(0, 1)
            ) + Fraction(path.probability_numerator, path.probability_denominator)
            path_keys.setdefault(path.terminal_state_hash, []).append(path.path_key)
        return tuple(
            ExactAnnulmentTerminalOption(
                terminal_state_hash=terminal_hash,
                probability_numerator=probability.numerator,
                probability_denominator=probability.denominator,
                path_count=len(path_keys[terminal_hash]),
                path_keys=tuple(
                    sorted(
                        path_keys[terminal_hash],
                        key=lambda key: "" if key is None else key,
                    )
                ),
            )
            for terminal_hash, probability in sorted(grouped.items())
        )

    def sample_once(
        self,
        *,
        state: ItemState,
        operation: AnnulmentOperation,
        decision_source: RecordingDecisionSource,
        sample_index: int,
        run_id: str,
    ) -> AnnulmentTrajectory:
        pool = self.build_pool(state, operation)
        pre_hash = state.state_hash()
        metadata_by_key = _metadata_by_candidate_key(pool)

        if not pool.candidates:
            _assert_no_transition_unchanged(state, state)
            return AnnulmentTrajectory(
                sample_index=sample_index,
                outcome="no_transition_no_consumption",
                pre_state_hash=pre_hash,
                post_state_hash=pre_hash,
                decision_id=None,
                selected_removal_candidate_key=None,
                selected_mod_id=None,
                selected_duplicate_ordinal=None,
                candidate_count=0,
                candidate_digest=None,
                removal_pool_fingerprint=pool.result_fingerprint,
                no_transition_reason=pool.empty_reason or "removal_pool_exhausted",
            )

        decision_id = (
            f"{run_id}.sample_{sample_index}.step_0."
            f"{operation.operation_id}.{operation.mode_id}"
        )
        decision = decision_source.choose_one(decision_id, pool.candidates)
        metadata = metadata_by_key[decision.selected.key]
        post_state = _remove_modifier_instance(state, metadata)
        _assert_annulment_runtime_invariants(
            pre_state=state,
            post_state=post_state,
            selected_metadata=metadata,
            operation_id=operation.operation_id,
            modifier_index=self.static.modifier_index,
        )
        return AnnulmentTrajectory(
            sample_index=sample_index,
            outcome="applied",
            pre_state_hash=pre_hash,
            post_state_hash=post_state.state_hash(),
            decision_id=decision.record.decision_id,
            selected_removal_candidate_key=decision.selected.key,
            selected_mod_id=metadata.mod_id,
            selected_duplicate_ordinal=metadata.duplicate_ordinal,
            candidate_count=decision.record.candidate_count,
            candidate_digest=decision.record.candidate_digest,
            removal_pool_fingerprint=pool.result_fingerprint,
            no_transition_reason=None,
        )

    def run(
        self,
        *,
        initial_state: ItemState,
        operation: AnnulmentOperation,
        seed: int,
        sample_count: int,
        run_id: str,
    ) -> AnnulmentRunResult:
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
            "schema_version": M35A_ANNULMENT_SCHEMA_VERSION,
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
        return AnnulmentRunResult(
            schema_version=M35A_ANNULMENT_SCHEMA_VERSION,
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

    def _validate_operation(self, operation: AnnulmentOperation, state: ItemState) -> None:
        if operation.operation_id != ANNULMENT_OPERATION_ID:
            raise M35AAnnulmentInvariantViolation(
                f"unsupported operation_id: {operation.operation_id}"
            )
        if operation.semantics_version != ANNULMENT_SEMANTICS_VERSION:
            raise M35AAnnulmentInvariantViolation("annulment semantics version mismatch")
        if operation.item_class != state.item_class:
            raise M35AAnnulmentInvariantViolation("operation item_class does not match state")
        if state.rarity not in {Rarity.MAGIC, Rarity.RARE}:
            raise M35AAnnulmentInvariantViolation("annulment supports magic and rare states only")


def _metadata_by_candidate_key(pool: PoolBuildResult) -> dict[str, RemovalInstanceMetadata]:
    metadata = {row.candidate_key: row for row in pool.removal_metadata}
    candidate_keys = {candidate.key for candidate in pool.candidates}
    if candidate_keys != set(metadata):
        raise M35AAnnulmentInvariantViolation("removal candidate metadata mismatch")
    return metadata


def _validate_annulment_pool(pool: PoolBuildResult) -> None:
    metadata = _metadata_by_candidate_key(pool)
    for candidate in pool.candidates:
        if candidate.weight != 1:
            raise M35AAnnulmentInvariantViolation("annulment removal candidates must be uniform")
        row = metadata[candidate.key]
        if row.fractured:
            raise M35AAnnulmentInvariantViolation(
                f"fractured candidate leaked from removal pool: {candidate.key}"
            )
    if not pool.candidates and pool.empty_reason is None:
        raise M35AAnnulmentInvariantViolation("empty removal pool requires explicit reason")


def _remove_modifier_instance(
    state: ItemState,
    selected: RemovalInstanceMetadata,
) -> ItemState:
    seen = 0
    output: list[ModifierInstance] = []
    removed = False
    for instance in state.modifiers:
        identity_match = (
            instance.mod_id == selected.mod_id
            and instance.crafted == selected.crafted
            and instance.desecrated == selected.desecrated
            and instance.fractured == selected.fractured
        )
        if identity_match:
            if seen == selected.duplicate_ordinal:
                if instance.fractured:
                    raise M35AAnnulmentInvariantViolation("attempted to remove fractured modifier")
                removed = True
                seen += 1
                continue
            seen += 1
        output.append(instance)
    if not removed:
        raise M35AAnnulmentInvariantViolation(
            f"selected removal candidate not found in state: {selected.candidate_key}"
        )
    return state.with_modifiers(tuple(output))


def _assert_annulment_runtime_invariants(
    *,
    pre_state: ItemState,
    post_state: ItemState,
    selected_metadata: RemovalInstanceMetadata,
    operation_id: str,
    modifier_index: Mapping[str, Any],
) -> None:
    if operation_id != ANNULMENT_OPERATION_ID:
        raise M35AAnnulmentInvariantViolation(f"unsupported operation_id: {operation_id}")
    if selected_metadata.fractured:
        raise M35AAnnulmentInvariantViolation("fractured modifier selected for removal")
    _assert_fractured_modifiers_unchanged(pre_state, post_state, modifier_index)
    if len(post_state.modifiers) != len(pre_state.modifiers) - 1:
        raise M35AAnnulmentInvariantViolation("annulment must remove exactly one modifier")


def _assert_no_transition_unchanged(pre_state: ItemState, post_state: ItemState) -> None:
    if pre_state != post_state or pre_state.state_hash() != post_state.state_hash():
        raise M35AAnnulmentInvariantViolation("no-transition mutated item state")


def _assert_fractured_modifiers_unchanged(
    pre_state: ItemState,
    post_state: ItemState,
    modifier_index: Mapping[str, Any],
) -> None:
    pre_fractured = tuple(m for m in pre_state.modifiers if m.fractured)
    post_fractured = tuple(m for m in post_state.modifiers if m.fractured)
    if pre_fractured != post_fractured:
        raise M35AAnnulmentInvariantViolation("fractured modifier changed during annulment")
    for instance in post_fractured:
        static = modifier_index.get(instance.mod_id)
        if static is None:
            raise M35AAnnulmentInvariantViolation(f"unknown fractured mod_id: {instance.mod_id}")


__all__ = [
    "ANNULMENT_OPERATION_ID",
    "ANNULMENT_SEMANTICS_VERSION",
    "M35A_ANNULMENT_SCHEMA_VERSION",
    "AnnulmentMonteCarloHarness",
    "AnnulmentOperation",
    "AnnulmentRunResult",
    "AnnulmentTrajectory",
    "ExactAnnulmentPath",
    "ExactAnnulmentTerminalOption",
    "M35AAnnulmentError",
    "M35AAnnulmentInvariantViolation",
]
