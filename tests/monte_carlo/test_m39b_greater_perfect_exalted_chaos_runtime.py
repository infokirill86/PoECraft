from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from pathlib import Path

import pytest

from p2c_engine.domain.enums import Rarity, Side
from p2c_engine.domain.item_state import ItemState, ModifierInstance
from p2c_engine.domain.pool_building import PoolBuildResult
from p2c_engine.domain.static_modifier import StaticModifier
from p2c_engine.legality.pool_builders import (
    OrdinaryAddPoolRequest,
    build_ordinary_add_pool,
)
from p2c_engine.monte_carlo.chaos_like import (
    ChaosLikeMonteCarloHarness,
    ChaosLikeOperation,
)
from p2c_engine.monte_carlo.ordinary_add import (
    OrdinaryAddMonteCarloHarness,
    OrdinaryAddOperation,
)
from p2c_engine.monte_carlo.rarity_progression import M40A_OPERATION_IDS
from p2c_engine.operations.resolver import (
    M39B_RESOLVER_SCHEMA_VERSION,
    M38AResolverAdmissionError,
    OperationResolver,
    OperationResolverRequest,
)
from p2c_engine.static_data import build_static_game_data
from p2c_engine.static_data.game_data import StaticGameData


ROOT = Path(__file__).resolve().parents[2]
MAX_EXACT_PATHS = 256


def _mod(
    mod_id: str,
    *,
    family: str,
    side: Side,
    level: int,
    weight: int = 1,
) -> StaticModifier:
    return StaticModifier(
        mod_id=mod_id,
        family_id=family,
        side=side,
        group_ids=(family,),
        tier=1,
        modifier_level=level,
        tags=(),
        generation_weight=weight,
        static_category="ordinary",
    )


def _chaos_transition(mml: int | None) -> dict[str, object]:
    return {
        "atomic": True,
        "remove": {
            "kind": "uniform_installed_instance",
            "count": 1,
            "exclude_flags": ["fractured"],
        },
        "add": {"kind": "ordinary_weighted", "count": 1, "mml": mml},
    }


def _operations() -> dict[str, object]:
    rows: list[dict[str, object]] = []
    for operation_id, mml in (
        ("greater_exalted", 35),
        ("perfect_exalted", 50),
    ):
        rows.append(
            {
                "operation_id": operation_id,
                "group": "exalted",
                "input_rarity": ["rare"],
                "active_in_current_simulation": True,
                "runtime_admission_status": "accepted_executable_runtime",
                "transition": {
                    "atomic": True,
                    "remove": {"kind": "none"},
                    "add": {"kind": "ordinary_weighted", "count": 1, "mml": mml},
                },
            }
        )
    rows.extend(
        {
            "operation_id": operation_id,
            "group": "chaos",
            "input_rarity": ["rare"],
            "active_in_current_simulation": True,
            "runtime_admission_status": "accepted_executable_runtime",
            "transition": _chaos_transition(mml),
        }
        for operation_id, mml in (
            ("chaos", None),
            ("greater_chaos", 35),
            ("perfect_chaos", 50),
        )
    )
    rows.extend(
        {
            "operation_id": operation_id,
            "group": group,
            "input_rarity": ["rare"],
            "active_in_current_simulation": True,
            "runtime_admission_status": "admission_candidate",
            "transition": {
                "atomic": True,
                "remove": {"kind": "none"},
                "add": {"kind": "ordinary_weighted", "count": 1, "mml": mml},
            },
        }
        for operation_id, group, mml in (
            ("exalted", "exalted", None),
            ("greater_transmutation", "transmutation", 44),
            ("greater_augmentation", "augmentation", 44),
            ("greater_regal", "regal", 35),
            ("greater_essence_abrasion", "essence", None),
        )
    )
    return {"operations": rows}


def _static() -> StaticGameData:
    mods = (
        _mod(
            "fixed_fractured_crit_suffix",
            family="fixed_crit_suffix",
            side=Side.SUFFIX,
            level=1,
        ),
        _mod("installed_alpha_prefix", family="installed_alpha", side=Side.PREFIX, level=1),
        _mod("installed_beta_suffix", family="installed_beta", side=Side.SUFFIX, level=1),
        _mod("physical_high_t1", family="physical", side=Side.PREFIX, level=70, weight=20),
        _mod("physical_mid_t2", family="physical", side=Side.PREFIX, level=40, weight=10),
        _mod("fallback_low_t1", family="fallback", side=Side.SUFFIX, level=20, weight=30),
    )
    return StaticGameData(
        modifier_index={mod.mod_id: mod for mod in mods},
        operations=_operations(),
        omens={},
        family_registry={},
        initial_states={},
        project_scope={"active_item_class": "quarterstaff"},
        success_criteria={},
        failure_policy={},
        item_state_schema={},
        static_modifier_schema={},
        source_fingerprint="m39b_fixture_source",
        semantic_fingerprint="m39b_fixture_semantic",
        root=None,  # type: ignore[arg-type]
    )


