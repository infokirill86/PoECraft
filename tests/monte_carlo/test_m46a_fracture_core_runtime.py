from __future__ import annotations

import math
from collections import Counter
from dataclasses import replace
from fractions import Fraction
from pathlib import Path

import pytest

from p2c_engine.decisions import RecordingDecisionSource, SeededDecisionSource
from p2c_engine.domain.candidate import Candidate
from p2c_engine.domain.enums import Rarity, Side
from p2c_engine.domain.item_state import (
    DesecratedPlaceholder,
    ItemState,
    ModifierInstance,
)
from p2c_engine.legality.capacity import capacity_snapshot
from p2c_engine.monte_carlo.alchemy import AlchemyHarness, AlchemyOperation
from p2c_engine.monte_carlo.annulment import AnnulmentMonteCarloHarness, AnnulmentOperation
from p2c_engine.monte_carlo.bounded_sequence import (
    AcceptedOperationExecutorRegistry,
    BoundedAcceptedOperationSequenceHarness,
    BoundedSequenceRequest,
    BoundedSequenceStep,
)
from p2c_engine.monte_carlo.chaos_like import ChaosLikeMonteCarloHarness, ChaosLikeOperation
from p2c_engine.monte_carlo.fracture import (
    FRACTURING_ORB_OPERATION_ID,
    M46A_FIXED_SEEDS,
    M46A_FRACTURE_SCHEMA_VERSION,
    M46A_FRACTURE_SEMANTICS_VERSION,
    M46AFractureInvariantViolation,
    FractureHarness,
    FractureOperation,
    build_fracture_pool,
)
from p2c_engine.monte_carlo.perfect_essence import PerfectEssenceHarness, PerfectEssenceOperation
from p2c_engine.operations import (
    M38AResolverAdmissionError,
    M46A_RESOLVER_SCHEMA_VERSION,
    OperationResolver,
    OperationResolverRequest,
)
from p2c_engine.static_data import build_static_game_data


ROOT = Path(__file__).resolve().parents[2]
PREFIX_PHYSICAL = "adds_value_to_value_physical_damage_t1"
PREFIX_ACCURACY = "value_to_accuracy_rating_t1"
SUFFIX_ATTACK_SPEED = "value_increased_attack_speed_t1"
SUFFIX_CRIT = "value_to_critical_hit_chance_t1"


@pytest.fixture(scope="module")
def static():
    return build_static_game_data(ROOT)


def _state(
    *modifiers: ModifierInstance,
    rarity: Rarity = Rarity.RARE,
    placeholder: DesecratedPlaceholder | None = None,
    item_class: str = "quarterstaff",
) -> ItemState:
    return ItemState(
        item_class=item_class,
        rarity=rarity,
        item_level=82,
        modifiers=tuple(modifiers),
        unrevealed_desecrated=placeholder,
        augment_socket_capacity=0,
        augment_socket_used=0,
        astrid_installed=False,
    )


def _clean_state(*, crafted: bool = True) -> ItemState:
    return _state(
        ModifierInstance(PREFIX_PHYSICAL),
        ModifierInstance(PREFIX_ACCURACY, crafted=crafted),
        ModifierInstance(SUFFIX_ATTACK_SPEED),
        ModifierInstance(SUFFIX_CRIT),
    )


def _operation(mode_id: str = "m46a_fracture") -> FractureOperation:
    return FractureOperation(mode_id=mode_id)


def _mass(row: object) -> Fraction:
    return Fraction(  # type: ignore[attr-defined]
        row.probability_numerator, row.probability_denominator
    )


def _resolved_fracture(static, state: ItemState, *, mode_id: str = "m46a_fracture"):
    plan = OperationResolver(static=static).resolve(
        OperationResolverRequest(
            currency_id=FRACTURING_ORB_OPERATION_ID,
            item_state=state,
            mode_id=mode_id,
        )
    )
    assert plan.schema_version == M46A_RESOLVER_SCHEMA_VERSION
    assert isinstance(plan.operation, FractureOperation)
    return plan


