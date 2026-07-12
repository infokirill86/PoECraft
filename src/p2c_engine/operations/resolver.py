from __future__ import annotations

from collections.abc import Mapping
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
from p2c_engine.monte_carlo.greater_essence import (
    M41A_OPERATION_IDS,
    M41A_SEMANTICS_VERSION,
    GreaterEssenceHarness,
    GreaterEssenceOperation,
    M41AGreaterEssenceInvariantViolation,
)
from p2c_engine.monte_carlo.perfect_essence import (
    M42A_OPERATION_IDS,
    M42A_SEMANTICS_VERSION,
    PerfectEssenceHarness,
    PerfectEssenceOperation,
    M42APerfectEssenceInvariantViolation,
)
from p2c_engine.monte_carlo.alchemy import (
    M44A_ADD_COUNT,
    M44A_ALCHEMY_OPERATION_ID,
    M44A_SEMANTICS_VERSION,
    AlchemyOperation,
)
from p2c_engine.monte_carlo.fracture import (
    FRACTURING_ORB_OPERATION_ID,
    M46A_FRACTURE_SEMANTICS_VERSION,
    FractureOperation,
)
from p2c_engine.monte_carlo.jawbone import (
    M47A1_OPERATION_IDS,
    M47A1_SEMANTICS_VERSION,
    JawboneOperation,
)
from p2c_engine.static_data.game_data import StaticGameData
from p2c_engine.operations.omen import (
    M45AOmenAdmissionError,
    ResolvedOmenEffects,
    compile_omen_effects,
)


M38A_RESOLVER_SCHEMA_VERSION = "p2c.m38a.operation_resolver_skeleton.v1"
M39A_RESOLVER_SCHEMA_VERSION = "p2c.m39a.operation_resolver_mml_filter_interface.v1"
M39B_RESOLVER_SCHEMA_VERSION = "p2c.m39b.greater_perfect_exalted_chaos_runtime.v1"
M40A_RESOLVER_SCHEMA_VERSION = "p2c.m40a.rarity_progression_runtime.v1"
M41A_RESOLVER_SCHEMA_VERSION = "p2c.m41a.greater_essence_quarterstaff_runtime.v1"
M42A_RESOLVER_SCHEMA_VERSION = "p2c.m42a.perfect_essence_quarterstaff_runtime.v1"
M44A_RESOLVER_SCHEMA_VERSION = "p2c.m44a.alchemy_runtime.v1"
M45A_RESOLVER_SCHEMA_VERSION = "p2c.m45a.independent_omen_layer.v1"
M46A_RESOLVER_SCHEMA_VERSION = "p2c.m46a.fracture_core_runtime.v1"
M47A1_RESOLVER_SCHEMA_VERSION = "p2c.m47a1.jawbone_placeholder_runtime.v1"
ACCEPTED_RUNTIME_STATUS = "accepted_executable_runtime"
BASE_VARIANT_IDS = frozenset({None, "", "base"})
M39B_EXALTED_CURRENCY_IDS = frozenset({"greater_exalted", "perfect_exalted"})
M39B_CHAOS_CURRENCY_IDS = frozenset({"greater_chaos", "perfect_chaos"})


AcceptedResolvedOperation = (
    OrdinaryAddOperation
    | AnnulmentOperation
    | ChaosLikeOperation
    | CatalogSingleAddOperation
    | GreaterEssenceOperation
    | PerfectEssenceOperation
    | AlchemyOperation
    | FractureOperation
    | JawboneOperation
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
    removal_side_filter: Side | None = None
    mml: int | None = None
    whittling: bool = False
    desecrated_only: bool = False
    add_count: int = 1


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
            "filter_removal_side": (
                self.filters.removal_side_filter.value
                if self.filters.removal_side_filter
                else None
            ),
            "filter_mml": self.filters.mml,
            "filter_whittling": self.filters.whittling,
            "filter_desecrated_only": self.filters.desecrated_only,
            "resolved_add_count": self.filters.add_count,
        }


