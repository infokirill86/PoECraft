from __future__ import annotations

from dataclasses import fields, replace
from fractions import Fraction
from pathlib import Path

import pytest

from p2c_engine.domain.enums import Rarity, Side
from p2c_engine.domain.item_state import ItemState, ModifierInstance
from p2c_engine.monte_carlo.bounded_branching import (
    AcceptedPredicateRegistry,
    AcceptedSuccessClassifier,
    BoundedBranchingRequest,
    BoundedBranchingRouteHarness,
    M48A_MAX_EDGES,
    M48A_MAX_NODES,
    M48A_MAX_OPERATION_STEPS,
    M48A_SUCCESS_PREDICATE_ID,
    M48ABranchingInvariantViolation,
    M48APredicateError,
    M48ARouteAdmissionError,
    OperationRouteNode,
    PredicateDecision,
    PredicateRouteNode,
    TerminalRouteNode,
)
from p2c_engine.monte_carlo.bounded_sequence import (
    BoundedAcceptedOperationSequenceHarness,
    BoundedSequenceRequest,
    BoundedSequenceStep,
)
from p2c_engine.static_data import build_static_game_data


ROOT = Path(__file__).resolve().parents[2]
PREFIX_PHYSICAL = "adds_value_to_value_physical_damage_t1"
PREFIX_ACCURACY = "value_to_accuracy_rating_t1"
PREFIX_PHYS_ACCURACY = (
    "value_increased_physical_damage_value_to_accuracy_rating_t1"
)
SUFFIX_ATTACK_SPEED = "value_increased_attack_speed_t1"
SUFFIX_CRIT = "value_to_critical_hit_chance_t1"


@pytest.fixture(scope="module")
def static():
    return build_static_game_data(ROOT)


def _state(
    *modifiers: ModifierInstance,
    rarity: Rarity = Rarity.RARE,
) -> ItemState:
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


def _step(currency_id: str, index: int, *, active_modifiers=()) -> BoundedSequenceStep:
    return BoundedSequenceStep(
        step_id=f"step_{index}_{currency_id}",
        currency_id=currency_id,
        mode_id=f"m48a_{currency_id}",
        active_modifier_ids=tuple(active_modifiers),
    )


def _linear_route(*steps: BoundedSequenceStep, route_id: str = "linear"):
    nodes = []
    for index, step in enumerate(steps):
        target = f"op_{index + 1}" if index + 1 < len(steps) else "end"
        nodes.append(
            OperationRouteNode(
                node_id=f"op_{index}",
                step=step,
                on_transition=target,
                on_no_transition="stopped",
            )
        )
    nodes.extend(
        (
            TerminalRouteNode(node_id="end", terminal_label="completed"),
            TerminalRouteNode(node_id="stopped", terminal_label="no_transition"),
        )
    )
    return BoundedBranchingRequest(
        route_id=route_id,
        start_node_id="op_0",
        nodes=tuple(nodes),
    )


def _one_step_route(step: BoundedSequenceStep, *, route_id="one_step"):
    return BoundedBranchingRequest(
        route_id=route_id,
        start_node_id="op",
        nodes=(
            OperationRouteNode(
                node_id="op",
                step=step,
                on_transition="end",
                on_no_transition="end",
            ),
            TerminalRouteNode(node_id="end", terminal_label="done"),
        ),
    )


def _success_modifiers(static):
    criteria = static.success_criteria

    def ordinary(family_id, *, max_tier=None):
        rows = [
            row
            for row in static.modifier_index.values()
            if row.static_category == "ordinary"
            and row.family_id == family_id
            and (max_tier is None or row.tier <= max_tier)
        ]
        assert rows, family_id
        return min(rows, key=lambda row: (row.tier, row.mod_id))

    physical = tuple(
        ordinary(family_id, max_tier=3)
        for family_id in criteria["family_sets"]["physical_top_families"]
    )
    critical = ordinary(criteria["single_families"]["critical_hit_chance"])
    melee = ordinary(criteria["single_families"]["all_melee_skills"], max_tier=3)
    final = ordinary(
        criteria["family_sets"]["top_final_suffix_families"][0], max_tier=3
    )
    excluded = {
        critical.family_id,
        melee.family_id,
        *criteria["family_sets"]["top_final_suffix_families"],
    }
    ordinary_third = next(
        row
        for row in sorted(static.modifier_index.values(), key=lambda row: row.mod_id)
        if row.static_category == "ordinary"
        and row.side == Side.SUFFIX
        and row.family_id not in excluded
    )
    return physical, critical, melee, final, ordinary_third


