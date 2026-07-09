from __future__ import annotations

from fractions import Fraction

import pytest

from p2c_engine.domain.candidate import Candidate
from p2c_engine.domain.enums import Rarity, Side
from p2c_engine.domain.item_state import ItemState, ModifierInstance
from p2c_engine.domain.pool_building import PoolBuildResult, RemovalInstanceMetadata
from p2c_engine.domain.static_modifier import StaticModifier
from p2c_engine.legality.pool_builders import (
    OrdinaryAddPoolRequest,
    RemovalPoolRequest,
    build_ordinary_add_pool,
    build_removal_pool,
)
from p2c_engine.monte_carlo.chaos_like import (
    M37A_CHAOSLIKE_SCHEMA_VERSION,
    M37A_PROJECT_MODEL_POLICY,
    ChaosLikeMonteCarloHarness,
    ChaosLikeOperation,
    M37AChaosLikeInvariantViolation,
)
from p2c_engine.static_data.game_data import StaticGameData


M37A_MAX_EXACT_PATHS = 64
M37A_SEED = 37001
M37A_SAMPLE_COUNT = 32


def _mod(
    mod_id: str,
    *,
    family: str,
    side: Side,
    weight: int = 1,
    groups: tuple[str, ...] = (),
) -> StaticModifier:
    return StaticModifier(
        mod_id=mod_id,
        family_id=family,
        side=side,
        group_ids=groups,
        tier=1,
        modifier_level=1,
        tags=(),
        generation_weight=weight,
        static_category="ordinary",
    )


def _operations(*, chaos_status: str = "accepted_executable_runtime") -> dict[str, object]:
    return {
        "operations": [
            {
                "operation_id": "chaos",
                "group": "chaos",
                "active_in_current_simulation": True,
                "runtime_admission_status": chaos_status,
                "transition": {"add": {"mml": None}},
            },
            {
                "operation_id": "greater_chaos",
                "group": "chaos",
                "active_in_current_simulation": True,
                "runtime_admission_status": "admission_candidate",
                "transition": {"add": {"mml": 35}},
            },
        ]
    }