class OperationResolver:
    """M38-A fail-closed single-operation admission/compilation seam."""

    def __init__(self, *, static: StaticGameData) -> None:
        self.static = static

    def resolve(self, request: OperationResolverRequest) -> ResolvedOperationPlan:
        self._reject_variant_layers(request.variant_id)
        mml = self._validated_mml_filter(request.mml)

        if request.currency_id == MC_OPERATION_ID:
            self._reject_modifier_layers(request.active_modifier_ids)
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
        omen_effects = self._resolve_omen_layers(group, request.active_modifier_ids)
        schema_version = M39A_RESOLVER_SCHEMA_VERSION
        filters = _resolved_filters(omen_effects)

        if request.currency_id in M40A_OPERATION_IDS:
            operation = _compile_m40a_single_add(row, request, omen_effects)
            schema_version = (
                M45A_RESOLVER_SCHEMA_VERSION
                if omen_effects.omen_ids
                else M40A_RESOLVER_SCHEMA_VERSION
            )
            filters = _resolved_filters(omen_effects, mml=declared_mml)
        elif request.currency_id in M41A_OPERATION_IDS:
            operation = _compile_m41a_greater_essence(self.static, row, request)
            schema_version = M41A_RESOLVER_SCHEMA_VERSION
        elif request.currency_id in M42A_OPERATION_IDS:
            operation = _compile_m42a_perfect_essence(
                self.static, row, request, omen_effects
            )
            schema_version = (
                M45A_RESOLVER_SCHEMA_VERSION
                if omen_effects.omen_ids
                else M42A_RESOLVER_SCHEMA_VERSION
            )
        elif request.currency_id == M44A_ALCHEMY_OPERATION_ID:
            operation = _compile_m44a_alchemy(row, request)
            schema_version = M44A_RESOLVER_SCHEMA_VERSION
        elif request.currency_id == FRACTURING_ORB_OPERATION_ID:
            _validate_catalog_input_rarity(row, request.item_state)
            if omen_effects.omen_ids:
                raise M38AResolverAdmissionError(
                    "Fracture modifier layers are not executable-admitted"
                )
            _validate_m46a_fracture_transition(row)
            operation = FractureOperation(
                mode_id=request.mode_id,
                item_class=request.item_state.item_class,
                semantics_version=M46A_FRACTURE_SEMANTICS_VERSION,
            )
            schema_version = M46A_RESOLVER_SCHEMA_VERSION
        elif request.currency_id in M47A1_OPERATION_IDS:
            _validate_catalog_input_rarity(row, request.item_state)
            if omen_effects.omen_ids:
                raise M38AResolverAdmissionError(
                    "Jawbone modifier layers are not executable-admitted"
                )
            operation = _compile_m47a1_jawbone(row, request)
            schema_version = M47A1_RESOLVER_SCHEMA_VERSION
        elif request.currency_id == ANNULMENT_OPERATION_ID:
            _validate_catalog_input_rarity(row, request.item_state)
            if declared_mml is not None:
                raise M38AResolverAdmissionError("Annulment catalog row must not declare add MML")
            operation = AnnulmentOperation(
                mode_id=request.mode_id,
                item_class=request.item_state.item_class,
                side_filter=omen_effects.removal_side_filter,
                active_modifier_ids=omen_effects.omen_ids,
            )
            if omen_effects.omen_ids:
                schema_version = M45A_RESOLVER_SCHEMA_VERSION
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
                side_filter=omen_effects.add_side_filter,
                mml=declared_mml,
                source_currency_id=request.currency_id,
                active_modifier_ids=omen_effects.omen_ids,
                add_count=omen_effects.add_count,
            )
            schema_version = (
                M45A_RESOLVER_SCHEMA_VERSION
                if omen_effects.omen_ids
                else M39B_RESOLVER_SCHEMA_VERSION
            )
            filters = _resolved_filters(omen_effects, mml=declared_mml)
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
                removal_side_filter=omen_effects.removal_side_filter,
                lowest_modifier_level=omen_effects.lowest_modifier_level,
                active_modifier_ids=omen_effects.omen_ids,
            )
            if request.currency_id in M39B_CHAOS_CURRENCY_IDS:
                if declared_mml is None:
                    raise M38AResolverAdmissionError(
                        f"M39-B Chaos variant requires row-declared MML: {request.currency_id}"
                    )
                _validate_m39b_chaos_transition(row)
                schema_version = M39B_RESOLVER_SCHEMA_VERSION
                filters = _resolved_filters(omen_effects, mml=declared_mml)
            if omen_effects.omen_ids:
                schema_version = M45A_RESOLVER_SCHEMA_VERSION
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
            active_modifier_ids=omen_effects.omen_ids,
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

    def _resolve_omen_layers(
        self, operation_group: Any, active_modifier_ids: tuple[str, ...]
    ) -> ResolvedOmenEffects:
        if not isinstance(operation_group, str):
            if active_modifier_ids:
                raise M38AResolverAdmissionError(
                    "Omen modifier layers require a catalog operation group"
                )
            return ResolvedOmenEffects()
        try:
            return compile_omen_effects(
                self.static.omens,
                operation_group=operation_group,
                active_modifier_ids=active_modifier_ids,
            )
        except M45AOmenAdmissionError as exc:
            raise M38AResolverAdmissionError(
                f"modifier layers are not executable-admitted: {exc}"
            ) from exc