def test_m46a_admission_and_execution_contract_are_exactly_pinned(static) -> None:
    row = next(
        row
        for row in static.operations["operations"]
        if row["operation_id"] == FRACTURING_ORB_OPERATION_ID
    )
    assert row["runtime_admission_status"] == "accepted_executable_runtime"
    assert row["active_in_current_simulation"] is True
    assert row["transition"]["target"]["selection_scope"] == "combined_prefix_suffix"
    assert row["transition"]["target"]["weighting"] == "uniform_instance_identity"
    assert "fracture" in static.project_scope["active_operation_groups"]
    assert "fracture" not in (static.project_scope["reference_only_operation_groups"] or ())
    assert AcceptedOperationExecutorRegistry().mapping[FRACTURING_ORB_OPERATION_ID] == "fracture"
    assert M46A_FRACTURE_SCHEMA_VERSION == "p2c.m46a.fracture_core_runtime.v1"
    assert M46A_FRACTURE_SEMANTICS_VERSION == "p2c.m46.fracture_core.project_model.v1"


def test_m46a_combined_pool_is_uniform_and_includes_crafted_instances(static) -> None:
    state = _clean_state()
    harness = FractureHarness(static=static)
    pool = harness.build_pool(state, _operation())
    paths = harness.enumerate_paths(
        state=state,
        operation=_operation(),
        decision_id="m46a.exact.combined_uniform",
    )

    assert len(pool.candidates) == len(state.modifiers) == 4
    assert {candidate.weight for candidate in pool.candidates} == {1}
    assert {row.side for row in pool.metadata} == {"prefix", "suffix"}
    assert {row.mod_id for row in pool.metadata} == {
        PREFIX_PHYSICAL,
        PREFIX_ACCURACY,
        SUFFIX_ATTACK_SPEED,
        SUFFIX_CRIT,
    }
    assert next(row for row in pool.metadata if row.mod_id == PREFIX_ACCURACY).crafted is True
    assert len(paths) == 4
    assert len({_mass(path) for path in paths}) == 1
    assert sum((_mass(path) for path in paths), Fraction()) == Fraction(1, 1)


def test_m46a_crafted_selection_preserves_crafted_and_changes_one_flag(static) -> None:
    state = _clean_state()
    path = next(
        path
        for path in FractureHarness(static=static).enumerate_paths(
            state=state,
            operation=_operation(),
            decision_id="m46a.exact.crafted",
        )
        if path.selected_mod_id == PREFIX_ACCURACY
    )
    selected = next(
        row for row in path.terminal_state.modifiers if row.mod_id == PREFIX_ACCURACY
    )
    assert selected == ModifierInstance(PREFIX_ACCURACY, crafted=True, fractured=True)
    assert len(path.terminal_state.modifiers) == len(state.modifiers)
    assert sum(row.fractured for row in path.terminal_state.modifiers) == 1
    assert path.terminal_state.with_modifiers(state.modifiers) == state


@pytest.mark.parametrize(
    ("state", "reason"),
    (
        (_state(ModifierInstance(PREFIX_PHYSICAL)), "at_least_four_explicit_modifiers_required"),
        (
            _state(
                ModifierInstance(PREFIX_PHYSICAL),
                ModifierInstance(PREFIX_ACCURACY),
                ModifierInstance(SUFFIX_ATTACK_SPEED),
                ModifierInstance(SUFFIX_CRIT),
                rarity=Rarity.MAGIC,
            ),
            "rare_input_required",
        ),
        (
            _state(
                ModifierInstance(PREFIX_PHYSICAL, fractured=True),
                ModifierInstance(PREFIX_ACCURACY),
                ModifierInstance(SUFFIX_ATTACK_SPEED),
                ModifierInstance(SUFFIX_CRIT),
            ),
            "existing_fractured_modifier_forbidden",
        ),
        (
            _state(
                ModifierInstance(PREFIX_PHYSICAL, desecrated=True),
                ModifierInstance(PREFIX_ACCURACY),
                ModifierInstance(SUFFIX_ATTACK_SPEED),
                ModifierInstance(SUFFIX_CRIT),
            ),
            "desecrated_modifier_state_forbidden",
        ),
    ),
)
def test_m46a_invalid_inputs_fail_closed_without_mutation(static, state, reason) -> None:
    path = FractureHarness(static=static).enumerate_paths(
        state=state,
        operation=_operation(),
        decision_id=f"m46a.invalid.{reason}",
    )[0]
    assert path.outcome == "no_transition_no_consumption"
    assert path.no_transition_reason == reason
    assert path.terminal_state == state
    assert path.terminal_state_hash == state.state_hash()
    assert _mass(path) == Fraction(1, 1)


