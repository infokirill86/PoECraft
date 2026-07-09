from __future__ import annotations

import pytest

from p2c_engine.domain.enums import Rarity, Side
from p2c_engine.domain.item_state import ItemState
from p2c_engine.domain.static_modifier import StaticModifier
from p2c_engine.legality.pool_builders import OrdinaryAddPoolRequest, build_ordinary_add_pool
from p2c_engine.monte_carlo.annulment import AnnulmentOperation
from p2c_engine.monte_carlo.chaos_like import ChaosLikeOperation
from p2c_engine.monte_carlo.ordinary_add import OrdinaryAddOperation
from p2c_engine.operations.resolver import (
    M38A_RESOLVER_SCHEMA_VERSION,
    M39A_RESOLVER_SCHEMA_VERSION,
    M38AResolverAdmissionError,
    OperationResolver,
    OperationResolverRequest,
)
from p2c_engine.static_data.game_data import StaticGameData


def _state() -> ItemState:
    return ItemState(
        item_class="quarterstaff",
        rarity=Rarity.RARE,
        item_level=82,
        modifiers=(),
        unrevealed_desecrated=None,
        augment_socket_capacity=0,
        augment_socket_used=0,
        astrid_installed=False,
    )


def _operations(
    *,
    annulment_status: str = "accepted_executable_runtime",
    chaos_status: str = "accepted_executable_runtime",
) -> dict[str, object]:
    return {
        "operations": [
            {
                "operation_id": "annulment",
                "group": "annulment",
                "active_in_current_simulation": True,
                "runtime_admission_status": annulment_status,
            },
            {
                "operation_id": "chaos",
                "group": "chaos",
                "active_in_current_simulation": True,
                "runtime_admission_status": chaos_status,
            },
            {
                "operation_id": "greater_chaos",
                "group": "chaos",
                "active_in_current_simulation": True,
                "runtime_admission_status": "admission_candidate",
            },
            {
                "operation_id": "perfect_chaos",
                "group": "chaos",
                "active_in_current_simulation": True,
                "runtime_admission_status": "admission_candidate",
            },
            {
                "operation_id": "exalted",
                "group": "exalted",
                "active_in_current_simulation": True,
                "runtime_admission_status": "admission_candidate",
            },
        ]
    }


def _static(**operation_statuses: str) -> StaticGameData:
    return StaticGameData(
        modifier_index={},
        operations=_operations(**operation_statuses),
        omens={
            "omens": [
                {"omen_id": "whittling", "operation_groups": ["chaos"]},
                {"omen_id": "sinistral_erasure", "operation_groups": ["chaos"]},
                {"omen_id": "sinistral_annulment", "operation_groups": ["annulment"]},
            ]
        },
        family_registry={},
        initial_states={},
        project_scope={"active_item_class": "quarterstaff"},
        success_criteria={},
        failure_policy={},
        item_state_schema={},
        static_modifier_schema={},
        source_fingerprint="m38a_fixture_source",
        semantic_fingerprint="m38a_fixture_semantic",
        root=None,  # type: ignore[arg-type]
    )


def _mod(
    mod_id: str,
    family_id: str,
    side: Side,
    *,
    tier: int,
    level: int,
    weight: int,
) -> StaticModifier:
    return StaticModifier(
        mod_id=mod_id,
        family_id=family_id,
        side=side,
        group_ids=(family_id,),
        tier=tier,
        modifier_level=level,
        tags=(),
        generation_weight=weight,
        static_category="ordinary",
    )


