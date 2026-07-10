from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, replace
from typing import Any

from p2c_engine.canonical.hashes import sha256_canonical
from p2c_engine.domain.decision import DecisionRecord
from p2c_engine.domain.defects import SamplingContractDefect
from p2c_engine.domain.enums import Rarity, Side
from p2c_engine.domain.item_state import ItemState, ModifierInstance
from p2c_engine.legality.state_validation import validate_item_state
from p2c_engine.monte_carlo.ordinary_add import (
    M32InvariantViolation,
    M32MonteCarloError,
    _assert_fractured_modifiers_unchanged,
)
from p2c_engine.static_data.game_data import StaticGameData


M41A_SCHEMA_VERSION = "p2c.m41a.greater_essence_quarterstaff.v1"
M41A_SEMANTICS_VERSION = "p2c.m41a.greater_essence.project_model.v1"
M41A_CRAFTED_CAPACITY_STATUS = "source_open_unverified_greater_only"
M41A_OPERATION_IDS = frozenset(
    {
        "greater_essence_abrasion",
        "greater_essence_flames",
        "greater_essence_ice",
        "greater_essence_electricity",
        "greater_essence_battle",
        "greater_essence_haste",
        "greater_essence_seeking",
        "greater_essence_infinite",
    }
)
ACCEPTED_RUNTIME_STATUS = "accepted_executable_runtime"


class M41AGreaterEssenceError(M32MonteCarloError):
    """Base error for the M41-A Greater Essence runtime."""


class M41AGreaterEssenceInvariantViolation(
    M41AGreaterEssenceError, M32InvariantViolation
):
    """Raised when admitted Greater Essence data or execution is inconsistent."""


@dataclass(frozen=True, slots=True)
class GreaterEssenceOperation:
    mode_id: str
    operation_id: str
    item_class: str
    guaranteed_mod_id: str
    guaranteed_family_id: str
    guaranteed_side: Side
    input_rarities: tuple[Rarity, ...] = (Rarity.MAGIC,)
    output_rarity: Rarity = Rarity.RARE
    crafted: bool = True
    semantics_version: str = M41A_SEMANTICS_VERSION


@dataclass(frozen=True, slots=True)
class GreaterEssenceExactPath:
    outcome: str
    terminal_state_hash: str
    guaranteed_mod_id: str | None
    no_transition_reason: str | None
    probability_numerator: int = 1
    probability_denominator: int = 1


@dataclass(frozen=True, slots=True)
class GreaterEssenceExactTerminal:
    outcome: str
    terminal_state_hash: str
    guaranteed_mod_id: str | None
    no_transition_reason: str | None
    path_count: int = 1
    probability_numerator: int = 1
    probability_denominator: int = 1


@dataclass(frozen=True, slots=True)
class GreaterEssenceTrajectory:
    sample_index: int
    outcome: str
    operation_id: str
    pre_state_hash: str
    post_state_hash: str
    guaranteed_mod_id: str | None
    decision_id: None
    candidate_count: int
    no_transition_reason: str | None

    def public_payload(self) -> dict[str, object]:
        return {
            "sample_index": self.sample_index,
            "outcome": self.outcome,
            "operation_id": self.operation_id,
            "pre_state_hash": self.pre_state_hash,
            "post_state_hash": self.post_state_hash,
            "guaranteed_mod_id": self.guaranteed_mod_id,
            "decision_id": self.decision_id,
            "candidate_count": self.candidate_count,
            "no_transition_reason": self.no_transition_reason,
        }


@dataclass(frozen=True, slots=True)
class GreaterEssenceRunResult:
    schema_version: str
    run_id: str
    seed: int
    sample_count: int
    mode_id: str
    operation_id: str
    source_fingerprint: str
    semantic_fingerprint: str
    code_version: str
    crafted_capacity_status: str
    trajectories: tuple[GreaterEssenceTrajectory, ...]
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
            "source_fingerprint": self.source_fingerprint,
            "semantic_fingerprint": self.semantic_fingerprint,
            "code_version": self.code_version,
            "crafted_capacity_status": self.crafted_capacity_status,
            "trajectory_count": len(self.trajectories),
            "decision_count": len(self.decisions),
            "terminal_state_hash_count": len(
                {row.post_state_hash for row in self.trajectories}
            ),
            "result_hash": self.result_hash,
        }