def _operation_row(operations: Any, operation_id: str) -> dict[str, Any] | None:
    if not isinstance(operations, Mapping):
        return None
    for row in operations.get("operations") or ():
        if isinstance(row, Mapping) and row.get("operation_id") == operation_id:
            return row
    return None


def _declared_add_mml(row: dict[str, Any]) -> int | None:
    transition = row.get("transition")
    add = transition.get("add") if isinstance(transition, Mapping) else None
    mml = add.get("mml") if isinstance(add, Mapping) else None
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
    if not isinstance(input_rarities, (list, tuple)) or any(
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
    remove = transition.get("remove") if isinstance(transition, Mapping) else None
    add = transition.get("add") if isinstance(transition, Mapping) else None
    if (
        not isinstance(transition, Mapping)
        or transition.get("atomic") is not True
        or transition.get("output_rarity") not in (None, "rare")
        or not isinstance(remove, Mapping)
        or remove.get("kind") != "none"
        or not isinstance(add, Mapping)
        or add.get("kind") != "ordinary_weighted"
        or add.get("count") != 1
    ):
        raise M38AResolverAdmissionError(
            f"unsupported M39-B Exalted transition shape: {row.get('operation_id')}"
        )


def _validate_m46a_fracture_transition(row: dict[str, Any]) -> None:
    transition = row.get("transition")
    preconditions = transition.get("preconditions") if isinstance(transition, Mapping) else None
    target = transition.get("target") if isinstance(transition, Mapping) else None
    mutation = transition.get("mutation") if isinstance(transition, Mapping) else None
    precondition_pairs = {
        (entry.get("type"), entry.get("operator"), entry.get("value"))
        for entry in preconditions or ()
        if isinstance(entry, Mapping)
    }
    required = {
        ("installed_modifier_or_placeholder_count", ">=", 4),
        ("fractured_modifier_count", "==", 0),
        ("desecrated_modifier_count", "==", 0),
    }
    if (
        not isinstance(transition, Mapping)
        or transition.get("atomic") is not True
        or transition.get("output_rarity") != "rare"
        or not required <= precondition_pairs
        or not isinstance(target, Mapping)
        or target.get("kind") != "uniform_installed_instance"
        or target.get("selection_scope") != "combined_prefix_suffix"
        or target.get("weighting") != "uniform_instance_identity"
        or not isinstance(mutation, Mapping)
        or mutation.get("set_flag") != {"fractured": True}
    ):
        raise M38AResolverAdmissionError(
            "unsupported M46-A Fracture transition shape"
        )


def _compile_m47a1_jawbone(
    row: dict[str, Any], request: OperationResolverRequest
) -> JawboneOperation:
    transition = row.get("transition")
    side_selection = (
        transition.get("side_selection") if isinstance(transition, Mapping) else None
    )
    replacement = (
        transition.get("replacement") if isinstance(transition, Mapping) else None
    )
    target = replacement.get("target") if isinstance(replacement, Mapping) else None
    install = transition.get("install") if isinstance(transition, Mapping) else None
    if (
        not isinstance(transition, Mapping)
        or transition.get("atomic") is not True
        or transition.get("output_rarity") != "rare"
        or not isinstance(side_selection, Mapping)
        or side_selection.get("when_one_side_has_capacity")
        != "install_on_the_only_free_side"
        or side_selection.get("when_both_sides_have_capacity")
        != "uniform_prefix_or_suffix"
        or side_selection.get("never_select_full_side_while_other_side_has_capacity")
        is not True
        or not isinstance(replacement, Mapping)
        or replacement.get("only_when_item_fully_occupied") is not True
        or not isinstance(target, Mapping)
        or target.get("kind") != "uniform_installed_instance"
        or target.get("selection_scope") != "combined_prefix_suffix"
        or "fractured" not in (target.get("exclude_flags") or ())
        or replacement.get("placeholder_side") != "removed_instance_side"
        or not isinstance(install, Mapping)
        or install.get("kind") != "unrevealed_desecrated_placeholder"
    ):
        raise M38AResolverAdmissionError(
            f"unsupported M47-A1 Jawbone transition shape: {request.currency_id}"
        )
    item_level_max = transition.get("item_level_max")
    reveal_mml = transition.get("reveal_mml")
    for name, value in (("item_level_max", item_level_max), ("reveal_mml", reveal_mml)):
        if value is not None and (
            isinstance(value, bool) or not isinstance(value, int) or value <= 0
        ):
            raise M38AResolverAdmissionError(
                f"invalid M47-A1 {name}: {request.currency_id}"
            )
    return JawboneOperation(
        mode_id=request.mode_id,
        operation_id=request.currency_id,
        item_class=request.item_state.item_class,
        item_level_max=item_level_max,
        reveal_mml=reveal_mml,
        lich_tag_constraint=None,
        semantics_version=M47A1_SEMANTICS_VERSION,
    )


def _validate_m39b_chaos_transition(row: dict[str, Any]) -> None:
    transition = row.get("transition")
    remove = transition.get("remove") if isinstance(transition, Mapping) else None
    add = transition.get("add") if isinstance(transition, Mapping) else None
    if (
        not isinstance(transition, Mapping)
        or transition.get("atomic") is not True
        or transition.get("output_rarity") not in (None, "rare")
        or not isinstance(remove, Mapping)
        or remove.get("kind") != "uniform_installed_instance"
        or remove.get("count") != 1
        or "fractured" not in (remove.get("exclude_flags") or ())
        or not isinstance(add, Mapping)
        or add.get("kind") != "ordinary_weighted"
        or add.get("count") != 1
    ):
        raise M38AResolverAdmissionError(
            f"unsupported M39-B Chaos transition shape: {row.get('operation_id')}"
        )


def _compile_m40a_single_add(
    row: dict[str, Any],
    request: OperationResolverRequest,
    omen_effects: ResolvedOmenEffects,
) -> CatalogSingleAddOperation:
    transition = row.get("transition")
    remove = transition.get("remove") if isinstance(transition, Mapping) else None
    add = transition.get("add") if isinstance(transition, Mapping) else None
    if (
        not isinstance(transition, Mapping)
        or transition.get("atomic") is not True
        or not isinstance(remove, Mapping)
        or remove.get("kind") != "none"
        or not isinstance(add, Mapping)
        or add.get("kind") != "ordinary_weighted"
        or add.get("count") != 1
        or add.get("side_filter") not in (None,)
    ):
        raise M38AResolverAdmissionError(
            f"unsupported M40-A single-add transition shape: {row.get('operation_id')}"
        )

    raw_inputs = row.get("input_rarity")
    if not isinstance(raw_inputs, (list, tuple)) or not raw_inputs:
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
        side_filter=omen_effects.add_side_filter,
        active_modifier_ids=omen_effects.omen_ids,
        add_count=omen_effects.add_count,
        semantics_version=M40A_SEMANTICS_VERSION,
    )


