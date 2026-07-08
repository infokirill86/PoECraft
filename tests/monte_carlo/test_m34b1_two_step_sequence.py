from __future__ import annotations

from collections import Counter
from collections.abc import Mapping
from dataclasses import dataclass
from fractions import Fraction
from math import isqrt

import pytest

from p2c_engine.domain.enums import Rarity, Side
from p2c_engine.domain.item_state import ItemState, ModifierInstance
from p2c_engine.domain.static_modifier import StaticModifier
from p2c_engine.legality.pool_builders import build_ordinary_add_pool
from p2c_engine.monte_carlo.ordinary_add import (
    ExactTerminalOption,
    M32InvariantViolation,
    OrdinaryAddMonteCarloHarness,
    OrdinaryAddOperation,
)
from p2c_engine.static_data.game_data import StaticGameData


M34B1_SEED_LIST = (34001, 34002, 34003)
M34B1_SAMPLE_TIERS = (512, 2048, 8192)
M34B1_SIGMA_MULTIPLIER = 6
M34B1_MAX_EXACT_PATHS = 64
M34B1_SEQUENCE_LENGTH = 2
M34B1_CONSTRUCTED_FIXTURE_LABEL = (
    "project-model hardening fixture; not a real crafting route"
)


@dataclass(frozen=True, slots=True)
class TerminalBreachDiagnostic:
    fixture_id: str
    seed: int
    run_id: str
    sample_tier: int
    branch_key: str
    deviation_scaled: int
    tolerance_scaled: int
    category: str = "m34b1_two_step_terminal_tolerance_breach"

    def message(self) -> str:
        return (
            f"{self.category}: "
            f"fixture_id={self.fixture_id}; "
            f"seed={self.seed}; "
            f"run_id={self.run_id}; "
            f"sample_tier={self.sample_tier}; "
            f"branch_key={self.branch_key}; "
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
        source_fingerprint="m34b1_fixture_source",
        semantic_fingerprint="m34b1_fixture_semantic",
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


def _balanced_two_step_fixture() -> tuple[StaticGameData, ItemState, OrdinaryAddOperation]:
    static = _static(
        (
            _base_fractured_suffix(),
            _mod("alpha_prefix", family="alpha", side=Side.PREFIX, weight=1),
            _mod("beta_prefix", family="beta", side=Side.PREFIX, weight=1),
            _mod("gamma_prefix", family="gamma", side=Side.PREFIX, weight=1),
        )
    )
    operation = OrdinaryAddOperation(
        mode_id="m34b1_constructed_balanced_two_step_fixture",
        side_filter=Side.PREFIX,
    )
    return static, _base_state(), operation


def _ceil_sqrt(value: int) -> int:
    root = isqrt(value)
    return root if root * root == value else root + 1


def _scaled_sigma_tolerance(option: ExactTerminalOption, sample_count: int) -> int:
    numerator = option.probability_numerator
    denominator = option.probability_denominator
    variance_numerator = sample_count * numerator * (denominator - numerator)
    return M34B1_SIGMA_MULTIPLIER * _ceil_sqrt(variance_numerator)


def _scaled_deviation(
    *, observed_count: int, option: ExactTerminalOption, sample_count: int
) -> int:
    return abs(
        observed_count * option.probability_denominator
        - sample_count * option.probability_numerator
    )


def _assert_no_terminal_breaches(
    *,
    fixture_id: str,
    seed: int,
    run_id: str,
    sample_tier: int,
    observed: Counter[str],
    exact: Mapping[str, ExactTerminalOption],
) -> None:
    assert set(observed) <= set(exact)
    assert sum(observed.values()) == sample_tier
    breaches: list[TerminalBreachDiagnostic] = []
    for key, option in exact.items():
        deviation = _scaled_deviation(
            observed_count=observed[key],
            option=option,
            sample_count=sample_tier,
        )
        tolerance = _scaled_sigma_tolerance(option, sample_tier)
        if deviation > tolerance:
            breaches.append(
                TerminalBreachDiagnostic(
                    fixture_id=fixture_id,
                    seed=seed,
                    run_id=run_id,
                    sample_tier=sample_tier,
                    branch_key=key,
                    deviation_scaled=deviation,
                    tolerance_scaled=tolerance,
                )
            )
    if breaches:
        raise AssertionError("\n".join(breach.message() for breach in breaches))


def _exact_terminal_by_hash(
    terminals: tuple[ExactTerminalOption, ...],
) -> dict[str, ExactTerminalOption]:
    return {terminal.terminal_state_hash: terminal for terminal in terminals}


def _terminal_counts(result) -> Counter[str]:  # type: ignore[no-untyped-def]
    return Counter(row.terminal_state_hash for row in result.trajectories)


def _step_counts(result, step_index: int) -> Counter[str]:  # type: ignore[no-untyped-def]
    return Counter(
        row.steps[step_index].selected_mod_id
        for row in result.trajectories
        if row.steps[step_index].selected_mod_id is not None
    )


def test_m34b1_execution_contract_is_pinned() -> None:
    assert M34B1_SEED_LIST == (34001, 34002, 34003)
    assert M34B1_SAMPLE_TIERS == (512, 2048, 8192)
    assert M34B1_SIGMA_MULTIPLIER == 6
    assert M34B1_MAX_EXACT_PATHS == 64
    assert M34B1_SEQUENCE_LENGTH == 2
    assert "project-model hardening fixture" in M34B1_CONSTRUCTED_FIXTURE_LABEL
    assert "not a real crafting route" in M34B1_CONSTRUCTED_FIXTURE_LABEL


def test_m34b1_exact_terminal_distribution_aggregates_canonical_terminals() -> None:
    static, state, operation = _balanced_two_step_fixture()
    harness = OrdinaryAddMonteCarloHarness(static=static)

    paths = harness.enumerate_two_step_paths(
        initial_state=state,
        first_operation=operation,
        second_operation=operation,
        decision_id_prefix="m34b1.exact.paths",
        max_exact_paths=M34B1_MAX_EXACT_PATHS,
    )
    terminals = harness.enumerate_two_step_terminal_distribution(
        initial_state=state,
        first_operation=operation,
        second_operation=operation,
        decision_id_prefix="m34b1.exact.terminals",
        max_exact_paths=M34B1_MAX_EXACT_PATHS,
    )

    assert len(paths) == 6
    assert len(terminals) == 3
    assert sum(
        Fraction(option.probability_numerator, option.probability_denominator)
        for option in terminals
    ) == Fraction(1, 1)
    assert {option.path_count for option in terminals} == {2}

    path_key_sets = {frozenset(path.path_key): path.terminal_state_hash for path in paths}
    assert frozenset(("alpha_prefix", "beta_prefix")) in path_key_sets
    alpha_beta_terminal = path_key_sets[frozenset(("alpha_prefix", "beta_prefix"))]
    alpha_beta_option = _exact_terminal_by_hash(terminals)[alpha_beta_terminal]
    assert set(alpha_beta_option.path_keys) == {
        ("alpha_prefix", "beta_prefix"),
        ("beta_prefix", "alpha_prefix"),
    }
    assert Fraction(
        alpha_beta_option.probability_numerator,
        alpha_beta_option.probability_denominator,
    ) == Fraction(1, 3)


def test_m34b1_branch_specific_pool_rebuild_blocks_step0_family() -> None:
    static, state, operation = _balanced_two_step_fixture()
    observed_pre_state_mods: list[tuple[str, ...]] = []

    def spy_builder(request, game_data):  # type: ignore[no-untyped-def]
        observed_pre_state_mods.append(tuple(mod.mod_id for mod in request.state.modifiers))
        return build_ordinary_add_pool(request, game_data)

    harness = OrdinaryAddMonteCarloHarness(static=static, pool_builder=spy_builder)
    paths = harness.enumerate_two_step_paths(
        initial_state=state,
        first_operation=operation,
        second_operation=operation,
        decision_id_prefix="m34b1.exact.rebuild",
        max_exact_paths=M34B1_MAX_EXACT_PATHS,
    )

    assert len(observed_pre_state_mods) == 4
    assert observed_pre_state_mods[0] == ("fixed_fractured_crit_suffix",)
    assert set(observed_pre_state_mods[1:]) == {
        ("fixed_fractured_crit_suffix", "alpha_prefix"),
        ("fixed_fractured_crit_suffix", "beta_prefix"),
        ("fixed_fractured_crit_suffix", "gamma_prefix"),
    }
    assert all(path.path_key[0] != path.path_key[1] for path in paths)
    assert all(path.steps[1].pre_state_hash == path.steps[0].post_state_hash for path in paths)


def test_m34b1_seeded_mc_converges_to_exact_terminals_and_step_marginals() -> None:
    static, state, operation = _balanced_two_step_fixture()
    harness = OrdinaryAddMonteCarloHarness(static=static)
    fixture_id = "m34b1_constructed_balanced_two_step"
    exact = _exact_terminal_by_hash(
        harness.enumerate_two_step_terminal_distribution(
            initial_state=state,
            first_operation=operation,
            second_operation=operation,
            decision_id_prefix=f"{fixture_id}.exact",
            max_exact_paths=M34B1_MAX_EXACT_PATHS,
        )
    )

    expected_step_mod_ids = {"alpha_prefix", "beta_prefix", "gamma_prefix"}
    for seed in M34B1_SEED_LIST:
        for sample_tier in M34B1_SAMPLE_TIERS:
            run_id = f"{fixture_id}.seed_{seed}.tier_{sample_tier}"
            result = harness.run_two_step_sequence(
                initial_state=state,
                first_operation=operation,
                second_operation=operation,
                seed=seed,
                sample_count=sample_tier,
                run_id=run_id,
            )
            _assert_no_terminal_breaches(
                fixture_id=fixture_id,
                seed=seed,
                run_id=run_id,
                sample_tier=sample_tier,
                observed=_terminal_counts(result),
                exact=exact,
            )
            assert set(_step_counts(result, 0)) == expected_step_mod_ids
            assert set(_step_counts(result, 1)) == expected_step_mod_ids


def test_m34b1_same_seed_and_run_id_replay_exactly() -> None:
    static, state, operation = _balanced_two_step_fixture()
    harness = OrdinaryAddMonteCarloHarness(static=static)
    seed = M34B1_SEED_LIST[0]
    sample_tier = M34B1_SAMPLE_TIERS[0]
    run_id = "m34b1_replay.seed_34001.tier_512"

    first = harness.run_two_step_sequence(
        initial_state=state,
        first_operation=operation,
        second_operation=operation,
        seed=seed,
        sample_count=sample_tier,
        run_id=run_id,
    )
    second = harness.run_two_step_sequence(
        initial_state=state,
        first_operation=operation,
        second_operation=operation,
        seed=seed,
        sample_count=sample_tier,
        run_id=run_id,
    )

    assert first.result_hash == second.result_hash
    assert [row.public_payload() for row in first.trajectories] == [
        row.public_payload() for row in second.trajectories
    ]


def test_m34b1_negative_control_proves_terminal_breach_reporting_can_fail() -> None:
    static, state, operation = _balanced_two_step_fixture()
    harness = OrdinaryAddMonteCarloHarness(static=static)
    fixture_id = "m34b1_negative_control_forced_terminal_breach"
    seed = M34B1_SEED_LIST[0]
    sample_tier = M34B1_SAMPLE_TIERS[-1]
    run_id = f"{fixture_id}.seed_{seed}.tier_{sample_tier}"
    exact = _exact_terminal_by_hash(
        harness.enumerate_two_step_terminal_distribution(
            initial_state=state,
            first_operation=operation,
            second_operation=operation,
            decision_id_prefix=f"{fixture_id}.exact",
            max_exact_paths=M34B1_MAX_EXACT_PATHS,
        )
    )
    first_terminal = next(iter(exact))
    observed = Counter({first_terminal: sample_tier})

    with pytest.raises(AssertionError) as exc_info:
        _assert_no_terminal_breaches(
            fixture_id=fixture_id,
            seed=seed,
            run_id=run_id,
            sample_tier=sample_tier,
            observed=observed,
            exact=exact,
        )

    message = str(exc_info.value)
    for required in (
        "fixture_id=m34b1_negative_control_forced_terminal_breach",
        "seed=34001",
        f"run_id={run_id}",
        "sample_tier=8192",
        "branch_key=",
        "deviation_scaled=",
        "tolerance_scaled=",
        "m34b1_two_step_terminal_tolerance_breach",
    ):
        assert required in message


def test_m34b1_fail_closed_on_non_ordinary_add_operation() -> None:
    static, state, operation = _balanced_two_step_fixture()
    harness = OrdinaryAddMonteCarloHarness(static=static)
    invalid = OrdinaryAddOperation(
        mode_id="m34b1_invalid_operation",
        operation_id="not_ordinary_add",
    )

    with pytest.raises(M32InvariantViolation, match="unsupported operation_id"):
        harness.run_two_step_sequence(
            initial_state=state,
            first_operation=operation,
            second_operation=invalid,
            seed=M34B1_SEED_LIST[0],
            sample_count=1,
            run_id="m34b1_invalid_operation",
        )


def test_m34b1_exact_enumeration_ceiling_is_hard_failure() -> None:
    static, state, operation = _balanced_two_step_fixture()
    harness = OrdinaryAddMonteCarloHarness(static=static)

    with pytest.raises(Exception, match="exact path ceiling exceeded"):
        harness.enumerate_two_step_paths(
            initial_state=state,
            first_operation=operation,
            second_operation=operation,
            decision_id_prefix="m34b1.exact.ceiling",
            max_exact_paths=1,
        )