def test_m46a_unknown_modifier_and_nonquarterstaff_fail_closed(static) -> None:
    unknown = _state(
        ModifierInstance("unknown_mod"),
        ModifierInstance(PREFIX_ACCURACY),
        ModifierInstance(SUFFIX_ATTACK_SPEED),
        ModifierInstance(SUFFIX_CRIT),
    )
    wrong_class = replace(_clean_state(), item_class="bow")
    harness = FractureHarness(static=static)
    assert harness.build_pool(unknown, _operation()).empty_reason == "unknown_installed_modifier"
    assert harness.build_pool(wrong_class, _operation()).empty_reason == "unsupported_item_class"


def test_m46a_negative_control_proves_nonuniform_pool_fails_hard(static) -> None:
    def bad_builder(state, operation, game_data):
        valid = build_fracture_pool(state, operation, game_data)
        return replace(
            valid,
            candidates=(replace(valid.candidates[0], weight=2),) + valid.candidates[1:],
        )

    with pytest.raises(M46AFractureInvariantViolation, match="uniform unit weight"):
        FractureHarness(static=static, pool_builder=bad_builder).enumerate_paths(
            state=_clean_state(),
            operation=_operation(),
            decision_id="m46a.negative.nonuniform",
        )


def test_m46a_seeded_replay_and_internal_mc_match_exact_envelope(static) -> None:
    state = _clean_state()
    harness = FractureHarness(static=static)
    sample_count = 8_192
    first = harness.run(
        initial_state=state,
        operation=_operation(),
        seed=M46A_FIXED_SEEDS[0],
        sample_count=sample_count,
        run_id="m46a.replay",
    )
    second = harness.run(
        initial_state=state,
        operation=_operation(),
        seed=M46A_FIXED_SEEDS[0],
        sample_count=sample_count,
        run_id="m46a.replay",
    )
    counts = Counter(row.selected_candidate_key for row in first.trajectories)
    expected_count = sample_count / len(state.modifiers)
    tolerance = math.ceil(
        6 * math.sqrt(sample_count * (1 / len(state.modifiers)) * (1 - 1 / len(state.modifiers)))
    )
    assert first.result_hash == second.result_hash
    assert first.trajectories == second.trajectories
    assert set(counts) == {
        row.candidate_key for row in harness.build_pool(state, _operation()).metadata
    }
    assert all(abs(value - expected_count) <= tolerance for value in counts.values())


def test_m46a_fractured_immutability_across_accepted_removal_and_capacity(static) -> None:
    original = _clean_state(crafted=False)
    fracture_path = next(
        path
        for path in FractureHarness(static=static).enumerate_paths(
            state=original,
            operation=_operation(),
            decision_id="m46a.immutability",
        )
        if path.selected_mod_id == PREFIX_PHYSICAL
    )
    fractured = fracture_path.terminal_state

    annul_pool = AnnulmentMonteCarloHarness(static=static).build_pool(
        fractured, AnnulmentOperation(mode_id="m46a_annulment_guard")
    )
    chaos_pool = ChaosLikeMonteCarloHarness(static=static).build_removal_pool(
        fractured, ChaosLikeOperation(mode_id="m46a_chaos_guard")
    )
    perfect_plan = OperationResolver(static=static).resolve(
        OperationResolverRequest(
            currency_id="perfect_essence_flames",
            item_state=fractured,
            mode_id="m46a_perfect_guard",
        )
    )
    assert isinstance(perfect_plan.operation, PerfectEssenceOperation)
    perfect_pool = PerfectEssenceHarness(static=static).build_feasible_pool(
        fractured, perfect_plan.operation
    )

    assert PREFIX_PHYSICAL not in {row.mod_id for row in annul_pool.removal_metadata}
    assert PREFIX_PHYSICAL not in {row.mod_id for row in chaos_pool.removal_metadata}
    assert PREFIX_PHYSICAL not in {row.mod_id for row in perfect_pool.removal_metadata}
    before = capacity_snapshot(original, static)
    after = capacity_snapshot(fractured, static)
    assert (before.prefix_used, before.suffix_used, before.total_used) == (
        after.prefix_used,
        after.suffix_used,
        after.total_used,
    )