def _static_with_mml_candidates() -> StaticGameData:
    static = _static()
    rows = (
        _mod("prefix_high_t1", "prefix_family", Side.PREFIX, tier=1, level=70, weight=20),
        _mod("prefix_low_t2", "prefix_family", Side.PREFIX, tier=2, level=10, weight=10),
        _mod("suffix_low_t3", "suffix_family", Side.SUFFIX, tier=3, level=10, weight=30),
        _mod("suffix_mid_t2", "suffix_family", Side.SUFFIX, tier=2, level=20, weight=40),
    )
    return StaticGameData(
        modifier_index={row.mod_id: row for row in rows},
        operations=static.operations,
        omens=static.omens,
        family_registry=static.family_registry,
        initial_states=static.initial_states,
        project_scope=static.project_scope,
        success_criteria=static.success_criteria,
        failure_policy=static.failure_policy,
        item_state_schema=static.item_state_schema,
        static_modifier_schema=static.static_modifier_schema,
        source_fingerprint=static.source_fingerprint,
        semantic_fingerprint=static.semantic_fingerprint,
        root=static.root,
    )


def _resolve(currency_id: str, **kwargs: object):
    return OperationResolver(static=_static()).resolve(
        OperationResolverRequest(currency_id=currency_id, item_state=_state(), **kwargs)
    )


def test_m38a_schema_and_single_operation_contract_are_pinned() -> None:
    plan = _resolve("ordinary_add", mode_id="m38a_ordinary_add")

    assert M38A_RESOLVER_SCHEMA_VERSION == "p2c.m38a.operation_resolver_skeleton.v1"
    assert M39A_RESOLVER_SCHEMA_VERSION == "p2c.m39a.operation_resolver_mml_filter_interface.v1"
    assert plan.schema_version == M39A_RESOLVER_SCHEMA_VERSION
    assert plan.plan_kind == "single_operation"
    assert isinstance(plan.operation, OrdinaryAddOperation)
    assert plan.operation.operation_id == "ordinary_add"
    assert plan.operation.item_class == "quarterstaff"
    assert plan.operation_kind == "engine_primitive"
    assert plan.runtime_admission_status == "accepted_executable_runtime"
    assert plan.filters.side_filter is None
    assert plan.filters.mml is None
    assert plan.filters.whittling is False
    assert plan.filters.desecrated_only is False


def test_m39a_explicit_mml_filter_compiles_to_ordinary_add_and_narrows_pool() -> None:
    static = _static_with_mml_candidates()
    resolver = OperationResolver(static=static)

    plan = resolver.resolve(
        OperationResolverRequest(currency_id="ordinary_add", item_state=_state(), mml=50)
    )

    assert isinstance(plan.operation, OrdinaryAddOperation)
    assert plan.operation.mml == 50
    assert plan.filters.mml == 50
    assert plan.public_summary()["filter_mml"] == 50

    unfiltered = build_ordinary_add_pool(
        OrdinaryAddPoolRequest("quarterstaff", _state(), mml=None),
        static,
    )
    filtered = build_ordinary_add_pool(
        OrdinaryAddPoolRequest("quarterstaff", _state(), mml=plan.operation.mml),
        static,
    )

    assert tuple(candidate.key for candidate in unfiltered.candidates) == (
        "prefix_high_t1",
        "prefix_low_t2",
        "suffix_low_t3",
        "suffix_mid_t2",
    )
    assert tuple(candidate.key for candidate in filtered.candidates) == (
        "prefix_high_t1",
        "suffix_mid_t2",
    )
    assert tuple(fallback.family_id for fallback in filtered.mml_fallbacks) == ("suffix_family",)


def test_m38a_resolves_only_already_accepted_catalog_runtime_operations() -> None:
    annulment = _resolve("annulment", mode_id="m38a_annulment")
    chaos = _resolve("chaos", mode_id="m38a_chaos")

    assert isinstance(annulment.operation, AnnulmentOperation)
    assert annulment.operation.operation_id == "annulment"
    assert annulment.operation_kind == "catalog_operation"
    assert isinstance(chaos.operation, ChaosLikeOperation)
    assert chaos.operation.operation_id == "chaos"
    assert chaos.operation_kind == "catalog_operation"


