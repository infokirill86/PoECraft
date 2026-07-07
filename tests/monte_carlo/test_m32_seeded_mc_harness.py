from __future__ import annotations

import pytest

from p2c_engine.decisions import RecordingDecisionSource, SeededDecisionSource
from p2c_engine.domain.candidate import Candidate
from p2c_engine.domain.enums import Rarity, Side
from p2c_engine.domain.item_state import ItemState, ModifierInstance
from p2c_engine.domain.pool_building import PoolBuildResult
from p2c_engine.domain.static_modifier import StaticModifier
from p2c_engine.legality.pool_builders import OrdinaryAddPoolRequest, build_ordinary_add_pool
from p2c_engine.monte_carlo.ordinary_add import (
    M32InvariantViolation,
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
        source_fingerprint="fixture_source",
        semantic_fingerprint="fixture_semantic",
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


def _fractured_state() -> tuple[StaticGameData, ItemState]:
    fractured = _mod(
        "fixed_fractured_crit",
        family="crit_chance",
        side=Side.SUFFIX,
        weight=1,
    )
    alpha = _mod("alpha_prefix", family="alpha", side=Side.PREFIX, weight=1)
    beta = _mod("beta_prefix", family="beta", side=Side.PREFIX, weight=3)
    static = _static((fractured, alpha, beta))
    state = _state(ModifierInstance("fixed_fractured_crit", fractured=True))
    return static, state


def test_same_seed_replay_gives_identical_public_summary() -> None:
    static, state = _fractured_state()
    harness = OrdinaryAddMonteCarloHarness(static=static)
    operation = OrdinaryAddOperation(mode_id="m32_fixture")

    first = harness.run(
        initial_state=state,
        operation=operation,
        seed=77,
        sample_count=12,
        run_id="m32_replay",
    )
    second = harness.run(
        initial_state=state,
        operation=operation,
        seed=77,
        sample_count=12,
        run_id="m32_replay",
    )

    assert first.result_hash == second.result_hash
    assert [row.public_payload() for row in first.trajectories] == [
        row.public_payload() for row in second.trajectories
    ]


def test_different_seed_can_change_sample_sequence() -> None:
    static, state = _fractured_state()
    harness = OrdinaryAddMonteCarloHarness(static=static)
    operation = OrdinaryAddOperation(mode_id="m32_fixture")

    first = harness.run(
        initial_state=state,
        operation=operation,
        seed=1,
        sample_count=20,
        run_id="m32_seed_a",
    )
    second = harness.run(
        initial_state=state,
        operation=operation,
        seed=2,
        sample_count=20,
        run_id="m32_seed_b",
    )

    assert [row.selected_mod_id for row in first.trajectories] != [
        row.selected_mod_id for row in second.trajectories
    ]


def test_exact_and_mc_use_same_injected_pool_builder() -> None:
    static, state = _fractured_state()
    calls: list[OrdinaryAddPoolRequest] = []

    def spy_builder(request: OrdinaryAddPoolRequest, game_data: StaticGameData) -> PoolBuildResult:
        calls.append(request)
        return build_ordinary_add_pool(request, game_data)

    harness = OrdinaryAddMonteCarloHarness(static=static, pool_builder=spy_builder)
    operation = OrdinaryAddOperation(mode_id="m32_fixture")
    exact_options = harness.enumerate_outcomes(
        state=state,
        operation=operation,
        decision_id="m32.exact.fixture",
    )
    decision_source = RecordingDecisionSource(SeededDecisionSource(77))
    trajectory = harness.sample_once(
        state=state,
        operation=operation,
        decision_source=decision_source,
        sample_index=0,
        run_id="m32_mc_fixture",
    )

    assert len(calls) == 2
    assert calls[0].state == calls[1].state == state
    assert {option.selected_key for option in exact_options} == {"alpha_prefix", "beta_prefix"}
    assert trajectory.selected_mod_id in {"alpha_prefix", "beta_prefix"}


def test_one_outcome_pool_is_deterministic() -> None:
    fixed = _mod("fixed_fractured_crit", family="crit", side=Side.SUFFIX, weight=1)
    only = _mod("only_prefix", family="only", side=Side.PREFIX, weight=9)
    static = _static((fixed, only))
    state = _state(ModifierInstance("fixed_fractured_crit", fractured=True))
    harness = OrdinaryAddMonteCarloHarness(static=static)
    result = harness.run(
        initial_state=state,
        operation=OrdinaryAddOperation(mode_id="m32_fixture"),
        seed=999,
        sample_count=5,
        run_id="m32_one_outcome",
    )

    assert {row.selected_mod_id for row in result.trajectories} == {"only_prefix"}


def test_empty_pool_no_transition_behavior() -> None:
    fixed = _mod("fixed_fractured_crit", family="crit", side=Side.SUFFIX, weight=1)
    static = _static((fixed,))
    state = _state(
        ModifierInstance("fixed_fractured_crit", fractured=True),
        ModifierInstance("p1"),
    )
    # Make the intentionally installed unknown p1 known and fill all prefix slots with blocked rows.
    static = _static(
        (
            fixed,
            _mod("p1", family="p1", side=Side.PREFIX, weight=1),
            _mod("p2", family="p2", side=Side.PREFIX, weight=1),
            _mod("p3", family="p3", side=Side.PREFIX, weight=1),
        )
    )
    state = _state(
        ModifierInstance("fixed_fractured_crit", fractured=True),
        ModifierInstance("p1"),
        ModifierInstance("p2"),
        ModifierInstance("p3"),
    )
    harness = OrdinaryAddMonteCarloHarness(static=static)
    result = harness.run(
        initial_state=state,
        operation=OrdinaryAddOperation(mode_id="m32_fixture", side_filter=Side.PREFIX),
        seed=11,
        sample_count=3,
        run_id="m32_empty_pool",
    )

    assert {row.outcome for row in result.trajectories} == {"no_transition"}
    assert all(row.decision_id is None for row in result.trajectories)


def test_runtime_invariants_fail_on_fractured_change() -> None:
    static, state = _fractured_state()
    harness = OrdinaryAddMonteCarloHarness(static=static)
    bad_post = state.with_modifiers((ModifierInstance("fixed_fractured_crit", fractured=False),))

    with pytest.raises(M32InvariantViolation, match="fractured"):
        harness._assert_runtime_invariants(
            pre_state=state,
            post_state=bad_post,
            expected_mode_id="m32_fixture",
            actual_mode_id="m32_fixture",
            operation_id="ordinary_add",
        )


def test_runtime_invariants_fail_on_unsupported_operation() -> None:
    static, state = _fractured_state()
    harness = OrdinaryAddMonteCarloHarness(static=static)

    with pytest.raises(M32InvariantViolation, match="unsupported operation_id"):
        harness._assert_runtime_invariants(
            pre_state=state,
            post_state=state,
            expected_mode_id="m32_fixture",
            actual_mode_id="m32_fixture",
            operation_id="chaos",
        )


def test_runtime_invariants_fail_on_capacity_family_and_group() -> None:
    fixed = _mod("fixed_fractured_crit", family="crit", side=Side.SUFFIX, weight=1)
    a = _mod("a_prefix", family="dup", side=Side.PREFIX, weight=1, groups=("g",))
    b = _mod("b_prefix", family="dup", side=Side.PREFIX, weight=1)
    c = _mod("c_prefix", family="c", side=Side.PREFIX, weight=1, groups=("g",))
    d = _mod("d_prefix", family="d", side=Side.PREFIX, weight=1)
    static = _static((fixed, a, b, c, d))
    harness = OrdinaryAddMonteCarloHarness(static=static)
    pre = _state(ModifierInstance("fixed_fractured_crit", fractured=True))

    duplicate_family = _state(
        ModifierInstance("fixed_fractured_crit", fractured=True),
        ModifierInstance("a_prefix"),
        ModifierInstance("b_prefix"),
    )
    with pytest.raises(M32InvariantViolation, match="duplicate family"):
        harness._assert_runtime_invariants(
            pre_state=pre,
            post_state=duplicate_family,
            expected_mode_id="m32_fixture",
            actual_mode_id="m32_fixture",
            operation_id="ordinary_add",
        )

    group_conflict = _state(
        ModifierInstance("fixed_fractured_crit", fractured=True),
        ModifierInstance("a_prefix"),
        ModifierInstance("c_prefix"),
    )
    with pytest.raises(M32InvariantViolation, match="group conflict"):
        harness._assert_runtime_invariants(
            pre_state=pre,
            post_state=group_conflict,
            expected_mode_id="m32_fixture",
            actual_mode_id="m32_fixture",
            operation_id="ordinary_add",
        )

    capacity_overflow = _state(
        ModifierInstance("fixed_fractured_crit", fractured=True),
        ModifierInstance("a_prefix"),
        ModifierInstance("c_prefix"),
        ModifierInstance("d_prefix"),
        ModifierInstance("b_prefix"),
    )
    with pytest.raises(M32InvariantViolation, match="capacity exceeded"):
        harness._assert_runtime_invariants(
            pre_state=pre,
            post_state=capacity_overflow,
            expected_mode_id="m32_fixture",
            actual_mode_id="m32_fixture",
            operation_id="ordinary_add",
        )


def test_public_summary_is_numeric_probability_free_metadata() -> None:
    static, state = _fractured_state()
    harness = OrdinaryAddMonteCarloHarness(static=static)
    result = harness.run(
        initial_state=state,
        operation=OrdinaryAddOperation(mode_id="m32_fixture"),
        seed=77,
        sample_count=4,
        run_id="m32_public_summary",
    )
    summary = result.public_summary()

    assert summary["numeric_probability_free"] is True
    assert summary["public_numeric_release"] is False
    assert summary["probability_values_printed"] is False
    forbidden_keys = {"probability", "percent", "expected_attempts", "ev", "ranking"}
    assert not (forbidden_keys & set(summary))
