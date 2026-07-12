from __future__ import annotations

from dataclasses import replace
from fractions import Fraction
from pathlib import Path

import pytest

from p2c_engine.domain.enums import Rarity, Side
from p2c_engine.domain.item_state import ItemState, ModifierInstance
from p2c_engine.domain.pool_building import PoolBuildResult
from p2c_engine.domain.static_modifier import StaticModifier
from p2c_engine.legality.pool_builders import (
    OrdinaryAddPoolRequest,
    RemovalPoolRequest,
    build_ordinary_add_pool,
    build_removal_pool,
)
from p2c_engine.monte_carlo.rarity_progression import (
    M40A_OPERATION_IDS,
    CatalogSingleAddHarness,
    CatalogSingleAddOperation,
    M40ARarityProgressionInvariantViolation,
)
from p2c_engine.monte_carlo.greater_essence import M41A_OPERATION_IDS
from p2c_engine.monte_carlo.perfect_essence import M42A_OPERATION_IDS
from p2c_engine.operations.resolver import (
    M40A_RESOLVER_SCHEMA_VERSION,
    M38AResolverAdmissionError,
    OperationResolver,
    OperationResolverRequest,
)
from p2c_engine.static_data import build_static_game_data
from p2c_engine.static_data.game_data import StaticGameData


ROOT = Path(__file__).resolve().parents[2]


def _mod(
    mod_id: str,
    *,
    family: str,
    side: Side,
    level: int,
    tier: int,
    weight: int,
    category: str = "ordinary",
) -> StaticModifier:
    return StaticModifier(
        mod_id=mod_id,
        family_id=family,
        side=side,
        group_ids=(family,),
        tier=tier,
        modifier_level=level,
        tags=(),
        generation_weight=weight,
        static_category=category,
    )


def _single_add_row(
    operation_id: str,
    group: str,
    source: str,
    output: str,
    mml: int | None,
    *,
    pool_build_rarity: str | None = None,
) -> dict[str, object]:
    transition: dict[str, object] = {
        "atomic": True,
        "output_rarity": output,
        "remove": {"kind": "none"},
        "add": {
            "kind": "ordinary_weighted",
            "count": 1,
            "side_filter": None,
            "mml": mml,
        },
    }
    if pool_build_rarity is not None:
        transition["pool_build_rarity"] = pool_build_rarity
    if group == "augmentation":
        transition["preconditions"] = [
            {"type": "occupied_explicit_slots", "operator": "<", "value": 2}
        ]
    if operation_id == "exalted":
        transition["preconditions"] = [
            {
                "type": "free_explicit_slots_after_side_filter",
                "operator": ">=",
                "value": "resolved_add_count",
            }
        ]
    return {
        "operation_id": operation_id,
        "group": group,
        "input_rarity": [source],
        "active_in_current_simulation": True,
        "runtime_admission_status": "accepted_executable_runtime",
        "transition": transition,
    }


def _operations() -> dict[str, object]:
    return {
        "operations": [
            _single_add_row("transmutation", "transmutation", "normal", "magic", None),
            _single_add_row(
                "greater_transmutation", "transmutation", "normal", "magic", 44
            ),
            _single_add_row(
                "perfect_transmutation", "transmutation", "normal", "magic", 70
            ),
            _single_add_row("augmentation", "augmentation", "magic", "magic", None),
            _single_add_row(
                "greater_augmentation", "augmentation", "magic", "magic", 44
            ),
            _single_add_row(
                "perfect_augmentation", "augmentation", "magic", "magic", 70
            ),
            _single_add_row(
                "regal", "regal", "magic", "rare", None, pool_build_rarity="rare"
            ),
            _single_add_row(
                "greater_regal", "regal", "magic", "rare", 35, pool_build_rarity="rare"
            ),
            _single_add_row(
                "perfect_regal", "regal", "magic", "rare", 50, pool_build_rarity="rare"
            ),
            _single_add_row("exalted", "exalted", "rare", "rare", None),
            {
                "operation_id": "alchemy",
                "group": "alchemy",
                "input_rarity": ["normal"],
                "active_in_current_simulation": False,
                "runtime_admission_status": "data_reference_candidate",
                "transition": {"atomic": True},
            },
        ]
    }


