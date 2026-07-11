from __future__ import annotations

import math
from collections import Counter
from dataclasses import replace
from fractions import Fraction
from pathlib import Path

import pytest
import yaml

from p2c_engine.decisions import RecordingDecisionSource, SeededDecisionSource
from p2c_engine.domain.enums import Rarity, Side
from p2c_engine.domain.item_state import ItemState, ModifierInstance
from p2c_engine.domain.pool_building import PoolBuildResult
from p2c_engine.domain.static_modifier import StaticModifier
from p2c_engine.legality.pool_builders import (
    OrdinaryAddPoolRequest,
    build_ordinary_add_pool,
)
from p2c_engine.monte_carlo.alchemy import (
    M44A_ALCHEMY_OPERATION_ID,
    M44A_SCHEMA_VERSION,
    M44A_SEMANTICS_VERSION,
    AlchemyHarness,
    AlchemyOperation,
    M44AAlchemyInvariantViolation,
    M44AExactCeilingExceeded,
)
from p2c_engine.monte_carlo.bounded_sequence import (
    BoundedAcceptedOperationSequenceHarness,
    BoundedSequenceRequest,
    BoundedSequenceStep,
)
from p2c_engine.operations.resolver import (
    M38AResolverAdmissionError,
    M44A_RESOLVER_SCHEMA_VERSION,
    OperationResolver,
    OperationResolverRequest,
)
from p2c_engine.static_data import build_static_game_data
from p2c_engine.static_data.game_data import StaticGameData


ROOT = Path(__file__).resolve().parents[2]


def _mod(
    mod_id: str,
    *,
    side: Side,
    weight: int,
    category: str = "ordinary",
) -> StaticModifier:
    return StaticModifier(
        mod_id=mod_id,
        family_id=f"family_{mod_id}",
        side=side,
        group_ids=(f"group_{mod_id}",),
        tier=1,
        modifier_level=1,
        tags=(),
        generation_weight=weight,
        static_category=category,
    )


def _alchemy_row() -> dict[str, object]:
    return {
        "operation_id": "alchemy",
        "group": "alchemy",
        "input_rarity": ["normal", "magic"],
        "active_in_current_simulation": True,
        "runtime_admission_status": "accepted_executable_runtime",
        "transition": {
            "atomic": True,
            "output_rarity": "rare",
            "sequence": [
                "discard_all_explicit",
                "create_empty_rare_shell",
                "add_ordinary_x4",
                "commit",
            ],
            "remove": {"kind": "all_explicit"},
            "add": {
                "kind": "ordinary_weighted_sequential",
                "count": 4,
                "mml": None,
            },
        },
    }


def _static() -> StaticGameData:
    mods = tuple(
        _mod(f"prefix_{index}", side=Side.PREFIX, weight=index)
        for index in range(1, 5)
    ) + tuple(
        _mod(f"suffix_{index}", side=Side.SUFFIX, weight=index + 4)
        for index in range(1, 5)
    ) + (
        _mod("old_magic_prefix", side=Side.PREFIX, weight=1, category="fixture"),
        _mod("old_magic_suffix", side=Side.SUFFIX, weight=1, category="fixture"),
        _mod("fractured_magic", side=Side.SUFFIX, weight=1, category="fixture"),
    )
    return StaticGameData(
        modifier_index={mod.mod_id: mod for mod in mods},
        operations={"operations": [_alchemy_row()]},
        omens={},
        family_registry={},
        initial_states={},
        project_scope={"active_item_class": "quarterstaff"},
        success_criteria={},
        failure_policy={},
        item_state_schema={},
        static_modifier_schema={},
        source_fingerprint="m44a_fixture_source",
        semantic_fingerprint="m44a_fixture_semantic",
        root=None,  # type: ignore[arg-type]
    )


def _state(rarity: Rarity, *modifiers: ModifierInstance) -> ItemState:
    return ItemState(
        item_class="quarterstaff",
        rarity=rarity,
        item_level=82,
        modifiers=modifiers,
        unrevealed_desecrated=None,
        augment_socket_capacity=0,
        augment_socket_used=0,
        astrid_installed=False,
    )