def _instances(rows):
    return tuple(ModifierInstance(row.mod_id) for row in rows)


def test_success_classifier_interprets_only_accepted_config(static) -> None:
    physical, critical, melee, final, ordinary_third = _success_modifiers(static)
    classifier = AcceptedSuccessClassifier(static=static)
    top = _state(*_instances(physical + (critical, melee, final)))
    acceptable = _state(*_instances(physical + (critical, melee, ordinary_third)))
    not_success = _state(*_instances(physical + (critical, melee)))

    assert classifier.classify(top) == "TOP"
    assert classifier.classify(acceptable) == "ACCEPTABLE"
    assert classifier.classify(not_success) == "NOT_SUCCESS"

    bad_static = replace(
        static,
        success_criteria={**dict(static.success_criteria), "invented_score": 1},
    )
    with pytest.raises(M48APredicateError, match="unsupported success_criteria shape"):
        AcceptedSuccessClassifier(static=bad_static)


def test_predicate_registry_is_closed_deterministic_and_score_free(static) -> None:
    registry = AcceptedPredicateRegistry(static=static)
    state = _state()
    first = registry.evaluate(M48A_SUCCESS_PREDICATE_ID, state)
    second = registry.evaluate(M48A_SUCCESS_PREDICATE_ID, state)
    forbidden = {"score", "cost", "probability", "ev", "utility", "ranking"}

    assert registry.predicate_ids == ("success_class.v1",)
    assert first == second
    assert first.result == "NOT_SUCCESS"
    assert forbidden.isdisjoint({field.name.lower() for field in fields(PredicateDecision)})
    assert forbidden.isdisjoint({key.lower() for key in first.public_payload()})
    with pytest.raises(M48ARouteAdmissionError) as exc:
        registry.evaluate("caller_python_callback", state)
    assert exc.value.code == "unsupported_predicate"


def test_exact_branching_routes_actual_post_operation_states(static) -> None:
    physical, critical, melee, _, _ = _success_modifiers(static)
    initial = _state(*_instances(physical + (critical, melee)))
    step = _step("ordinary_add", 0)
    request = BoundedBranchingRequest(
        route_id="classify_actual_add_result",
        start_node_id="add",
        nodes=(
            OperationRouteNode("add", step, "classify", "failed"),
            PredicateRouteNode(
                "classify",
                M48A_SUCCESS_PREDICATE_ID,
                (
                    ("TOP", "top"),
                    ("ACCEPTABLE", "acceptable"),
                    ("NOT_SUCCESS", "not_success"),
                ),
            ),
            TerminalRouteNode("top", "top"),
            TerminalRouteNode("acceptable", "acceptable"),
            TerminalRouteNode("not_success", "not_success"),
            TerminalRouteNode("failed", "no_transition"),
        ),
    )
    result = BoundedBranchingRouteHarness(static=static).enumerate_exact(
        initial_state=initial,
        request=request,
        decision_id_prefix="m48a.actual_state",
    )
    labels = {row.terminal_label for row in result.terminals}

    assert result.status == "completed"
    assert result.mass_sum_exactly_one is True
    assert {"top", "acceptable"} <= labels
    assert "no_transition" not in labels
    assert all(
        event.predicate_decision.state_hash == event.pre_state_hash
        for path in result.paths
        for event in path.events
        if event.predicate_decision is not None
    )
    assert all(
        path.events[0].post_state_hash == path.events[1].pre_state_hash
        for path in result.paths
    )