def test_m38a_does_not_infer_runtime_permission_from_active_catalog_flag() -> None:
    resolver = OperationResolver(static=_static())

    with pytest.raises(M38AResolverAdmissionError, match="not executable-admitted"):
        resolver.resolve(OperationResolverRequest(currency_id="exalted", item_state=_state()))

    with pytest.raises(M38AResolverAdmissionError, match="not executable-admitted"):
        resolver.resolve(
            OperationResolverRequest(currency_id="greater_chaos", item_state=_state())
        )

    with pytest.raises(M38AResolverAdmissionError, match="not executable-admitted"):
        resolver.resolve(
            OperationResolverRequest(currency_id="greater_chaos", item_state=_state(), mml=35)
        )


def test_m38a_rejects_greater_perfect_variant_layers_for_admitted_base_currency() -> None:
    resolver = OperationResolver(static=_static())

    with pytest.raises(M38AResolverAdmissionError, match="variants are not executable-admitted"):
        resolver.resolve(
            OperationResolverRequest(
                currency_id="chaos",
                item_state=_state(),
                variant_id="greater",
            )
        )

    with pytest.raises(M38AResolverAdmissionError, match="variants are not executable-admitted"):
        resolver.resolve(
            OperationResolverRequest(
                currency_id="annulment",
                item_state=_state(),
                variant_id="perfect",
            )
        )


def test_m39a_mml_filter_does_not_admit_catalog_or_greater_perfect_runtime() -> None:
    resolver = OperationResolver(static=_static())

    with pytest.raises(M38AResolverAdmissionError, match="MML filters are executable-admitted"):
        resolver.resolve(OperationResolverRequest(currency_id="chaos", item_state=_state(), mml=35))

    with pytest.raises(M38AResolverAdmissionError, match="variants are not executable-admitted"):
        resolver.resolve(
            OperationResolverRequest(
                currency_id="chaos",
                item_state=_state(),
                variant_id="greater",
                mml=35,
            )
        )


def test_m39a_mml_filter_fails_closed_on_invalid_thresholds() -> None:
    resolver = OperationResolver(static=_static())

    for value in (0, -1, True, "35"):
        with pytest.raises(M38AResolverAdmissionError, match="MML filter"):
            resolver.resolve(
                OperationResolverRequest(
                    currency_id="ordinary_add",
                    item_state=_state(),
                    mml=value,  # type: ignore[arg-type]
                )
            )


def test_m38a_rejects_omen_and_modifier_layers_without_admitting_filter_runtime() -> None:
    resolver = OperationResolver(static=_static())

    for modifier_id in ("whittling", "sinistral_erasure", "sinistral_annulment"):
        with pytest.raises(
            M38AResolverAdmissionError,
            match="modifier layers are not executable-admitted",
        ):
            resolver.resolve(
                OperationResolverRequest(
                    currency_id="chaos",
                    item_state=_state(),
                    active_modifier_ids=(modifier_id,),
                )
            )


def test_m38a_fail_closed_when_catalog_runtime_status_is_revoked() -> None:
    resolver = OperationResolver(static=_static(chaos_status="admission_candidate"))

    with pytest.raises(M38AResolverAdmissionError, match="not executable-admitted"):
        resolver.resolve(OperationResolverRequest(currency_id="chaos", item_state=_state()))


def test_m38a_rejects_unknown_currency_or_operation() -> None:
    resolver = OperationResolver(static=_static())

    with pytest.raises(M38AResolverAdmissionError, match="unknown operation/currency"):
        resolver.resolve(
            OperationResolverRequest(currency_id="mirror_of_kalandra", item_state=_state())
        )


def test_m38a_public_summary_is_metadata_only() -> None:
    summary = _resolve("chaos", mode_id="m38a_summary").public_summary()

    assert summary == {
        "schema_version": "p2c.m39a.operation_resolver_mml_filter_interface.v1",
        "plan_kind": "single_operation",
        "currency_id": "chaos",
        "operation_id": "chaos",
        "operation_kind": "catalog_operation",
        "runtime_admission_status": "accepted_executable_runtime",
        "variant_id": None,
        "active_modifier_count": 0,
        "filter_side": None,
        "filter_mml": None,
        "filter_whittling": False,
        "filter_desecrated_only": False,
    }
