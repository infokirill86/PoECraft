from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest

from tools.analyze_reveal_observations import (
    RevealObservationError,
    analyze_observations,
    load_schema,
    main,
    validate_dataset,
)


ROOT = Path(__file__).resolve().parents[2]
SCHEMA = load_schema(ROOT / "schemas/reveal_observation.schema.yaml")


def _offer(
    modifier_id: str,
    order: int,
    *,
    family: str,
    group: str,
    exclusive: bool,
    tier: int = 1,
) -> dict[str, object]:
    return {
        "modifier_id": modifier_id,
        "tier": tier,
        "family_id": family,
        "group_ids": [group],
        "exclusive": exclusive,
        "generation_weight": 1000,
        "display_order": order,
    }


def _pool_row(offer: dict[str, object]) -> dict[str, object]:
    return {key: value for key, value in offer.items() if key != "display_order"}


def _observation(observation_id: str = "obs-001") -> dict[str, object]:
    offers = [
        _offer("exclusive_a_t1", 1, family="exclusive_a", group="g_exclusive", exclusive=True),
        _offer("ordinary_b_t1", 2, family="ordinary_b", group="g_b", exclusive=False),
        _offer("ordinary_c_t1", 3, family="ordinary_c", group="g_c", exclusive=False),
    ]
    return {
        "observation_id": observation_id,
        "setup_id": "quarterstaff-preserved-prefix-fixed-v1",
        "captured_at_utc": "2026-07-12T12:00:00Z",
        "item_class": "quarterstaff",
        "item_level": 82,
        "jawbone_row": "preserved_jawbone",
        "stored_mml": None,
        "placeholder_side": "prefix",
        "installed_modifier_ids": ["installed_suffix_a"],
        "installed_family_ids": ["installed_suffix_family"],
        "installed_group_ids": ["g_installed"],
        "compatible_exclusive_known": True,
        "compatible_exclusive_modifier_ids": ["exclusive_a_t1"],
        "eligible_pool_snapshot": [_pool_row(row) for row in offers],
        "offers": offers,
        "reveal_success_or_failure": "success",
        "failure_code": None,
        "display_order_recorded": True,
        "item_unchanged_after_failure": None,
        "currency_consumed_on_failure": None,
        "screenshot_references": ["screenshots/obs-001.png"],
        "notes": "fixed pilot setup",
    }


def _dataset(*observations: dict[str, object]) -> dict[str, object]:
    return {
        "schema_version": "p2c.m47a2v.reveal_observation.v1",
        "observations": list(observations),
    }


def test_valid_dataset_reports_internal_exclusive_and_structural_evidence() -> None:
    observations = validate_dataset(_dataset(_observation()), SCHEMA)
    report = analyze_observations(observations)

    assert report["classification"] == "internal_quarantined_evidence_only"
    assert report["public_release_allowed"] is False
    assert report["accepted_truth_update_performed"] is False
    assert report["observation_summary"]["windows_with_exclusive_count"] == 1
    assert report["d3_guaranteed_exclusive"]["assessment"] == "no_counterexample_in_testable_observations"
    assert report["d4_sampling"]["assessment"] == "structurally_compatible_but_sampling_model_not_identified"
    assert report["d4_sampling"]["display_order"]["assessment"] == "screening_only_no_independence_claim"


def test_d3_counterexample_and_family_group_conflict_are_detected() -> None:
    row = _observation("obs-d3-counterexample")
    row["offers"] = [
        _offer("ordinary_a_t1", 1, family="same_family", group="shared_group", exclusive=False),
        _offer("ordinary_a_t2", 2, family="same_family", group="shared_group", exclusive=False, tier=2),
        _offer("ordinary_c_t1", 3, family="ordinary_c", group="g_c", exclusive=False),
    ]
    row["eligible_pool_snapshot"] = [
        _pool_row(offer) for offer in row["offers"]
    ] + [
        {
            "modifier_id": "exclusive_a_t1",
            "tier": 1,
            "family_id": "exclusive_a",
            "group_ids": ["g_exclusive"],
            "exclusive": True,
            "generation_weight": 1,
        }
    ]
    observations = validate_dataset(_dataset(row), SCHEMA)
    report = analyze_observations(observations)

    assert report["d3_guaranteed_exclusive"]["assessment"] == "counterexample_observed"
    assert report["d3_guaranteed_exclusive"]["counterexample_observation_ids"] == [
        "obs-d3-counterexample"
    ]
    assert report["family_group_conflicts"]["within_offer_set_observation_ids"] == [
        "obs-d3-counterexample"
    ]
    assert report["d4_sampling"]["assessment"] == "candidate_structurally_contradicted"


def test_d5_failure_support_and_contradiction_are_separated() -> None:
    supportive = _observation("obs-failure-safe")
    supportive.update(
        {
            "compatible_exclusive_known": False,
            "compatible_exclusive_modifier_ids": [],
            "eligible_pool_snapshot": [],
            "offers": [],
            "reveal_success_or_failure": "failure",
            "failure_code": "could_not_generate_mod",
            "display_order_recorded": False,
            "item_unchanged_after_failure": True,
            "currency_consumed_on_failure": False,
        }
    )
    contradicting = deepcopy(supportive)
    contradicting["observation_id"] = "obs-failure-consumed"
    contradicting["currency_consumed_on_failure"] = True

    report = analyze_observations(
        validate_dataset(_dataset(supportive, contradicting), SCHEMA)
    )
    assert report["d5_insufficient_set"]["assessment"] == "candidate_contradicted"
    assert report["d5_insufficient_set"]["supporting_observation_ids"] == [
        "obs-failure-safe"
    ]
    assert report["d5_insufficient_set"]["contradicting_observation_ids"] == [
        "obs-failure-consumed"
    ]


def test_schema_and_custom_contract_fail_closed() -> None:
    too_few = _observation()
    too_few["offers"] = too_few["offers"][:2]
    with pytest.raises(RevealObservationError, match="schema validation failed"):
        validate_dataset(_dataset(too_few), SCHEMA)

    duplicate = _observation("duplicate")
    with pytest.raises(RevealObservationError, match="duplicate observation_id"):
        validate_dataset(_dataset(duplicate, deepcopy(duplicate)), SCHEMA)

    wrong_mml = _observation("wrong-mml")
    wrong_mml["jawbone_row"] = "ancient_jawbone"
    with pytest.raises(RevealObservationError, match="stored_mml"):
        validate_dataset(_dataset(wrong_mml), SCHEMA)


def test_cli_writes_quarantined_report_without_repo_mutation(tmp_path: Path) -> None:
    dataset_path = tmp_path / "observations.json"
    output_path = tmp_path / "report.json"
    dataset_path.write_text(json.dumps(_dataset(_observation())), encoding="utf-8")

    assert main(
        [
            str(dataset_path),
            "--schema",
            str(ROOT / "schemas/reveal_observation.schema.yaml"),
            "--output",
            str(output_path),
        ]
    ) == 0
    report = json.loads(output_path.read_text(encoding="utf-8"))
    assert report["runtime_mechanics_update_performed"] is False
    assert report["crafting_advice_or_ranking"] is False
