from __future__ import annotations

from collections import Counter
from collections.abc import Mapping
from math import isqrt

from p2c_engine.domain.candidate import BranchOption
from p2c_engine.domain.enums import Rarity, Side
from p2c_engine.domain.item_state import ItemState, ModifierInstance
from p2c_engine.domain.static_modifier import StaticModifier
from p2c_engine.monte_carlo.ordinary_add import (
    OrdinaryAddMonteCarloHarness,
    OrdinaryAddOperation,
)
from p2c_engine.static_data.game_data import StaticGameData


SIGMA_MULTIPLIER = 6
SAMPLE_COUNT_TIERS = (1024, 4096, 16384)
LARGE_SAMPLE_COUNT = SAMPLE_COUNT_TIERS[-1]


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


def _ceil_sqrt(value: int) -> int:
    root = isqrt(value)
    return root if root * root == value else root + 1


def _scaled_sigma_tolerance(option: BranchOption, sample_count: int) -> int:
    numerator = option.probability_numerator
    denominator = option.probability_denominator
    variance_numerator = sample_count * numerator * (denominator - numerator)
    return SIGMA_MULTIPLIER * _ceil_sqrt(variance_numerator)


def _scaled_deviation(
    *, observed_count: int, option: BranchOption, sample_count: int
) -> int:
    return abs(
        observed_count * option.probability_denominator
        - sample_count * option.probability_numerator
    )


def _assert_counts_within_exact_oracle_tolerance(
    *,
    observed: Counter[str],
    exact: Mapping[str, BranchOption],
    sample_count: int,
) -> None:
    assert set(observed) <= set(exact)
    assert sum(observed.values()) == sample_count
    for key, option in exact.items():
        assert _scaled_deviation(
            observed_count=observed[key],
            option=option,
            sample_count=sample_count,
        ) <= _scaled_sigma_tolerance(option, sample_count)


def _max_scaled_proportion_error(
    *, observed: Counter[str], exact: Mapping[str, BranchOption], sample_count: int
) -> tuple[int, int]:
    """Return max empirical proportion error as numerator/denominator.

    The value is kept as integer numerator/denominator so the test does not use
    floating-point probability comparison or post-hoc eyeballing.
    """

    denominator = sample_count
    max_numerator = 0
    for key, option in exact.items():
        deviation = _scaled_deviation(
            observed_count=observed[key],
            option=option,
            sample_count=sample_count,
        )
        numerator = deviation
        branch_denominator = sample_count * option.probability_denominator
        if numerator * denominator > max_numerator * branch_denominator:
            max_numerator = numerator
            denominator = branch_denominator
    return max_numerator, denominator


def _assert_largest_tier_shrinks_roughly_with_sqrt_n(
    tier_errors: Mapping[int, tuple[int, int]],
) -> None:
    """Hard-fail if the largest tier does not show expected shrinkage direction.

    With a sixteenfold sample-count increase between the smallest and largest
    tiers, a square-root convergence model expects roughly fourfold tighter
    empirical proportion error. The test uses a conservative twofold requirement
    to avoid overfitting one deterministic seed while still making shrinkage a
    real assertion.
    """

    smallest = min(tier_errors)
    largest = max(tier_errors)
    small_num, small_den = tier_errors[smallest]
    large_num, large_den = tier_errors[largest]
    assert large_num * small_den * 2 <= small_num * large_den


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

    sample_count = LARGE_SAMPLE_COUNT
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

    sample_count = LARGE_SAMPLE_COUNT
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
    )


def test_m33_sample_count_tiers_show_sqrt_n_shrinkage_direction() -> None:
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
    operation = OrdinaryAddOperation(mode_id="m33_tier_fixture", side_filter=Side.PREFIX)
    exact = _exact_by_key(
        harness.enumerate_outcomes(
            state=state,
            operation=operation,
            decision_id="m33.exact.tiers",
        )
    )

    tier_errors: dict[int, tuple[int, int]] = {}
    for sample_count in SAMPLE_COUNT_TIERS:
        observed = _observed_counts(
            harness=harness,
            state=state,
            operation=operation,
            seed=33005,
            sample_count=sample_count,
            run_id="m33_mc_tiers",
        )
        _assert_counts_within_exact_oracle_tolerance(
            observed=observed,
            exact=exact,
            sample_count=sample_count,
        )
        tier_errors[sample_count] = _max_scaled_proportion_error(
            observed=observed,
            exact=exact,
            sample_count=sample_count,
        )

    _assert_largest_tier_shrinks_roughly_with_sqrt_n(tier_errors)


def test_m33_broad_skewed_fixture_converges_with_family_group_capacity_filters() -> None:
    static = _static(
        (
            _base_fractured_suffix(),
            _mod("installed_suffix_one", family="installed_suffix_one", side=Side.SUFFIX, weight=1),
            _mod("installed_suffix_two", family="installed_suffix_two", side=Side.SUFFIX, weight=1),
            _mod(
                "installed_prefix_blocker",
                family="installed_prefix_family",
                side=Side.PREFIX,
                weight=1,
                groups=("installed_group",),
            ),
            _mod("eligible_a", family="eligible_a", side=Side.PREFIX, weight=1),
            _mod("eligible_b", family="eligible_b", side=Side.PREFIX, weight=2),
            _mod("eligible_c", family="eligible_c", side=Side.PREFIX, weight=3),
            _mod("eligible_d", family="eligible_d", side=Side.PREFIX, weight=5),
            _mod("eligible_e", family="eligible_e", side=Side.PREFIX, weight=8),
            _mod("eligible_f", family="eligible_f", side=Side.PREFIX, weight=13),
            _mod("eligible_g", family="eligible_g", side=Side.PREFIX, weight=21),
            _mod("eligible_h", family="eligible_h", side=Side.PREFIX, weight=34),
            _mod(
                "blocked_by_family",
                family="installed_prefix_family",
                side=Side.PREFIX,
                weight=55,
            ),
            _mod(
                "blocked_by_group",
                family="blocked_group_family",
                side=Side.PREFIX,
                weight=89,
                groups=("installed_group",),
            ),
            _mod("blocked_by_suffix_capacity", family="suffix_candidate", side=Side.SUFFIX, weight=144),
        )
    )
    state = _state(
        ModifierInstance("fixed_fractured_crit_suffix", fractured=True),
        ModifierInstance("installed_suffix_one"),
        ModifierInstance("installed_suffix_two"),
        ModifierInstance("installed_prefix_blocker"),
    )
    harness = OrdinaryAddMonteCarloHarness(static=static)
    operation = OrdinaryAddOperation(mode_id="m33_broad_skewed_fixture")

    exact = _exact_by_key(
        harness.enumerate_outcomes(
            state=state,
            operation=operation,
            decision_id="m33.exact.broad_skewed",
        )
    )
    assert {key for key in exact} == {
        "eligible_a",
        "eligible_b",
        "eligible_c",
        "eligible_d",
        "eligible_e",
        "eligible_f",
        "eligible_g",
        "eligible_h",
    }

    observed = _observed_counts(
        harness=harness,
        state=state,
        operation=operation,
        seed=33006,
        sample_count=LARGE_SAMPLE_COUNT,
        run_id="m33_mc_broad_skewed",
    )
    _assert_counts_within_exact_oracle_tolerance(
        observed=observed,
        exact=exact,
        sample_count=LARGE_SAMPLE_COUNT,
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