def _static() -> StaticGameData:
    mods = (
        _mod(
            "prefix_low_t4",
            family="prefix_power",
            side=Side.PREFIX,
            level=20,
            tier=4,
            weight=1,
        ),
        _mod(
            "prefix_mid_t3",
            family="prefix_power",
            side=Side.PREFIX,
            level=40,
            tier=3,
            weight=2,
        ),
        _mod(
            "prefix_high_t2",
            family="prefix_power",
            side=Side.PREFIX,
            level=60,
            tier=2,
            weight=3,
        ),
        _mod(
            "prefix_top_t1",
            family="prefix_power",
            side=Side.PREFIX,
            level=80,
            tier=1,
            weight=5,
        ),
        _mod(
            "suffix_low_t4",
            family="suffix_speed",
            side=Side.SUFFIX,
            level=20,
            tier=4,
            weight=7,
        ),
        _mod(
            "suffix_mid_t3",
            family="suffix_speed",
            side=Side.SUFFIX,
            level=40,
            tier=3,
            weight=11,
        ),
        _mod(
            "suffix_high_t2",
            family="suffix_speed",
            side=Side.SUFFIX,
            level=60,
            tier=2,
            weight=13,
        ),
        _mod(
            "suffix_top_t1",
            family="suffix_speed",
            side=Side.SUFFIX,
            level=80,
            tier=1,
            weight=17,
        ),
        _mod(
            "installed_prefix",
            family="installed_prefix_family",
            side=Side.PREFIX,
            level=1,
            tier=1,
            weight=1,
            category="fixture_installed",
        ),
        _mod(
            "installed_suffix",
            family="installed_suffix_family",
            side=Side.SUFFIX,
            level=1,
            tier=1,
            weight=1,
            category="fixture_installed",
        ),
        _mod(
            "fractured_prefix",
            family="fractured_prefix_family",
            side=Side.PREFIX,
            level=1,
            tier=1,
            weight=1,
            category="fixture_installed",
        ),
        _mod(
            "fractured_crit_suffix",
            family="fractured_crit_family",
            side=Side.SUFFIX,
            level=1,
            tier=1,
            weight=1,
            category="fixture_installed",
        ),
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
        source_fingerprint="m40a_fixture_source",
        semantic_fingerprint="m40a_fixture_semantic",
        root=None,  # type: ignore[arg-type]
    )


def _state(rarity: Rarity, *mods: ModifierInstance) -> ItemState:
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


def _resolve(
    static: StaticGameData, operation_id: str, state: ItemState
) -> CatalogSingleAddOperation:
    plan = OperationResolver(static=static).resolve(
        OperationResolverRequest(
            currency_id=operation_id,
            item_state=state,
            mode_id=f"m40a_{operation_id}",
        )
    )
    assert plan.schema_version == M40A_RESOLVER_SCHEMA_VERSION
    assert isinstance(plan.operation, CatalogSingleAddOperation)
    return plan.operation


def _mass(row: object) -> Fraction:
    return Fraction(row.probability_numerator, row.probability_denominator)  # type: ignore[attr-defined]


def test_m40a_real_catalog_admits_exactly_the_authorized_rows_plus_prior_runtime() -> None:
    static = build_static_game_data(ROOT)
    admitted = {
        row["operation_id"]
        for row in static.operations["operations"]
        if row["runtime_admission_status"] == "accepted_executable_runtime"
    }
    assert admitted == M40A_OPERATION_IDS | M41A_OPERATION_IDS | M42A_OPERATION_IDS | {
        "greater_exalted",
        "perfect_exalted",
        "annulment",
        "chaos",
        "greater_chaos",
        "perfect_chaos",
        "alchemy",
        "fracturing_orb",
    }