def _resolve(static: StaticGameData, state: ItemState) -> AlchemyOperation:
    plan = OperationResolver(static=static).resolve(
        OperationResolverRequest(
            currency_id="alchemy",
            item_state=state,
            mode_id="m44a_alchemy",
        )
    )
    assert plan.schema_version == M44A_RESOLVER_SCHEMA_VERSION
    assert isinstance(plan.operation, AlchemyOperation)
    return plan.operation


def _mass(row: object) -> Fraction:
    return Fraction(  # type: ignore[attr-defined]
        row.probability_numerator, row.probability_denominator
    )


def _sequence_request() -> BoundedSequenceRequest:
    return BoundedSequenceRequest(
        sequence_id="m44a_one_step_parity",
        steps=(
            BoundedSequenceStep(
                step_id="alchemy_0",
                currency_id="alchemy",
                mode_id="m44a_alchemy",
            ),
        ),
    )


def test_m44a_real_data_admits_only_base_alchemy_for_this_family() -> None:
    static = build_static_game_data(ROOT)
    row = next(
        row
        for row in static.operations["operations"]
        if row["operation_id"] == "alchemy"
    )
    assert row["runtime_admission_status"] == "accepted_executable_runtime"
    assert row["active_in_current_simulation"] is True
    assert "alchemy" in static.project_scope["active_operation_groups"]
    assert "alchemy" not in static.project_scope["reference_only_operation_groups"]
    evidence = yaml.safe_load(
        (ROOT / "data/mechanics_evidence.yaml").read_text(encoding="utf-8")
    )["alchemy_m44a"]
    assert evidence["server_truth_claimed"] is False
    assert evidence["generation"]["add_count"] == 4
    assert evidence["generation"]["fixed_two_prefix_two_suffix"] is False


def test_m44a_real_catalog_and_real_pool_builder_complete_four_adds() -> None:
    static = build_static_game_data(ROOT)
    state = _state(Rarity.NORMAL)
    operation = _resolve(static, state)
    run = AlchemyHarness(static=static).run(
        initial_state=state,
        operation=operation,
        seed=44_004,
        sample_count=8,
        run_id="m44a_real_pool_smoke",
    )
    assert all(row.outcome == "completed" for row in run.trajectories)
    assert all(len(row.selected_mod_ids) == 4 for row in run.trajectories)
    assert all(len(row.traces) == 4 for row in run.trajectories)


@pytest.mark.parametrize(
    "state",
    (
        _state(Rarity.NORMAL),
        _state(
            Rarity.MAGIC,
            ModifierInstance("old_magic_prefix"),
            ModifierInstance("old_magic_suffix"),
        ),
    ),
)
def test_m44a_normal_and_magic_exact_paths_discard_old_mods_and_add_exactly_four(
    state: ItemState,
) -> None:
    static = _static()
    operation = _resolve(static, state)
    paths = AlchemyHarness(static=static).enumerate_paths(
        initial_state=state,
        operation=operation,
        decision_id_prefix="m44a.exact",
        max_exact_paths=2_000,
    )

    assert paths
    assert all(path.outcome == "completed" for path in paths)
    assert sum((_mass(path) for path in paths), Fraction()) == Fraction(1, 1)
    assert all(path.terminal_state.rarity == Rarity.RARE for path in paths)
    assert all(len(path.terminal_state.modifiers) == 4 for path in paths)
    assert all(len(path.traces) == 4 for path in paths)
    assert all(
        {modifier.mod_id for modifier in path.terminal_state.modifiers}.isdisjoint(
            {"old_magic_prefix", "old_magic_suffix"}
        )
        for path in paths
    )


def test_m44a_weight_driven_side_distributions_cover_three_one_two_two_one_three() -> None:
    static = _static()
    state = _state(Rarity.NORMAL)
    paths = AlchemyHarness(static=static).enumerate_paths(
        initial_state=state,
        operation=_resolve(static, state),
        decision_id_prefix="m44a.side_distribution",
        max_exact_paths=2_000,
    )
    side_counts = {
        sum(
            static.modifier_index[modifier.mod_id].side == Side.PREFIX
            for modifier in path.terminal_state.modifiers
        )
        for path in paths
    }
    assert side_counts == {1, 2, 3}
    assert all(
        1
        <= sum(
            static.modifier_index[modifier.mod_id].side == Side.PREFIX
            for modifier in path.terminal_state.modifiers
        )
        <= 3
        for path in paths
    )


