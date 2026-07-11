from __future__ import annotations

import math
from collections import Counter
from dataclasses import replace
from fractions import Fraction
from pathlib import Path

import pytest

from p2c_engine.decisions import RecordingDecisionSource, SeededDecisionSource
from p2c_engine.domain.enums import Rarity
from p2c_engine.domain.item_state import ItemState, ModifierInstance
from p2c_engine.monte_carlo.annulment import (
    AnnulmentMonteCarloHarness,
    AnnulmentOperation,
)
from p2c_engine.monte_carlo.bounded_sequence import (
    AcceptedOperationExecutorRegistry,
    BoundedAcceptedOperationSequenceHarness,
    BoundedSequenceRequest,
    BoundedSequenceStep,
    M43A_MAX_STEPS,
    M43ASequenceAdmissionError,
    M43ASequenceInvariantViolation,
)
from p2c_engine.monte_carlo.chaos_like import (
    ChaosLikeMonteCarloHarness,
    ChaosLikeOperation,
)
from p2c_engine.monte_carlo.greater_essence import (
    GreaterEssenceHarness,
    GreaterEssenceOperation,
)
from p2c_engine.monte_carlo.ordinary_add import (
    OrdinaryAddMonteCarloHarness,
    OrdinaryAddOperation,
    _append_ordinary_modifier,
)
from p2c_engine.monte_carlo.perfect_essence import (
    PerfectEssenceHarness,
    PerfectEssenceOperation,
)
from p2c_engine.monte_carlo.rarity_progression import (
    CatalogSingleAddHarness,
    CatalogSingleAddOperation,
)
from p2c_engine.operations import OperationResolver, OperationResolverRequest
from p2c_engine.sampling.exact import branch_options
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


def _step(currency_id: str, *, index: int = 0) -> BoundedSequenceStep:
    return BoundedSequenceStep(
        step_id=f"step_{index}_{currency_id}",
        currency_id=currency_id,
        mode_id=f"m43a_{currency_id}",
    )


def _request(*currency_ids: str, sequence_id: str = "m43a_test") -> BoundedSequenceRequest:
    return BoundedSequenceRequest(
        sequence_id=sequence_id,
        steps=tuple(
            _step(currency_id, index=index)
            for index, currency_id in enumerate(currency_ids)
        ),
    )


def _parity_cases() -> tuple[tuple[str, ItemState], ...]:
    return (
        (
            "ordinary_add",
            _state(ModifierInstance(SUFFIX_CRIT, fractured=True)),
        ),
        (
            "annulment",
            _state(
                ModifierInstance(PREFIX_ACCURACY),
                ModifierInstance(SUFFIX_CRIT, fractured=True),
            ),
        ),
        (
            "chaos",
            _state(
                ModifierInstance(PREFIX_ACCURACY),
                ModifierInstance(SUFFIX_ATTACK_SPEED),
                ModifierInstance(SUFFIX_CRIT, fractured=True),
            ),
        ),
        (
            "greater_chaos",
            _state(
                ModifierInstance(PREFIX_ACCURACY),
                ModifierInstance(SUFFIX_ATTACK_SPEED),
                ModifierInstance(SUFFIX_CRIT, fractured=True),
            ),
        ),
        (
            "greater_exalted",
            _state(ModifierInstance(SUFFIX_CRIT, fractured=True)),
        ),
        ("transmutation", _state(rarity=Rarity.NORMAL)),
        ("greater_essence_abrasion", _state(rarity=Rarity.MAGIC)),
        (
            "perfect_essence_abrasion",
            _state(
                ModifierInstance(PREFIX_ACCURACY),
                ModifierInstance(SUFFIX_ATTACK_SPEED),
            ),
        ),
    )


def _resolved(static, currency_id: str, state: ItemState):
    return OperationResolver(static=static).resolve(
        OperationResolverRequest(
            currency_id=currency_id,
            item_state=state,
            mode_id=f"m43a_{currency_id}",
        )
    ).operation