@pytest.mark.parametrize(
    ("operation_id", "source", "pool_rarity", "output", "mml"),
    (
        ("transmutation", Rarity.NORMAL, Rarity.MAGIC, Rarity.MAGIC, None),
        ("greater_transmutation", Rarity.NORMAL, Rarity.MAGIC, Rarity.MAGIC, 44),
        ("perfect_transmutation", Rarity.NORMAL, Rarity.MAGIC, Rarity.MAGIC, 70),
        ("augmentation", Rarity.MAGIC, Rarity.MAGIC, Rarity.MAGIC, None),
        ("greater_augmentation", Rarity.MAGIC, Rarity.MAGIC, Rarity.MAGIC, 44),
        ("perfect_augmentation", Rarity.MAGIC, Rarity.MAGIC, Rarity.MAGIC, 70),
        ("regal", Rarity.MAGIC, Rarity.RARE, Rarity.RARE, None),
        ("greater_regal", Rarity.MAGIC, Rarity.RARE, Rarity.RARE, 35),
        ("perfect_regal", Rarity.MAGIC, Rarity.RARE, Rarity.RARE, 50),
        ("exalted", Rarity.RARE, Rarity.RARE, Rarity.RARE, None),
    ),
)
def test_m40a_resolver_compiles_all_ten_rows_from_data(
    operation_id: str,
    source: Rarity,
    pool_rarity: Rarity,
    output: Rarity,
    mml: int | None,
) -> None:
    operation = _resolve(_static(), operation_id, _state(source))
    assert operation.operation_id == operation_id
    assert operation.input_rarities == (source,)
    assert operation.pool_build_rarity == pool_rarity
    assert operation.output_rarity == output
    assert operation.mml == mml
    if operation_id.startswith(("augmentation", "greater_augmentation", "perfect_augmentation")):
        assert operation.preconditions[0].kind == "occupied_explicit_slots"
    elif operation_id == "exalted":
        assert operation.preconditions[0].kind == "free_explicit_slots_after_side_filter"
    else:
        assert operation.preconditions == ()


@pytest.mark.parametrize(
    ("operation_id", "source", "expected_pool_rarity"),
    (
        ("transmutation", Rarity.NORMAL, Rarity.MAGIC),
        ("regal", Rarity.MAGIC, Rarity.RARE),
    ),
)
def test_m40a_transition_families_build_target_rarity_pool_and_commit_atomically(
    operation_id: str, source: Rarity, expected_pool_rarity: Rarity
) -> None:
    static = _static()
    initial = _state(source)
    observed: list[Rarity] = []

    def spy(request: OrdinaryAddPoolRequest, game_data: StaticGameData) -> PoolBuildResult:
        observed.append(request.state.rarity)
        return build_ordinary_add_pool(request, game_data)

    operation = _resolve(static, operation_id, initial)
    paths = CatalogSingleAddHarness(static=static, pool_builder=spy).enumerate_paths(
        initial_state=initial,
        operation=operation,
        decision_id=f"m40a.{operation_id}.exact",
    )

    assert observed and set(observed) == {expected_pool_rarity}
    assert paths and all(path.outcome == "applied" for path in paths)
    for path in paths:
        expected = replace(initial, rarity=expected_pool_rarity).with_modifiers(
            (ModifierInstance(path.selected_mod_id),)  # type: ignore[arg-type]
        )
        assert path.terminal_state_hash == expected.state_hash()
    assert sum((_mass(path) for path in paths), Fraction()) == Fraction(1, 1)


@pytest.mark.parametrize(
    ("operation_id", "source"),
    (("transmutation", Rarity.NORMAL), ("regal", Rarity.MAGIC)),
)
def test_m40a_empty_target_pool_rolls_back_rarity_and_consumes_nothing(
    operation_id: str, source: Rarity
) -> None:
    static = _static()
    initial = _state(source)

    def empty_pool(
        request: OrdinaryAddPoolRequest, game_data: StaticGameData
    ) -> PoolBuildResult:
        return PoolBuildResult(
            candidates=(),
            candidate_digest=None,
            result_fingerprint="m40a_empty_pool",
            stages=(),
            empty_reason="ordinary_add_pool_exhausted",
        )

    operation = _resolve(static, operation_id, initial)
    harness = CatalogSingleAddHarness(static=static, pool_builder=empty_pool)
    paths = harness.enumerate_paths(
        initial_state=initial,
        operation=operation,
        decision_id=f"m40a.{operation_id}.empty",
    )
    run = harness.run(
        initial_state=initial,
        operation=operation,
        seed=4001,
        sample_count=2,
        run_id=f"m40a_{operation_id}_empty",
    )

    assert len(paths) == 1
    assert paths[0].outcome == "no_transition_no_consumption"
    assert paths[0].terminal_state_hash == initial.state_hash()
    assert _mass(paths[0]) == Fraction(1, 1)
    assert all(row.pre_state_hash == row.post_state_hash for row in run.trajectories)


