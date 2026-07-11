from __future__ import annotations

from dataclasses import replace
from fractions import Fraction
from pathlib import Path

import pytest

from p2c_engine.domain.enums import Rarity, Side
from p2c_engine.domain.item_state import ItemState, ModifierInstance
from p2c_engine.monte_carlo.perfect_essence import (
    M42A_CRAFTED_CAPACITY_POLICY,
    M42A_OPERATION_IDS,
    M42A_REMOVAL_POLICY,
    PerfectEssenceHarness,
    PerfectEssenceOperation,
    M42APerfectEssenceInvariantViolation,
)
from p2c_engine.operations import (
    M42A_RESOLVER_SCHEMA_VERSION,
    M38AResolverAdmissionError,
    OperationResolver,
    OperationResolverRequest,
)
from p2c_engine.static_data import build_static_game_data


ROOT = Path(__file__).resolve().parents[2]
PREFIX_IDS = (
    "adds_value_to_value_physical_damage_t1",
    "value_increased_physical_damage_t1",
    "value_to_accuracy_rating_t1",
)
SUFFIX_IDS = (
    "value_increased_attack_speed_t1",
    "value_to_critical_hit_chance_t1",
    "value_to_level_of_all_melee_skills_t1",
)


def _state(*modifiers: ModifierInstance, rarity: Rarity = Rarity.RARE) -> ItemState:
    return ItemState(
        item_class="quarterstaff",
        rarity=rarity,
        item_level=82,
        modifiers=tuple(modifiers),
        unrevealed_desecrated=None,
        augment_socket_capacity=0,
        augment_socket_used=0,
        astrid_installed=False,
    )


def _resolve(static, operation_id: str, state: ItemState) -> PerfectEssenceOperation:
    plan = OperationResolver(static=static).resolve(
        OperationResolverRequest(
            currency_id=operation_id,
            item_state=state,
            mode_id=f"m42a_{operation_id}",
        )
    )
    assert plan.schema_version == M42A_RESOLVER_SCHEMA_VERSION
    assert isinstance(plan.operation, PerfectEssenceOperation)
    return plan.operation


def _mass(row: object) -> Fraction:
    return Fraction(row.probability_numerator, row.probability_denominator)  # type: ignore[attr-defined]


def test_m42a_activation_is_exactly_six_prepared_rows() -> None:
    static = build_static_game_data(ROOT)
    rows = tuple(static.operations["operations"])
    perfect = {row["operation_id"]: row for row in rows if row["group"] == "perfect_essence"}

    assert set(perfect) == M42A_OPERATION_IDS
    assert {
        operation_id
        for operation_id, row in perfect.items()
        if row["active_in_current_simulation"] is True
        and row["runtime_admission_status"] == "accepted_executable_runtime"
    } == M42A_OPERATION_IDS
    assert "perfect_essence" in static.project_scope["active_operation_groups"]
    assert "perfect_essences" in static.project_scope["active_mechanics"]
    assert not any(
        operation_id in perfect
        for operation_id in ("perfect_essence_seeking", "perfect_essence_infinite")
    )


@pytest.mark.parametrize("operation_id", sorted(M42A_OPERATION_IDS))
def test_m42a_all_rows_resolve_canonical_guaranteed_modifier(
    operation_id: str,
) -> None:
    static = build_static_game_data(ROOT)
    state = _state(
        ModifierInstance(PREFIX_IDS[0]),
        ModifierInstance(SUFFIX_IDS[0]),
    )
    operation = _resolve(static, operation_id, state)
    output = next(
        row
        for row in static.essence_outputs["perfect"]
        if row["operation_id"] == operation_id
    )
    canonical = static.modifier_index[operation.guaranteed_mod_id]

    assert operation.guaranteed_mod_id == output["guaranteed_mod_id"] == canonical.mod_id
    assert operation.guaranteed_family_id == output["family_id"] == canonical.family_id
    assert operation.guaranteed_side == Side(output["side"]) == canonical.side
    assert canonical.static_category == "perfect_essence"
    assert canonical.group_ids == tuple(sorted(output["group_ids"]))

    paths = PerfectEssenceHarness(static=static).enumerate_paths(
        initial_state=state,
        operation=operation,
        decision_id=f"m42a.exact.{operation_id}",
    )
    assert paths
    assert all(path.outcome == "completed" for path in paths)
    assert all(path.guaranteed_mod_id == operation.guaranteed_mod_id for path in paths)
    assert sum(_mass(path) for path in paths) == Fraction(1, 1)