def _state(*mods: ModifierInstance, rarity: Rarity = Rarity.RARE) -> ItemState:
    return ItemState(
        item_class="quarterstaff",
        rarity=rarity,
        item_level=82,
        modifiers=mods,
        unrevealed_desecrated=None,
        augment_socket_capacity=0,
        augment_socket_used=0,
        astrid_installed=False,
    )


def _fractured() -> ModifierInstance:
    return ModifierInstance("fixed_fractured_crit_suffix", fractured=True)


def _resolve(static: StaticGameData, currency_id: str, state: ItemState):
    return OperationResolver(static=static).resolve(
        OperationResolverRequest(
            currency_id=currency_id,
            item_state=state,
            mode_id=f"m39b_{currency_id}",
        )
    )


def _mass(row: object) -> Fraction:
    return Fraction(row.probability_numerator, row.probability_denominator)  # type: ignore[attr-defined]


def test_m39b_rows_remain_admitted_with_later_m40a_surface() -> None:
    static = build_static_game_data(ROOT)
    rows = {row["operation_id"]: row for row in static.operations["operations"]}

    assert {
        operation_id
        for operation_id, row in rows.items()
        if row["runtime_admission_status"] == "accepted_executable_runtime"
    } == M40A_OPERATION_IDS | {
        "annulment",
        "chaos",
        "greater_exalted",
        "perfect_exalted",
        "greater_chaos",
        "perfect_chaos",
    }
    assert rows["exalted"]["runtime_admission_status"] == "accepted_executable_runtime"


def test_m39b_resolver_compiles_four_catalog_rows_with_row_declared_mml() -> None:
    static = _static()
    state = _state(_fractured())

    for currency_id, expected_mml, operation_type in (
        ("greater_exalted", 35, OrdinaryAddOperation),
        ("perfect_exalted", 50, OrdinaryAddOperation),
        ("greater_chaos", 35, ChaosLikeOperation),
        ("perfect_chaos", 50, ChaosLikeOperation),
    ):
        plan = _resolve(static, currency_id, state)
        assert plan.schema_version == M39B_RESOLVER_SCHEMA_VERSION
        assert plan.currency_id == currency_id
        assert plan.operation_kind == "catalog_operation"
        assert plan.runtime_admission_status == "accepted_executable_runtime"
        assert plan.filters.mml == expected_mml
        assert isinstance(plan.operation, operation_type)
        assert plan.operation.mml == expected_mml


def test_m39b_exalted_variants_share_ordinary_add_and_apply_different_mml_pools() -> None:
    static = _static()
    state = _state(_fractured())
    harness = OrdinaryAddMonteCarloHarness(static=static)

    greater = _resolve(static, "greater_exalted", state)
    perfect = _resolve(static, "perfect_exalted", state)
    greater_pool = harness.build_pool(state, greater.operation)  # type: ignore[arg-type]
    perfect_pool = harness.build_pool(state, perfect.operation)  # type: ignore[arg-type]
    greater_keys = {candidate.key for candidate in greater_pool.candidates}
    perfect_keys = {candidate.key for candidate in perfect_pool.candidates}

    assert greater.operation.operation_id == "ordinary_add"  # type: ignore[union-attr]
    assert perfect.operation.operation_id == "ordinary_add"  # type: ignore[union-attr]
    assert "physical_high_t1" in greater_keys & perfect_keys
    assert "physical_mid_t2" in greater_keys
    assert "physical_mid_t2" not in perfect_keys


def test_m39b_chaos_variants_rebuild_branch_pool_then_apply_declared_mml() -> None:
    static = _static()
    state = _state(
        _fractured(),
        ModifierInstance("installed_alpha_prefix"),
        ModifierInstance("installed_beta_suffix"),
    )

    for currency_id, expected_mml in (("greater_chaos", 35), ("perfect_chaos", 50)):
        observed: list[tuple[int | None, tuple[str, ...]]] = []

        def spy_builder(
            request: OrdinaryAddPoolRequest,
            game_data: StaticGameData,
        ) -> PoolBuildResult:
            observed.append(
                (request.mml, tuple(mod.mod_id for mod in request.state.modifiers))
            )
            return build_ordinary_add_pool(request, game_data)

        operation = _resolve(static, currency_id, state).operation
        harness = ChaosLikeMonteCarloHarness(
            static=static,
            ordinary_add_pool_builder=spy_builder,
        )
        paths = harness.enumerate_paths(
            initial_state=state,
            operation=operation,  # type: ignore[arg-type]
            decision_id_prefix=f"m39b.{currency_id}",
            max_exact_paths=MAX_EXACT_PATHS,
        )

        assert paths
        assert observed
        assert {mml for mml, _ in observed} == {expected_mml}
        assert all(len(mod_ids) == 2 for _, mod_ids in observed)
        assert all(
            not {
                "installed_alpha_prefix",
                "installed_beta_suffix",
            }.issubset(mod_ids)
            for _, mod_ids in observed
        )


