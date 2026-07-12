#!/usr/bin/env python3
"""Validate and summarize quarantined M47-A2V Reveal observations.

This tool is evidence support only. It never edits runtime/data/ledger files and
never promotes an observed contour into accepted project truth.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
from typing import Any, Iterable, Mapping

import yaml
from jsonschema import Draft202012Validator, FormatChecker


SCHEMA_VERSION = "p2c.m47a2v.reveal_observation.v1"
REPORT_VERSION = "p2c.m47a2v.reveal_analysis_report.v1"
DEFAULT_SCHEMA = Path("schemas/reveal_observation.schema.yaml")


class RevealObservationError(ValueError):
    """Fail-closed input or observation-contract error."""


def load_dataset(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".jsonl":
        observations = [
            json.loads(line)
            for line in text.splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        ]
        return {"schema_version": SCHEMA_VERSION, "observations": observations}
    value = json.loads(text)
    if isinstance(value, list):
        return {"schema_version": SCHEMA_VERSION, "observations": value}
    if not isinstance(value, dict):
        raise RevealObservationError("dataset must be a JSON object, array, or JSONL stream")
    return value


def load_schema(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RevealObservationError("observation schema must be a mapping")
    return value


def validate_dataset(
    dataset: Mapping[str, Any], schema: Mapping[str, Any]
) -> tuple[dict[str, Any], ...]:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(dataset), key=lambda row: list(row.absolute_path))
    if errors:
        details = []
        for error in errors:
            path = "/".join(str(part) for part in error.absolute_path) or "<root>"
            details.append(f"{path}: {error.message}")
        raise RevealObservationError("schema validation failed: " + "; ".join(details))

    observations = tuple(dict(row) for row in dataset["observations"])
    ids = [row["observation_id"] for row in observations]
    duplicates = sorted(key for key, count in Counter(ids).items() if count > 1)
    if duplicates:
        raise RevealObservationError(f"duplicate observation_id values: {duplicates}")

    for row in observations:
        _validate_observation_contract(row)
    return observations


def _validate_observation_contract(row: Mapping[str, Any]) -> None:
    observation_id = row["observation_id"]
    if row["reveal_success_or_failure"] == "success":
        orders = sorted(offer["display_order"] for offer in row["offers"])
        if orders != [1, 2, 3]:
            raise RevealObservationError(
                f"{observation_id}: successful offers require display_order 1,2,3 exactly"
            )
    expected_mml = 40 if row["jawbone_row"] == "ancient_jawbone" else None
    if row["stored_mml"] != expected_mml:
        raise RevealObservationError(
            f"{observation_id}: stored_mml does not match accepted Jawbone placeholder context"
        )
    snapshot = row.get("eligible_pool_snapshot")
    compatible = set(row["compatible_exclusive_modifier_ids"])
    if snapshot is not None:
        snapshot_ids = {entry["modifier_id"] for entry in snapshot}
        missing = compatible - snapshot_ids
        if missing:
            raise RevealObservationError(
                f"{observation_id}: compatible exclusive IDs absent from pool snapshot: {sorted(missing)}"
            )


def analyze_observations(observations: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    rows = tuple(observations)
    successful = tuple(row for row in rows if row["reveal_success_or_failure"] == "success")
    failures = tuple(row for row in rows if row["reveal_success_or_failure"] == "failure")
    offers = tuple(offer for row in successful for offer in row["offers"])

    exclusive_offer_count = sum(bool(offer["exclusive"]) for offer in offers)
    windows_with_exclusive = sum(
        any(offer["exclusive"] for offer in row["offers"]) for row in successful
    )
    d3_testable = tuple(
        row
        for row in successful
        if row["compatible_exclusive_known"]
        and row["compatible_exclusive_modifier_ids"]
    )
    d3_violations = tuple(
        row["observation_id"]
        for row in d3_testable
        if not any(offer["exclusive"] for offer in row["offers"])
    )

    conflicts = _conflict_report(successful)
    snapshot_report = _snapshot_report(successful)
    position_report = _position_report(successful)
    d5_report = _d5_report(failures)
    setup_counts = Counter(row["setup_id"] for row in rows)

    d3_assessment = (
        "counterexample_observed"
        if d3_violations
        else "no_counterexample_in_testable_observations"
        if d3_testable
        else "inconclusive_no_confirmed_compatible_exclusive_setup"
    )
    d4_structural_violations = sorted(
        set(conflicts["within_offer_set_observation_ids"])
        | set(snapshot_report["offered_rows_missing_from_snapshot_observation_ids"])
        | set(snapshot_report["duplicate_offer_identity_observation_ids"])
    )
    d4_assessment = (
        "candidate_structurally_contradicted"
        if d4_structural_violations
        else "structurally_compatible_but_sampling_model_not_identified"
        if snapshot_report["complete_snapshot_observation_count"]
        else "inconclusive_missing_eligible_pool_snapshots"
    )

    return {
        "report_version": REPORT_VERSION,
        "classification": "internal_quarantined_evidence_only",
        "public_release_allowed": False,
        "accepted_truth_update_performed": False,
        "runtime_mechanics_update_performed": False,
        "crafting_advice_or_ranking": False,
        "observation_summary": {
            "observation_count": len(rows),
            "successful_window_count": len(successful),
            "failure_count": len(failures),
            "offer_count": len(offers),
            "exclusive_offer_count": exclusive_offer_count,
            "windows_with_exclusive_count": windows_with_exclusive,
            "exclusive_offer_frequency_internal": {
                "numerator": exclusive_offer_count,
                "denominator": len(offers),
                "value": exclusive_offer_count / len(offers) if offers else None,
            },
            "setup_observation_counts": dict(sorted(setup_counts.items())),
        },
        "d3_guaranteed_exclusive": {
            "candidate": "D3-A",
            "testable_observation_count": len(d3_testable),
            "counterexample_observation_ids": list(d3_violations),
            "assessment": d3_assessment,
            "shared_mixture_comparison": (
                "not_distinguishable_without_a_pre_registered_category_distribution"
            ),
        },
        "d4_sampling": {
            "candidate": "D4-A",
            "assessment": d4_assessment,
            "structural_violation_observation_ids": d4_structural_violations,
            "tier_row_weighting": snapshot_report,
            "family_first_comparison": (
                "not_distinguishable_from_tier_row_sampling_by_offer_windows_alone; "
                "requires repeated homogeneous setups plus complete eligible-pool snapshots"
            ),
            "display_order": position_report,
        },
        "d5_insufficient_set": d5_report,
        "family_group_conflicts": conflicts,
        "decision_support": _decision_support(),
        "limitations": [
            "No observation count alone proves an exact server algorithm.",
            "D4 weight/order identification requires homogeneous setups and complete pool snapshots.",
            "Display-position counts are screening evidence only, not proof of independence.",
            "This report cannot alter runtime, data truth, ledgers, or acceptance status.",
        ],
    }


def _conflict_report(successful: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    within_ids: list[str] = []
    installed_ids: list[str] = []
    details: list[dict[str, Any]] = []
    for row in successful:
        observation_conflict = False
        offers = row["offers"]
        for left, right in combinations(offers, 2):
            shared_groups = sorted(set(left["group_ids"]) & set(right["group_ids"]))
            same_family = left["family_id"] == right["family_id"]
            if same_family or shared_groups:
                observation_conflict = True
                details.append(
                    {
                        "observation_id": row["observation_id"],
                        "kind": "within_offer_set",
                        "left": left["modifier_id"],
                        "right": right["modifier_id"],
                        "same_family": same_family,
                        "shared_group_ids": shared_groups,
                    }
                )
        if observation_conflict:
            within_ids.append(row["observation_id"])

        installed_families = set(row["installed_family_ids"])
        installed_groups = set(row["installed_group_ids"])
        bad_offers = [
            offer["modifier_id"]
            for offer in offers
            if offer["family_id"] in installed_families
            or bool(set(offer["group_ids"]) & installed_groups)
        ]
        if bad_offers:
            installed_ids.append(row["observation_id"])
            details.append(
                {
                    "observation_id": row["observation_id"],
                    "kind": "conflicts_with_installed_state",
                    "modifier_ids": sorted(bad_offers),
                }
            )
    return {
        "within_offer_set_observation_ids": sorted(set(within_ids)),
        "installed_state_conflict_observation_ids": sorted(set(installed_ids)),
        "details": details,
    }


def _snapshot_report(successful: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    complete = 0
    weighted = 0
    missing_rows: list[str] = []
    duplicate_ids: list[str] = []
    for row in successful:
        snapshot = row.get("eligible_pool_snapshot")
        offer_keys = [(offer["modifier_id"], offer["tier"]) for offer in row["offers"]]
        if len(offer_keys) != len(set(offer_keys)):
            duplicate_ids.append(row["observation_id"])
        if snapshot is None:
            continue
        complete += 1
        snapshot_keys = {(entry["modifier_id"], entry["tier"]) for entry in snapshot}
        if not set(offer_keys) <= snapshot_keys:
            missing_rows.append(row["observation_id"])
        if snapshot and all(entry.get("generation_weight") is not None for entry in snapshot):
            weighted += 1
    return {
        "complete_snapshot_observation_count": complete,
        "weighted_snapshot_observation_count": weighted,
        "offered_rows_missing_from_snapshot_observation_ids": sorted(set(missing_rows)),
        "duplicate_offer_identity_observation_ids": sorted(set(duplicate_ids)),
        "weight_model_assessment": (
            "screening_possible_but_no_exact_model_acceptance"
            if weighted
            else "inconclusive_missing_complete_generation_weights"
        ),
    }


def _position_report(successful: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    exclusive_by_position = Counter({1: 0, 2: 0, 3: 0})
    modifier_positions: dict[str, Counter[int]] = defaultdict(Counter)
    recorded = 0
    for row in successful:
        if not row["display_order_recorded"]:
            continue
        recorded += 1
        for offer in row["offers"]:
            position = offer["display_order"]
            if offer["exclusive"]:
                exclusive_by_position[position] += 1
            modifier_positions[offer["modifier_id"]][position] += 1
    return {
        "recorded_window_count": recorded,
        "exclusive_offer_counts_by_position": {
            str(key): exclusive_by_position[key] for key in (1, 2, 3)
        },
        "modifier_position_counts": {
            modifier_id: {str(position): counts[position] for position in (1, 2, 3)}
            for modifier_id, counts in sorted(modifier_positions.items())
        },
        "assessment": "screening_only_no_independence_claim",
    }


def _d5_report(failures: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    rows = tuple(failures)
    supportive = [
        row["observation_id"]
        for row in rows
        if row["item_unchanged_after_failure"] is True
        and row["currency_consumed_on_failure"] is False
    ]
    contradictions = [
        row["observation_id"]
        for row in rows
        if row["item_unchanged_after_failure"] is False
        or row["currency_consumed_on_failure"] is True
    ]
    assessment = (
        "candidate_contradicted"
        if contradictions
        else "supporting_failure_observation_present"
        if supportive
        else "inconclusive_failure_consumption_or_state_not_observed"
        if rows
        else "inconclusive_no_failure_observation"
    )
    return {
        "candidate": "D5-A",
        "failure_observation_count": len(rows),
        "supporting_observation_ids": supportive,
        "contradicting_observation_ids": contradictions,
        "assessment": assessment,
    }


def _decision_support() -> dict[str, Any]:
    return {
        "D3": {
            "accept_candidate_if": "pre-registered compatible-exclusive setups show no zero-exclusive window and no source contradiction; User still gates acceptance",
            "reject_candidate_if": "one verified successful window has a known compatible exclusive pool but contains no exclusive offer",
            "inconclusive_if": "compatible exclusive eligibility is not independently established",
            "next_decision": "ChatGPT/User explicitly accepts D3-A or selects another model",
        },
        "D4": {
            "accept_candidate_if": "complete homogeneous setup/pool captures are structurally compatible and a pre-registered model comparison supports tier-row sequential weighting; User still gates acceptance",
            "reject_candidate_if": "verified offers are outside the eligible tier-row pool, contain forbidden conflicts, or systematically contradict the pre-registered weighted model",
            "inconclusive_if": "pool snapshots/weights are missing or sample size cannot distinguish tier-row from family-first",
            "next_decision": "ChatGPT/User explicitly accepts D4-A, chooses a different project model, or requests more capture",
        },
        "D5": {
            "accept_candidate_if": "repeatable insufficient-pool failures preserve the item/placeholder and do not consume currency; User still gates acceptance",
            "reject_candidate_if": "a verified failure consumes currency, mutates state, presents fewer offers, or relaxes constraints",
            "inconclusive_if": "failure occurs but post-state/consumption is not observed",
            "next_decision": "ChatGPT/User explicitly accepts D5-A or selects observed behavior",
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate and analyze quarantined P2C Reveal observations."
    )
    parser.add_argument("dataset", type=Path)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        dataset = load_dataset(args.dataset)
        observations = validate_dataset(dataset, load_schema(args.schema))
        report = analyze_observations(observations)
    except (OSError, json.JSONDecodeError, yaml.YAMLError, RevealObservationError) as exc:
        print(f"REVEAL_OBSERVATION_ANALYSIS: FAIL: {exc}", file=sys.stderr)
        return 1
    payload = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        sys.stdout.write(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
