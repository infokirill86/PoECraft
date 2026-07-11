from __future__ import annotations

from fractions import Fraction
from pathlib import Path

import pytest
import yaml

from p2c_engine.domain.enums import Rarity, Side
from p2c_engine.domain.item_state import ItemState, ModifierInstance
from p2c_engine.monte_carlo.annulment import AnnulmentMonteCarloHarness, AnnulmentOperation
from p2c_engine.monte_carlo.bounded_sequence import (
    BoundedAcceptedOperationSequenceHarness,
    BoundedSequenceRequest,
    BoundedSequenceStep,
)
from p2c_engine.monte_carlo.chaos_like import ChaosLikeMonteCarloHarness, ChaosLikeOperation
from p2c_engine.monte_carlo.greater_exaltation import GreaterExaltationHarness
from p2c_engine.monte_carlo.ordinary_add import (
    OrdinaryAddMonteCarloHarness,
    OrdinaryAddOperation,
    _append_ordinary_modifier,
)
from p2c_engine.monte_carlo.perfect_essence import PerfectEssenceHarness, PerfectEssenceOperation
from p2c_engine.monte_carlo.rarity_progression import CatalogSingleAddHarness, CatalogSingleAddOperation
from p2c_engine.operations.omen import (
    M45A_ACCEPTED_OMEN_IDS,
    M45AOmenAdmissionError,
    compile_omen_effects,
)
from p2c_engine.operations.resolver import (
    M45A_RESOLVER_SCHEMA_VERSION,
    M38AResolverAdmissionError,
    OperationResolver,
    OperationResolverRequest,
)
from p2c_engine.sampling.exact import branch_options
from p2c_engine.static_data import build_static_game_data


ROOT = Path(__file__).resolve().parents[2]
PREFIX_PHYSICAL = "adds_value_to_value_physical_damage_t1"
PREFIX_ACCURACY = "value_to_accuracy_rating_t1"
PREFIX_LOW_FRACTURED = "adds_value_to_value_fire_damage_t10"
SUFFIX_ATTACK_SPEED = "value_increased_attack_speed_t1"
SUFFIX_CRIT = "value_to_critical_hit_chance_t1"
SUFFIX_MELEE = "value_to_level_of_all_melee_skills_t1"


@pytest.fixture(scope="module")
def static():
    return build_static_game_data(ROOT)


def _state(*mods: ModifierInstance, rarity: Rarity = Rarity.RARE) -> ItemState:
    return ItemState(
        item_class="quarterstaff",
        rarity=rarity,
        item_level=82,
        modifiers=tuple(mods),
        unrevealed_desecrated=None,
        augment_socket_capacity=0,
        augment_socket_used=0,
        astrid_installed=False,
    )


def _resolve(static, currency_id: str, state: ItemState, *omens: str):
    return OperationResolver(static=static).resolve(
        OperationResolverRequest(
            currency_id=currency_id,
            item_state=state,
            mode_id=f"m45a_{currency_id}",
            active_modifier_ids=tuple(omens),
        )
    )


def _mass(row) -> Fraction:
    return Fraction(row.probability_numerator, row.probability_denominator)


def test_m45a_registry_admits_exactly_ten_rows_and_blocks_reference_rows(static) -> None:
    rows = {row["omen_id"]: row for row in static.omens["omens"]}
    admitted = {
        omen_id
        for omen_id, row in rows.items()
        if row["runtime_admission_status"] == "accepted_executable_modifier"
        and row["availability_status"] == "available_project_model"
    }
    assert admitted == M45A_ACCEPTED_OMEN_IDS
    assert all(
        rows[omen_id]["runtime_admission_status"] == "blocked_or_out_of_scope"
        for omen_id in set(rows) - admitted
    )