def _compile_m40a_preconditions(
    value: Any, row: dict[str, Any]
) -> tuple[CatalogSingleAddPrecondition, ...]:
    if value is None:
        return ()
    if not isinstance(value, (list, tuple)):
        raise M38AResolverAdmissionError(
            f"invalid M40-A preconditions: {row.get('operation_id')}"
        )
    output: list[CatalogSingleAddPrecondition] = []
    for raw in value:
        if not isinstance(raw, Mapping):
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


def _compile_m41a_greater_essence(
    static: StaticGameData,
    row: dict[str, Any],
    request: OperationResolverRequest,
) -> GreaterEssenceOperation:
    _validate_catalog_input_rarity(row, request.item_state)
    transition = row.get("transition")
    if not isinstance(transition, Mapping):
        raise M38AResolverAdmissionError(
            f"invalid M41-A Greater Essence transition: {request.currency_id}"
        )
    guaranteed_mod_id = transition.get("guaranteed_mod_id")
    guaranteed_family_id = transition.get("guaranteed_family_id")
    guaranteed_side = transition.get("guaranteed_side")
    if not isinstance(guaranteed_mod_id, str) or not isinstance(
        guaranteed_family_id, str
    ):
        raise M38AResolverAdmissionError(
            f"missing M41-A guaranteed modifier metadata: {request.currency_id}"
        )
    try:
        side = Side(guaranteed_side)
    except (TypeError, ValueError) as exc:
        raise M38AResolverAdmissionError(
            f"invalid M41-A guaranteed side: {request.currency_id}"
        ) from exc
    operation = GreaterEssenceOperation(
        mode_id=request.mode_id,
        operation_id=request.currency_id,
        item_class=request.item_state.item_class,
        guaranteed_mod_id=guaranteed_mod_id,
        guaranteed_family_id=guaranteed_family_id,
        guaranteed_side=side,
        semantics_version=M41A_SEMANTICS_VERSION,
    )
    try:
        GreaterEssenceHarness(static=static).validate_operation_contract(operation)
    except M41AGreaterEssenceInvariantViolation as exc:
        raise M38AResolverAdmissionError(
            f"invalid admitted M41-A Greater Essence row: {request.currency_id}: {exc}"
        ) from exc
    return operation


