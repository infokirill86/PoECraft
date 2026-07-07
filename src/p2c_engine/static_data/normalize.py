from __future__ import annotations
from typing import Any
from p2c_engine.domain.enums import Side
from p2c_engine.domain.static_modifier import StaticModifier


def _weight(row: dict[str, Any]) -> int:
    value = row.get("generation_weight", row.get("weight", 0))
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"Active generation weight must be integer for {row.get('mod_id')}: {value!r}")
    return value


def normalize_modifier(row: dict[str, Any], category: str, *, forced_tier: int | None = None) -> StaticModifier:
    return StaticModifier(
        mod_id=str(row["mod_id"]),
        family_id=str(row["family_id"]),
        side=Side(str(row["side"])),
        group_ids=tuple(sorted(str(x) for x in (row.get("group_ids") or []))),
        tier=int(forced_tier if forced_tier is not None else row.get("tier", 1)),
        modifier_level=int(row["modifier_level"]),
        tags=tuple(sorted(str(x) for x in (row.get("tags") or []))),
        generation_weight=_weight(row),
        static_category=category,
        lich_tag=str(row["lich_tag"]) if row.get("lich_tag") is not None else None,
    )