def test_m39b_chaos_mml_does_not_change_base_removal_distribution_or_fracture_guard() -> None:
    static = _static()
    state = _state(
        _fractured(),
        ModifierInstance("installed_alpha_prefix"),
        ModifierInstance("installed_beta_suffix"),
    )
    removal_marginals: dict[str, dict[str, Fraction]] = {}

    for currency_id in ("chaos", "greater_chaos", "perfect_chaos"):
        operation = _resolve(static, currency_id, state).operation
        paths = ChaosLikeMonteCarloHarness(static=static).enumerate_paths(
            initial_state=state,
            operation=operation,  # type: ignore[arg-type]
            decision_id_prefix=f"m39b.removal.{currency_id}",
            max_exact_paths=MAX_EXACT_PATHS,
        )
        grouped: defaultdict[str, Fraction] = defaultdict(Fraction)
        for path in paths:
            removed = path.steps[0].selected_mod_id
            assert removed is not None
            assert removed != "fixed_fractured_crit_suffix"
            grouped[removed] += _mass(path)
        removal_marginals[currency_id] = dict(grouped)

    assert removal_marginals["greater_chaos"] == removal_marginals["chaos"]
    assert removal_marginals["perfect_chaos"] == removal_marginals["chaos"]


def test_m39b_chaos_empty_add_pool_is_atomic_and_aggregates_duplicate_terminal() -> None:
    static = _static()
    state = _state(
        _fractured(),
        ModifierInstance("installed_alpha_prefix"),
        ModifierInstance("installed_beta_suffix"),
    )

    def empty_add_builder(
        request: OrdinaryAddPoolRequest,
        game_data: StaticGameData,
    ) -> PoolBuildResult:
        return PoolBuildResult(
            candidates=(),
            candidate_digest=None,
            result_fingerprint="m39b_empty_add_pool",
            stages=(),
            empty_reason="ordinary_add_pool_exhausted",
        )

    operation = _resolve(static, "perfect_chaos", state).operation
    harness = ChaosLikeMonteCarloHarness(
        static=static,
        ordinary_add_pool_builder=empty_add_builder,
    )
    paths = harness.enumerate_paths(
        initial_state=state,
        operation=operation,  # type: ignore[arg-type]
        decision_id_prefix="m39b.atomic_empty_add",
        max_exact_paths=MAX_EXACT_PATHS,
    )
    terminals = harness.enumerate_terminal_distribution(
        initial_state=state,
        operation=operation,  # type: ignore[arg-type]
        decision_id_prefix="m39b.atomic_empty_add.terminals",
        max_exact_paths=MAX_EXACT_PATHS,
    )

    assert paths
    assert {path.outcome for path in paths} == {"no_transition_no_consumption"}
    assert {path.terminal_state_hash for path in paths} == {state.state_hash()}
    assert len(terminals) == 1
    assert terminals[0].terminal_state_hash == state.state_hash()
    assert terminals[0].path_count == len(paths)
    assert _mass(terminals[0]) == Fraction(1, 1)


def test_m39b_non_admitted_families_manual_mml_and_modifiers_remain_fail_closed() -> None:
    static = _static()
    state = _state(_fractured())
    resolver = OperationResolver(static=static)

    for currency_id in (
        "exalted",
        "greater_transmutation",
        "greater_augmentation",
        "greater_regal",
        "greater_essence_abrasion",
    ):
        with pytest.raises(M38AResolverAdmissionError, match="not executable-admitted"):
            resolver.resolve(OperationResolverRequest(currency_id=currency_id, item_state=state))

    with pytest.raises(M38AResolverAdmissionError, match="fixed by its admitted operation row"):
        resolver.resolve(
            OperationResolverRequest(
                currency_id="greater_chaos",
                item_state=state,
                mml=50,
            )
        )
    with pytest.raises(M38AResolverAdmissionError, match="modifier layers"):
        resolver.resolve(
            OperationResolverRequest(
                currency_id="perfect_chaos",
                item_state=state,
                active_modifier_ids=("whittling",),
            )
        )


def test_m39b_exalted_variants_fail_closed_outside_rare_items() -> None:
    static = _static()
    with pytest.raises(M38AResolverAdmissionError, match="does not accept the current item rarity"):
        _resolve(static, "greater_exalted", _state(rarity=Rarity.MAGIC))


def test_m39b_admitted_variant_with_unexpected_transition_shape_fails_closed() -> None:
    static = _static()
    row = next(
        row
        for row in static.operations["operations"]
        if row["operation_id"] == "greater_exalted"
    )
    row["transition"]["add"]["count"] = 2

    with pytest.raises(M38AResolverAdmissionError, match="unsupported M39-B Exalted"):
        _resolve(static, "greater_exalted", _state(_fractured()))