def _direct_exact_projection(static, currency_id: str, state: ItemState) -> dict[str, Fraction]:
    operation = _resolved(static, currency_id, state)
    decision_id = f"m43a.parity.step_0.{currency_id}.m43a_{currency_id}"
    if isinstance(operation, OrdinaryAddOperation):
        harness = OrdinaryAddMonteCarloHarness(static=static)
        pool = harness.build_pool(state, operation)
        if not pool.candidates:
            return {state.state_hash(): Fraction(1, 1)}
        output: dict[str, Fraction] = {}
        for option in branch_options(decision_id, pool.candidates):
            terminal = _append_ordinary_modifier(state, option.selected_key)
            output[terminal.state_hash()] = output.get(
                terminal.state_hash(), Fraction(0, 1)
            ) + Fraction(option.probability_numerator, option.probability_denominator)
        return output
    if isinstance(operation, AnnulmentOperation):
        rows = AnnulmentMonteCarloHarness(static=static).enumerate_terminal_distribution(
            state=state, operation=operation, decision_id=decision_id
        )
    elif isinstance(operation, ChaosLikeOperation):
        rows = ChaosLikeMonteCarloHarness(static=static).enumerate_terminal_distribution(
            initial_state=state,
            operation=operation,
            decision_id_prefix=decision_id.rsplit(".step_0", 1)[0],
            max_exact_paths=65_536,
        )
    elif isinstance(operation, CatalogSingleAddOperation):
        rows = CatalogSingleAddHarness(static=static).enumerate_terminal_distribution(
            initial_state=state, operation=operation, decision_id=decision_id
        )
    elif isinstance(operation, GreaterEssenceOperation):
        rows = GreaterEssenceHarness(static=static).enumerate_terminal_distribution(
            initial_state=state, operation=operation
        )
    elif isinstance(operation, PerfectEssenceOperation):
        rows = PerfectEssenceHarness(static=static).enumerate_terminal_distribution(
            initial_state=state, operation=operation, decision_id=decision_id
        )
    else:  # pragma: no cover - resolver/registry contract protects this branch
        raise AssertionError(type(operation))
    return {
        row.terminal_state_hash: Fraction(
            row.probability_numerator, row.probability_denominator
        )
        for row in rows
    }


def _direct_sample(static, currency_id: str, state: ItemState, *, seed: int, run_id: str):
    operation = _resolved(static, currency_id, state)
    source = RecordingDecisionSource(SeededDecisionSource(seed))
    if isinstance(operation, OrdinaryAddOperation):
        row = OrdinaryAddMonteCarloHarness(static=static).sample_once(
            state=state,
            operation=operation,
            decision_source=source,
            sample_index=0,
            run_id=run_id,
        )
        terminal_hash = row.post_state_hash
    elif isinstance(operation, AnnulmentOperation):
        row = AnnulmentMonteCarloHarness(static=static).sample_once(
            state=state,
            operation=operation,
            decision_source=source,
            sample_index=0,
            run_id=run_id,
        )
        terminal_hash = row.post_state_hash
    elif isinstance(operation, ChaosLikeOperation):
        row = ChaosLikeMonteCarloHarness(static=static).sample_once(
            initial_state=state,
            operation=operation,
            decision_source=source,
            sample_index=0,
            run_id=run_id,
        )
        terminal_hash = row.terminal_state_hash
    elif isinstance(operation, CatalogSingleAddOperation):
        row = CatalogSingleAddHarness(static=static).sample_once(
            state=state,
            operation=operation,
            decision_source=source,
            sample_index=0,
            run_id=run_id,
        )
        terminal_hash = row.post_state_hash
    elif isinstance(operation, GreaterEssenceOperation):
        row = GreaterEssenceHarness(static=static).sample_once(
            state=state,
            operation=operation,
            sample_index=0,
        )
        terminal_hash = row.post_state_hash
    elif isinstance(operation, PerfectEssenceOperation):
        row = PerfectEssenceHarness(static=static).sample_once(
            initial_state=state,
            operation=operation,
            decision_source=source,
            sample_index=0,
            run_id=run_id,
        )
        terminal_hash = row.terminal_state_hash
    else:  # pragma: no cover
        raise AssertionError(type(operation))
    return terminal_hash, source.records