class GreaterEssenceHarness:
    """Deterministic exact/seeded harness for the eight admitted Greater Essences.

    The guaranteed modifier resolves through StaticGameData.modifier_index. There
    is no weighted candidate pool and no random decision. General crafted-capacity
    semantics remain source-open; this Greater-only lane simply applies the
    existing shared state validator to one atomic Magic-to-Rare transition.
    """

    def __init__(
        self,
        *,
        static: StaticGameData,
        code_version: str = "p2c.m41a.dev",
    ) -> None:
        self.static = static
        self.code_version = code_version

    def validate_operation_contract(self, operation: GreaterEssenceOperation) -> None:
        if operation.semantics_version != M41A_SEMANTICS_VERSION:
            raise M41AGreaterEssenceInvariantViolation(
                "M41-A Greater Essence semantics version mismatch"
            )
        if operation.operation_id not in M41A_OPERATION_IDS:
            raise M41AGreaterEssenceInvariantViolation(
                f"unsupported M41-A operation_id: {operation.operation_id}"
            )
        if (
            operation.input_rarities != (Rarity.MAGIC,)
            or operation.output_rarity != Rarity.RARE
            or operation.crafted is not True
        ):
            raise M41AGreaterEssenceInvariantViolation(
                f"invalid Greater Essence operation shape: {operation.operation_id}"
            )

        row = _operation_row(self.static.operations, operation.operation_id)
        if row is None:
            raise M41AGreaterEssenceInvariantViolation(
                f"missing Greater Essence operation row: {operation.operation_id}"
            )
        if row.get("runtime_admission_status") != ACCEPTED_RUNTIME_STATUS:
            raise M41AGreaterEssenceInvariantViolation(
                f"operation is not executable-admitted: {operation.operation_id}"
            )
        if row.get("group") != "greater_essence" or row.get(
            "active_in_current_simulation"
        ) is not True:
            raise M41AGreaterEssenceInvariantViolation(
                f"Greater Essence activation mismatch: {operation.operation_id}"
            )

        transition = row.get("transition")
        remove = transition.get("remove") if isinstance(transition, Mapping) else None
        prevalidate = transition.get("prevalidate") if isinstance(transition, Mapping) else None
        required_prevalidate = {
            "family_absent",
            "crafted_capacity_free",
            "result_side_capacity_free",
        }
        if (
            not isinstance(transition, Mapping)
            or transition.get("atomic") is not True
            or transition.get("output_rarity") != "rare"
            or not isinstance(remove, Mapping)
            or remove.get("kind") != "none"
            or set(prevalidate or ()) != required_prevalidate
            or transition.get("crafted") is not True
        ):
            raise M41AGreaterEssenceInvariantViolation(
                f"unsupported Greater Essence transition shape: {operation.operation_id}"
            )

        output = _essence_output_row(
            self.static.essence_outputs, operation.operation_id
        )
        if output is None:
            raise M41AGreaterEssenceInvariantViolation(
                f"missing Greater Essence output row: {operation.operation_id}"
            )
        canonical = self.static.modifier_index.get(operation.guaranteed_mod_id)
        if canonical is None:
            raise M41AGreaterEssenceInvariantViolation(
                f"guaranteed modifier missing from canonical index: {operation.guaranteed_mod_id}"
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
            row_contract
            == output_contract
            == operation_contract
            == canonical_contract
        ):
            raise M41AGreaterEssenceInvariantViolation(
                f"Greater Essence canonical contract mismatch: {operation.operation_id}"
            )
        if canonical.static_category != "greater_essence" or canonical.tier != 1:
            raise M41AGreaterEssenceInvariantViolation(
                f"invalid canonical Greater Essence modifier: {canonical.mod_id}"
            )
        if tuple(canonical.group_ids) != tuple(
            sorted(str(value) for value in (output.get("group_ids") or ()))
        ):
            raise M41AGreaterEssenceInvariantViolation(
                f"Greater Essence group contract mismatch: {operation.operation_id}"
            )
        if operation.item_class not in (output.get("item_classes") or ()):
            raise M41AGreaterEssenceInvariantViolation(
                f"Greater Essence output does not apply to item class: {operation.item_class}"
            )

    def enumerate_paths(
        self,
        *,
        initial_state: ItemState,
        operation: GreaterEssenceOperation,
    ) -> tuple[GreaterEssenceExactPath, ...]:
        self.validate_operation_contract(operation)
        terminal, reason = self._transition(initial_state, operation)
        if terminal is None:
            return (
                GreaterEssenceExactPath(
                    outcome="no_transition_no_consumption",
                    terminal_state_hash=initial_state.state_hash(),
                    guaranteed_mod_id=None,
                    no_transition_reason=reason,
                ),
            )
        return (
            GreaterEssenceExactPath(
                outcome="applied",
                terminal_state_hash=terminal.state_hash(),
                guaranteed_mod_id=operation.guaranteed_mod_id,
                no_transition_reason=None,
            ),
        )

    def enumerate_terminal_distribution(
        self,
        *,
        initial_state: ItemState,
        operation: GreaterEssenceOperation,
    ) -> tuple[GreaterEssenceExactTerminal, ...]:
        path = self.enumerate_paths(
            initial_state=initial_state,
            operation=operation,
        )[0]
        return (
            GreaterEssenceExactTerminal(
                outcome=path.outcome,
                terminal_state_hash=path.terminal_state_hash,
                guaranteed_mod_id=path.guaranteed_mod_id,
                no_transition_reason=path.no_transition_reason,
            ),
        )

    def sample_once(
        self,
        *,
        state: ItemState,
        operation: GreaterEssenceOperation,
        sample_index: int,
    ) -> GreaterEssenceTrajectory:
        self.validate_operation_contract(operation)
        terminal, reason = self._transition(state, operation)
        pre_hash = state.state_hash()
        if terminal is None:
            return GreaterEssenceTrajectory(
                sample_index=sample_index,
                outcome="no_transition_no_consumption",
                operation_id=operation.operation_id,
                pre_state_hash=pre_hash,
                post_state_hash=pre_hash,
                guaranteed_mod_id=None,
                decision_id=None,
                candidate_count=0,
                no_transition_reason=reason,
            )
        return GreaterEssenceTrajectory(
            sample_index=sample_index,
            outcome="applied",
            operation_id=operation.operation_id,
            pre_state_hash=pre_hash,
            post_state_hash=terminal.state_hash(),
            guaranteed_mod_id=operation.guaranteed_mod_id,
            decision_id=None,
            candidate_count=0,
            no_transition_reason=None,
        )

    def run(
        self,
        *,
        initial_state: ItemState,
        operation: GreaterEssenceOperation,
        seed: int,
        sample_count: int,
        run_id: str,
    ) -> GreaterEssenceRunResult:
        if (
            isinstance(sample_count, bool)
            or not isinstance(sample_count, int)
            or sample_count < 0
        ):
            raise SamplingContractDefect(
                "sample_count must be a non-negative non-bool integer"
            )
        trajectories = tuple(
            self.sample_once(
                state=initial_state,
                operation=operation,
                sample_index=index,
            )
            for index in range(sample_count)
        )
        payload = {
            "schema_version": M41A_SCHEMA_VERSION,
            "run_id": run_id,
            "seed": seed,
            "sample_count": sample_count,
            "mode_id": operation.mode_id,
            "operation_id": operation.operation_id,
            "source_fingerprint": self.static.source_fingerprint,
            "semantic_fingerprint": self.static.semantic_fingerprint,
            "code_version": self.code_version,
            "crafted_capacity_status": M41A_CRAFTED_CAPACITY_STATUS,
            "trajectories": [row.public_payload() for row in trajectories],
            "decisions": [],
        }
        return GreaterEssenceRunResult(
            schema_version=M41A_SCHEMA_VERSION,
            run_id=run_id,
            seed=seed,
            sample_count=sample_count,
            mode_id=operation.mode_id,
            operation_id=operation.operation_id,
            source_fingerprint=self.static.source_fingerprint,
            semantic_fingerprint=self.static.semantic_fingerprint,
            code_version=self.code_version,
            crafted_capacity_status=M41A_CRAFTED_CAPACITY_STATUS,
            trajectories=trajectories,
            decisions=(),
            result_hash=sha256_canonical(payload, schema_version=1),
        )

    def _transition(
        self,
        state: ItemState,
        operation: GreaterEssenceOperation,
    ) -> tuple[ItemState | None, str | None]:
        if state.item_class != operation.item_class:
            return None, "item_class_mismatch"
        if state.rarity not in operation.input_rarities:
            return None, "invalid_source_rarity"
        source_validation = validate_item_state(state, self.static)
        if not source_validation.ok:
            return None, "invalid_source_state"

        terminal = replace(
            state,
            rarity=operation.output_rarity,
            modifiers=state.modifiers
            + (
                ModifierInstance(
                    mod_id=operation.guaranteed_mod_id,
                    crafted=True,
                    desecrated=False,
                    fractured=False,
                ),
            ),
        )
        terminal_validation = validate_item_state(terminal, self.static)
        if not terminal_validation.ok:
            code = terminal_validation.errors[0].code.value
            return None, f"post_state_{code}"
        _assert_fractured_modifiers_unchanged(
            state, terminal, self.static.modifier_index
        )
        if terminal.modifiers[:-1] != state.modifiers:
            raise M41AGreaterEssenceInvariantViolation(
                "Greater Essence changed existing modifier instances"
            )
        if terminal.modifiers[-1] != ModifierInstance(
            mod_id=operation.guaranteed_mod_id,
            crafted=True,
            desecrated=False,
            fractured=False,
        ):
            raise M41AGreaterEssenceInvariantViolation(
                "Greater Essence did not install the exact guaranteed modifier"
            )
        return terminal, None


def _operation_row(operations: Any, operation_id: str) -> dict[str, Any] | None:
    if not isinstance(operations, Mapping):
        return None
    for row in operations.get("operations") or ():
        if isinstance(row, Mapping) and row.get("operation_id") == operation_id:
            return row
    return None


def _essence_output_row(
    essence_outputs: Any, operation_id: str
) -> dict[str, Any] | None:
    if not isinstance(essence_outputs, Mapping):
        return None
    for row in essence_outputs.get("greater") or ():
        if isinstance(row, Mapping) and row.get("operation_id") == operation_id:
            return row
    return None


__all__ = [
    "M41A_CRAFTED_CAPACITY_STATUS",
    "M41A_OPERATION_IDS",
    "M41A_SCHEMA_VERSION",
    "M41A_SEMANTICS_VERSION",
    "GreaterEssenceExactPath",
    "GreaterEssenceExactTerminal",
    "GreaterEssenceHarness",
    "GreaterEssenceOperation",
    "GreaterEssenceRunResult",
    "GreaterEssenceTrajectory",
    "M41AGreaterEssenceError",
    "M41AGreaterEssenceInvariantViolation",
]