def test_m42a_free_target_side_keeps_all_nonfractured_removal_instances() -> None:
    static = build_static_game_data(ROOT)
    state = _state(
        ModifierInstance(PREFIX_IDS[0]),
        ModifierInstance(SUFFIX_IDS[0]),
        ModifierInstance(SUFFIX_IDS[1]),
        ModifierInstance(SUFFIX_IDS[2], fractured=True),
    )
    operation = _resolve(static, "perfect_essence_abrasion", state)
    pool = PerfectEssenceHarness(static=static).build_feasible_pool(state, operation)

    assert pool.target_side_was_full is False
    assert {row.mod_id for row in pool.removal_metadata} == {
        PREFIX_IDS[0],
        SUFFIX_IDS[0],
        SUFFIX_IDS[1],
    }
    assert all(not row.fractured for row in pool.removal_metadata)


@pytest.mark.parametrize(
    ("operation_id", "mod_ids", "expected_side"),
    (
        (
            "perfect_essence_abrasion",
            PREFIX_IDS + SUFFIX_IDS[:2],
            Side.PREFIX,
        ),
        (
            "perfect_essence_battle",
            PREFIX_IDS[:2] + SUFFIX_IDS,
            Side.SUFFIX,
        ),
    ),
)
def test_m42a_full_target_side_keeps_only_removals_that_create_capacity(
    operation_id: str,
    mod_ids: tuple[str, ...],
    expected_side: Side,
) -> None:
    static = build_static_game_data(ROOT)
    state = _state(*(ModifierInstance(mod_id) for mod_id in mod_ids))
    operation = _resolve(static, operation_id, state)
    pool = PerfectEssenceHarness(static=static).build_feasible_pool(state, operation)

    assert pool.target_side_was_full is True
    assert pool.candidates
    assert {row.side for row in pool.removal_metadata} == {expected_side.value}
    assert len(pool.candidates) == 3


def test_m42a_empty_feasible_pool_fails_unchanged_before_draw() -> None:
    static = build_static_game_data(ROOT)
    state = _state(
        *(ModifierInstance(mod_id, fractured=True) for mod_id in PREFIX_IDS),
        ModifierInstance(SUFFIX_IDS[0]),
    )
    operation = _resolve(static, "perfect_essence_abrasion", state)
    harness = PerfectEssenceHarness(static=static)
    pool = harness.build_feasible_pool(state, operation)
    path = harness.enumerate_paths(
        initial_state=state,
        operation=operation,
        decision_id="m42a.empty_feasible",
    )[0]
    result = harness.run(
        initial_state=state,
        operation=operation,
        seed=42001,
        sample_count=1,
        run_id="m42a_empty_feasible",
    )

    assert pool.candidates == ()
    assert pool.empty_reason == "feasible_removal_pool_exhausted"
    assert path.outcome == "no_transition_no_consumption"
    assert path.terminal_state_hash == state.state_hash()
    assert result.decisions == ()
    assert result.trajectories[0].terminal_state_hash == state.state_hash()


def test_m42a_uniform_exact_mass_and_terminal_normalization() -> None:
    static = build_static_game_data(ROOT)
    state = _state(
        ModifierInstance(PREFIX_IDS[0]),
        ModifierInstance(PREFIX_IDS[1]),
        ModifierInstance(SUFFIX_IDS[0]),
    )
    operation = _resolve(static, "perfect_essence_abrasion", state)
    harness = PerfectEssenceHarness(static=static)
    paths = harness.enumerate_paths(
        initial_state=state,
        operation=operation,
        decision_id="m42a.uniform_exact",
    )
    terminals = harness.enumerate_terminal_distribution(
        initial_state=state,
        operation=operation,
        decision_id="m42a.uniform_exact",
    )

    assert len(paths) == 3
    assert {_mass(path) for path in paths} == {Fraction(1, 3)}
    assert sum(_mass(path) for path in paths) == Fraction(1, 1)
    assert sum(_mass(row) for row in terminals) == Fraction(1, 1)


def test_m42a_existing_crafted_modifier_fails_closed_unchanged() -> None:
    static = build_static_game_data(ROOT)
    state = _state(
        ModifierInstance("crafted_greater_abrasion_flat_physical", crafted=True),
        ModifierInstance(SUFFIX_IDS[0]),
    )
    operation = _resolve(static, "perfect_essence_battle", state)
    harness = PerfectEssenceHarness(static=static)
    path = harness.enumerate_paths(
        initial_state=state,
        operation=operation,
        decision_id="m42a.crafted_block",
    )[0]
    result = harness.run(
        initial_state=state,
        operation=operation,
        seed=42002,
        sample_count=2,
        run_id="m42a_crafted_block",
    )

    assert path.outcome == "no_transition_no_consumption"
    assert path.no_transition_reason == "crafted_count_not_zero"
    assert path.terminal_state_hash == state.state_hash()
    assert result.decisions == ()
    assert result.crafted_capacity_policy == M42A_CRAFTED_CAPACITY_POLICY


