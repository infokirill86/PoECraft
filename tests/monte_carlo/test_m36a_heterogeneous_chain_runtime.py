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
from p2c_engine.monte_carlo.annulment import AnnulmentOperation
from p2c_engine.monte_carlo.heterogeneous_chain import (
    M36A_CHAIN_SCHEMA_VERSION,
    M36A_CONSTRUCTED_FIXTURE_LABEL,
    M36A_SEQUENCE_LENGTH,
    CatalogOperationInvocation,
    M36AChainInvariantViolation,
    M36AHeterogeneousChainHarness,
)
from p2c_engine.monte_carlo.ordinary_add import OrdinaryAddOperation
from p2c_engine.static_data.game_data import StaticGameData


M36A_MAX_EXACT_PATHS = 32
M36A_SEED = 36001
M36A_SAMPLE_COUNT = 64


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


def _operations(*, annulment_status: str = "accepted_executable_runtime") -> dict[str, object]:
    return {
        "operations": [
            {
                "operation_id": "annulment",
                "group": "annulment",
                "active_in_current_simulation": True,
                "runtime_admission_status": annulment_status,
            },
            {
                "operation_id": "exalted",
                "group": "exalted",
                "active_in_current_simulation": True,
                "runtime_admission_status": "admission_candidate",
            },
        ]
    }


def _static(
    mods: tuple[StaticModifier, ...],
    *,
    annulment_status: str = "accepted_executable_runtime",
) -> StaticGameData:
    return StaticGameData(
        modifier_index={mod.mod_id: mod for mod in mods},
        operations=_operations(annulment_status=annulment_status),
        omens={},
        family_registry={},
        initial_states={},
        project_scope={"active_item_class": "quarterstaff"},
        success_criteria={},
        failure_policy={},
        item_state_schema={},
        static_modifier_schema={},
        source_fingerprint="m36a_fixture_source",
        semantic_fingerprint="m36a_fixture_semantic",
        root=None,  # type: ignore[arg-type]
    )