def test_m44a_rebuilds_real_ordinary_pool_after_every_internal_add() -> None:
    static = _static()
    state = _state(Rarity.NORMAL)
    observed: list[tuple[Rarity, int, str]] = []

    def spy(
        request: OrdinaryAddPoolRequest, game_data: StaticGameData
    ) -> PoolBuildResult:
        observed.append(
            (request.state.rarity, len(request.state.modifiers), request.state.state_hash())
        )
        return build_ordinary_add_pool(request, game_data)

    AlchemyHarness(static=static, pool_builder=spy).enumerate_paths(
        initial_state=state,
        operation=_resolve(static, state),
        decision_id_prefix="m44a.pool_rebuild",
        max_exact_paths=2_000,
    )

    assert {count for _, count, _ in observed} == {0, 1, 2, 3}
    assert {rarity for rarity, _, _ in observed} == {Rarity.RARE}
    for count in (1, 2, 3):
        assert len({digest for _, observed_count, digest in observed if observed_count == count}) > 1


def test_m44a_intermediate_pool_failure_rolls_back_magic_item_atomically() -> None:
    static = _static()
    initial = _state(
        Rarity.MAGIC,
        ModifierInstance("old_magic_prefix"),
        ModifierInstance("old_magic_suffix"),
    )

    def fail_after_two(
        request: OrdinaryAddPoolRequest, game_data: StaticGameData
    ) -> PoolBuildResult:
        if len(request.state.modifiers) == 2:
            return PoolBuildResult(
                candidates=(),
                candidate_digest=None,
                result_fingerprint="m44a_forced_intermediate_failure",
                stages=(),
                empty_reason="forced_intermediate_pool_failure",
            )
        return build_ordinary_add_pool(request, game_data)

    harness = AlchemyHarness(static=static, pool_builder=fail_after_two)
    operation = _resolve(static, initial)
    paths = harness.enumerate_paths(
        initial_state=initial,
        operation=operation,
        decision_id_prefix="m44a.rollback",
        max_exact_paths=2_000,
    )
    trajectory = harness.sample_once(
        initial_state=initial,
        operation=operation,
        decision_source=RecordingDecisionSource(SeededDecisionSource(44_010)),
        sample_index=0,
        run_id="m44a_rollback",
    )

    assert paths
    assert {path.terminal_state_hash for path in paths} == {initial.state_hash()}
    assert {path.outcome for path in paths} == {"no_transition_no_consumption"}
    assert sum((_mass(path) for path in paths), Fraction()) == Fraction(1, 1)
    assert trajectory.outcome == "no_transition_no_consumption"
    assert trajectory.pre_state_hash == trajectory.post_state_hash == initial.state_hash()
    assert len(trajectory.traces) == 3
    assert trajectory.traces[-1].outcome == "failed_atomic_rollback"


def test_m44a_fractured_input_fails_closed_and_original_is_unchanged() -> None:
    static = _static()
    initial = _state(
        Rarity.MAGIC,
        ModifierInstance("fractured_magic", fractured=True),
    )
    operation = _resolve(static, initial)
    path = AlchemyHarness(static=static).enumerate_paths(
        initial_state=initial,
        operation=operation,
        decision_id_prefix="m44a.fractured",
    )[0]
    assert path.outcome == "no_transition_no_consumption"
    assert path.no_transition_reason == "fractured_input_not_admitted"
    assert path.terminal_state_hash == initial.state_hash()
    assert _mass(path) == Fraction(1, 1)


