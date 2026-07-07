from __future__ import annotations
from types import MappingProxyType
from typing import Iterable, Mapping
from p2c_engine.domain.static_modifier import StaticModifier
from p2c_engine.domain.defects import StaticDataDefect


def build_modifier_index(records: Iterable[StaticModifier]) -> Mapping[str, StaticModifier]:
    result: dict[str, StaticModifier] = {}
    duplicates: set[str] = set()
    for record in records:
        if record.mod_id in result:
            duplicates.add(record.mod_id)
        result[record.mod_id] = record
    if duplicates:
        raise StaticDataDefect(f"Duplicate mod_id values: {sorted(duplicates)}")
    return MappingProxyType(dict(sorted(result.items())))
