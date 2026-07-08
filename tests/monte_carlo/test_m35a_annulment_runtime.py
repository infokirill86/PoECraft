from __future__ import annotations

from fractions import Fraction

import pytest

from p2c_engine.decisions import RecordingDecisionSource, SeededDecisionSource
from p2c_engine.domain.candidate import Candidate
from p2c_engine.domain.enums import Rarity, Side
from p2c_engine.domain.item_state import ItemState, ModifierInstance
from p2c_engine.domain.pool_building import PoolBuildResult, RemovalInstanceMetadata
from p2c_engine.domain.static_modifier import StaticModifier
from p2c_engine.legality.pool_builders import RemovalPoolRequest, build_removal_pool
from p2c_engine.monte_carlo.annulment import (
    ANNULMENT_OPERATION_ID,
    ANNULMENT_SEMANTICS_VERSION,
    M35A_ANNULMENT_SCHEMA_VERSION,
    AnnulmentMonteCarloHarness,
    AnnulmentOperation,
    M35AAnnulmentInvariantViolation,
)
from p2c_engine.static_data.game_data import StaticGameData


M35A_PROJECT_MODEL_LABEL = "project-model hardening fixture; not server truth"


def _mod(
    mod_id: str,
    *,
    family: str,
    side: Side,
    weight: int = 1,
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
        source_fingerprint="m35a_fixture_source",
        semantic_fingerprint="m35a_fixture_semantic",
        root=None,  # type: ignore[arg-type]
    )


def _state(*mods: ModifierInstance, rarity: Rarity = Rarity.RARE) -> ItemState:
    return ItemState(
        item_class="quarterstaff",
        rarity=rarity,
        item_level=82,
        modifiers=mods,
        unrevealed_desecrated=None,
        augment_socket_capacity=0,
        augment_socket_used=0,
        astrid_installed=False,
    )


def _fixed_fractured_suffix() -> StaticModifier:
    return _mod(
        "fixed_fractured_crit_suffix",
        family="fixed_crit_suffix",
        side=Side.SUFFIX,
    )


def _three_removable_fixture() -> tuple[StaticGameData, ItemState, AnnulmentOperation]:
    static = _static(
        (
            _fixed_fractured_suffix(),
            _mod("alpha_prefix", family="alpha", side=Side.PREFIX),
            _mod("beta_prefix", family="beta", side=Side.PREFIX),
            _mod("gamma_prefix", family="gamma", side=Side.PREFIX),
        )
    )
    state = _state(
        ModifierInstance("fixed_fractured_crit_suffix", fractured=True),
        ModifierInstance("alpha_prefix"),
        ModifierInstance("beta_prefix"),
        ModifierInstance("gamma_prefix"),
    )
    return static, state, AnnulmentOperation(mode_id="m35a_base_annulment")


def test_m35a_execution_contract_is_pinned() -> None:
    assert ANNULMENT_OPERATION_ID == "annulment"
    assert ANNULMENT_SEMANTICS_VERSION == "p2c.m35.annulment.project_model.v1"
    assert M35A_ANNULMENT_SCHEMA_VERSION == "p2c.m35a.annulment_runtime.v1"
    assert "project-model" in M35A_PROJECT_MODEL_LABEL
    assert "not server truth" in M35A_PROJECT_MODEL_LABEL


def test_m35a_exact_paths_are_uniform_over_non_fractured_installed_instances() -> None:
    static, state, operation = _three_removable_fixture()
    harness = AnnulmentMonteCarloHarness(static=static)

    paths = harness.enumerate_paths(
        state=state,
        operation=operation,
        decision_id="m35a.exact.uniform",
    )

    assert len(paths) == 3
    assert {path.selected_mod_id for path in paths} == {
        "alpha_prefix",
        "beta_prefix",
        "gamma_prefix",
    }
    assert "fixed_fractured_crit_suffix" not in {path.selected_mod_id for path in paths}
    assert {
        Fraction(path.probability_numerator, path.probability_denominator)
        for path in paths
    } == {Fraction(1, 3)}
    assert sum(
        Fraction(path.probability_numerator, path.probability_denominator)
        for path in paths
    ) == Fraction(1, 1)


