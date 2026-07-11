from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest
import yaml

from p2c_engine.domain.enums import Rarity, Side
from p2c_engine.domain.item_state import ItemState, ModifierInstance
from p2c_engine.monte_carlo.greater_essence import (
    M41A_CRAFTED_CAPACITY_STATUS,
    M41A_OPERATION_IDS,
    GreaterEssenceHarness,
    GreaterEssenceOperation,
    M41AGreaterEssenceInvariantViolation,
)
from p2c_engine.monte_carlo.perfect_essence import M42A_OPERATION_IDS
from p2c_engine.operations import (
    M41A_RESOLVER_SCHEMA_VERSION,
    M38AResolverAdmissionError,
    OperationResolver,
    OperationResolverRequest,
)
from p2c_engine.static_data import build_static_game_data


ROOT = Path(__file__).resolve().parents[2]


def _state(*modifiers: ModifierInstance, rarity: Rarity = Rarity.MAGIC) -> ItemState:
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


def _resolve(static, operation_id: str, state: ItemState) -> GreaterEssenceOperation:
    plan = OperationResolver(static=static).resolve(
        OperationResolverRequest(
            currency_id=operation_id,
            item_state=state,
            mode_id=f"m41a_{operation_id}",
        )
    )
    assert plan.schema_version == M41A_RESOLVER_SCHEMA_VERSION
    assert isinstance(plan.operation, GreaterEssenceOperation)
    return plan.operation


def test_m41a_activation_is_exactly_the_authorized_eight_rows() -> None:
    static = build_static_game_data(ROOT)
    scope = static.project_scope
    rows = tuple(static.operations["operations"])
    greater_rows = {row["operation_id"]: row for row in rows if row["group"] == "greater_essence"}

    assert set(greater_rows) == M41A_OPERATION_IDS
    assert {
        operation_id
        for operation_id, row in greater_rows.items()
        if row["runtime_admission_status"] == "accepted_executable_runtime"
        and row["active_in_current_simulation"] is True
    } == M41A_OPERATION_IDS
    assert "greater_essence" in scope["active_operation_groups"]
    assert "greater_essence" not in scope["reference_only_operation_groups"]
    assert "greater_essence_magic_to_rare_route" not in scope["excluded_from_active_solver"]
    assert {
        row["operation_id"]
        for row in rows
        if row["group"] == "perfect_essence"
        and row["runtime_admission_status"] == "accepted_executable_runtime"
    } == M42A_OPERATION_IDS


@pytest.mark.parametrize("operation_id", sorted(M41A_OPERATION_IDS))
def test_m41a_resolves_canonical_guaranteed_modifier_and_applies_deterministically(
    operation_id: str,
) -> None:
    static = build_static_game_data(ROOT)
    state = _state()
    operation = _resolve(static, operation_id, state)
    output = next(
        row
        for row in static.essence_outputs["greater"]
        if row["operation_id"] == operation_id
    )
    canonical = static.modifier_index[operation.guaranteed_mod_id]

    assert operation.guaranteed_mod_id == output["guaranteed_mod_id"]
    assert operation.guaranteed_family_id == output["family_id"] == canonical.family_id
    assert operation.guaranteed_side == Side(output["side"]) == canonical.side
    assert canonical.static_category == "greater_essence"
    assert canonical.group_ids == tuple(sorted(output["group_ids"]))

    expected = replace(
        state,
        rarity=Rarity.RARE,
        modifiers=(ModifierInstance(operation.guaranteed_mod_id, crafted=True),),
    )
    path = GreaterEssenceHarness(static=static).enumerate_paths(
        initial_state=state,
        operation=operation,
    )[0]
    assert path.outcome == "applied"
    assert path.guaranteed_mod_id == operation.guaranteed_mod_id
    assert path.terminal_state_hash == expected.state_hash()
    assert (path.probability_numerator, path.probability_denominator) == (1, 1)


def test_m41a_preserves_existing_and_fractured_instances_atomically() -> None:
    static = build_static_game_data(ROOT)
    fractured = ModifierInstance("value_to_critical_hit_chance_t1", fractured=True)
    state = _state(fractured)
    operation = _resolve(static, "greater_essence_abrasion", state)
    expected = replace(
        state,
        rarity=Rarity.RARE,
        modifiers=state.modifiers
        + (ModifierInstance(operation.guaranteed_mod_id, crafted=True),),
    )

    path = GreaterEssenceHarness(static=static).enumerate_paths(
        initial_state=state,
        operation=operation,
    )[0]
    assert path.outcome == "applied"
    assert path.terminal_state_hash == expected.state_hash()
    assert expected.modifiers[0] == fractured