@pytest.mark.parametrize(
    ("currency_id", "omen_ids", "operation_type"),
    (
        ("exalted", ("sinistral_exaltation",), CatalogSingleAddOperation),
        (
            "perfect_exalted",
            ("greater_exaltation", "dextral_exaltation"),
            OrdinaryAddOperation,
        ),
        ("annulment", ("sinistral_annulment",), AnnulmentOperation),
        ("chaos", ("dextral_erasure", "whittling"), ChaosLikeOperation),
        (
            "perfect_essence_abrasion",
            ("sinistral_crystallisation",),
            PerfectEssenceOperation,
        ),
    ),
)
def test_m45a_resolver_compiles_only_pinned_effect_dimensions(
    static, currency_id, omen_ids, operation_type
) -> None:
    state = _state(
        ModifierInstance(PREFIX_ACCURACY),
        ModifierInstance(SUFFIX_ATTACK_SPEED),
    )
    plan = _resolve(static, currency_id, state, *omen_ids)
    assert plan.schema_version == M45A_RESOLVER_SCHEMA_VERSION
    assert isinstance(plan.operation, operation_type)
    assert plan.active_modifier_ids == tuple(sorted(omen_ids))
    assert plan.filters.add_count == (2 if "greater_exaltation" in omen_ids else 1)


def test_m45a_registry_fails_closed_on_duplicate_incompatible_unavailable_and_wrong_group(
    static,
) -> None:
    state = _state(ModifierInstance(PREFIX_ACCURACY), ModifierInstance(SUFFIX_ATTACK_SPEED))
    bad_requests = (
        ("exalted", ("sinistral_exaltation", "sinistral_exaltation")),
        ("exalted", ("sinistral_exaltation", "dextral_exaltation")),
        ("annulment", ("light",)),
        ("chaos", ("sinistral_annulment",)),
        ("chaos", ("unknown_omen",)),
    )
    for currency_id, omens in bad_requests:
        with pytest.raises(M38AResolverAdmissionError):
            _resolve(static, currency_id, state, *omens)

    raw = yaml.safe_load((ROOT / "data/omens.yaml").read_text(encoding="utf-8"))
    row = next(value for value in raw["omens"] if value["omen_id"] == "whittling")
    row["availability_status"] = "historical_or_unavailable"
    with pytest.raises(M45AOmenAdmissionError, match="not available"):
        compile_omen_effects(
            raw,
            operation_group="chaos",
            active_modifier_ids=("whittling",),
        )


def test_m45a_side_filters_are_load_bearing_at_the_correct_pool_stage(static) -> None:
    state = _state(
        ModifierInstance(PREFIX_ACCURACY),
        ModifierInstance(SUFFIX_ATTACK_SPEED),
        ModifierInstance(SUFFIX_CRIT, fractured=True),
    )

    exalted = _resolve(static, "exalted", state, "sinistral_exaltation").operation
    assert isinstance(exalted, CatalogSingleAddOperation)
    add_pool = CatalogSingleAddHarness(static=static).build_pool(state, exalted)
    assert add_pool.candidates
    assert {
        static.modifier_index[candidate.key].side for candidate in add_pool.candidates
    } == {Side.PREFIX}

    annulment = _resolve(static, "annulment", state, "sinistral_annulment").operation
    assert isinstance(annulment, AnnulmentOperation)
    removal_pool = AnnulmentMonteCarloHarness(static=static).build_pool(state, annulment)
    assert {row.side for row in removal_pool.removal_metadata} == {"prefix"}
    assert all(not row.fractured for row in removal_pool.removal_metadata)


def test_m45a_chaos_erasure_and_whittling_filter_removal_before_unchanged_add(static) -> None:
    state = _state(
        ModifierInstance(PREFIX_PHYSICAL),
        ModifierInstance(PREFIX_ACCURACY),
        ModifierInstance(PREFIX_LOW_FRACTURED, fractured=True),
        ModifierInstance(SUFFIX_ATTACK_SPEED),
    )
    operation = _resolve(
        static, "chaos", state, "sinistral_erasure", "whittling"
    ).operation
    assert isinstance(operation, ChaosLikeOperation)
    harness = ChaosLikeMonteCarloHarness(static=static)
    removal_pool = harness.build_removal_pool(state, operation)
    assert {row.side for row in removal_pool.removal_metadata} == {"prefix"}
    assert {row.modifier_level for row in removal_pool.removal_metadata} == {75}
    assert all(not row.fractured for row in removal_pool.removal_metadata)

    selected = removal_pool.removal_metadata[0]
    from p2c_engine.monte_carlo.annulment import _remove_modifier_instance

    post_removal = _remove_modifier_instance(state, selected)
    add_pool = harness.build_add_pool(post_removal, operation)
    assert add_pool.candidates
    side_stage = next(stage for stage in add_pool.stages if stage.stage_id == "side")
    assert dict((param.name, param.value) for param in side_stage.params)["side_filter"] is None