@pytest.mark.parametrize(("currency_id", "state"), _parity_cases())
def test_one_step_exact_parity_for_every_accepted_executor_family(
    static, currency_id: str, state: ItemState
) -> None:
    harness = BoundedAcceptedOperationSequenceHarness(static=static)
    result = harness.enumerate_exact(
        initial_state=state,
        request=_request(currency_id, sequence_id=f"exact_{currency_id}"),
        decision_id_prefix="m43a.parity",
    )
    projection = {
        row.terminal_state_hash: Fraction(
            row.probability_numerator, row.probability_denominator
        )
        for row in result.state_only_projection()
    }

    assert result.status == "completed"
    assert result.mass_sum_exactly_one is True
    assert projection == _direct_exact_projection(static, currency_id, state)


@pytest.mark.parametrize(("currency_id", "state"), _parity_cases())
def test_one_step_seeded_parity_for_every_accepted_executor_family(
    static, currency_id: str, state: ItemState
) -> None:
    seed = 43_001
    run_id = f"m43a.direct_parity.{currency_id}"
    direct_hash, direct_decisions = _direct_sample(
        static, currency_id, state, seed=seed, run_id=run_id
    )
    result = BoundedAcceptedOperationSequenceHarness(static=static).run(
        initial_state=state,
        request=_request(currency_id, sequence_id=f"sample_{currency_id}"),
        seed=seed,
        sample_count=1,
        run_id=run_id,
    )

    assert result.trajectories[0].terminal_state_hash == direct_hash
    assert result.decisions == direct_decisions


def test_registry_is_complete_for_current_admitted_rows_and_primitive(static) -> None:
    accepted_rows = {
        row["operation_id"]
        for row in static.operations["operations"]
        if row.get("runtime_admission_status") == "accepted_executable_runtime"
    }
    registered = set(AcceptedOperationExecutorRegistry().mapping)
    assert registered == accepted_rows | {"ordinary_add"}


def test_every_registered_currency_compiles_on_a_compatible_state(static) -> None:
    resolver = OperationResolver(static=static)
    for currency_id in sorted(AcceptedOperationExecutorRegistry().mapping):
        if "transmutation" in currency_id:
            state = _state(rarity=Rarity.NORMAL)
        elif "augmentation" in currency_id:
            state = _state(ModifierInstance(PREFIX_ACCURACY), rarity=Rarity.MAGIC)
        elif "regal" in currency_id:
            state = _state(
                ModifierInstance(PREFIX_ACCURACY),
                ModifierInstance(SUFFIX_ATTACK_SPEED),
                rarity=Rarity.MAGIC,
            )
        elif currency_id == "alchemy":
            state = _state(rarity=Rarity.NORMAL)
        elif currency_id.startswith("greater_essence_"):
            state = _state(rarity=Rarity.MAGIC)
        elif currency_id.startswith("perfect_essence_"):
            state = _state(
                ModifierInstance(PREFIX_ACCURACY),
                ModifierInstance(SUFFIX_ATTACK_SPEED),
            )
        elif currency_id == "annulment":
            state = _state(ModifierInstance(PREFIX_ACCURACY))
        elif "chaos" in currency_id:
            state = _state(
                ModifierInstance(PREFIX_ACCURACY),
                ModifierInstance(SUFFIX_ATTACK_SPEED),
            )
        else:
            state = _state(ModifierInstance(SUFFIX_CRIT, fractured=True))

        plan = resolver.resolve(
            OperationResolverRequest(
                currency_id=currency_id,
                item_state=state,
                mode_id=f"m43a_registry_{currency_id}",
            )
        )
        assert plan.currency_id == currency_id
        assert plan.runtime_admission_status == "accepted_executable_runtime"


def test_branch_state_is_load_bearing_and_add_annul_aggregates_terminals(static) -> None:
    initial = _state(ModifierInstance(SUFFIX_CRIT, fractured=True))
    result = BoundedAcceptedOperationSequenceHarness(static=static).enumerate_exact(
        initial_state=initial,
        request=_request("ordinary_add", "annulment", sequence_id="add_annul"),
        decision_id_prefix="m43a.add_annul",
    )

    assert result.status == "completed"
    assert result.mass_sum_exactly_one is True
    assert result.path_count > 1
    assert result.terminal_count == 1
    assert result.terminals[0].terminal_state_hash == initial.state_hash()
    assert result.terminals[0].path_count == result.path_count
    assert all(path.steps[1].pre_state_hash == path.steps[0].post_state_hash for path in result.paths)
    assert all(path.steps[1].selected_keys for path in result.paths)
    assert all(path.steps[0].resolver_plan_digest != path.steps[1].resolver_plan_digest for path in result.paths)
    marginals = result.step_marginals()
    for step_index in (0, 1):
        assert sum(
            Fraction(row.probability_numerator, row.probability_denominator)
            for row in marginals
            if row.step_index == step_index
        ) == Fraction(1, 1)


