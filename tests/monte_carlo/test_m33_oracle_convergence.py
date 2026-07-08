from __future__ import annotations

from collections import Counter
from collections.abc import Mapping

from p2c_engine.domain.candidate import BranchOption
from p2c_engine.domain.enums import Rarity, Side
from p2c_engine.domain.item_state import ItemState, ModifierInstance
from p2c_engine.domain.static_modifier import StaticModifier
from p2c_engine.monte_carlo.ordinary_add import (
    OrdinaryAddMonteCarloHarness,
    OrdinaryAddOperation,
)
from p2c_engine.static_data.game_data import StaticGameData


def _mod(
    mod_id: str,
    *,
    family: str,
    side: Side,
    weight: int,
    groups: tuple[str, ...] = (),
    level: int = 1,
) -> StaticModifier:
    return StaticModifier(
        mod_id=mod_id,
        family_id=family,
        side=side,
        group_ids=groups,
        tier=1,
        modifier_level=level,
        tags=(),
        generation_weight=weight,
        static_category="ordinary",
    )


def _static(mods: tuple[StaticModifier, ...]) -> StaticGameData:
    return StaticGameData(
        modifier_index={mod.mod_id: mod for mod in mods},
        operations={},
        omens={},
        family_registry={},
        initial_states={},
        project_scope={"active_item_class": "quarterstaff"},
        success_criteria={},
        failure_policy={},
        item_state_schema={},
        static_modifier_schema={},
        source_fingerprint="m33_fixture_source",
        semantic_fingerprint="m33_fixture_semantic",
        root=None,  # type: ignore[arg-type]
    )


def _state(*mods: ModifierInstance, item_level: int = 82) -> ItemState:
    return ItemState(
        item_class="quarterstaff",
        rarity=Rarity.RARE,
        item_level=item_level,
        modifiers=mods,
        unrevealed_desecrated=None,
        augment_socket_capacity=0,
        augment_socket_used=0,
        astrid_installed=False,
    )


def _base_fractured_suffix() -> StaticModifier:
    return _mod(
        "fixed_fractured_crit_suffix",
        family="fixed_crit_suffix",
        side=Side.SUFFIX,
        weight=1,
    )


def _base_state() -> ItemState:
    return _state(ModifierInstance("fixed_fractured_crit_suffix", fractured=True))


def _exact_by_key(options: tuple[BranchOption, ...]) -> Mapping[str, BranchOption]:
    return {option.selected_key: option for option in options}


def _observed_counts(
    *,
    harness: OrdinaryAddMonteCarloHarness,
    state: ItemState,
    operation: OrdinaryAddOperation,
    seed: int,
    sample_count: int,
    run_id: str,
) -> Counter[str]:
    result = harness.run(
        initial_state=state,
        operation=operation,
        seed=seed,
        sample_count=sample_count,
        run_id=run_id,
        operation_sequence_id="m33_single_ordinary_add_oracle_validation",
    )
    return Counter(row.selected_mod_id for row in result.trajectories)


def _assert_counts_within_exact_oracle_tolerance(
    *,
    observed: Counter[str],
    exact: Mapping[str, BranchOption],
    sample_count: int,
    absolute_count_tolerance: int,
) -> None:
    assert set(observed) == set(exact)
    assert sum(observed.values()) == sample_count
    for key, option in exact.items():
        deviation_scaled_to_denominator = abs(
            observed[key] * option.probability_denominator
            - sample_count * option.probability_numerator
        )
        assert (
            deviation_scaled_to_denominator
            <= absolute_count_tolerance * option.probability_denominator
        )


def test_m33_two_branch_seeded_mc_converges_to_exact_oracle_fixture() -> None:
    static = _static(
        (
            _base_fractured_suffix(),
            _mod("alpha_prefix", family="alpha", side=Side.PREFIX, weight=1),
            _mod("beta_prefix", family="beta", side=Side.PREFIX, weight=3),
        )
    )
    state = _base_state()
    harness = OrdinaryAddMonteCarloHarness(static=static)
    operation = OrdinaryAddOperation(mode_id="m33_two_branch_fixture", side_filter=Side.PREFIX)

    exact = _exact_by_key(
        harness.enumerate_outcomes(
            state=state,
            operation=operation,
            decision_id="m33.exact.two_branch",
        )
    )
    assert {key: option.weight for key, option in exact.items()} == {
        "alpha_prefix": 1,
        "beta_prefix": 3,
    }

    sample_count = 4096
    observed = _observed_counts(
        harness=harness,
        state=state,
        operation=operation,
        seed=33001,
        sample_count=sample_count,
        run_id="m33_mc_two_branch",
    )
    _assert_counts_within_exact_oracle_tolerance(
        observed=observed,
        exact=exact,
        sample_count=sample_count,
        absolute_count_tolerance=sample_count // 16,
    )