def test_m45a_crystallisation_filters_feasible_removal_not_guaranteed_add(static) -> None:
    state = _state(
        ModifierInstance(PREFIX_PHYSICAL),
        ModifierInstance(SUFFIX_ATTACK_SPEED),
    )
    operation = _resolve(
        static,
        "perfect_essence_abrasion",
        state,
        "dextral_crystallisation",
    ).operation
    assert isinstance(operation, PerfectEssenceOperation)
    harness = PerfectEssenceHarness(static=static)
    pool = harness.build_feasible_pool(state, operation)
    assert {row.side for row in pool.removal_metadata} == {"suffix"}
    paths = harness.enumerate_paths(
        initial_state=state,
        operation=operation,
        decision_id="m45a.crystallisation",
    )
    assert all(path.guaranteed_mod_id == operation.guaranteed_mod_id for path in paths)
    assert static.modifier_index[operation.guaranteed_mod_id].side == Side.PREFIX
    assert sum(_mass(path) for path in paths) == Fraction(1, 1)


def _greater_state() -> ItemState:
    return _state(
        ModifierInstance(PREFIX_ACCURACY),
        ModifierInstance(SUFFIX_ATTACK_SPEED),
        ModifierInstance(SUFFIX_CRIT, fractured=True),
        ModifierInstance(SUFFIX_MELEE),
    )


def test_m45a_greater_exaltation_is_atomic_exact_and_replayable(static) -> None:
    state = _greater_state()
    operation = _resolve(
        static,
        "perfect_exalted",
        state,
        "greater_exaltation",
        "sinistral_exaltation",
    ).operation
    assert isinstance(operation, OrdinaryAddOperation)
    harness = GreaterExaltationHarness(static=static)
    paths = harness.enumerate_paths(
        initial_state=state,
        operation=operation,
        decision_id_prefix="m45a.greater.exact",
    )
    assert paths and all(path.outcome == "completed" for path in paths)
    assert all(len(path.selected_mod_ids) == 2 for path in paths)
    assert all(
        all(static.modifier_index[mod_id].side == Side.PREFIX for mod_id in path.selected_mod_ids)
        for path in paths
    )
    assert sum(_mass(path) for path in paths) == Fraction(1, 1)
    terminals = harness.enumerate_terminal_distribution(
        initial_state=state,
        operation=operation,
        decision_id_prefix="m45a.greater.exact",
    )
    assert sum(_mass(row) for row in terminals) == Fraction(1, 1)
    assert any(row.path_count > 1 for row in terminals)

    run = harness.run(
        initial_state=state,
        operation=operation,
        seed=45_001,
        sample_count=64,
        run_id="m45a.greater.replay",
    )
    assert harness.verify_replay(
        initial_state=state, operation=operation, expected=run
    ) == run
    assert all(row.outcome == "completed" for row in run.trajectories)


def test_m45a_greater_exaltation_insufficient_side_capacity_rolls_back_before_draw(static) -> None:
    state = _state(
        ModifierInstance(PREFIX_PHYSICAL),
        ModifierInstance(PREFIX_ACCURACY),
        ModifierInstance(SUFFIX_ATTACK_SPEED),
        ModifierInstance(SUFFIX_CRIT, fractured=True),
        ModifierInstance(SUFFIX_MELEE),
    )
    operation = _resolve(
        static,
        "exalted",
        state,
        "greater_exaltation",
        "sinistral_exaltation",
    ).operation
    harness = GreaterExaltationHarness(static=static)
    paths = harness.enumerate_paths(
        initial_state=state,
        operation=operation,
        decision_id_prefix="m45a.rollback",
    )
    assert len(paths) == 1
    assert paths[0].outcome == "no_transition_no_consumption"
    assert paths[0].terminal_state == state
    assert paths[0].selected_mod_ids == ()


