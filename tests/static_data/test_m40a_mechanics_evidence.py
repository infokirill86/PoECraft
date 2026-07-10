from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]


def test_m40a_thresholds_capacity_and_sources_are_explicit_and_source_open() -> None:
    evidence = yaml.safe_load((ROOT / "data/mechanics_evidence.yaml").read_text(encoding="utf-8"))
    sources = yaml.safe_load((ROOT / "data/sources.yaml").read_text(encoding="utf-8"))
    operations = yaml.safe_load((ROOT / "data/operations.yaml").read_text(encoding="utf-8"))

    source_ids = {row["source_id"] for row in sources["sources"]}
    assert "official_patch_0_3" in source_ids

    expected = {
        "greater_transmutation": (44, "target_magic_add_pool"),
        "perfect_transmutation": (70, "target_magic_add_pool"),
        "greater_augmentation": (44, "magic_add_pool"),
        "perfect_augmentation": (70, "magic_add_pool"),
        "greater_regal": (35, "target_rare_add_pool"),
        "perfect_regal": (50, "target_rare_add_pool"),
        "greater_exalted": (35, "rare_add_pool"),
        "perfect_exalted": (50, "rare_add_pool"),
    }
    threshold_evidence = evidence["mml"]["accepted_runtime_thresholds"]
    rows = {row["operation_id"]: row for row in operations["operations"]}
    assert threshold_evidence["broader_mml_closure"] is False
    assert threshold_evidence["server_truth_claimed"] is False
    assert set(threshold_evidence["exact_threshold_source_refs"]) <= source_ids
    assert set(threshold_evidence["corroborating_context_source_refs"]) <= source_ids
    for operation_id, (mml, stage) in expected.items():
        assert threshold_evidence["values"][operation_id] == {
            "add_pool_mml": mml,
            "application_stage": stage,
        }
        assert rows[operation_id]["transition"]["add"]["mml"] == mml

    model = evidence["rarity_capacity_and_mutable_modifier_count"]
    assert model["server_truth_claimed"] is False
    assert model["evidence_level"] == "project_model_source_open"
    assert model["capacity"] == {
        "normal": {"prefix": 0, "suffix": 0},
        "magic": {"prefix": 1, "suffix": 1},
        "rare": {"prefix": 3, "suffix": 3},
    }
    assert model["current_modifier_count"]["magic_zero_after_removal_supported"] is True
    assert model["current_modifier_count"]["rare_below_generated_count_supported"] is True
    assert model["fractured_modifiers"][
        "current_fractured_critical_suffix_staff_is_supported_scenario_not_global_invariant"
    ] is True
    assert model["augmentation"]["separate_side_lottery"] is False
    assert model["rarity_transition_add"] == {
        "transmutation_pool_build_rarity": "magic",
        "regal_pool_build_rarity": "rare",
        "commit": "target_rarity_and_added_modifier_atomic",
        "failure": "no_transition_no_consumption_original_state_unchanged",
    }