def test_m41a_family_conflict_is_no_transition_no_consumption() -> None:
    static = build_static_game_data(ROOT)
    state = _state(ModifierInstance("adds_value_to_value_physical_damage_t1"))
    operation = _resolve(static, "greater_essence_abrasion", state)

    path = GreaterEssenceHarness(static=static).enumerate_paths(
        initial_state=state,
        operation=operation,
    )[0]
    assert path.outcome == "no_transition_no_consumption"
    assert path.terminal_state_hash == state.state_hash()
    assert path.no_transition_reason == "post_state_duplicate_family_blocked"


def test_m41a_crafted_capacity_stays_explicit_source_open_shared_validation() -> None:
    static = build_static_game_data(ROOT)
    state = _state(
        ModifierInstance("value_to_critical_hit_chance_t1", crafted=True)
    )
    operation = _resolve(static, "greater_essence_abrasion", state)
    harness = GreaterEssenceHarness(static=static)

    path = harness.enumerate_paths(initial_state=state, operation=operation)[0]
    result = harness.run(
        initial_state=state,
        operation=operation,
        seed=41001,
        sample_count=1,
        run_id="m41a_crafted_capacity_source_open",
    )
    assert path.outcome == "no_transition_no_consumption"
    assert path.terminal_state_hash == state.state_hash()
    assert path.no_transition_reason == "post_state_crafted_capacity_exceeded"
    assert result.crafted_capacity_status == M41A_CRAFTED_CAPACITY_STATUS
    assert result.public_summary()["crafted_capacity_status"] == (
        "source_open_unverified_greater_only"
    )


def test_m41a_exact_and_seeded_paths_have_no_random_candidate_draw() -> None:
    static = build_static_game_data(ROOT)
    state = _state()
    operation = _resolve(static, "greater_essence_abrasion", state)
    harness = GreaterEssenceHarness(static=static)
    exact = harness.enumerate_terminal_distribution(
        initial_state=state,
        operation=operation,
    )
    left = harness.run(
        initial_state=state,
        operation=operation,
        seed=41001,
        sample_count=4,
        run_id="m41a_deterministic_replay",
    )
    replay = harness.run(
        initial_state=state,
        operation=operation,
        seed=41001,
        sample_count=4,
        run_id="m41a_deterministic_replay",
    )
    other_seed = harness.run(
        initial_state=state,
        operation=operation,
        seed=41002,
        sample_count=4,
        run_id="m41a_deterministic_replay",
    )

    assert left == replay
    assert left.decisions == other_seed.decisions == ()
    assert all(row.decision_id is None and row.candidate_count == 0 for row in left.trajectories)
    assert {row.post_state_hash for row in left.trajectories} == {
        exact[0].terminal_state_hash
    }
    assert {row.post_state_hash for row in other_seed.trajectories} == {
        exact[0].terminal_state_hash
    }


def test_m41a_invalid_rarity_remains_no_transition() -> None:
    static = build_static_game_data(ROOT)
    magic = _state()
    operation = _resolve(static, "greater_essence_abrasion", magic)
    rare = _state(rarity=Rarity.RARE)
    path = GreaterEssenceHarness(static=static).enumerate_paths(
        initial_state=rare,
        operation=operation,
    )[0]
    assert path.outcome == "no_transition_no_consumption"
    assert path.no_transition_reason == "invalid_source_rarity"


def test_m41a_missing_or_inconsistent_canonical_output_fails_closed() -> None:
    static = build_static_game_data(ROOT)
    state = _state()
    missing_index = dict(static.modifier_index)
    missing_index.pop("crafted_greater_abrasion_flat_physical")
    missing_static = replace(static, modifier_index=missing_index)
    with pytest.raises(M38AResolverAdmissionError, match="canonical index"):
        OperationResolver(static=missing_static).resolve(
            OperationResolverRequest(
                currency_id="greater_essence_abrasion",
                item_state=state,
            )
        )

    essence = yaml.safe_load((ROOT / "data/essence_outputs.yaml").read_text(encoding="utf-8"))
    row = next(
        row
        for row in essence["greater"]
        if row["operation_id"] == "greater_essence_abrasion"
    )
    row["family_id"] = "wrong_family"
    inconsistent_static = replace(static, essence_outputs=essence)
    with pytest.raises(M38AResolverAdmissionError, match="canonical contract mismatch"):
        OperationResolver(static=inconsistent_static).resolve(
            OperationResolverRequest(
                currency_id="greater_essence_abrasion",
                item_state=state,
            )
        )


def test_m41a_tampered_operation_contract_fails_hard() -> None:
    static = build_static_game_data(ROOT)
    state = _state()
    operation = replace(
        _resolve(static, "greater_essence_abrasion", state),
        guaranteed_family_id="wrong_family",
    )
    with pytest.raises(
        M41AGreaterEssenceInvariantViolation,
        match="canonical contract mismatch",
    ):
        GreaterEssenceHarness(static=static).enumerate_paths(
            initial_state=state,
            operation=operation,
        )
