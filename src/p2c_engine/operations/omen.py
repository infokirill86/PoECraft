from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from p2c_engine.domain.enums import Side


M45A_OMEN_SEMANTICS_VERSION = "p2c.m45a.independent_omen_layer.project_model.v1"
M45A_ACCEPTED_OMEN_STATUS = "accepted_executable_modifier"
M45A_AVAILABLE_STATUS = "available_project_model"
M45A_ACCEPTED_OMEN_IDS = frozenset(
    {
        "greater_exaltation",
        "sinistral_exaltation",
        "dextral_exaltation",
        "sinistral_annulment",
        "dextral_annulment",
        "sinistral_erasure",
        "dextral_erasure",
        "whittling",
        "sinistral_crystallisation",
        "dextral_crystallisation",
    }
)


class M45AOmenAdmissionError(ValueError):
    """Fail-closed Omen catalogue, admission, or compatibility defect."""


@dataclass(frozen=True, slots=True)
class ResolvedOmenEffects:
    omen_ids: tuple[str, ...] = ()
    add_count: int = 1
    add_side_filter: Side | None = None
    removal_side_filter: Side | None = None
    lowest_modifier_level: bool = False
    semantics_version: str = M45A_OMEN_SEMANTICS_VERSION

    @property
    def active_dimensions(self) -> tuple[str, ...]:
        dimensions: list[str] = []
        if self.add_count != 1:
            dimensions.append("add_count")
        if self.add_side_filter is not None:
            dimensions.append("add_side")
        if self.removal_side_filter is not None:
            dimensions.append("removal_side")
        if self.lowest_modifier_level:
            dimensions.append("removal_selector")
        return tuple(dimensions)


_PINNED_ROWS: dict[str, tuple[str, str, Mapping[str, Any]]] = {
    "greater_exaltation": (
        "exalted",
        "add_count",
        {
            "add_count_override": 2,
            "requires_free_legal_slots": 2,
            "partial_execution": False,
            "on_insufficient_slots": "NO_TRANSITION_NO_CONSUMPTION",
        },
    ),
    "sinistral_exaltation": ("exalted", "add_side", {"side_filter": "prefix"}),
    "dextral_exaltation": ("exalted", "add_side", {"side_filter": "suffix"}),
    "sinistral_annulment": ("annulment", "removal_side", {"side_filter": "prefix"}),
    "dextral_annulment": ("annulment", "removal_side", {"side_filter": "suffix"}),
    "sinistral_erasure": ("chaos", "removal_side", {"removal_side_filter": "prefix"}),
    "dextral_erasure": ("chaos", "removal_side", {"removal_side_filter": "suffix"}),
    "whittling": (
        "chaos",
        "removal_selector",
        {"selection": "minimum_modifier_level", "tie_breaker": "uniform"},
    ),
    "sinistral_crystallisation": (
        "perfect_essence",
        "removal_side",
        {"removal_side_filter": "prefix"},
    ),
    "dextral_crystallisation": (
        "perfect_essence",
        "removal_side",
        {"removal_side_filter": "suffix"},
    ),
}


def compile_omen_effects(
    omens: Mapping[str, Any],
    *,
    operation_group: str,
    active_modifier_ids: Sequence[str],
) -> ResolvedOmenEffects:
    if not isinstance(active_modifier_ids, (tuple, list)):
        raise M45AOmenAdmissionError("active_modifier_ids must be an ordered sequence")
    requested = tuple(active_modifier_ids)
    if any(not isinstance(value, str) or not value for value in requested):
        raise M45AOmenAdmissionError("active_modifier_ids must contain non-empty strings")
    if len(requested) != len(set(requested)):
        raise M45AOmenAdmissionError("duplicate Omen requests are forbidden")
    if not requested:
        return ResolvedOmenEffects()

    rows = _omen_rows(omens)
    dimensions: dict[str, str] = {}
    add_count = 1
    add_side: Side | None = None
    removal_side: Side | None = None
    lowest = False

    for omen_id in sorted(requested):
        row = rows.get(omen_id)
        if row is None:
            raise M45AOmenAdmissionError(f"unknown Omen: {omen_id}")
        if row.get("runtime_admission_status") != M45A_ACCEPTED_OMEN_STATUS:
            raise M45AOmenAdmissionError(f"Omen is not executable-admitted: {omen_id}")
        if row.get("availability_status") != M45A_AVAILABLE_STATUS:
            raise M45AOmenAdmissionError(f"Omen is not available for the M45-A project model: {omen_id}")
        pinned = _PINNED_ROWS.get(omen_id)
        if pinned is None or omen_id not in M45A_ACCEPTED_OMEN_IDS:
            raise M45AOmenAdmissionError(f"Omen is outside the M45-A allowlist: {omen_id}")
        expected_group, dimension, expected_effect = pinned
        groups = tuple(row.get("operation_groups") or ())
        if groups != (expected_group,) or operation_group != expected_group:
            raise M45AOmenAdmissionError(
                f"Omen/operation-group mismatch: {omen_id} -> {operation_group}"
            )
        effect = row.get("effect")
        if not isinstance(effect, Mapping) or dict(effect) != dict(expected_effect):
            raise M45AOmenAdmissionError(f"Omen effect contract drift: {omen_id}")
        if dimension in dimensions:
            raise M45AOmenAdmissionError(
                f"incompatible same-dimension Omens: {dimensions[dimension]}, {omen_id}"
            )
        dimensions[dimension] = omen_id

        if dimension == "add_count":
            add_count = 2
        elif dimension == "add_side":
            add_side = Side(effect["side_filter"])
        elif dimension == "removal_side":
            raw_side = effect.get("side_filter", effect.get("removal_side_filter"))
            removal_side = Side(raw_side)
        elif dimension == "removal_selector":
            lowest = True
        else:  # pragma: no cover - pinned map makes this unreachable
            raise M45AOmenAdmissionError(f"unsupported Omen effect dimension: {dimension}")

    return ResolvedOmenEffects(
        omen_ids=tuple(sorted(requested)),
        add_count=add_count,
        add_side_filter=add_side,
        removal_side_filter=removal_side,
        lowest_modifier_level=lowest,
    )


def _omen_rows(omens: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    rows: dict[str, Mapping[str, Any]] = {}
    for row in omens.get("omens") or ():
        if not isinstance(row, Mapping):
            raise M45AOmenAdmissionError("every Omen row must be a mapping")
        omen_id = row.get("omen_id")
        if not isinstance(omen_id, str) or not omen_id:
            raise M45AOmenAdmissionError("every Omen row requires omen_id")
        if omen_id in rows:
            raise M45AOmenAdmissionError(f"duplicate Omen row: {omen_id}")
        rows[omen_id] = row
    return rows


__all__ = [
    "M45A_ACCEPTED_OMEN_IDS",
    "M45A_ACCEPTED_OMEN_STATUS",
    "M45A_AVAILABLE_STATUS",
    "M45A_OMEN_SEMANTICS_VERSION",
    "M45AOmenAdmissionError",
    "ResolvedOmenEffects",
    "compile_omen_effects",
]
