from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

from p2c_engine.domain.enums import Rarity, Side
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
from p2c_engine.monte_carlo.rarity_progression import (
    M40A_OPERATION_IDS,
    M40A_SEMANTICS_VERSION,
    CatalogSingleAddOperation,
    CatalogSingleAddPrecondition,
)
from p2c_engine.static_data.game_data import StaticGameData


M38A_RESOLVER_SCHEMA_VERSION = "p2c.m38a.operation_resolver_skeleton.v1"
M39A_RESOLVER_SCHEMA_VERSION = "p2c.m39a.operation_resolver_mml_filter_interface.v1"
M39B_RESOLVER_SCHEMA_VERSION = "p2c.m39b.greater_perfect_exalted_chaos_runtime.v1"
M40A_RESOLVER_SCHEMA_VERSION = "p2c.m40a.rarity_progression_runtime.v1"
ACCEPTED_RUNTIME_STATUS = "accepted_executable_runtime"
BASE_VARIANT_IDS = frozenset({None, "", "base"})
M39B_EXALTED_CURRENCY_IDS = frozenset({"greater_exalted", "perfect_exalted"})
M39B_CHAOS_CURRENCY_IDS = frozenset({"greater_chaos", "perfect_chaos"})


AcceptedResolvedOperation = (
    OrdinaryAddOperation
    | AnnulmentOperation
    | ChaosLikeOperation
    | CatalogSingleAddOperation
)
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
    but every non-base/non-empty value fails closed.

    M39-A admits an explicit MML filter parameter for the accepted ordinary_add
    engine primitive. M39-B additionally admits four independent catalog rows:
    Greater/Perfect Exalted compile to ordinary_add plus row-declared MML, while
    Greater/Perfect Chaos compile to accepted base Chaos mechanics plus
    row-declared MML on the post-removal add pool. Caller-supplied catalog MML,
    Essence, Whittling, Omens, and side/desecrated modifiers remain fail-closed.
    """

    currency_id: str
    item_state: ItemState
    mode_id: str = "m38a_resolved_operation"
    variant_id: str | None = None
    active_modifier_ids: tuple[str, ...] = ()
    mml: int | None = None


@dataclass(frozen=True, slots=True)
class ResolvedOperationFilters:
    """Resolved filter shape.

    In M39-A, only `mml` may be active, and only for explicit ordinary_add
    engine-primitive requests. All other fields remain future fail-closed
    interfaces.
    """

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
        mml = self._validated_mml_filter(request.mml)

        if request.currency_id == MC_OPERATION_ID:
            operation = OrdinaryAddOperation(
                mode_id=request.mode_id,
                item_class=request.item_state.item_class,
                mml=mml,
            )
            return ResolvedOperationPlan(
                schema_version=M39A_RESOLVER_SCHEMA_VERSION,
                plan_kind="single_operation",
                currency_id=request.currency_id,
                operation_id=operation.operation_id,
                operation_kind="engine_primitive",
                runtime_admission_status=ACCEPTED_RUNTIME_STATUS,
                variant_id=None,
                active_modifier_ids=(),
                filters=ResolvedOperationFilters(mml=mml),
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

        if mml is not None:
            raise M38AResolverAdmissionError(
                "MML filters are executable-admitted only for explicit ordinary_add "
                "requests when supplied by the caller; catalog-operation MML is fixed "
                f"by its admitted operation row: {request.currency_id}"
            )

        declared_mml = _declared_add_mml(row)
        group = row.get("group")
        schema_version = M39A_RESOLVER_SCHEMA_VERSION
        filters = ResolvedOperationFilters()

        if request.currency_id in M40A_OPERATION_IDS:
            operation = _compile_m40a_single_add(row, request)
            schema_version = M40A_RESOLVER_SCHEMA_VERSION
            filters = ResolvedOperationFilters(mml=declared_mml)
        elif request.currency_id == ANNULMENT_OPERATION_ID:
            _validate_catalog_input_rarity(row, request.item_state)
            if declared_mml is not None:
                raise M38AResolverAdmissionError("Annulment catalog row must not declare add MML")
            operation = AnnulmentOperation(
                mode_id=request.mode_id,
                item_class=request.item_state.item_class,
            )
        elif group == "exalted":
            _validate_catalog_input_rarity(row, request.item_state)
            if request.currency_id not in M39B_EXALTED_CURRENCY_IDS:
                raise M38AResolverAdmissionError(
                    "admitted Exalted-family row is outside the M39-B allowlist: "
                    f"{request.currency_id}"
                )
            if declared_mml is None:
                raise M38AResolverAdmissionError(
                    f"M39-B Exalted variant requires row-declared MML: {request.currency_id}"
                )
            _validate_m39b_exalted_transition(row)
            operation = OrdinaryAddOperation(
                mode_id=request.mode_id,
                item_class=request.item_state.item_class,
                mml=declared_mml,
            )
            schema_version = M39B_RESOLVER_SCHEMA_VERSION
            filters = ResolvedOperationFilters(mml=declared_mml)
        elif group == "chaos":
            _validate_catalog_input_rarity(row, request.item_state)
            if (
                request.currency_id != CHAOS_OPERATION_ID
                and request.currency_id not in M39B_CHAOS_CURRENCY_IDS
            ):
                raise M38AResolverAdmissionError(
                    "admitted Chaos-family row is outside the accepted resolver allowlist: "
                    f"{request.currency_id}"
                )
            operation = ChaosLikeOperation(
                mode_id=request.mode_id,
                operation_id=request.currency_id,
                item_class=request.item_state.item_class,
                mml=declared_mml,
            )
            if request.currency_id in M39B_CHAOS_CURRENCY_IDS:
                if declared_mml is None:
                    raise M38AResolverAdmissionError(
                        f"M39-B Chaos variant requires row-declared MML: {request.currency_id}"
                    )
                _validate_m39b_chaos_transition(row)
                schema_version = M39B_RESOLVER_SCHEMA_VERSION
                filters = ResolvedOperationFilters(mml=declared_mml)
        else:
            raise M38AResolverAdmissionError(
                "operation row is admitted but unsupported by the M38-A resolver skeleton: "
                f"{request.currency_id}"
            )

        return ResolvedOperationPlan(
            schema_version=schema_version,
            plan_kind="single_operation",
            currency_id=request.currency_id,
            operation_id=operation.operation_id,
            operation_kind="catalog_operation",
            runtime_admission_status=ACCEPTED_RUNTIME_STATUS,
            variant_id=None,
            active_modifier_ids=(),
            filters=filters,
            operation=operation,
        )

    def _validated_mml_filter(self, mml: int | None) -> int | None:
        if mml is None:
            return None
        if isinstance(mml, bool) or not isinstance(mml, int):
            raise M38AResolverAdmissionError(f"MML filter must be an integer or null: {mml!r}")
        if mml <= 0:
            raise M38AResolverAdmissionError(f"MML filter must be a positive integer: {mml!r}")
        return mml

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


def _declared_add_mml(row: dict[str, Any]) -> int | None:
    transition = row.get("transition")
    add = transition.get("add") if isinstance(transition, dict) else None
    mml = add.get("mml") if isinstance(add, dict) else None
    if mml is None:
        return None
    if isinstance(mml, bool) or not isinstance(mml, int) or mml <= 0:
        raise M38AResolverAdmissionError(
            f"catalog row has invalid add MML: {row.get('operation_id')} ({mml!r})"
        )
    return mml


def _validate_catalog_input_rarity(row: dict[str, Any], state: ItemState) -> None:
    input_rarities = row.get("input_rarity")
    if input_rarities is None:
        return
    if not isinstance(input_rarities, list) or any(
        not isinstance(value, str) for value in input_rarities
    ):
        raise M38AResolverAdmissionError(
            f"catalog row has invalid input_rarity: {row.get('operation_id')}"
        )
    if state.rarity.value not in input_rarities:
        raise M38AResolverAdmissionError(
            "catalog operation does not accept the current item rarity: "
            f"{row.get('operation_id')} ({state.rarity.value})"
        )


def _validate_m39b_exalted_transition(row: dict[str, Any]) -> None:
    transition = row.get("transition")
    remove = transition.get("remove") if isinstance(transition, dict) else None
    add = transition.get("add") if isinstance(transition, dict) else None
    if (
        not isinstance(transition, dict)
        or transition.get("atomic") is not True
        or transition.get("output_rarity") not in (None, "rare")
        or not isinstance(remove, dict)
        or remove.get("kind") != "none"
        or not isinstance(add, dict)
        or add.get("kind") != "ordinary_weighted"
        or add.get("count") != 1
    ):
        raise M38AResolverAdmissionError(
            f"unsupported M39-B Exalted transition shape: {row.get('operation_id')}"
        )


def _validate_m39b_chaos_transition(row: dict[str, Any]) -> None:
    transition = row.get("transition")
    remove = transition.get("remove") if isinstance(transition, dict) else None
    add = transition.get("add") if isinstance(transition, dict) else None
    if (
        not isinstance(transition, dict)
        or transition.get("atomic") is not True
        or transition.get("output_rarity") not in (None, "rare")
        or not isinstance(remove, dict)
        or remove.get("kind") != "uniform_installed_instance"
        or remove.get("count") != 1
        or "fractured" not in (remove.get("exclude_flags") or ())
        or not isinstance(add, dict)
        or add.get("kind") != "ordinary_weighted"
        or add.get("count") != 1
    ):
        raise M38AResolverAdmissionError(
            f"unsupported M39-B Chaos transition shape: {row.get('operation_id')}"
        )


def _compile_m40a_single_add(
    row: dict[str, Any], request: OperationResolverRequest
) -> CatalogSingleAddOperation:
    transition = row.get("transition")
    remove = transition.get("remove") if isinstance(transition, dict) else None
    add = transition.get("add") if isinstance(transition, dict) else None
    if (
        not isinstance(transition, dict)
        or transition.get("atomic") is not True
        or not isinstance(remove, dict)
        or remove.get("kind") != "none"
        or not isinstance(add, dict)
        or add.get("kind") != "ordinary_weighted"
        or add.get("count") != 1
        or add.get("side_filter") not in (None,)
    ):
        raise M38AResolverAdmissionError(
            f"unsupported M40-A single-add transition shape: {row.get('operation_id')}"
        )

    raw_inputs = row.get("input_rarity")
    if not isinstance(raw_inputs, list) or not raw_inputs:
        raise M38AResolverAdmissionError(
            f"M40-A row requires input_rarity: {row.get('operation_id')}"
        )
    try:
        input_rarities = tuple(Rarity(value) for value in raw_inputs)
        output_rarity = Rarity(transition.get("output_rarity"))
        pool_build_rarity = Rarity(
            transition.get("pool_build_rarity", output_rarity.value)
        )
    except (TypeError, ValueError) as exc:
        raise M38AResolverAdmissionError(
            f"invalid M40-A rarity contract: {row.get('operation_id')}"
        ) from exc

    return CatalogSingleAddOperation(
        mode_id=request.mode_id,
        operation_id=request.currency_id,
        item_class=request.item_state.item_class,
        input_rarities=input_rarities,
        pool_build_rarity=pool_build_rarity,
        output_rarity=output_rarity,
        preconditions=_compile_m40a_preconditions(transition.get("preconditions"), row),
        mml=_declared_add_mml(row),
        semantics_version=M40A_SEMANTICS_VERSION,
    )


def _compile_m40a_preconditions(
    value: Any, row: dict[str, Any]
) -> tuple[CatalogSingleAddPrecondition, ...]:
    if value is None:
        return ()
    if not isinstance(value, list):
        raise M38AResolverAdmissionError(
            f"invalid M40-A preconditions: {row.get('operation_id')}"
        )
    output: list[CatalogSingleAddPrecondition] = []
    for raw in value:
        if not isinstance(raw, dict):
            raise M38AResolverAdmissionError(
                f"invalid M40-A precondition: {row.get('operation_id')}"
            )
        precondition = CatalogSingleAddPrecondition(
            kind=raw.get("type"),
            operator=raw.get("operator"),
            value=raw.get("value"),
        )
        supported = (
            precondition.kind == "occupied_explicit_slots"
            and precondition.operator == "<"
            and isinstance(precondition.value, int)
            and not isinstance(precondition.value, bool)
            and precondition.value > 0
        ) or (
            precondition.kind == "free_explicit_slots_after_side_filter"
            and precondition.operator == ">="
            and precondition.value == "resolved_add_count"
        )
        if not supported:
            raise M38AResolverAdmissionError(
                "unsupported M40-A precondition: "
                f"{row.get('operation_id')} ({precondition!r})"
            )
        output.append(precondition)
    return tuple(output)


__all__ = [
    "ACCEPTED_RUNTIME_STATUS",
    "M38A_RESOLVER_SCHEMA_VERSION",
    "M39A_RESOLVER_SCHEMA_VERSION",
    "M39B_RESOLVER_SCHEMA_VERSION",
    "M40A_RESOLVER_SCHEMA_VERSION",
    "M38AResolverAdmissionError",
    "M38AResolverError",
    "OperationResolver",
    "OperationResolverRequest",
    "ResolvedOperationFilters",
    "ResolvedOperationPlan",
]
