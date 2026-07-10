from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]


def test_m39b_runtime_thresholds_match_operations_and_trusted_source_registry() -> None:
    operations = yaml.safe_load((ROOT / "data/operations.yaml").read_text(encoding="utf-8"))
    evidence = yaml.safe_load(
        (ROOT / "data/mechanics_evidence.yaml").read_text(encoding="utf-8")
    )
    sources = yaml.safe_load((ROOT / "data/sources.yaml").read_text(encoding="utf-8"))

    threshold_evidence = evidence["mml"]["accepted_runtime_thresholds"]
    expected = {
        "greater_exalted": (35, "rare_add_pool"),
        "perfect_exalted": (50, "rare_add_pool"),
        "greater_chaos": (35, "rebuilt_post_removal_add_pool"),
        "perfect_chaos": (50, "rebuilt_post_removal_add_pool"),
    }
    operation_rows = {row["operation_id"]: row for row in operations["operations"]}
    source_ids = {row["source_id"] for row in sources["sources"]}

    assert threshold_evidence["runtime_status"] == "USER_APPROVED_PROJECT_RULE"
    assert threshold_evidence["evidence_level"] == "project_model_source_open"
    assert threshold_evidence["broader_mml_closure"] is False
    assert threshold_evidence["server_truth_claimed"] is False
    assert set(threshold_evidence["exact_threshold_source_refs"]) <= source_ids
    assert set(threshold_evidence["corroborating_context_source_refs"]) <= source_ids

    assert set(expected) <= set(threshold_evidence["values"])
    for operation_id, (mml, application_stage) in expected.items():
        evidence_row = threshold_evidence["values"][operation_id]
        operation_row = operation_rows[operation_id]
        assert operation_row["runtime_admission_status"] == "accepted_executable_runtime"
        assert operation_row["transition"]["add"]["mml"] == mml
        assert evidence_row == {
            "add_pool_mml": mml,
            "application_stage": application_stage,
        }