def test_early_no_transition_preserves_prior_success_and_skips_later_steps(static) -> None:
    initial = _state(rarity=Rarity.MAGIC)
    request = _request(
        "greater_essence_abrasion",
        "greater_essence_abrasion",
        "annulment",
        sequence_id="early_stop",
    )
    result = BoundedAcceptedOperationSequenceHarness(static=static).run(
        initial_state=initial,
        request=request,
        seed=43_001,
        sample_count=1,
        run_id="m43a.early_stop",
    )
    trajectory = result.trajectories[0]

    assert trajectory.outcome == "no_transition_no_consumption"
    assert trajectory.completed_step_count == 1
    assert trajectory.terminal_step_index == 1
    assert len(trajectory.steps) == 2
    assert trajectory.terminal_state.rarity == Rarity.RARE
    assert trajectory.terminal_state.modifiers == (
        ModifierInstance(
            trajectory.steps[0].selected_keys[0],
            crafted=True,
        ),
    )


def test_eight_step_seeded_sequence_replays_exactly(static) -> None:
    initial = _state(ModifierInstance(SUFFIX_CRIT, fractured=True))
    request = _request(
        "ordinary_add",
        "annulment",
        "ordinary_add",
        "annulment",
        "ordinary_add",
        "annulment",
        "ordinary_add",
        "annulment",
        sequence_id="eight_steps",
    )
    harness = BoundedAcceptedOperationSequenceHarness(static=static)
    result = harness.run(
        initial_state=initial,
        request=request,
        seed=43_003,
        sample_count=8,
        run_id="m43a.eight_steps",
    )

    assert len(request.steps) == M43A_MAX_STEPS
    assert all(len(row.steps) == M43A_MAX_STEPS for row in result.trajectories)
    assert all(row.completed_step_count == M43A_MAX_STEPS for row in result.trajectories)
    assert harness.verify_replay(
        expected=result, initial_state=initial, request=request
    ) == result
    with pytest.raises(M43ASequenceInvariantViolation, match="replay mismatch"):
        harness.verify_replay(
            expected=replace(result, result_hash="0" * 64),
            initial_state=initial,
            request=request,
        )


def test_six_step_mixed_fixture_covers_essence_remove_add_and_chaos(static) -> None:
    request = _request(
        "greater_essence_abrasion",
        "chaos",
        "annulment",
        "exalted",
        "chaos",
        "annulment",
        sequence_id="mixed_six_step",
    )
    result = BoundedAcceptedOperationSequenceHarness(static=static).run(
        initial_state=_state(rarity=Rarity.MAGIC),
        request=request,
        seed=43_002,
        sample_count=4,
        run_id="m43a.mixed_six_step",
    )

    assert all(row.outcome == "completed" for row in result.trajectories)
    assert all(row.completed_step_count == 6 for row in result.trajectories)
    assert all(
        tuple(step.executor_id for step in row.steps)
        == (
            "greater_essence",
            "chaos_like",
            "annulment",
            "catalog_single_add",
            "chaos_like",
            "annulment",
        )
        for row in result.trajectories
    )
    assert all(
        row.steps[index].post_state_hash == row.steps[index + 1].pre_state_hash
        for row in result.trajectories
        for index in range(5)
    )