def test_one_step_exact_and_seeded_parity_with_m43a(static) -> None:
    initial = _state(ModifierInstance(SUFFIX_CRIT, fractured=True))
    step = _step("ordinary_add", 0)
    route = _one_step_route(step)
    sequence = BoundedSequenceRequest(sequence_id="one_step", steps=(step,))
    m48 = BoundedBranchingRouteHarness(static=static)
    m43 = BoundedAcceptedOperationSequenceHarness(static=static)

    route_exact = m48.enumerate_exact(
        initial_state=initial,
        request=route,
        decision_id_prefix="m48a.one_step",
    )
    sequence_exact = m43.enumerate_exact(
        initial_state=initial,
        request=sequence,
        decision_id_prefix="m48a.one_step",
    )
    route_projection = {
        row.terminal_state_hash: Fraction(
            row.probability_numerator, row.probability_denominator
        )
        for row in route_exact.state_only_projection()
    }
    sequence_projection = {
        row.terminal_state_hash: Fraction(
            row.probability_numerator, row.probability_denominator
        )
        for row in sequence_exact.state_only_projection()
    }
    assert route_projection == sequence_projection

    route_sample = m48.run(
        initial_state=initial,
        request=route,
        seed=48_001,
        sample_count=8,
        run_id="m48a.one_step",
    )
    sequence_sample = m43.run(
        initial_state=initial,
        request=sequence,
        seed=48_001,
        sample_count=8,
        run_id="m48a.one_step",
    )
    assert [row.terminal_state_hash for row in route_sample.trajectories] == [
        row.terminal_state_hash for row in sequence_sample.trajectories
    ]
    assert route_sample.decisions == sequence_sample.decisions


def test_linear_dag_parity_mass_conservation_and_terminal_aggregation(static) -> None:
    initial = _state(ModifierInstance(SUFFIX_CRIT, fractured=True))
    steps = (_step("ordinary_add", 0), _step("annulment", 1))
    route = _linear_route(*steps, route_id="add_annul")
    sequence = BoundedSequenceRequest(sequence_id="add_annul", steps=steps)
    m48 = BoundedBranchingRouteHarness(static=static)
    m43 = BoundedAcceptedOperationSequenceHarness(static=static)

    route_exact = m48.enumerate_exact(
        initial_state=initial,
        request=route,
        decision_id_prefix="m48a.linear",
    )
    sequence_exact = m43.enumerate_exact(
        initial_state=initial,
        request=sequence,
        decision_id_prefix="m48a.linear",
    )
    assert route_exact.mass_sum_exactly_one is True
    assert route_exact.terminal_count == 1
    assert route_exact.terminals[0].path_count == route_exact.path_count
    assert route_exact.terminals[0].terminal_state_hash == initial.state_hash()
    assert {
        row.terminal_state_hash: Fraction(
            row.probability_numerator, row.probability_denominator
        )
        for row in route_exact.state_only_projection()
    } == {
        row.terminal_state_hash: Fraction(
            row.probability_numerator, row.probability_denominator
        )
        for row in sequence_exact.state_only_projection()
    }