def _compile_m42a_perfect_essence(
    static: StaticGameData,
    row: dict[str, Any],
    request: OperationResolverRequest,
    omen_effects: ResolvedOmenEffects,
) -> PerfectEssenceOperation:
    _validate_catalog_input_rarity(row, request.item_state)
    transition = row.get("transition")
    if not isinstance(transition, Mapping):
        raise M38AResolverAdmissionError(
            f"invalid M42-A Perfect Essence transition: {request.currency_id}"
        )
    guaranteed_mod_id = transition.get("guaranteed_mod_id")
    guaranteed_family_id = transition.get("guaranteed_family_id")
    guaranteed_side = transition.get("guaranteed_side")
    if not isinstance(guaranteed_mod_id, str) or not isinstance(
        guaranteed_family_id, str
    ):
        raise M38AResolverAdmissionError(
            f"missing M42-A guaranteed modifier metadata: {request.currency_id}"
        )
    try:
        side = Side(guaranteed_side)
    except (TypeError, ValueError) as exc:
        raise M38AResolverAdmissionError(
            f"invalid M42-A guaranteed side: {request.currency_id}"
        ) from exc
    operation = PerfectEssenceOperation(
        mode_id=request.mode_id,
        operation_id=request.currency_id,
        item_class=request.item_state.item_class,
        guaranteed_mod_id=guaranteed_mod_id,
        guaranteed_family_id=guaranteed_family_id,
        guaranteed_side=side,
        removal_side_filter=omen_effects.removal_side_filter,
        active_modifier_ids=omen_effects.omen_ids,
        semantics_version=M42A_SEMANTICS_VERSION,
    )
    try:
        PerfectEssenceHarness(static=static).validate_operation_contract(operation)
    except M42APerfectEssenceInvariantViolation as exc:
        raise M38AResolverAdmissionError(
            f"invalid admitted M42-A Perfect Essence row: {request.currency_id}: {exc}"
        ) from exc
    return operation