def _direct_projection(static, state, currency_id, omen_ids):
    plan = _resolve(static, currency_id, state, *omen_ids)
    operation = plan.operation
    decision_id = f"m45a.parity.step_0.{currency_id}.m45a_{currency_id}"
    if plan.filters.add_count == 2:
        rows = GreaterExaltationHarness(static=static).enumerate_terminal_distribution(
            initial_state=state,
            operation=operation,
            decision_id_prefix=decision_id,
        )
    elif isinstance(operation, CatalogSingleAddOperation):
        rows = CatalogSingleAddHarness(static=static).enumerate_terminal_distribution(
            initial_state=state, operation=operation, decision_id=decision_id
        )
    elif isinstance(operation, OrdinaryAddOperation):
        pool = OrdinaryAddMonteCarloHarness(static=static).build_pool(state, operation)
        output = {}
        for option in branch_options(decision_id, pool.candidates):
            terminal = _append_ordinary_modifier(state, option.selected_key)
            output[terminal.state_hash()] = output.get(
                terminal.state_hash(), Fraction(0, 1)
            ) + Fraction(option.probability_numerator, option.probability_denominator)
        return output
    elif isinstance(operation, AnnulmentOperation):
        rows = AnnulmentMonteCarloHarness(static=static).enumerate_terminal_distribution(
            state=state, operation=operation, decision_id=decision_id
        )
    elif isinstance(operation, ChaosLikeOperation):
        rows = ChaosLikeMonteCarloHarness(static=static).enumerate_terminal_distribution(
            initial_state=state,
            operation=operation,
            decision_id_prefix="m45a.parity",
            max_exact_paths=65_536,
        )
    elif isinstance(operation, PerfectEssenceOperation):
        rows = PerfectEssenceHarness(static=static).enumerate_terminal_distribution(
            initial_state=state, operation=operation, decision_id=decision_id
        )
    else:  # pragma: no cover
        raise AssertionError(type(operation))
    return {row.terminal_state_hash: _mass(row) for row in rows}


@pytest.mark.parametrize(
    ("currency_id", "omen_ids", "state"),
    (
        ("exalted", ("sinistral_exaltation",), _state(ModifierInstance(SUFFIX_CRIT, fractured=True))),
        ("perfect_exalted", ("greater_exaltation", "sinistral_exaltation"), _greater_state()),
        (
            "annulment",
            ("sinistral_annulment",),
            _state(ModifierInstance(PREFIX_ACCURACY), ModifierInstance(SUFFIX_CRIT, fractured=True)),
        ),
        (
            "chaos",
            ("dextral_erasure",),
            _state(
                ModifierInstance(PREFIX_ACCURACY),
                ModifierInstance(SUFFIX_ATTACK_SPEED),
                ModifierInstance(SUFFIX_CRIT, fractured=True),
            ),
        ),
        (
            "perfect_essence_abrasion",
            ("sinistral_crystallisation",),
            _state(ModifierInstance(PREFIX_PHYSICAL), ModifierInstance(SUFFIX_ATTACK_SPEED)),
        ),
    ),
)
def test_m45a_direct_resolver_and_m43a_one_step_exact_parity(
    static, currency_id, omen_ids, state
) -> None:
    direct = _direct_projection(static, state, currency_id, omen_ids)
    request = BoundedSequenceRequest(
        sequence_id=f"m45a_parity_{currency_id}",
        steps=(
            BoundedSequenceStep(
                step_id="step_0",
                currency_id=currency_id,
                mode_id=f"m45a_{currency_id}",
                active_modifier_ids=omen_ids,
            ),
        ),
    )
    exact = BoundedAcceptedOperationSequenceHarness(static=static).enumerate_exact(
        initial_state=state,
        request=request,
        decision_id_prefix="m45a.parity",
    )
    sequence_projection = {
        row.terminal_state_hash: _mass(row) for row in exact.state_only_projection()
    }
    assert exact.ceiling_stop is None
    assert sequence_projection == direct


def test_m45a_m43a_seeded_replay_preserves_modifier_diagnostics(static) -> None:
    state = _greater_state()
    request = BoundedSequenceRequest(
        sequence_id="m45a_sequence_replay",
        steps=(
            BoundedSequenceStep(
                step_id="greater_exaltation",
                currency_id="perfect_exalted",
                mode_id="m45a_perfect_exalted",
                active_modifier_ids=("greater_exaltation", "sinistral_exaltation"),
            ),
        ),
    )
    harness = BoundedAcceptedOperationSequenceHarness(static=static)
    run = harness.run(
        initial_state=state,
        request=request,
        seed=45_002,
        sample_count=32,
        run_id="m45a.sequence.replay",
    )
    assert harness.verify_replay(
        initial_state=state, request=request, expected=run
    ) == run
    assert all(len(row.steps[0].selected_keys) == 2 for row in run.trajectories)
    assert all(row.steps[0].resolver_plan_digest for row in run.trajectories)