def test_m35a_fractured_modifier_is_never_removed_by_exact_or_mc_path() -> None:
    static, state, operation = _three_removable_fixture()
    harness = AnnulmentMonteCarloHarness(static=static)
    exact_selected = {
        path.selected_mod_id
        for path in harness.enumerate_paths(
            state=state,
            operation=operation,
            decision_id="m35a.exact.fractured_guard",
        )
    }
    assert "fixed_fractured_crit_suffix" not in exact_selected

    result = harness.run(
        initial_state=state,
        operation=operation,
        seed=35001,
        sample_count=24,
        run_id="m35a_mc_fractured_guard",
    )
    assert "fixed_fractured_crit_suffix" not in {
        row.selected_mod_id for row in result.trajectories
    }
    assert all(row.outcome == "applied" for row in result.trajectories)


def test_m35a_empty_pool_no_transition_no_mutation_and_exact_mass_one() -> None:
    static = _static((_fixed_fractured_suffix(),))
    state = _state(ModifierInstance("fixed_fractured_crit_suffix", fractured=True))
    operation = AnnulmentOperation(mode_id="m35a_empty_pool")
    harness = AnnulmentMonteCarloHarness(static=static)

    paths = harness.enumerate_paths(
        state=state,
        operation=operation,
        decision_id="m35a.exact.empty_pool",
    )
    terminals = harness.enumerate_terminal_distribution(
        state=state,
        operation=operation,
        decision_id="m35a.exact.empty_pool.terminals",
    )
    result = harness.run(
        initial_state=state,
        operation=operation,
        seed=35001,
        sample_count=5,
        run_id="m35a_empty_pool",
    )

    assert len(paths) == 1
    assert paths[0].outcome == "no_transition_no_consumption"
    assert paths[0].pre_state_hash == paths[0].post_state_hash == state.state_hash()
    assert Fraction(paths[0].probability_numerator, paths[0].probability_denominator) == Fraction(1, 1)
    assert len(terminals) == 1
    assert Fraction(terminals[0].probability_numerator, terminals[0].probability_denominator) == Fraction(1, 1)
    assert {row.outcome for row in result.trajectories} == {"no_transition_no_consumption"}
    assert all(row.pre_state_hash == row.post_state_hash == state.state_hash() for row in result.trajectories)
    assert result.decisions == ()


def test_m35a_duplicate_instance_terminal_aggregation_sums_paths() -> None:
    duplicate = _mod("duplicate_prefix", family="duplicate", side=Side.PREFIX)
    static = _static((_fixed_fractured_suffix(), duplicate))
    state = _state(
        ModifierInstance("fixed_fractured_crit_suffix", fractured=True),
        ModifierInstance("duplicate_prefix"),
        ModifierInstance("duplicate_prefix"),
    )
    harness = AnnulmentMonteCarloHarness(static=static)
    operation = AnnulmentOperation(mode_id="m35a_duplicate_aggregation")

    paths = harness.enumerate_paths(
        state=state,
        operation=operation,
        decision_id="m35a.exact.duplicates",
    )
    terminals = harness.enumerate_terminal_distribution(
        state=state,
        operation=operation,
        decision_id="m35a.exact.duplicates.terminals",
    )

    assert len(paths) == 2
    assert {path.selected_duplicate_ordinal for path in paths} == {0, 1}
    assert len(terminals) == 1
    assert terminals[0].path_count == 2
    assert Fraction(terminals[0].probability_numerator, terminals[0].probability_denominator) == Fraction(1, 1)
    assert set(terminals[0].path_keys) == {path.path_key for path in paths}


def test_m35a_exact_and_mc_use_same_shared_removal_pool_path() -> None:
    static, state, operation = _three_removable_fixture()
    calls: list[RemovalPoolRequest] = []

    def spy_builder(request: RemovalPoolRequest, game_data: StaticGameData) -> PoolBuildResult:
        calls.append(request)
        return build_removal_pool(request, game_data)

    harness = AnnulmentMonteCarloHarness(static=static, removal_pool_builder=spy_builder)
    exact_paths = harness.enumerate_paths(
        state=state,
        operation=operation,
        decision_id="m35a.exact.shared_builder",
    )
    decision_source = RecordingDecisionSource(SeededDecisionSource(35001))
    trajectory = harness.sample_once(
        state=state,
        operation=operation,
        decision_source=decision_source,
        sample_index=0,
        run_id="m35a_mc_shared_builder",
    )

    assert len(calls) == 2
    assert calls[0].state == calls[1].state == state
    assert all(call.item_class == "quarterstaff" for call in calls)
    assert {path.selected_mod_id for path in exact_paths} == {
        "alpha_prefix",
        "beta_prefix",
        "gamma_prefix",
    }
    assert trajectory.selected_mod_id in {"alpha_prefix", "beta_prefix", "gamma_prefix"}