@pytest.mark.parametrize(
    ("conflict_kind", "expected_reason"),
    (
        ("family", "guaranteed_family_present"),
        ("group", "guaranteed_group_present"),
    ),
)
def test_m42a_guaranteed_family_or_group_conflict_fails_closed_unchanged(
    conflict_kind: str,
    expected_reason: str,
) -> None:
    static = build_static_game_data(ROOT)
    modified_index = dict(static.modifier_index)
    if conflict_kind == "family":
        modified_index[SUFFIX_IDS[0]] = replace(
            modified_index[SUFFIX_IDS[0]],
            family_id="prefix_extra_physical",
        )
    else:
        modified_index[SUFFIX_IDS[0]] = replace(
            modified_index[SUFFIX_IDS[0]],
            group_ids=("crafted_extra_physical_damage",),
        )
    conflict_static = replace(static, modifier_index=modified_index)
    state = _state(ModifierInstance(SUFFIX_IDS[0]))
    operation = _resolve(conflict_static, "perfect_essence_abrasion", state)
    path = PerfectEssenceHarness(static=conflict_static).enumerate_paths(
        initial_state=state,
        operation=operation,
        decision_id="m42a.group_conflict",
    )[0]

    assert path.outcome == "no_transition_no_consumption"
    assert path.no_transition_reason == expected_reason
    assert path.terminal_state_hash == state.state_hash()


def test_m42a_seeded_replay_uses_one_removal_decision_and_no_add_draw() -> None:
    static = build_static_game_data(ROOT)
    state = _state(
        ModifierInstance(PREFIX_IDS[0]),
        ModifierInstance(PREFIX_IDS[1]),
        ModifierInstance(SUFFIX_IDS[0]),
    )
    operation = _resolve(static, "perfect_essence_abrasion", state)
    harness = PerfectEssenceHarness(static=static)
    exact = harness.enumerate_terminal_distribution(
        initial_state=state,
        operation=operation,
        decision_id="m42a.replay.exact",
    )
    left = harness.run(
        initial_state=state,
        operation=operation,
        seed=42003,
        sample_count=16,
        run_id="m42a_replay",
    )
    replay = harness.run(
        initial_state=state,
        operation=operation,
        seed=42003,
        sample_count=16,
        run_id="m42a_replay",
    )

    assert left == replay
    assert len(left.decisions) == 16
    assert all(".remove" in row.decision_id for row in left.decisions)
    assert {row.terminal_state_hash for row in left.trajectories}.issubset(
        {row.terminal_state_hash for row in exact}
    )
    assert left.removal_policy == M42A_REMOVAL_POLICY


def test_m42a_atomic_terminal_preserves_unselected_and_fractured_instances() -> None:
    static = build_static_game_data(ROOT)
    fractured = ModifierInstance(SUFFIX_IDS[1], fractured=True)
    state = _state(
        ModifierInstance(PREFIX_IDS[0]),
        ModifierInstance(SUFFIX_IDS[0]),
        fractured,
    )
    operation = _resolve(static, "perfect_essence_abrasion", state)
    paths = PerfectEssenceHarness(static=static).enumerate_paths(
        initial_state=state,
        operation=operation,
        decision_id="m42a.atomic",
    )

    assert paths
    for path in paths:
        assert path.outcome == "completed"
        assert path.guaranteed_mod_id == operation.guaranteed_mod_id
        assert path.selected_mod_id != fractured.mod_id


def test_m42a_missing_canonical_output_and_unprepared_rows_fail_closed() -> None:
    static = build_static_game_data(ROOT)
    state = _state(ModifierInstance(PREFIX_IDS[0]))
    missing_index = dict(static.modifier_index)
    missing_index.pop("crafted_perfect_abrasion_extra_physical")
    missing_static = replace(static, modifier_index=missing_index)

    with pytest.raises(M38AResolverAdmissionError, match="canonical index"):
        OperationResolver(static=missing_static).resolve(
            OperationResolverRequest(
                currency_id="perfect_essence_abrasion",
                item_state=state,
            )
        )
    with pytest.raises(M38AResolverAdmissionError, match="unknown operation"):
        OperationResolver(static=static).resolve(
            OperationResolverRequest(
                currency_id="perfect_essence_seeking",
                item_state=state,
            )
        )


def test_m42a_tampered_operation_contract_fails_hard() -> None:
    static = build_static_game_data(ROOT)
    state = _state(ModifierInstance(PREFIX_IDS[0]))
    operation = replace(
        _resolve(static, "perfect_essence_abrasion", state),
        guaranteed_family_id="wrong_family",
    )

    with pytest.raises(
        M42APerfectEssenceInvariantViolation,
        match="canonical contract mismatch",
    ):
        PerfectEssenceHarness(static=static).enumerate_paths(
            initial_state=state,
            operation=operation,
            decision_id="m42a.tampered",
        )