def test_m40a_wrong_source_rarity_is_explicit_no_transition() -> None:
    static = _static()
    wrong_state = _state(Rarity.RARE)
    operation = _resolve(static, "transmutation", wrong_state)
    paths = CatalogSingleAddHarness(static=static).enumerate_paths(
        initial_state=wrong_state,
        operation=operation,
        decision_id="m40a.wrong_source",
    )

    assert len(paths) == 1
    assert paths[0].outcome == "no_transition_no_consumption"
    assert paths[0].no_transition_reason == "invalid_source_rarity"
    assert paths[0].terminal_state_hash == wrong_state.state_hash()


def test_m40a_augmentation_capacity_derives_opposite_side_and_supports_zero_mods() -> None:
    static = _static()
    harness = CatalogSingleAddHarness(static=static)

    empty_magic = _state(Rarity.MAGIC)
    base = _resolve(static, "augmentation", empty_magic)
    empty_sides = {
        static.modifier_index[row.key].side for row in harness.build_pool(empty_magic, base).candidates
    }
    assert empty_sides == {Side.PREFIX, Side.SUFFIX}

    prefix_state = _state(Rarity.MAGIC, ModifierInstance("installed_prefix"))
    prefix_pool = harness.build_pool(prefix_state, _resolve(static, "augmentation", prefix_state))
    assert prefix_pool.candidates
    assert {
        static.modifier_index[row.key].side for row in prefix_pool.candidates
    } == {Side.SUFFIX}

    suffix_state = _state(Rarity.MAGIC, ModifierInstance("installed_suffix"))
    suffix_pool = harness.build_pool(suffix_state, _resolve(static, "augmentation", suffix_state))
    assert suffix_pool.candidates
    assert {
        static.modifier_index[row.key].side for row in suffix_pool.candidates
    } == {Side.PREFIX}


def test_m40a_full_magic_augmentation_is_no_transition_no_consumption() -> None:
    static = _static()
    state = _state(
        Rarity.MAGIC,
        ModifierInstance("installed_prefix"),
        ModifierInstance("installed_suffix"),
    )
    paths = CatalogSingleAddHarness(static=static).enumerate_paths(
        initial_state=state,
        operation=_resolve(static, "augmentation", state),
        decision_id="m40a.augmentation.full",
    )
    assert len(paths) == 1
    assert paths[0].outcome == "no_transition_no_consumption"
    assert paths[0].terminal_state_hash == state.state_hash()


@pytest.mark.parametrize(
    ("operation_id", "source", "expected_keys"),
    (
        (
            "greater_transmutation",
            Rarity.NORMAL,
            {"prefix_high_t2", "prefix_top_t1", "suffix_high_t2", "suffix_top_t1"},
        ),
        (
            "perfect_transmutation",
            Rarity.NORMAL,
            {"prefix_top_t1", "suffix_top_t1"},
        ),
        (
            "greater_augmentation",
            Rarity.MAGIC,
            {"prefix_high_t2", "prefix_top_t1", "suffix_high_t2", "suffix_top_t1"},
        ),
        (
            "perfect_augmentation",
            Rarity.MAGIC,
            {"prefix_top_t1", "suffix_top_t1"},
        ),
        (
            "greater_regal",
            Rarity.MAGIC,
            {
                "prefix_mid_t3",
                "prefix_high_t2",
                "prefix_top_t1",
                "suffix_mid_t3",
                "suffix_high_t2",
                "suffix_top_t1",
            },
        ),
        (
            "perfect_regal",
            Rarity.MAGIC,
            {"prefix_high_t2", "prefix_top_t1", "suffix_high_t2", "suffix_top_t1"},
        ),
    ),
)
def test_m40a_row_declared_mml_filters_shared_pool(
    operation_id: str, source: Rarity, expected_keys: set[str]
) -> None:
    static = _static()
    state = _state(source)
    operation = _resolve(static, operation_id, state)
    pool = CatalogSingleAddHarness(static=static).build_pool(state, operation)
    assert {row.key for row in pool.candidates} == expected_keys