def _compile_m44a_alchemy(
    row: dict[str, Any], request: OperationResolverRequest
) -> AlchemyOperation:
    _validate_catalog_input_rarity(row, request.item_state)
    transition = row.get("transition")
    remove = transition.get("remove") if isinstance(transition, Mapping) else None
    add = transition.get("add") if isinstance(transition, Mapping) else None
    sequence = transition.get("sequence") if isinstance(transition, Mapping) else None
    if (
        not isinstance(transition, Mapping)
        or transition.get("atomic") is not True
        or transition.get("output_rarity") != "rare"
        or tuple(sequence or ())
        != (
            "discard_all_explicit",
            "create_empty_rare_shell",
            "add_ordinary_x4",
            "commit",
        )
        or not isinstance(remove, Mapping)
        or remove.get("kind") != "all_explicit"
        or not isinstance(add, Mapping)
        or add.get("kind") != "ordinary_weighted_sequential"
        or add.get("count") != M44A_ADD_COUNT
        or add.get("mml") is not None
    ):
        raise M38AResolverAdmissionError("unsupported admitted M44-A Alchemy transition")

    raw_inputs = row.get("input_rarity")
    if not isinstance(raw_inputs, (list, tuple)):
        raise M38AResolverAdmissionError("invalid admitted M44-A Alchemy input_rarity")
    try:
        input_rarities = tuple(Rarity(value) for value in raw_inputs)
    except (TypeError, ValueError) as exc:
        raise M38AResolverAdmissionError(
            "invalid admitted M44-A Alchemy input_rarity"
        ) from exc
    if input_rarities != (Rarity.NORMAL, Rarity.MAGIC):
        raise M38AResolverAdmissionError(
            "M44-A Alchemy admits exactly Normal and Magic input"
        )
    return AlchemyOperation(
        mode_id=request.mode_id,
        operation_id=request.currency_id,
        item_class=request.item_state.item_class,
        input_rarities=input_rarities,
        output_rarity=Rarity.RARE,
        add_count=M44A_ADD_COUNT,
        semantics_version=M44A_SEMANTICS_VERSION,
    )


def _resolved_filters(
    effects: ResolvedOmenEffects, *, mml: int | None = None
) -> ResolvedOperationFilters:
    return ResolvedOperationFilters(
        side_filter=effects.add_side_filter,
        removal_side_filter=effects.removal_side_filter,
        mml=mml,
        whittling=effects.lowest_modifier_level,
        add_count=effects.add_count,
    )


__all__ = [
    "ACCEPTED_RUNTIME_STATUS",
    "M38A_RESOLVER_SCHEMA_VERSION",
    "M39A_RESOLVER_SCHEMA_VERSION",
    "M39B_RESOLVER_SCHEMA_VERSION",
    "M40A_RESOLVER_SCHEMA_VERSION",
    "M41A_RESOLVER_SCHEMA_VERSION",
    "M42A_RESOLVER_SCHEMA_VERSION",
    "M44A_RESOLVER_SCHEMA_VERSION",
    "M45A_RESOLVER_SCHEMA_VERSION",
    "M46A_RESOLVER_SCHEMA_VERSION",
    "M38AResolverAdmissionError",
    "M38AResolverError",
    "OperationResolver",
    "OperationResolverRequest",
    "ResolvedOperationFilters",
    "ResolvedOperationPlan",
]