def test_m44a_exact_terminal_aggregation_and_seeded_mc_convergence_replay() -> None:
    static = _static()
    state = _state(Rarity.NORMAL)
    operation = _resolve(static, state)
    harness = AlchemyHarness(static=static)
    terminals = harness.enumerate_terminal_distribution(
        initial_state=state,
        operation=operation,
        decision_id_prefix="m44a.oracle",
        max_exact_paths=2_000,
    )
    exact = {
        row.terminal_state_hash: _mass(row)
        for row in terminals
        if row.outcome == "completed"
    }
    run = harness.run(
        initial_state=state,
        operation=operation,
        seed=44_001,
        sample_count=2_048,
        run_id="m44a_convergence",
    )
    replay = harness.verify_replay(
        expected=run,
        initial_state=state,
        operation=operation,
    )
    observed = Counter(row.post_state_hash for row in run.trajectories)

    assert replay == run
    assert set(observed) <= set(exact)
    assert sum((_mass(row) for row in terminals), Fraction()) == Fraction(1, 1)
    assert sum(row.path_count for row in terminals) > len(terminals)
    for terminal_hash, probability in exact.items():
        expected = run.sample_count * float(probability)
        tolerance = math.ceil(
            6
            * math.sqrt(
                run.sample_count
                * float(probability)
                * (1 - float(probability))
            )
        ) + 1
        assert abs(observed[terminal_hash] - expected) <= tolerance
    assert run.public_summary()["probability_values_printed"] is False


def test_m44a_resolver_direct_and_m43a_one_step_parity() -> None:
    static = _static()
    state = _state(Rarity.NORMAL)
    operation = _resolve(static, state)
    direct = AlchemyHarness(static=static)
    sequence = BoundedAcceptedOperationSequenceHarness(static=static)
    request = _sequence_request()

    direct_terminals = direct.enumerate_terminal_distribution(
        initial_state=state,
        operation=operation,
        decision_id_prefix="m44a.parity.step_0.alchemy.m44a_alchemy",
        max_exact_paths=2_000,
    )
    sequence_exact = sequence.enumerate_exact(
        initial_state=state,
        request=request,
        decision_id_prefix="m44a.parity",
        max_exact_paths=2_000,
        max_exact_terminals=100,
    )
    assert sequence_exact.status == "completed"
    assert {
        row.terminal_state_hash: _mass(row) for row in direct_terminals
    } == {
        row.terminal_state_hash: _mass(row)
        for row in sequence_exact.state_only_projection()
    }

    direct_run = direct.run(
        initial_state=state,
        operation=operation,
        seed=44_002,
        sample_count=32,
        run_id="m44a_parity",
    )
    sequence_run = sequence.run(
        initial_state=state,
        request=request,
        seed=44_002,
        sample_count=32,
        run_id="m44a_parity",
    )
    assert [row.post_state_hash for row in direct_run.trajectories] == [
        row.terminal_state_hash for row in sequence_run.trajectories
    ]
    assert [row.selected_mod_ids for row in direct_run.trajectories] == [
        row.steps[0].selected_keys for row in sequence_run.trajectories
    ]


def test_m44a_exact_ceiling_and_contract_negative_controls_fail_hard() -> None:
    static = _static()
    state = _state(Rarity.NORMAL)
    operation = _resolve(static, state)
    with pytest.raises(M44AExactCeilingExceeded, match="max_exact_paths"):
        AlchemyHarness(static=static).enumerate_paths(
            initial_state=state,
            operation=operation,
            decision_id_prefix="m44a.ceiling",
            max_exact_paths=1,
        )
    with pytest.raises(
        M44AAlchemyInvariantViolation, match="does not match admitted catalog row"
    ):
        AlchemyHarness(static=static).enumerate_paths(
            initial_state=state,
            operation=replace(operation, add_count=3),
            decision_id_prefix="m44a.bad_contract",
        )
    with pytest.raises(M38AResolverAdmissionError, match="modifier layers"):
        OperationResolver(static=static).resolve(
            OperationResolverRequest(
                currency_id=M44A_ALCHEMY_OPERATION_ID,
                item_state=state,
                active_modifier_ids=("whittling",),
            )
        )
    assert M44A_SCHEMA_VERSION == "p2c.m44a.alchemy_runtime.v1"
    assert M44A_SEMANTICS_VERSION.endswith("project_model.v1")
