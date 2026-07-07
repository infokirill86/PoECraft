from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class TraceEvent:
    event_type: str
    payload: Mapping[str, Any]
