from __future__ import annotations

from collections import Counter
from dataclasses import replace
from fractions import Fraction
from pathlib import Path

import pytest

from p2c_engine.decisions import RecordingDecisionSource, SeededDecisionSource
from p2c_engine.domain.enums import Rarity, Side
from p2c_engine.domain.item_state import DesecratedPlaceholder, ItemState, ModifierInstance
from p2c_engine.monte_carlo.bounded_sequence import (
    AcceptedOperationExecutorRegistry,
    BoundedAcceptedOperationSequenceHarness,
    BoundedSequenceRequest,
    BoundedSequenceStep,
)
from p2c_engine.monte_carlo.fracture import FractureHarness, FractureOperation
from p2c_engine.monte_carlo.jawbone import (
    M47A1_FIXED_SEEDS,
    M47A1_OPERATION_IDS,
    M47A1_SCHEMA_VERSION,
    M47A1JawboneInvariantViolation,
    JawboneHarness,
    JawboneOperation,
    _validate_pool,
)
from p2c_engine.operations import (
    M38AResolverAdmissionError,
    M47A1_RESOLVER_SCHEMA_VERSION,
    OperationResolver,
    OperationResolverRequest,
)
from p2c_engine.static_data import build_static_game_data


ROOT = Path(__file__).resolve().parents[2]
P1 = "adds_value_to_value_physical_damage_t1"
P2 = "value_to_accuracy_rating_t1"
P3 = "value_increased_elemental_damage_with_attacks_t1"
S1 = "value_increased_attack_speed_t1"
S2 = "value_to_critical_hit_chance_t1"
S3 = "value_to_dexterity_t1"


@pytest.fixture(scope="module")
def static():
    return build_static_game_data(ROOT)


def _state(
    *mods: ModifierInstance,
    item_level: int = 82,
    placeholder: DesecratedPlaceholder | None = None,
) -> ItemState:
    return ItemState(
        item_class="quarterstaff",
        rarity=Rarity.RARE,
        item_level=item_level,
        modifiers=tuple(mods),
        unrevealed_desecrated=placeholder,
        augment_socket_capacity=0,
        augment_socket_used=0,
        astrid_installed=False,
    )


def _operation(operation_id: str = "preserved_jawbone") -> JawboneOperation:
    return JawboneOperation(
        mode_id="m47a1_test",
        operation_id=operation_id,
        item_level_max=64 if operation_id == "gnawed_jawbone" else None,
        reveal_mml=40 if operation_id == "ancient_jawbone" else None,
    )


def _mass(row) -> Fraction:
    return Fraction(row.probability_numerator, row.probability_denominator)


def _full_state(*, fractured_first: bool = False) -> ItemState:
    return _state(
        ModifierInstance(P1, fractured=fractured_first),
        ModifierInstance(P2, crafted=True),
        ModifierInstance(P3),
        ModifierInstance(S1),
        ModifierInstance(S2),
        ModifierInstance(S3),
    )


def test_m47a1_three_rows_are_admitted_and_resolver_compiles_data_contract(static) -> None:
    rows = {
        row["operation_id"]: row
        for row in static.operations["operations"]
        if row["operation_id"] in M47A1_OPERATION_IDS
    }
    assert set(rows) == set(M47A1_OPERATION_IDS)
    assert all(row["runtime_admission_status"] == "accepted_executable_runtime" for row in rows.values())
    assert all(row["transition"]["replacement"]["only_when_item_fully_occupied"] is True for row in rows.values())
    registry = AcceptedOperationExecutorRegistry().mapping
    assert all(registry[row_id] == "jawbone" for row_id in M47A1_OPERATION_IDS)

    for operation_id in M47A1_OPERATION_IDS:
        state = _state(ModifierInstance(P1), ModifierInstance(S1), item_level=60)
        plan = OperationResolver(static=static).resolve(
            OperationResolverRequest(currency_id=operation_id, item_state=state)
        )
        assert plan.schema_version == M47A1_RESOLVER_SCHEMA_VERSION
        assert isinstance(plan.operation, JawboneOperation)
        assert plan.operation.item_level_max == (64 if operation_id == "gnawed_jawbone" else None)
        assert plan.operation.reveal_mml == (40 if operation_id == "ancient_jawbone" else None)


