from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

from p2c_engine.domain.enums import Side
from p2c_engine.domain.item_state import ItemState
from p2c_engine.monte_carlo.annulment import (
    ANNULMENT_OPERATION_ID,
    AnnulmentOperation,
)
from p2c_engine.monte_carlo.chaos_like import CHAOS_OPERATION_ID, ChaosLikeOperation
from p2c_engine.monte_carlo.ordinary_add import (
    MC_OPERATION_ID,
    M32InvariantViolation,
    M32MonteCarloError,
    OrdinaryAddOperation,
)
from p2c_engine.static_data.game_data import StaticGameData


M38A_RESOLVER_SCHEMA_VERSION = "p2c.m38a.operation_resolver_skeleton.v1"
ACCEPTED_RUNTIME_STATUS = "accepted_executable_runtime"
BASE_VARIANT_IDS = frozenset({None, "", "base"})


AcceptedResolvedOperation = OrdinaryAddOperation | AnnulmentOperation | ChaosLikeOperation
OperationKind = Literal["engine_primitive", "catalog_operation"]


class M38AResolverError(M32MonteCarloError):
    """Base class for M38-A operation resolver failures."""


class M38AResolverAdmissionError(M38AResolverError, M32InvariantViolation):
    """Raised when a requested operation is not admitted for runtime execution."""


@dataclass(frozen=True, slots=True)
class OperationResolverRequest:
    """Single-operation resolver request.

    M38-A is intentionally not a route planner. It compiles one currency or
    engine-primitive invocation into one already accepted runtime operation.
    Variant and active-modifier fields are present as a future interface shape,
    but every non-base/non-empty value fails closed in M38-A.
    """

    currency_id: str
    item_state: ItemState
    mode_id: str = "m38a_resolved_operation"
    variant_id: str | None = None
    active_modifier_ids: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class ResolvedOperationFilters:
    """Future filter shape; all fields must be inactive in M38-A."""

    side_filter: Side | None = None
    mml: int | None = None
    whittling: bool = False
    desecrated_only: bool = False


@dataclass(frozen=True, slots=True)
class ResolvedOperationPlan:
    schema_version: str
    plan_kind: Literal["single_operation"]
    currency_id: str
    operation_id: str
    operation_kind: OperationKind
    runtime_admission_status: str
    variant_id: str | None
    active_modifier_ids: tuple[str, ...]
    filters: ResolvedOperationFilters
    operation: AcceptedResolvedOperation

    def public_summary(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "plan_kind": self.plan_kind,
            "currency_id": self.currency_id,
            "operation_id": self.operation_id,
            "operation_kind": self.operation_kind,
            "runtime_admission_status": self.runtime_admission_status,
            "variant_id": self.variant_id,
            "active_modifier_count": len(self.active_modifier_ids),
            "filter_side": self.filters.side_filter.value if self.filters.side_filter else None,
            "filter_mml": self.filters.mml,
            "filter_whittling": self.filters.whittling,
            "filter_desecrated_only": self.filters.desecrated_only,
        }


class OperationResolver:
    """M38-A fail-closed single-operation admission/compilation seam."""

    def __init__(self, *, static: StaticGameData) -> None:
        self.static = static

    def resolve(self, request: OperationResolverRequest) -> ResolvedOperationPlan:
        self._reject_variant_layers(request.variant_id)
        self._reject_modifier_layers(request.active_modifier_ids)

        if request.currency_id == MC_OPERATION_ID:
            operation = OrdinaryAddOperation(
                mode_id=request.mode_id,
                item_class=request.item_state.item_class,
            )
            return ResolvedOperationPlan(
                schema_version=M38A_RESOLVER_SCHEMA_VERSION,
                plan_kind="single_operation",
                currency_id=request.currency_id,
                operation_id=operation.operation_id,
                operation_kind="engine_primitive",
                runtime_admission_status=ACCEPTED_RUNTIME_STATUS,
                variant_id=None,
                active_modifier_ids=(),
                filters=ResolvedOperationFilters(),
                operation=operation,
            )

        row = _operation_row(self.static.operations, request.currency_id)
        if row is None:
            raise M38AResolverAdmissionError(
                f"unknown operation/currency for M38-A resolver: {request.currency_id}"
            )
        status = row.get("runtime_admission_status")
        if status != ACCEPTED_RUNTIME_STATUS:
            raise M38AResolverAdmissionError(
                "operation/currency is not executable-admitted for M38-A resolver: "
                f"{request.currency_id} (runtime_admission_status={status!r})"
            )

        if request.currency_id == ANNULMENT_OPERATION_ID:
            operation = AnnulmentOperation(
                mode_id=request.mode_id,
                item_class=request.item_state.item_class,
            )
        elif request.currency_id == CHAOS_OPERATION_ID:
            operation = ChaosLikeOperation(
                mode_id=request.mode_id,
                item_class=request.item_state.item_class,
            )
        else:
            raise M38AResolverAdmissionError(
                "operation row is admitted but unsupported by the M38-A resolver skeleton: "
                f"{request.currency_id}"
            )

        return ResolvedOperationPlan(
            schema_version=M38A_RESOLVER_SCHEMA_VERSION,
            plan_kind="single_operation",
            currency_id=request.currency_id,
            operation_id=operation.operation_id,
            operation_kind="catalog_operation",
            runtime_admission_status=ACCEPTED_RUNTIME_STATUS,
            variant_id=None,
            active_modifier_ids=(),
            filters=ResolvedOperationFilters(),
            operation=operation,
        )

    def _reject_variant_layers(self, variant_id: str | None) -> None:
        if variant_id not in BASE_VARIANT_IDS:
            raise M38AResolverAdmissionError(
                "operation variants are not executable-admitted in M38-A resolver: "
                f"{variant_id}"
            )

    def _reject_modifier_layers(self, active_modifier_ids: tuple[str, ...]) -> None:
        if active_modifier_ids:
            raise M38AResolverAdmissionError(
                "operation modifier layers are not executable-admitted in M38-A resolver: "
                f"{active_modifier_ids!r}"
            )


def _operation_row(operations: Any, operation_id: str) -> dict[str, Any] | None:
    if not isinstance(operations, dict):
        return None
    for row in operations.get("operations") or ():
        if isinstance(row, dict) and row.get("operation_id") == operation_id:
            return row
    return None


__all__ = [
    "ACCEPTED_RUNTIME_STATUS",
    "M38A_RESOLVER_SCHEMA_VERSION",
    "M38AResolverAdmissionError",
    "M38AResolverError",
    "OperationResolver",
    "OperationResolverRequest",
    "ResolvedOperationFilters",
    "ResolvedOperationPlan",
]
