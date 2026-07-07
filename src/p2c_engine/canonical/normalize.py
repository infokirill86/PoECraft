from __future__ import annotations

from dataclasses import asdict, is_dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Mapping


def normalize_primitive(value: Any) -> Any:
    """Normalize already-domain-safe values into deterministic JSON primitives.

    This module intentionally imports no other p2c_engine modules.
    """
    if is_dataclass(value):
        value = asdict(value)
    if isinstance(value, Enum):
        return normalize_primitive(value.value)
    if isinstance(value, Path):
        return value.as_posix()
    if isinstance(value, Mapping):
        return {str(k): normalize_primitive(value[k]) for k in sorted(value, key=lambda x: str(x))}
    if isinstance(value, (set, frozenset)):
        normalized = [normalize_primitive(v) for v in value]
        return sorted(normalized, key=lambda x: repr(x))
    if isinstance(value, (tuple, list)):
        return [normalize_primitive(v) for v in value]
    if value is None or isinstance(value, (str, int, bool, float)):
        return value
    raise TypeError(f"Unsupported canonical value type: {type(value).__name__}")