@pytest.mark.parametrize(
    ("currency_id", "state", "active_modifiers"),
    (
        ("ordinary_add", _state(ModifierInstance(SUFFIX_CRIT, fractured=True)), ()),
        ("annulment", _state(ModifierInstance(PREFIX_ACCURACY)), ()),
        (
            "chaos",
            _state(ModifierInstance(PREFIX_ACCURACY), ModifierInstance(SUFFIX_CRIT)),
            (),
        ),
        ("transmutation", _state(rarity=Rarity.NORMAL), ()),
        ("greater_essence_abrasion", _state(rarity=Rarity.MAGIC), ()),
        (
            "perfect_essence_abrasion",
            _state(ModifierInstance(PREFIX_ACCURACY), ModifierInstance(SUFFIX_CRIT)),
            (),
        ),
        ("alchemy", _state(rarity=Rarity.NORMAL), ()),
        (
            "fracturing_orb",
            _state(
                ModifierInstance(PREFIX_PHYSICAL),
                ModifierInstance(PREFIX_ACCURACY),
                ModifierInstance(PREFIX_PHYS_ACCURACY),
                ModifierInstance(SUFFIX_CRIT),
            ),
            (),
        ),
        ("gnawed_jawbone", _state(ModifierInstance(PREFIX_ACCURACY)), ()),
        (
            "exalted",
            _state(ModifierInstance(SUFFIX_CRIT, fractured=True)),
            ("greater_exaltation",),
        ),
    ),
)
def test_seeded_parity_covers_every_accepted_executor_family(
    static, currency_id, state, active_modifiers
) -> None:
    step = _step(currency_id, 0, active_modifiers=active_modifiers)
    route = BoundedBranchingRouteHarness(static=static).run(
        initial_state=state,
        request=_one_step_route(step, route_id=f"route_{currency_id}"),
        seed=48_002,
        sample_count=2,
        run_id=f"m48a.family.{currency_id}",
    )
    sequence = BoundedAcceptedOperationSequenceHarness(static=static).run(
        initial_state=state,
        request=BoundedSequenceRequest(
            sequence_id=f"sequence_{currency_id}", steps=(step,)
        ),
        seed=48_002,
        sample_count=2,
        run_id=f"m48a.family.{currency_id}",
    )
    assert [row.terminal_state_hash for row in route.trajectories] == [
        row.terminal_state_hash for row in sequence.trajectories
    ]
    assert route.decisions == sequence.decisions


def test_no_transition_preserves_state_and_uses_explicit_edge(static) -> None:
    initial = _state()
    request = _one_step_route(_step("annulment", 0), route_id="empty_annulment")
    result = BoundedBranchingRouteHarness(static=static).enumerate_exact(
        initial_state=initial,
        request=request,
        decision_id_prefix="m48a.no_transition",
    )
    path = result.paths[0]

    assert path.terminal_state == initial
    assert path.last_operation_outcome == "no_transition_no_consumption"
    assert path.visited_operation_count == 1
    assert path.completed_operation_count == 0
    assert path.events[0].operation_trace.no_transition_reason is not None


def test_exact_ceiling_is_structured_and_never_returns_partial_mass(static) -> None:
    initial = _state(ModifierInstance(SUFFIX_CRIT, fractured=True))
    result = BoundedBranchingRouteHarness(static=static).enumerate_exact(
        initial_state=initial,
        request=_one_step_route(_step("ordinary_add", 0)),
        decision_id_prefix="m48a.ceiling",
        max_exact_paths=1,
    )

    assert result.status == "ceiling_exceeded"
    assert result.mass_sum_exactly_one is False
    assert result.paths == ()
    assert result.terminals == ()
    assert result.ceiling_stop.stop_code == "exact_path_ceiling_exceeded"


def test_seeded_replay_and_diagnostics_are_deterministic(static) -> None:
    request = _linear_route(
        _step("ordinary_add", 0),
        _step("annulment", 1),
        route_id="replay",
    )
    initial = _state(ModifierInstance(SUFFIX_CRIT, fractured=True))
    harness = BoundedBranchingRouteHarness(static=static)
    result = harness.run(
        initial_state=initial,
        request=request,
        seed=48_003,
        sample_count=8,
        run_id="m48a.replay",
    )

    assert harness.verify_replay(
        expected=result, initial_state=initial, request=request
    ) == result
    assert all(
        event.next_node_id is not None
        for row in result.trajectories
        for event in row.events
        if event.node_kind != "terminal"
    )
    with pytest.raises(M48ABranchingInvariantViolation, match="replay mismatch"):
        harness.verify_replay(
            expected=replace(result, result_hash="0" * 64),
            initial_state=initial,
            request=request,
        )