def test_seeded_mc_matches_tractable_mixed_exact_projection(static) -> None:
    initial = _state(
        ModifierInstance(PREFIX_ACCURACY),
        ModifierInstance(SUFFIX_ATTACK_SPEED),
        ModifierInstance(SUFFIX_CRIT, fractured=True),
    )
    request = _request(
        "annulment",
        "ordinary_add",
        sequence_id="mixed_exact_mc",
    )
    harness = BoundedAcceptedOperationSequenceHarness(static=static)
    exact = harness.enumerate_exact(
        initial_state=initial,
        request=request,
        decision_id_prefix="m43a.mixed_exact_mc",
    )
    sample_count = 8_192
    sampled = harness.run(
        initial_state=initial,
        request=request,
        seed=43_001,
        sample_count=sample_count,
        run_id="m43a.mixed_exact_mc",
    )
    expected = {
        row.terminal_state_hash: Fraction(
            row.probability_numerator, row.probability_denominator
        )
        for row in exact.state_only_projection()
    }
    counts = Counter(row.terminal_state_hash for row in sampled.trajectories)

    assert set(counts) <= set(expected)
    for state_hash, probability in expected.items():
        p = float(probability)
        tolerance = max(
            1,
            math.ceil(6 * math.sqrt(sample_count * p * (1 - p))),
        )
        assert abs(counts[state_hash] - sample_count * p) <= tolerance


@pytest.mark.parametrize(
    ("kwargs", "stop_code"),
    (
        ({"max_candidates_per_pool": 1}, "candidate_branch_ceiling_exceeded"),
        ({"max_exact_paths": 1}, "exact_path_ceiling_exceeded"),
        ({"max_exact_terminals": 1}, "exact_terminal_ceiling_exceeded"),
    ),
)
def test_exact_ceiling_returns_structured_stop_without_partial_or_mc_output(
    static, kwargs, stop_code
) -> None:
    result = BoundedAcceptedOperationSequenceHarness(static=static).enumerate_exact(
        initial_state=_state(ModifierInstance(SUFFIX_CRIT, fractured=True)),
        request=_request("ordinary_add", sequence_id=f"ceiling_{stop_code}"),
        decision_id_prefix="m43a.ceiling",
        **kwargs,
    )

    assert result.status == "ceiling_exceeded"
    assert result.ceiling_stop is not None
    assert result.ceiling_stop.stop_code == stop_code
    assert result.paths == ()
    assert result.terminals == ()
    assert result.mass_sum_exactly_one is False


def test_missing_executor_and_nonadmitted_operation_fail_closed(static) -> None:
    mapping = dict(AcceptedOperationExecutorRegistry().mapping)
    mapping.pop("annulment")
    missing = BoundedAcceptedOperationSequenceHarness(
        static=static,
        executor_registry=AcceptedOperationExecutorRegistry(mapping),
    )
    with pytest.raises(M43ASequenceAdmissionError, match="no M43-A accepted executor"):
        missing.run(
            initial_state=_state(ModifierInstance(PREFIX_ACCURACY)),
            request=_request("annulment"),
            seed=43_001,
            sample_count=1,
            run_id="m43a.missing_executor",
        )

    with pytest.raises(M43ASequenceAdmissionError, match="not admitted"):
        BoundedAcceptedOperationSequenceHarness(static=static).run(
            initial_state=_state(rarity=Rarity.NORMAL),
            request=_request("fracturing_orb"),
            seed=43_001,
            sample_count=1,
            run_id="m43a.fracturing_orb_blocked",
        )


def test_request_schema_blocks_modifiers_unbounded_steps_and_continue_policy(static) -> None:
    harness = BoundedAcceptedOperationSequenceHarness(static=static)
    modifier_request = BoundedSequenceRequest(
        sequence_id="modifier_blocked",
        steps=(
            replace(
                _step("ordinary_add"),
                active_modifier_ids=("omen_of_whittling",),
            ),
        ),
    )
    with pytest.raises(M43ASequenceAdmissionError, match="modifier"):
        harness.run(
            initial_state=_state(),
            request=modifier_request,
            seed=43_001,
            sample_count=1,
            run_id="m43a.modifier_blocked",
        )

    too_long = BoundedSequenceRequest(
        sequence_id="too_long",
        steps=tuple(_step("ordinary_add", index=index) for index in range(9)),
    )
    with pytest.raises(M43ASequenceAdmissionError, match="1-8 steps"):
        harness.run(
            initial_state=_state(),
            request=too_long,
            seed=43_001,
            sample_count=1,
            run_id="m43a.too_long",
        )

    continue_request = replace(
        _request("ordinary_add"), stop_on_no_transition=False
    )
    with pytest.raises(M43ASequenceAdmissionError, match="stop_on_no_transition"):
        harness.run(
            initial_state=_state(),
            request=continue_request,
            seed=43_001,
            sample_count=1,
            run_id="m43a.continue_blocked",
        )