def _static(
    mods: tuple[StaticModifier, ...],
    *,
    chaos_status: str = "accepted_executable_runtime",
) -> StaticGameData:
    return StaticGameData(
        modifier_index={mod.mod_id: mod for mod in mods},
        operations=_operations(chaos_status=chaos_status),
        omens={},
        family_registry={},
        initial_states={},
        project_scope={"active_item_class": "quarterstaff"},
        success_criteria={},
        failure_policy={},
        item_state_schema={},
        static_modifier_schema={},
        source_fingerprint="m37a_fixture_source",
        semantic_fingerprint="m37a_fixture_semantic",
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
    return _mod("fixed_fractured_crit_suffix", family="fixed_crit_suffix", side=Side.SUFFIX)


def _operation(mode_id: str = "m37a_base_chaos") -> ChaosLikeOperation:
    return ChaosLikeOperation(mode_id=mode_id)


def _mass(option) -> Fraction:  # type: ignore[no-untyped-def]
    return Fraction(option.probability_numerator, option.probability_denominator)


def _base_static() -> StaticGameData:
    return _static(
        (
            _fixed_fractured_suffix(),
            _mod("installed_alpha_prefix", family="installed_alpha", side=Side.PREFIX),
            _mod("installed_beta_suffix", family="installed_beta", side=Side.SUFFIX),
            _mod("add_gamma_prefix", family="add_gamma", side=Side.PREFIX, weight=3),
            _mod("add_delta_suffix", family="add_delta", side=Side.SUFFIX, weight=1),
        )
    )


def test_m37a_execution_contract_is_pinned() -> None:
    assert M37A_CHAOSLIKE_SCHEMA_VERSION == "p2c.m37a.chaoslike_remove_then_add.v1"
    assert "Whittling" in M37A_PROJECT_MODEL_POLICY
    assert "generation_weight" in M37A_PROJECT_MODEL_POLICY


def test_m37a_base_chaos_happy_path_exact_mass_and_combined_add_weights() -> None:
    static = _base_static()
    state = _state(
        ModifierInstance("fixed_fractured_crit_suffix", fractured=True),
        ModifierInstance("installed_alpha_prefix"),
    )
    harness = ChaosLikeMonteCarloHarness(static=static)

    paths = harness.enumerate_paths(
        initial_state=state,
        operation=_operation("m37a_happy_path"),
        decision_id_prefix="m37a.happy_path",
        max_exact_paths=M37A_MAX_EXACT_PATHS,
    )

    assert len(paths) == 4
    assert sum(_mass(path) for path in paths) == Fraction(1, 1)
    assert {path.steps[0].stage for path in paths} == {"remove"}
    assert {path.steps[1].stage for path in paths} == {"add"}
    assert {path.steps[0].selected_mod_id for path in paths} == {"installed_alpha_prefix"}
    add_masses = {path.steps[1].selected_mod_id: _mass(path) for path in paths}
    assert add_masses["add_gamma_prefix"] == Fraction(3, 6)
    assert add_masses["add_delta_suffix"] == Fraction(1, 6)
    assert add_masses["installed_alpha_prefix"] == Fraction(1, 6)
    assert add_masses["installed_beta_suffix"] == Fraction(1, 6)


def test_m37a_uniform_removal_over_eligible_non_fractured_instances() -> None:
    static = _static(
        (
            _fixed_fractured_suffix(),
            _mod("remove_alpha_prefix", family="remove_alpha", side=Side.PREFIX),
            _mod("remove_beta_prefix", family="remove_beta", side=Side.PREFIX),
            _mod("remove_gamma_suffix", family="remove_gamma", side=Side.SUFFIX),
            _mod("add_only_suffix", family="add_only", side=Side.SUFFIX),
        )
    )
    state = _state(
        ModifierInstance("fixed_fractured_crit_suffix", fractured=True),
        ModifierInstance("remove_alpha_prefix"),
        ModifierInstance("remove_beta_prefix"),
        ModifierInstance("remove_gamma_suffix"),
    )
    harness = ChaosLikeMonteCarloHarness(static=static)

    paths = harness.enumerate_paths(
        initial_state=state,
        operation=_operation("m37a_uniform_removal"),
        decision_id_prefix="m37a.uniform_removal",
        max_exact_paths=M37A_MAX_EXACT_PATHS,
    )

    removal_masses = {
        path.steps[0].selected_mod_id: path.steps[0].probability_numerator
        / path.steps[0].probability_denominator
        for path in paths
    }
    assert removal_masses == {
        "remove_alpha_prefix": 1 / 3,
        "remove_beta_prefix": 1 / 3,
        "remove_gamma_suffix": 1 / 3,
    }
    assert "fixed_fractured_crit_suffix" not in removal_masses


def test_m37a_no_removable_modifiers_no_transition_no_consumption() -> None:
    static = _static((_fixed_fractured_suffix(),))
    state = _state(ModifierInstance("fixed_fractured_crit_suffix", fractured=True))
    harness = ChaosLikeMonteCarloHarness(static=static)

    paths = harness.enumerate_paths(
        initial_state=state,
        operation=_operation("m37a_no_removable"),
        decision_id_prefix="m37a.no_removable",
        max_exact_paths=M37A_MAX_EXACT_PATHS,
    )
    result = harness.run(
        initial_state=state,
        operation=_operation("m37a_no_removable"),
        seed=M37A_SEED,
        sample_count=4,
        run_id="m37a_no_removable",
    )

    assert len(paths) == 1
    assert paths[0].outcome == "no_transition_no_consumption"
    assert paths[0].terminal_state_hash == state.state_hash()
    assert _mass(paths[0]) == Fraction(1, 1)
    assert result.decisions == ()
    assert {trajectory.outcome for trajectory in result.trajectories} == {
        "no_transition_no_consumption"
    }


def test_m37a_fractured_modifiers_are_never_removed_exact_or_mc() -> None:
    static = _base_static()
    state = _state(
        ModifierInstance("fixed_fractured_crit_suffix", fractured=True),
        ModifierInstance("installed_alpha_prefix"),
    )
    harness = ChaosLikeMonteCarloHarness(static=static)

    paths = harness.enumerate_paths(
        initial_state=state,
        operation=_operation("m37a_fractured_guard"),
        decision_id_prefix="m37a.fractured_guard.exact",
        max_exact_paths=M37A_MAX_EXACT_PATHS,
    )
    result = harness.run(
        initial_state=state,
        operation=_operation("m37a_fractured_guard"),
        seed=M37A_SEED,
        sample_count=M37A_SAMPLE_COUNT,
        run_id="m37a_fractured_guard",
    )

    assert "fixed_fractured_crit_suffix" not in {
        path.steps[0].selected_mod_id for path in paths
    }
    assert "fixed_fractured_crit_suffix" not in {
        trajectory.steps[0].selected_mod_id
        for trajectory in result.trajectories
        if trajectory.steps
    }


def test_m37a_rebuilds_add_pool_from_branch_specific_post_removal_state() -> None:
    static = _base_static()
    state = _state(
        ModifierInstance("fixed_fractured_crit_suffix", fractured=True),
        ModifierInstance("installed_alpha_prefix"),
        ModifierInstance("installed_beta_suffix"),
    )
    observed_add_states: list[tuple[str, ...]] = []

    def spy_add_builder(
        request: OrdinaryAddPoolRequest,
        game_data: StaticGameData,
    ) -> PoolBuildResult:
        observed_add_states.append(tuple(mod.mod_id for mod in request.state.modifiers))
        return build_ordinary_add_pool(request, game_data)

    harness = ChaosLikeMonteCarloHarness(
        static=static,
        ordinary_add_pool_builder=spy_add_builder,
    )
    paths = harness.enumerate_paths(
        initial_state=state,
        operation=_operation("m37a_branch_rebuild"),
        decision_id_prefix="m37a.branch_rebuild",
        max_exact_paths=M37A_MAX_EXACT_PATHS,
    )

    assert paths
    assert set(observed_add_states) == {
        ("fixed_fractured_crit_suffix", "installed_alpha_prefix"),
        ("fixed_fractured_crit_suffix", "installed_beta_suffix"),
    }
    assert (
        "fixed_fractured_crit_suffix",
        "installed_alpha_prefix",
        "installed_beta_suffix",
    ) not in observed_add_states
    assert all(path.steps[1].pre_state_hash == path.steps[0].post_state_hash for path in paths)


def test_m37a_empty_post_removal_add_pool_does_not_commit_partial_remove() -> None:
    static = _static(
        (
            _fixed_fractured_suffix(),
            _mod("installed_alpha_prefix", family="installed_alpha", side=Side.PREFIX),
        )
    )
    state = _state(
        ModifierInstance("fixed_fractured_crit_suffix", fractured=True),
        ModifierInstance("installed_alpha_prefix"),
    )

    def empty_add_builder(
        request: OrdinaryAddPoolRequest,
        game_data: StaticGameData,
    ) -> PoolBuildResult:
        return PoolBuildResult(
            candidates=(),
            candidate_digest=None,
            result_fingerprint="m37a_empty_add_pool_fingerprint",
            stages=(),
            empty_reason="ordinary_add_pool_exhausted",
        )

    harness = ChaosLikeMonteCarloHarness(static=static, ordinary_add_pool_builder=empty_add_builder)
    paths = harness.enumerate_paths(
        initial_state=state,
        operation=_operation("m37a_empty_add_pool"),
        decision_id_prefix="m37a.empty_add_pool",
        max_exact_paths=M37A_MAX_EXACT_PATHS,
    )
    trajectory = harness.run(
        initial_state=state,
        operation=_operation("m37a_empty_add_pool"),
        seed=M37A_SEED,
        sample_count=1,
        run_id="m37a_empty_add_pool",
    ).trajectories[0]

    assert len(paths) == 1
    assert paths[0].outcome == "no_transition_no_consumption"
    assert paths[0].terminal_state_hash == state.state_hash()
    assert paths[0].steps[0].post_state_hash != state.state_hash()
    assert paths[0].steps[1].post_state_hash == state.state_hash()
    assert trajectory.outcome == "no_transition_no_consumption"
    assert trajectory.terminal_state_hash == state.state_hash()


def test_m37a_duplicate_terminal_aggregation_sums_paths() -> None:
    duplicate = _mod("duplicate_prefix", family="duplicate", side=Side.PREFIX)
    static = _static((_fixed_fractured_suffix(), duplicate))
    state = _state(
        ModifierInstance("fixed_fractured_crit_suffix", fractured=True),
        ModifierInstance("duplicate_prefix"),
        ModifierInstance("duplicate_prefix"),
    )

    def empty_add_builder(
        request: OrdinaryAddPoolRequest,
        game_data: StaticGameData,
    ) -> PoolBuildResult:
        return PoolBuildResult(
            candidates=(),
            candidate_digest=None,
            result_fingerprint="m37a_duplicate_empty_add_pool",
            stages=(),
            empty_reason="ordinary_add_pool_exhausted",
        )

    harness = ChaosLikeMonteCarloHarness(static=static, ordinary_add_pool_builder=empty_add_builder)
    terminals = harness.enumerate_terminal_distribution(
        initial_state=state,
        operation=_operation("m37a_duplicate_terminal"),
        decision_id_prefix="m37a.duplicate_terminal",
        max_exact_paths=M37A_MAX_EXACT_PATHS,
    )

    assert len(terminals) == 1
    assert terminals[0].terminal_state_hash == state.state_hash()
    assert terminals[0].path_count == 2
    assert _mass(terminals[0]) == Fraction(1, 1)


def test_m37a_same_seed_and_run_id_replay_exactly() -> None:
    static = _base_static()
    state = _state(
        ModifierInstance("fixed_fractured_crit_suffix", fractured=True),
        ModifierInstance("installed_alpha_prefix"),
    )
    harness = ChaosLikeMonteCarloHarness(static=static)

    first = harness.run(
        initial_state=state,
        operation=_operation("m37a_replay"),
        seed=M37A_SEED,
        sample_count=M37A_SAMPLE_COUNT,
        run_id="m37a_replay",
    )
    second = harness.run(
        initial_state=state,
        operation=_operation("m37a_replay"),
        seed=M37A_SEED,
        sample_count=M37A_SAMPLE_COUNT,
        run_id="m37a_replay",
    )

    assert first.result_hash == second.result_hash
    assert [row.public_payload() for row in first.trajectories] == [
        row.public_payload() for row in second.trajectories
    ]


def test_m37a_fail_closed_non_admitted_operation_and_variants() -> None:
    static = _static(
        (
            _fixed_fractured_suffix(),
            _mod("installed_alpha_prefix", family="installed_alpha", side=Side.PREFIX),
        ),
        chaos_status="admission_candidate",
    )
    harness = ChaosLikeMonteCarloHarness(static=static)
    state = _state(
        ModifierInstance("fixed_fractured_crit_suffix", fractured=True),
        ModifierInstance("installed_alpha_prefix"),
    )

    with pytest.raises(M37AChaosLikeInvariantViolation, match="not executable-admitted"):
        harness.enumerate_paths(
            initial_state=state,
            operation=_operation("m37a_not_admitted"),
            decision_id_prefix="m37a.not_admitted",
            max_exact_paths=M37A_MAX_EXACT_PATHS,
        )

    admitted_static = _static(
        (
            _fixed_fractured_suffix(),
            _mod("installed_alpha_prefix", family="installed_alpha", side=Side.PREFIX),
        )
    )
    admitted_harness = ChaosLikeMonteCarloHarness(static=admitted_static)
    with pytest.raises(M37AChaosLikeInvariantViolation, match="unsupported M37-A operation_id"):
        admitted_harness.enumerate_paths(
            initial_state=state,
            operation=ChaosLikeOperation(
                mode_id="m37a_greater_chaos_rejected",
                operation_id="greater_chaos",
            ),
            decision_id_prefix="m37a.greater_chaos_rejected",
            max_exact_paths=M37A_MAX_EXACT_PATHS,
        )


def test_m37a_negative_control_fractured_removal_pool_leak_fails() -> None:
    static = _base_static()
    state = _state(
        ModifierInstance("fixed_fractured_crit_suffix", fractured=True),
        ModifierInstance("installed_alpha_prefix"),
    )

    def bad_removal_builder(
        request: RemovalPoolRequest,
        game_data: StaticGameData,
    ) -> PoolBuildResult:
        valid = build_removal_pool(request, game_data)
        bad_key = "rm:fixed_fractured_crit_suffix:c0:d0:f1:o0"
        return PoolBuildResult(
            candidates=valid.candidates + (Candidate(bad_key, 1),),
            candidate_digest="m37a_negative_control_bad_digest",
            result_fingerprint="m37a_negative_control_bad_fingerprint",
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

    harness = ChaosLikeMonteCarloHarness(static=static, removal_pool_builder=bad_removal_builder)

    with pytest.raises(Exception, match="fractured candidate leaked"):
        harness.enumerate_paths(
            initial_state=state,
            operation=_operation("m37a_negative_control"),
            decision_id_prefix="m37a.negative_control",
            max_exact_paths=M37A_MAX_EXACT_PATHS,
        )


def test_m37a_public_summary_is_numeric_probability_free_metadata() -> None:
    static = _base_static()
    state = _state(
        ModifierInstance("fixed_fractured_crit_suffix", fractured=True),
        ModifierInstance("installed_alpha_prefix"),
    )
    result = ChaosLikeMonteCarloHarness(static=static).run(
        initial_state=state,
        operation=_operation("m37a_public_summary"),
        seed=M37A_SEED,
        sample_count=4,
        run_id="m37a_public_summary",
    )

    summary = result.public_summary()
    assert summary["numeric_probability_free"] is True
    assert summary["public_numeric_release"] is False
    assert summary["probability_values_printed"] is False
    forbidden_keys = {"probability", "percent", "expected_attempts", "ev", "ranking"}
    assert not (forbidden_keys & set(summary))