def test_m46a_alchemy_remains_fail_closed_on_fractured_input(static) -> None:
    state = _state(
        ModifierInstance(PREFIX_PHYSICAL, fractured=True), rarity=Rarity.MAGIC
    )
    operation = AlchemyOperation(
        mode_id="m46a_alchemy_guard",
        item_class="quarterstaff",
        input_rarities=(Rarity.NORMAL, Rarity.MAGIC),
    )
    path = AlchemyHarness(static=static).enumerate_paths(
        initial_state=state,
        operation=operation,
        decision_id_prefix="m46a.alchemy_guard",
    )[0]
    assert path.outcome == "no_transition_no_consumption"
    assert path.no_transition_reason == "fractured_input_not_admitted"
    assert path.terminal_state_hash == state.state_hash()


def test_m46a_direct_resolver_and_m43a_exact_and_seeded_parity(static) -> None:
    state = _clean_state()
    mode_id = "m46a_parity"
    operation = _resolved_fracture(static, state, mode_id=mode_id).operation
    direct = FractureHarness(static=static)
    direct_terminals = direct.enumerate_terminal_distribution(
        state=state,
        operation=operation,
        decision_id="m46a.parity.step_0.fracturing_orb.m46a_parity",
    )
    request = BoundedSequenceRequest(
        sequence_id="m46a_parity",
        steps=(
            BoundedSequenceStep(
                step_id="fracture",
                currency_id=FRACTURING_ORB_OPERATION_ID,
                mode_id=mode_id,
            ),
        ),
    )
    sequence = BoundedAcceptedOperationSequenceHarness(static=static)
    exact = sequence.enumerate_exact(
        initial_state=state,
        request=request,
        decision_id_prefix="m46a.parity",
    )
    assert {
        row.terminal_state_hash: _mass(row) for row in direct_terminals
    } == {
        row.terminal_state_hash: _mass(row) for row in exact.state_only_projection()
    }

    seed = M46A_FIXED_SEEDS[1]
    run_id = "m46a.seeded_parity"
    source = RecordingDecisionSource(SeededDecisionSource(seed))
    direct_sample = direct.sample_once(
        state=state,
        operation=operation,
        decision_source=source,
        sample_index=0,
        run_id=run_id,
    )
    sampled = sequence.run(
        initial_state=state,
        request=request,
        seed=seed,
        sample_count=1,
        run_id=run_id,
    )
    assert sampled.trajectories[0].terminal_state_hash == direct_sample.post_state_hash
    assert sampled.decisions == source.records


def test_m46a_resolver_fails_closed_on_variant_omen_and_wrong_rarity(static) -> None:
    resolver = OperationResolver(static=static)
    with pytest.raises(M38AResolverAdmissionError, match="variants"):
        resolver.resolve(
            OperationResolverRequest(
                currency_id=FRACTURING_ORB_OPERATION_ID,
                item_state=_clean_state(),
                variant_id="side_directed",
            )
        )
    with pytest.raises(M38AResolverAdmissionError, match="modifier"):
        resolver.resolve(
            OperationResolverRequest(
                currency_id=FRACTURING_ORB_OPERATION_ID,
                item_state=_clean_state(),
                active_modifier_ids=("whittling",),
            )
        )
    with pytest.raises(M38AResolverAdmissionError, match="rarity"):
        resolver.resolve(
            OperationResolverRequest(
                currency_id=FRACTURING_ORB_OPERATION_ID,
                item_state=replace(_clean_state(), rarity=Rarity.MAGIC),
            )
        )


def test_m46a_public_summary_remains_numeric_probability_free(static) -> None:
    result = FractureHarness(static=static).run(
        initial_state=_clean_state(),
        operation=_operation(),
        seed=M46A_FIXED_SEEDS[2],
        sample_count=4,
        run_id="m46a.public_summary",
    )
    summary = result.public_summary()
    assert summary["numeric_probability_free"] is True
    assert summary["public_numeric_release"] is False
    assert summary["probability_values_printed"] is False
    assert not ({"probability", "percent", "expected_attempts", "ev", "ranking"} & set(summary))