def test_m47a1_d1_uses_only_free_side_and_never_replaces(static) -> None:
    one_free = _state(
        ModifierInstance(P1), ModifierInstance(P2), ModifierInstance(P3), ModifierInstance(S1)
    )
    harness = JawboneHarness(static=static)
    pool = harness.build_pool(one_free, _operation())
    paths = harness.enumerate_paths(
        state=one_free, operation=_operation(), decision_id="m47a1.d1.one_free"
    )
    assert pool.policy_branch == "d1_free_capacity"
    assert [row.side for row in pool.metadata] == [Side.SUFFIX]
    assert len(paths) == 1
    assert paths[0].terminal_state.modifiers == one_free.modifiers
    assert paths[0].terminal_state.unrevealed_desecrated.side is Side.SUFFIX

    both_free = _state(ModifierInstance(P1), ModifierInstance(S1))
    paths = harness.enumerate_paths(
        state=both_free, operation=_operation(), decision_id="m47a1.d1.both_free"
    )
    assert {row.selected_side for row in paths} == {Side.PREFIX, Side.SUFFIX}
    assert {row.candidate_count for row in paths} == {2}
    assert sum((_mass(row) for row in paths), Fraction()) == Fraction(1, 1)
    assert len({_mass(row) for row in paths}) == 1
    assert all(row.terminal_state.modifiers == both_free.modifiers for row in paths)


def test_m47a1_d2_full_item_uniformly_replaces_nonfractured_instance(static) -> None:
    state = _full_state(fractured_first=True)
    harness = JawboneHarness(static=static)
    pool = harness.build_pool(state, _operation())
    paths = harness.enumerate_paths(
        state=state, operation=_operation(), decision_id="m47a1.d2.full"
    )
    assert pool.policy_branch == "d2_full_item_replacement"
    assert len(pool.candidates) == 5
    assert P1 not in {row.mod_id for row in pool.metadata}
    assert {candidate.weight for candidate in pool.candidates} == {1}
    assert sum((_mass(row) for row in paths), Fraction()) == Fraction(1, 1)
    assert len({_mass(row) for row in paths}) == 1
    for path in paths:
        terminal = path.terminal_state
        assert len(terminal.modifiers) == 5
        assert ModifierInstance(P1, fractured=True) in terminal.modifiers
        assert terminal.unrevealed_desecrated is not None
        removed_side = next(
            row.side for row in pool.metadata if row.candidate_key == path.path_key
        )
        assert terminal.unrevealed_desecrated.side is removed_side


def test_m47a1_row_preconditions_one_desecrated_invariant_and_atomic_failure(static) -> None:
    harness = JawboneHarness(static=static)
    existing = DesecratedPlaceholder(Side.PREFIX, "preserved_jawbone", None, None)
    cases = (
        (_state(ModifierInstance(P1), item_level=65), _operation("gnawed_jawbone"), "item_level_above_jawbone_maximum"),
        (_state(ModifierInstance(P1), placeholder=existing), _operation(), "desecrated_limit_reached"),
        (_state(ModifierInstance(P1, desecrated=True)), _operation(), "desecrated_limit_reached"),
    )
    for state, operation, reason in cases:
        path = harness.enumerate_paths(
            state=state, operation=operation, decision_id=f"m47a1.fail.{reason}"
        )[0]
        assert path.outcome == "no_transition_no_consumption"
        assert path.no_transition_reason == reason
        assert path.terminal_state == state
        assert path.terminal_state_hash == state.state_hash()
        assert _mass(path) == Fraction(1, 1)


def test_m47a1_ancient_stores_hidden_canonical_context(static) -> None:
    state = _state(ModifierInstance(P1), ModifierInstance(S1))
    path = JawboneHarness(static=static).enumerate_paths(
        state=state,
        operation=_operation("ancient_jawbone"),
        decision_id="m47a1.ancient.context",
    )[0]
    placeholder = path.terminal_state.unrevealed_desecrated
    assert placeholder is not None
    assert placeholder.jawbone_id == "ancient_jawbone"
    assert placeholder.reveal_mml == 40
    assert placeholder.lich_tag_constraint is None