def test_m40a_base_exalted_uses_combined_weighted_pool_and_general_item_model() -> None:
    static = _static()
    state = _state(
        Rarity.RARE,
        ModifierInstance("fractured_prefix", fractured=True),
    )
    operation = _resolve(static, "exalted", state)
    harness = CatalogSingleAddHarness(static=static)
    pool = harness.build_pool(state, operation)
    sides = {static.modifier_index[row.key].side for row in pool.candidates}
    paths = harness.enumerate_paths(
        initial_state=state,
        operation=operation,
        decision_id="m40a.exalted.exact",
    )

    assert sides == {Side.PREFIX, Side.SUFFIX}
    assert {row.key: row.weight for row in pool.candidates} == {
        "prefix_low_t4": 1,
        "prefix_mid_t3": 2,
        "prefix_high_t2": 3,
        "prefix_top_t1": 5,
        "suffix_low_t4": 7,
        "suffix_mid_t3": 11,
        "suffix_high_t2": 13,
        "suffix_top_t1": 17,
    }
    assert paths
    total_weight = sum(row.weight for row in pool.candidates)
    expected_weights = {row.key: row.weight for row in pool.candidates}
    assert {
        path.selected_mod_id: _mass(path) for path in paths
    } == {
        key: Fraction(weight, total_weight) for key, weight in expected_weights.items()
    }
    assert all(
        replace(state, modifiers=state.modifiers + (ModifierInstance(path.selected_mod_id),)).state_hash()
        == path.terminal_state_hash
        for path in paths
    )


def test_m40a_fractured_prefix_is_capacity_state_and_remains_removal_protected() -> None:
    static = _static()
    state = _state(
        Rarity.RARE,
        ModifierInstance("fractured_prefix", fractured=True),
        ModifierInstance("installed_suffix"),
    )
    pool = build_removal_pool(RemovalPoolRequest("quarterstaff", state), static)
    removable_ids = {row.mod_id for row in pool.removal_metadata}
    assert removable_ids == {"installed_suffix"}


def test_m40a_catalog_threshold_is_compiled_from_row_not_runtime_branch() -> None:
    static = _static()
    row = next(
        row
        for row in static.operations["operations"]
        if row["operation_id"] == "greater_transmutation"
    )
    row["transition"]["add"]["mml"] = 45
    operation = _resolve(static, "greater_transmutation", _state(Rarity.NORMAL))
    assert operation.mml == 45


@pytest.mark.parametrize(
    ("operation_id", "source"),
    (
        ("transmutation", Rarity.NORMAL),
        ("augmentation", Rarity.MAGIC),
        ("regal", Rarity.MAGIC),
        ("exalted", Rarity.RARE),
    ),
)
def test_m40a_seeded_mc_replays_and_stays_within_exact_terminals(
    operation_id: str, source: Rarity
) -> None:
    static = _static()
    state = _state(source)
    operation = _resolve(static, operation_id, state)
    harness = CatalogSingleAddHarness(static=static)
    exact_hashes = {
        row.terminal_state_hash
        for row in harness.enumerate_terminal_distribution(
            initial_state=state,
            operation=operation,
            decision_id=f"m40a.{operation_id}.oracle",
        )
    }
    left = harness.run(
        initial_state=state,
        operation=operation,
        seed=4040,
        sample_count=64,
        run_id=f"m40a_{operation_id}_replay",
    )
    right = harness.run(
        initial_state=state,
        operation=operation,
        seed=4040,
        sample_count=64,
        run_id=f"m40a_{operation_id}_replay",
    )

    assert left == right
    assert {row.post_state_hash for row in left.trajectories} <= exact_hashes
    assert left.public_summary()["probability_values_printed"] is False


def test_m40a_negative_control_wrong_pool_rarity_fails_hard() -> None:
    static = _static()
    state = _state(Rarity.NORMAL)
    operation = replace(
        _resolve(static, "transmutation", state), pool_build_rarity=Rarity.NORMAL
    )
    with pytest.raises(
        M40ARarityProgressionInvariantViolation,
        match="does not match admitted catalog row",
    ):
        CatalogSingleAddHarness(static=static).enumerate_paths(
            initial_state=state,
            operation=operation,
            decision_id="m40a.negative.wrong_pool_rarity",
        )


def test_m40a_closed_operations_and_modifier_layers_remain_fail_closed() -> None:
    static = _static()
    resolver = OperationResolver(static=static)
    with pytest.raises(M38AResolverAdmissionError, match="not executable-admitted"):
        resolver.resolve(
            OperationResolverRequest(currency_id="alchemy", item_state=_state(Rarity.NORMAL))
        )
    with pytest.raises(M38AResolverAdmissionError, match="modifier layers"):
        resolver.resolve(
            OperationResolverRequest(
                currency_id="exalted",
                item_state=_state(Rarity.RARE),
                active_modifier_ids=("whittling",),
            )
        )