def test_m33_three_branch_seeded_mc_converges_to_exact_oracle_fixture() -> None:
    static = _static(
        (
            _base_fractured_suffix(),
            _mod("alpha_prefix", family="alpha", side=Side.PREFIX, weight=2),
            _mod("beta_prefix", family="beta", side=Side.PREFIX, weight=3),
            _mod("gamma_prefix", family="gamma", side=Side.PREFIX, weight=5),
        )
    )
    state = _base_state()
    harness = OrdinaryAddMonteCarloHarness(static=static)
    operation = OrdinaryAddOperation(mode_id="m33_three_branch_fixture", side_filter=Side.PREFIX)

    exact = _exact_by_key(
        harness.enumerate_outcomes(
            state=state,
            operation=operation,
            decision_id="m33.exact.three_branch",
        )
    )
    assert {key: option.weight for key, option in exact.items()} == {
        "alpha_prefix": 2,
        "beta_prefix": 3,
        "gamma_prefix": 5,
    }

    sample_count = 8192
    observed = _observed_counts(
        harness=harness,
        state=state,
        operation=operation,
        seed=33002,
        sample_count=sample_count,
        run_id="m33_mc_three_branch",
    )
    _assert_counts_within_exact_oracle_tolerance(
        observed=observed,
        exact=exact,
        sample_count=sample_count,
        absolute_count_tolerance=sample_count // 16,
    )


def test_m33_empty_oracle_pool_matches_seeded_mc_no_transition() -> None:
    static = _static((_base_fractured_suffix(),))
    state = _state(
        ModifierInstance("fixed_fractured_crit_suffix", fractured=True),
    )
    harness = OrdinaryAddMonteCarloHarness(static=static)
    operation = OrdinaryAddOperation(mode_id="m33_empty_fixture", side_filter=Side.PREFIX)

    exact_options = harness.enumerate_outcomes(
        state=state,
        operation=operation,
        decision_id="m33.exact.empty",
    )
    result = harness.run(
        initial_state=state,
        operation=operation,
        seed=33003,
        sample_count=8,
        run_id="m33_mc_empty",
        operation_sequence_id="m33_single_ordinary_add_oracle_validation",
    )

    assert exact_options == ()
    assert {row.outcome for row in result.trajectories} == {"no_transition"}
    assert {row.post_state_hash for row in result.trajectories} == {state.state_hash()}


def test_m33_oracle_and_mc_paths_share_same_pool_builder() -> None:
    static = _static(
        (
            _base_fractured_suffix(),
            _mod("alpha_prefix", family="alpha", side=Side.PREFIX, weight=1),
            _mod("beta_prefix", family="beta", side=Side.PREFIX, weight=1),
        )
    )
    state = _base_state()
    call_count = 0

    def spy_builder(request, game_data):  # type: ignore[no-untyped-def]
        nonlocal call_count
        call_count += 1
        from p2c_engine.legality.pool_builders import build_ordinary_add_pool

        return build_ordinary_add_pool(request, game_data)

    harness = OrdinaryAddMonteCarloHarness(static=static, pool_builder=spy_builder)
    operation = OrdinaryAddOperation(mode_id="m33_shared_builder_fixture", side_filter=Side.PREFIX)

    exact_options = harness.enumerate_outcomes(
        state=state,
        operation=operation,
        decision_id="m33.exact.shared_builder",
    )
    result = harness.run(
        initial_state=state,
        operation=operation,
        seed=33004,
        sample_count=4,
        run_id="m33_mc_shared_builder",
        operation_sequence_id="m33_single_ordinary_add_oracle_validation",
    )

    assert {option.selected_key for option in exact_options} == {"alpha_prefix", "beta_prefix"}
    assert {row.selected_mod_id for row in result.trajectories} <= {
        "alpha_prefix",
        "beta_prefix",
    }
    assert call_count == 1 + len(result.trajectories)
