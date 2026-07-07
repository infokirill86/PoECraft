from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Mapping
from .enums import FailureCode, Side

@dataclass(frozen=True, slots=True)
class Violation:
    code: FailureCode
    path: tuple[str | int, ...]
    detail: Mapping[str, Any]

@dataclass(frozen=True, slots=True)
class CapacitySnapshot:
    rarity: str
    prefix_used: int
    suffix_used: int
    total_used: int
    prefix_capacity: int
    suffix_capacity: int
    total_capacity: int
    crafted_count: int
    crafted_limit: int
    desecrated_count: int
    desecrated_limit: int

@dataclass(frozen=True, slots=True)
class BlockerEvidence:
    family_ids: tuple[str, ...]
    group_ids: tuple[str, ...]

@dataclass(frozen=True, slots=True)
class StateValidation:
    ok: bool
    errors: tuple[Violation, ...]
    capacity: CapacitySnapshot | None
    blockers: BlockerEvidence | None

@dataclass(frozen=True, slots=True)
class LegalityReport:
    legal: bool
    violations: tuple[Violation, ...]
    evidence: tuple[Any, ...]
