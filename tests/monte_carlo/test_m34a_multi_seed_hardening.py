from __future__ import annotations

from collections import Counter
from collections.abc import Mapping
from dataclasses import dataclass
from math import isqrt

import pytest

from p2c_engine.domain.candidate import BranchOption
from p2c_engine.domain.enums import Rarity, Side
from p2c_engine.domain.item_state import ItemState, ModifierInstance
from p2c_engine.domain.static_modifier import StaticModifier
from p2c_engine.monte_carlo.ordinary_add import (
    OrdinaryAddMonteCarloHarness,
    OrdinaryAddOperation,
)
from p2c_engine.static_data.game_data import StaticGameData


M34A_SEED_LIST = (34001, 34002, 34003)
M34A_SAMPLE_TIERS = (512, 2048, 8192)
M34A_SIGMA_MULTIPLIER = 6


@dataclass(frozen=True, slots=True)
class BranchBreachDiagnostic:
    fixture_id: str
    seed: int
    run_id: str
    sample_tier: int
    branch_key: str
    pool_digest: str
    deviation_scaled: int
    tolerance_scaled: int
    category: str = "m34a_multi_seed_tolerance_breach"

    def message(self) -> str:
        return (
            f"{self.category}: "
            f"fixture_id={self.fixture_id}; "
            f"seed={self.seed}; "
            f"run_id={self.run_id}; "
            f"sample_tier={self.sample_tier}; "
            f"branch_key={self.branch_key}; "
            f"pool_digest={self.pool_digest}; "
            f"deviation_scaled={self.deviation_scaled}; "
            f"tolerance_scaled={self.tolerance_scaled}"
        )


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
        source_fingerprint="m34a_fixture_source",
        semantic_fingerprint="m34a_fixture_semantic",
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


def _broad_skewed_fixture() -> tuple[StaticGameData, ItemState, OrdinaryAddOperation]:
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
    operation = OrdinaryAddOperation(mode_id="m34a_broad_skewed_fixture")
    return static, state, operation


def _exact_by_key(options: tuple[BranchOption, ...]) -> Mapping[str, BranchOption]:
    return {option.selected_key: option for option in options}


def _ceil_sqrt(value: int) -> int:
    root = isqrt(value)
    return root if root * root == value else root + 1


def _scaled_sigma_tolerance(option: BranchOption, sample_count: int) -> int:
    numerator = option.probability_numerator
    denominator = option.probability_denominator
    variance_numerator = sample_count * numerator * (denominator - numerator)
    return M34A_SIGMA_MULTIPLIER * _ceil_sqrt(variance_numerator)


def _scaled_deviation(
    *, observed_count: int, option: BranchOption, sample_count: int
) -> int:
    return abs(
        observed_count * option.probability_denominator
        - sample_count * option.probability_numerator
    )


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
        operation_sequence_id="m34a_single_ordinary_add_multi_seed",
    )
    return Counter(row.selected_mod_id for row in result.trajectories)


def _collect_breaches(
    *,
    fixture_id: str,
    seed: int,
    run_id: str,
    sample_tier: int,
    observed: Counter[str],
    exact: Mapping[str, BranchOption],
) -> tuple[BranchBreachDiagnostic, ...]:
    breaches: list[BranchBreachDiagnostic] = []
    for key, option in exact.items():
        deviation = _scaled_deviation(
            observed_count=observed[key],
            option=option,
            sample_count=sample_tier,
        )
        tolerance = _scaled_sigma_tolerance(option, sample_tier)
        if deviation > tolerance:
            breaches.append(
                BranchBreachDiagnostic(
                    fixture_id=fixture_id,
                    seed=seed,
                    run_id=run_id,
                    sample_tier=sample_tier,
                    branch_key=key,
                    pool_digest=option.candidate_digest,
                    deviation_scaled=deviation,
                    tolerance_scaled=tolerance,
                )
            )
    return tuple(breaches)