def test_m35a_same_seed_and_run_id_replay_exactly() -> None:
    static, state, operation = _three_removable_fixture()
    harness = AnnulmentMonteCarloHarness(static=static)

    first = harness.run(
        initial_state=state,
        operation=operation,
        seed=35001,
        sample_count=16,
        run_id="m35a_replay",
    )
    second = harness.run(
        initial_state=state,
        operation=operation,
        seed=35001,
        sample_count=16,
        run_id="m35a_replay",
    )

    assert first.result_hash == second.result_hash
    assert [row.public_payload() for row in first.trajectories] == [
        row.public_payload() for row in second.trajectories
    ]


def test_m35a_negative_control_fails_on_fractured_candidate_leak() -> None:
    static, state, operation = _three_removable_fixture()

    def bad_builder(request: RemovalPoolRequest, game_data: StaticGameData) -> PoolBuildResult:
        valid = build_removal_pool(request, game_data)
        bad_key = "rm:fixed_fractured_crit_suffix:c0:d0:f1:o0"
        return PoolBuildResult(
            candidates=valid.candidates + (Candidate(bad_key, 1),),
            candidate_digest="negative_control_bad_digest",
            result_fingerprint="negative_control_bad_fingerprint",
            stages=valid.stages,
            removal_metadata=valid.removal_metadata
            + (
                RemovalInstanceMetadata(
                    candidate_key=bad_key,
                    mod_id="fixed_fractured_crit_suffix",
                    crafted=False,
                    desecrated=False,
                    fractured=True,
                    duplicate_ordinal=0,
                    modifier_level=1,
                    side="suffix",
                ),
            ),
            empty_reason=None,
        )

    harness = AnnulmentMonteCarloHarness(static=static, removal_pool_builder=bad_builder)

    with pytest.raises(
        M35AAnnulmentInvariantViolation,
        match="fractured candidate leaked from removal pool",
    ):
        harness.enumerate_paths(
            state=state,
            operation=operation,
            decision_id="m35a.negative_control.fractured_leak",
        )


def test_m35a_fail_closed_on_unsupported_operation_and_rarity() -> None:
    static, state, _operation = _three_removable_fixture()
    harness = AnnulmentMonteCarloHarness(static=static)

    with pytest.raises(M35AAnnulmentInvariantViolation, match="unsupported operation_id"):
        harness.run(
            initial_state=state,
            operation=AnnulmentOperation(
                mode_id="m35a_invalid_operation",
                operation_id="chaos",
            ),
            seed=35001,
            sample_count=1,
            run_id="m35a_invalid_operation",
        )

    with pytest.raises(M35AAnnulmentInvariantViolation, match="magic and rare"):
        harness.run(
            initial_state=_state(rarity=Rarity.NORMAL),
            operation=AnnulmentOperation(mode_id="m35a_invalid_rarity"),
            seed=35001,
            sample_count=1,
            run_id="m35a_invalid_rarity",
        )


def test_m35a_public_summary_is_numeric_probability_free_metadata() -> None:
    static, state, operation = _three_removable_fixture()
    harness = AnnulmentMonteCarloHarness(static=static)
    result = harness.run(
        initial_state=state,
        operation=operation,
        seed=35001,
        sample_count=4,
        run_id="m35a_public_summary",
    )
    summary = result.public_summary()

    assert summary["numeric_probability_free"] is True
    assert summary["public_numeric_release"] is False
    assert summary["probability_values_printed"] is False
    forbidden_keys = {"probability", "percent", "expected_attempts", "ev", "ranking"}
    assert not (forbidden_keys & set(summary))