def test_m47a1_fracture_counts_placeholder_but_never_targets_it(static) -> None:
    state = _state(
        ModifierInstance(P1),
        ModifierInstance(P2),
        ModifierInstance(S1),
        placeholder=DesecratedPlaceholder(Side.SUFFIX, "ancient_jawbone", 40, None),
    )
    pool = FractureHarness(static=static).build_pool(
        state, FractureOperation(mode_id="m47a1_fracture_extension")
    )
    assert len(pool.candidates) == 3
    assert {row.mod_id for row in pool.metadata} == {P1, P2, S1}
    assert all("placeholder" not in candidate.key for candidate in pool.candidates)


def test_m47a1_seeded_replay_exact_and_sequence_one_step_parity(static) -> None:
    state = _state(ModifierInstance(P1), ModifierInstance(S1))
    operation = _operation("ancient_jawbone")
    harness = JawboneHarness(static=static)
    first = harness.run(
        initial_state=state,
        operation=operation,
        seed=M47A1_FIXED_SEEDS[0],
        sample_count=512,
        run_id="m47a1.replay",
    )
    second = harness.run(
        initial_state=state,
        operation=operation,
        seed=M47A1_FIXED_SEEDS[0],
        sample_count=512,
        run_id="m47a1.replay",
    )
    assert first == second
    assert set(Counter(row.selected_side for row in first.trajectories)) == {Side.PREFIX, Side.SUFFIX}

    request = BoundedSequenceRequest(
        sequence_id="m47a1_one_step",
        steps=(BoundedSequenceStep("jawbone", "ancient_jawbone", "m47a1_test"),),
    )
    exact = BoundedAcceptedOperationSequenceHarness(static=static).enumerate_exact(
        initial_state=state,
        request=request,
        decision_id_prefix="m47a1.parity",
    )
    direct = harness.enumerate_terminal_distribution(
        state=state,
        operation=operation,
        decision_id="m47a1.parity.step_0.ancient_jawbone.m47a1_test",
    )
    assert {row.terminal_state_hash: _mass(row) for row in direct} == {
        row.terminal_state_hash: _mass(row) for row in exact.state_only_projection()
    }

    seed = M47A1_FIXED_SEEDS[1]
    source = RecordingDecisionSource(SeededDecisionSource(seed))
    direct_sample = harness.sample_once(
        state=state,
        operation=operation,
        decision_source=source,
        sample_index=0,
        run_id="m47a1.seeded",
    )
    sampled = BoundedAcceptedOperationSequenceHarness(static=static).run(
        initial_state=state,
        request=request,
        seed=seed,
        sample_count=1,
        run_id="m47a1.seeded",
    )
    assert sampled.trajectories[0].terminal_state_hash == direct_sample.post_state_hash
    assert sampled.decisions == source.records


def test_m47a1_negative_control_and_fail_closed_layers(static) -> None:
    state = _state(ModifierInstance(P1), ModifierInstance(S1))
    pool = JawboneHarness(static=static).build_pool(state, _operation())
    with pytest.raises(M47A1JawboneInvariantViolation, match="uniform unit weights"):
        _validate_pool(
            replace(
                pool,
                candidates=(replace(pool.candidates[0], weight=2),) + pool.candidates[1:],
            )
        )
    resolver = OperationResolver(static=static)
    with pytest.raises(M38AResolverAdmissionError, match="modifier"):
        resolver.resolve(
            OperationResolverRequest(
                currency_id="preserved_jawbone",
                item_state=state,
                active_modifier_ids=("omen_of_putrefaction",),
            )
        )
    with pytest.raises(M38AResolverAdmissionError, match="not executable-admitted"):
        resolver.resolve(
            OperationResolverRequest(currency_id="reveal_desecrated", item_state=state)
        )


def test_m47a1_public_summary_has_no_numeric_probability_release(static) -> None:
    result = JawboneHarness(static=static).run(
        initial_state=_state(ModifierInstance(P1), ModifierInstance(S1)),
        operation=_operation(),
        seed=M47A1_FIXED_SEEDS[2],
        sample_count=4,
        run_id="m47a1.public",
    )
    summary = result.public_summary()
    assert summary["numeric_probability_free"] is True
    assert summary["public_numeric_release"] is False
    assert summary["probability_values_printed"] is False
    assert not ({"probability", "percent", "ev", "ranking"} & set(summary))
    assert M47A1_SCHEMA_VERSION == "p2c.m47a1.jawbone_placeholder_runtime.v1"