def _assert_no_breaches(
    *,
    fixture_id: str,
    seed: int,
    run_id: str,
    sample_tier: int,
    observed: Counter[str],
    exact: Mapping[str, BranchOption],
) -> None:
    assert set(observed) <= set(exact)
    assert sum(observed.values()) == sample_tier
    breaches = _collect_breaches(
        fixture_id=fixture_id,
        seed=seed,
        run_id=run_id,
        sample_tier=sample_tier,
        observed=observed,
        exact=exact,
    )
    if breaches:
        raise AssertionError("\n".join(breach.message() for breach in breaches))


def test_m34a_execution_contract_is_pinned() -> None:
    assert M34A_SEED_LIST == (34001, 34002, 34003)
    assert M34A_SAMPLE_TIERS == (512, 2048, 8192)
    assert M34A_SIGMA_MULTIPLIER == 6


def test_m34a_multi_seed_single_step_convergence_hardening() -> None:
    static, state, operation = _broad_skewed_fixture()
    harness = OrdinaryAddMonteCarloHarness(static=static)
    fixture_id = "m34a_broad_skewed_single_step"
    exact = _exact_by_key(
        harness.enumerate_outcomes(
            state=state,
            operation=operation,
            decision_id=f"{fixture_id}.exact",
        )
    )
    assert set(exact) == {
        "eligible_a",
        "eligible_b",
        "eligible_c",
        "eligible_d",
        "eligible_e",
        "eligible_f",
        "eligible_g",
        "eligible_h",
    }

    for seed in M34A_SEED_LIST:
        for sample_tier in M34A_SAMPLE_TIERS:
            run_id = f"{fixture_id}.seed_{seed}.tier_{sample_tier}"
            observed = _observed_counts(
                harness=harness,
                state=state,
                operation=operation,
                seed=seed,
                sample_count=sample_tier,
                run_id=run_id,
            )
            _assert_no_breaches(
                fixture_id=fixture_id,
                seed=seed,
                run_id=run_id,
                sample_tier=sample_tier,
                observed=observed,
                exact=exact,
            )


def test_m34a_same_seed_and_run_id_replay_exactly_across_seed_list() -> None:
    static, state, operation = _broad_skewed_fixture()
    harness = OrdinaryAddMonteCarloHarness(static=static)
    sample_tier = M34A_SAMPLE_TIERS[0]

    for seed in M34A_SEED_LIST:
        run_id = f"m34a_replay.seed_{seed}.tier_{sample_tier}"
        first = harness.run(
            initial_state=state,
            operation=operation,
            seed=seed,
            sample_count=sample_tier,
            run_id=run_id,
            operation_sequence_id="m34a_single_ordinary_add_multi_seed",
        )
        second = harness.run(
            initial_state=state,
            operation=operation,
            seed=seed,
            sample_count=sample_tier,
            run_id=run_id,
            operation_sequence_id="m34a_single_ordinary_add_multi_seed",
        )
        assert first.result_hash == second.result_hash
        assert [row.public_payload() for row in first.trajectories] == [
            row.public_payload() for row in second.trajectories
        ]


def test_m34a_negative_control_proves_breach_reporting_can_fail() -> None:
    static, state, operation = _broad_skewed_fixture()
    harness = OrdinaryAddMonteCarloHarness(static=static)
    fixture_id = "m34a_negative_control_forced_breach"
    sample_tier = M34A_SAMPLE_TIERS[-1]
    seed = M34A_SEED_LIST[0]
    run_id = f"{fixture_id}.seed_{seed}.tier_{sample_tier}"
    exact = _exact_by_key(
        harness.enumerate_outcomes(
            state=state,
            operation=operation,
            decision_id=f"{fixture_id}.exact",
        )
    )
    observed = Counter({next(iter(exact)): sample_tier})

    with pytest.raises(AssertionError) as exc_info:
        _assert_no_breaches(
            fixture_id=fixture_id,
            seed=seed,
            run_id=run_id,
            sample_tier=sample_tier,
            observed=observed,
            exact=exact,
        )

    message = str(exc_info.value)
    for required in (
        "fixture_id=m34a_negative_control_forced_breach",
        "seed=34001",
        f"run_id={run_id}",
        "sample_tier=8192",
        "branch_key=",
        "pool_digest=",
        "deviation_scaled=",
        "tolerance_scaled=",
        "m34a_multi_seed_tolerance_breach",
    ):
        assert required in message
