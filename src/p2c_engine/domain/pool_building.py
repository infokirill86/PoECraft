from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .candidate import Candidate


@dataclass(frozen=True, slots=True)
class EvidenceParam:
    name: str
    value: Any


@dataclass(frozen=True, slots=True)
class ReasonExclusion:
    reason_id: str
    keys: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class PoolStageEvidence:
    stage_id: str
    input_count: int
    output_count: int
    excluded: tuple[ReasonExclusion, ...]
    params: tuple[EvidenceParam, ...] = ()


@dataclass(frozen=True, slots=True)
class MmlFallbackEvidence:
    family_id: str
    threshold: int
    retained_mod_id: str
    strongest_tier: int


@dataclass(frozen=True, slots=True)
class RemovalInstanceMetadata:
    candidate_key: str
    mod_id: str
    crafted: bool
    desecrated: bool
    fractured: bool
    duplicate_ordinal: int
    modifier_level: int
    side: str


@dataclass(frozen=True, slots=True)
class PoolBuildResult:
    candidates: tuple[Candidate, ...]
    candidate_digest: str | None
    result_fingerprint: str
    stages: tuple[PoolStageEvidence, ...]
    mml_fallbacks: tuple[MmlFallbackEvidence, ...] = ()
    removal_metadata: tuple[RemovalInstanceMetadata, ...] = ()
    empty_reason: str | None = None