def test_graph_validation_fail_closed_diagnostics(static) -> None:
    harness = BoundedBranchingRouteHarness(static=static)
    step = _step("ordinary_add", 0)

    cycle = BoundedBranchingRequest(
        route_id="cycle",
        start_node_id="a",
        nodes=(
            OperationRouteNode("a", step, "b", "end"),
            OperationRouteNode("b", _step("annulment", 1), "a", "end"),
            TerminalRouteNode("end", "end"),
        ),
    )
    with pytest.raises(M48ARouteAdmissionError) as exc:
        harness.validate_request(cycle)
    assert exc.value.code == "cycle_detected"

    unreachable = BoundedBranchingRequest(
        route_id="unreachable",
        start_node_id="end",
        nodes=(
            TerminalRouteNode("end", "end"),
            TerminalRouteNode("orphan", "orphan"),
        ),
    )
    with pytest.raises(M48ARouteAdmissionError) as exc:
        harness.validate_request(unreachable)
    assert exc.value.code == "unreachable_nodes"

    unsupported = _one_step_route(_step("reveal_desecrated", 0))
    with pytest.raises(M48ARouteAdmissionError) as exc:
        harness.validate_request(unsupported)
    assert exc.value.code == "unsupported_operation"

    invalid_predicate = BoundedBranchingRequest(
        route_id="invalid_predicate",
        start_node_id="branch",
        nodes=(
            PredicateRouteNode(
                "branch",
                "probability_above_threshold",
                (("YES", "end"),),
            ),
            TerminalRouteNode("end", "end"),
        ),
    )
    with pytest.raises(M48ARouteAdmissionError) as exc:
        harness.validate_request(invalid_predicate)
    assert exc.value.code == "unsupported_predicate"


def test_node_edge_depth_and_ambiguous_terminal_limits_fail_closed(static) -> None:
    harness = BoundedBranchingRouteHarness(static=static)
    step = _step("ordinary_add", 0)
    too_many_nodes = replace(_one_step_route(step), node_ceiling=1)
    with pytest.raises(M48ARouteAdmissionError) as exc:
        harness.validate_request(too_many_nodes)
    assert exc.value.code == "node_ceiling_exceeded"

    too_many_edges = replace(_one_step_route(step), edge_ceiling=1)
    with pytest.raises(M48ARouteAdmissionError) as exc:
        harness.validate_request(too_many_edges)
    assert exc.value.code == "edge_ceiling_exceeded"

    above_pin = replace(_one_step_route(step), node_ceiling=M48A_MAX_NODES + 1)
    with pytest.raises(M48ARouteAdmissionError) as exc:
        harness.validate_request(above_pin)
    assert exc.value.code == "ceiling_above_accepted_maximum"

    repeated = tuple(_step("ordinary_add", index) for index in range(9))
    too_deep = _linear_route(*repeated, route_id="too_deep")
    with pytest.raises(M48ARouteAdmissionError) as exc:
        harness.validate_request(too_deep)
    assert exc.value.code == "operation_step_ceiling_exceeded"

    ambiguous = BoundedBranchingRequest(
        route_id="ambiguous",
        start_node_id="op",
        nodes=(
            OperationRouteNode("op", step, "a", "b"),
            TerminalRouteNode("a", "same"),
            TerminalRouteNode("b", "same"),
        ),
    )
    with pytest.raises(M48ARouteAdmissionError) as exc:
        harness.validate_request(ambiguous)
    assert exc.value.code == "ambiguous_terminal_label"

    assert M48A_MAX_NODES == 64
    assert M48A_MAX_EDGES == 128
    assert M48A_MAX_OPERATION_STEPS == 8


def test_incomplete_predicate_cases_and_planner_surface_are_absent(static) -> None:
    request = BoundedBranchingRequest(
        route_id="incomplete",
        start_node_id="branch",
        nodes=(
            PredicateRouteNode(
                "branch",
                M48A_SUCCESS_PREDICATE_ID,
                (("TOP", "top"), ("NOT_SUCCESS", "not_success")),
            ),
            TerminalRouteNode("top", "top"),
            TerminalRouteNode("not_success", "not_success"),
        ),
    )
    harness = BoundedBranchingRouteHarness(static=static)
    with pytest.raises(M48ARouteAdmissionError) as exc:
        harness.validate_request(request)
    assert exc.value.code == "incomplete_predicate_cases"

    forbidden_surface = {
        "generate_route",
        "generate_routes",
        "compare_routes",
        "rank_routes",
        "recommend_route",
        "optimize",
    }
    assert all(not hasattr(harness, name) for name in forbidden_surface)