def _state(*mods: ModifierInstance) -> ItemState:
    return ItemState(
        item_class="quarterstaff",
        rarity=Rarity.RARE,
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


def _base_state() -> ItemState:
    return _state(ModifierInstance("fixed_fractured_crit_suffix", fractured=True))


def _fixture_static() -> StaticGameData:
    return _static(
        (
            _fixed_fractured_suffix(),
            _mod("alpha_prefix", family="alpha", side=Side.PREFIX),
            _mod("beta_prefix", family="beta", side=Side.PREFIX),
            _mod("gamma_prefix", family="gamma", side=Side.PREFIX),
        )
    )


def _add_operation(mode_id: str = "m36a_add") -> OrdinaryAddOperation:
    return OrdinaryAddOperation(mode_id=mode_id, side_filter=Side.PREFIX)


def _annul_operation(mode_id: str = "m36a_annul") -> AnnulmentOperation:
    return AnnulmentOperation(mode_id=mode_id)


def _mass(option) -> Fraction:  # type: ignore[no-untyped-def]
    return Fraction(option.probability_numerator, option.probability_denominator)


def test_m36a_execution_contract_is_pinned() -> None:
    assert M36A_CHAIN_SCHEMA_VERSION == "p2c.m36a.heterogeneous_chain.v1"
    assert M36A_SEQUENCE_LENGTH == 2
    assert "project-model hardening fixture" in M36A_CONSTRUCTED_FIXTURE_LABEL
    assert "not a real crafting route" in M36A_CONSTRUCTED_FIXTURE_LABEL


def test_m36a_add_then_annul_aggregates_duplicate_terminal_and_mass_one() -> None:
    static = _fixture_static()
    harness = M36AHeterogeneousChainHarness(static=static)
    operations = (_add_operation("m36a_add_then_annul_add"), _annul_operation("m36a_add_then_annul_annul"))

    paths = harness.enumerate_paths(
        initial_state=_base_state(),
        operations=operations,
        decision_id_prefix="m36a.add_then_annul.paths",
        max_exact_paths=M36A_MAX_EXACT_PATHS,
    )
    terminals = harness.enumerate_terminal_distribution(
        initial_state=_base_state(),
        operations=operations,
        decision_id_prefix="m36a.add_then_annul.terminals",
        max_exact_paths=M36A_MAX_EXACT_PATHS,
    )

    assert len(paths) == 3
    assert all(len(path.steps) == 2 for path in paths)
    assert sum(_mass(path) for path in paths) == Fraction(1, 1)
    assert len(terminals) == 1
    assert terminals[0].path_count == 3
    assert _mass(terminals[0]) == Fraction(1, 1)
    assert terminals[0].terminal_state_hash == _base_state().state_hash()
    assert {path.steps[0].operation_id for path in paths} == {"ordinary_add"}
    assert {path.steps[1].operation_id for path in paths} == {"annulment"}


def test_m36a_annul_then_add_rebuilds_add_pool_from_branch_specific_state() -> None:
    static = _fixture_static()
    state = _state(
        ModifierInstance("fixed_fractured_crit_suffix", fractured=True),
        ModifierInstance("alpha_prefix"),
        ModifierInstance("beta_prefix"),
    )
    observed_add_states: list[tuple[str, ...]] = []

    def spy_add_builder(
        request: OrdinaryAddPoolRequest,
        game_data: StaticGameData,
    ):
        observed_add_states.append(tuple(mod.mod_id for mod in request.state.modifiers))
        return build_ordinary_add_pool(request, game_data)

    harness = M36AHeterogeneousChainHarness(
        static=static,
        ordinary_add_pool_builder=spy_add_builder,
    )
    operations = (_annul_operation("m36a_annul_then_add_annul"), _add_operation("m36a_annul_then_add_add"))
    paths = harness.enumerate_paths(
        initial_state=state,
        operations=operations,
        decision_id_prefix="m36a.annul_then_add.rebuild",
        max_exact_paths=M36A_MAX_EXACT_PATHS,
    )

    assert len(paths) == 4
    assert sum(_mass(path) for path in paths) == Fraction(1, 1)
    assert set(observed_add_states) == {
        ("fixed_fractured_crit_suffix", "alpha_prefix"),
        ("fixed_fractured_crit_suffix", "beta_prefix"),
    }
    assert (
        "fixed_fractured_crit_suffix",
        "alpha_prefix",
        "beta_prefix",
    ) not in observed_add_states
    assert all(path.steps[1].pre_state_hash == path.steps[0].post_state_hash for path in paths)


def test_m36a_fail_closed_on_active_catalog_row_without_runtime_admission() -> None:
    static = _fixture_static()
    harness = M36AHeterogeneousChainHarness(static=static)
    operations = (
        _add_operation("m36a_add"),
        CatalogOperationInvocation(mode_id="m36a_exalted_catalog_row", operation_id="exalted"),
    )

    with pytest.raises(
        M36AChainInvariantViolation,
        match="catalog operation is not executable",
    ):
        harness.enumerate_paths(
            initial_state=_base_state(),
            operations=operations,
            decision_id_prefix="m36a.fail_closed.exalted",
            max_exact_paths=M36A_MAX_EXACT_PATHS,
        )


def test_m36a_fail_closed_if_annulment_row_is_not_runtime_admitted() -> None:
    static = _static(
        (
            _fixed_fractured_suffix(),
            _mod("alpha_prefix", family="alpha", side=Side.PREFIX),
        ),
        annulment_status="admission_candidate",
    )
    harness = M36AHeterogeneousChainHarness(static=static)

    with pytest.raises(
        M36AChainInvariantViolation,
        match="operation row is not executable-admitted",
    ):
        harness.enumerate_paths(
            initial_state=_base_state(),
            operations=(_add_operation("m36a_add"), _annul_operation("m36a_annul")),
            decision_id_prefix="m36a.fail_closed.annulment_status",
            max_exact_paths=M36A_MAX_EXACT_PATHS,
        )


def test_m36a_fractured_modifier_is_protected_through_exact_and_mc_chain() -> None:
    static = _fixture_static()
    state = _state(
        ModifierInstance("fixed_fractured_crit_suffix", fractured=True),
        ModifierInstance("alpha_prefix"),
        ModifierInstance("beta_prefix"),
    )
    harness = M36AHeterogeneousChainHarness(static=static)
    operations = (_annul_operation("m36a_fractured_guard_annul"), _add_operation("m36a_fractured_guard_add"))

    paths = harness.enumerate_paths(
        initial_state=state,
        operations=operations,
        decision_id_prefix="m36a.fractured_guard.exact",
        max_exact_paths=M36A_MAX_EXACT_PATHS,
    )
    result = harness.run(
        initial_state=state,
        operations=operations,
        seed=M36A_SEED,
        sample_count=M36A_SAMPLE_COUNT,
        run_id="m36a_fractured_guard_mc",
    )

    assert "fixed_fractured_crit_suffix" not in {
        step.selected_mod_id
        for path in paths
        for step in path.steps
        if step.operation_id == "annulment"
    }
    assert "fixed_fractured_crit_suffix" not in {
        step.selected_mod_id
        for trajectory in result.trajectories
        for step in trajectory.steps
        if step.operation_id == "annulment"
    }


def test_m36a_same_seed_and_run_id_replay_exactly() -> None:
    static = _fixture_static()
    harness = M36AHeterogeneousChainHarness(static=static)
    operations = (_add_operation("m36a_replay_add"), _annul_operation("m36a_replay_annul"))

    first = harness.run(
        initial_state=_base_state(),
        operations=operations,
        seed=M36A_SEED,
        sample_count=M36A_SAMPLE_COUNT,
        run_id="m36a_replay",
    )
    second = harness.run(
        initial_state=_base_state(),
        operations=operations,
        seed=M36A_SEED,
        sample_count=M36A_SAMPLE_COUNT,
        run_id="m36a_replay",
    )

    assert first.result_hash == second.result_hash
    assert [row.public_payload() for row in first.trajectories] == [
        row.public_payload() for row in second.trajectories
    ]


def test_m36a_negative_control_fractured_removal_pool_leak_fails() -> None:
    static = _fixture_static()
    state = _state(
        ModifierInstance("fixed_fractured_crit_suffix", fractured=True),
        ModifierInstance("alpha_prefix"),
    )

    def bad_removal_builder(
        request: RemovalPoolRequest,
        game_data: StaticGameData,
    ) -> PoolBuildResult:
        valid = build_removal_pool(request, game_data)
        bad_key = "rm:fixed_fractured_crit_suffix:c0:d0:f1:o0"
        return PoolBuildResult(
            candidates=valid.candidates + (Candidate(bad_key, 1),),
            candidate_digest="m36a_negative_control_bad_digest",
            result_fingerprint="m36a_negative_control_bad_fingerprint",
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

    harness = M36AHeterogeneousChainHarness(
        static=static,
        removal_pool_builder=bad_removal_builder,
    )

    with pytest.raises(Exception, match="fractured candidate leaked"):
        harness.enumerate_paths(
            initial_state=state,
            operations=(_annul_operation("m36a_bad_annul"), _add_operation("m36a_add")),
            decision_id_prefix="m36a.negative_control.fractured_leak",
            max_exact_paths=M36A_MAX_EXACT_PATHS,
        )


def test_m36a_rejects_sequences_that_are_not_two_step_heterogeneous() -> None:
    static = _fixture_static()
    harness = M36AHeterogeneousChainHarness(static=static)

    with pytest.raises(M36AChainInvariantViolation, match="one ordinary_add step"):
        harness.enumerate_paths(
            initial_state=_base_state(),
            operations=(_add_operation("first"), _add_operation("second")),
            decision_id_prefix="m36a.reject.two_adds",
            max_exact_paths=M36A_MAX_EXACT_PATHS,
        )

    with pytest.raises(M36AChainInvariantViolation, match="exactly two fixed steps"):
        harness.enumerate_paths(  # type: ignore[arg-type]
            initial_state=_base_state(),
            operations=(
                _add_operation("first"),
                _annul_operation("second"),
                _add_operation("third"),
            ),
            decision_id_prefix="m36a.reject.three_steps",
            max_exact_paths=M36A_MAX_EXACT_PATHS,
        )


def test_m36a_public_summary_is_numeric_probability_free_metadata() -> None:
    static = _fixture_static()
    harness = M36AHeterogeneousChainHarness(static=static)
    result = harness.run(
        initial_state=_base_state(),
        operations=(_add_operation("m36a_public_add"), _annul_operation("m36a_public_annul")),
        seed=M36A_SEED,
        sample_count=4,
        run_id="m36a_public_summary",
    )

    summary = result.public_summary()
    assert summary["numeric_probability_free"] is True
    assert summary["public_numeric_release"] is False
    assert summary["probability_values_printed"] is False
    forbidden_keys = {"probability", "percent", "expected_attempts", "ev", "ranking"}
    assert not (forbidden_keys & set(summary))
