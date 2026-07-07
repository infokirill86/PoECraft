from __future__ import annotations

from dataclasses import dataclass

from p2c_engine.domain.decision import DecisionRecord


@dataclass(frozen=True, slots=True)
class ReplayContext:
    trace_schema_version: int
    semantic_fingerprint: str
    action_fingerprint: str
    pre_state_hash: str


@dataclass(frozen=True, slots=True)
class AuditPool:
    decision_id: str
    candidates: tuple[tuple[str, int], ...]
    cumulative: tuple[int, ...]
    total_weight: int


@dataclass(frozen=True, slots=True)
class AuditExpansion:
    pools: tuple[AuditPool, ...]
    master_seed: int | None = None
    rng_stream_version: int | None = None
    sampling_algorithm_id: str | None = None


@dataclass(frozen=True, slots=True)
class LedgerEnvelope:
    trace_schema_version: int
    semantic_fingerprint: str
    action_fingerprint: str
    pre_state_hash: str
    post_state_hash: str | None
    outcome_kind: str | None
    decisions: tuple[DecisionRecord, ...]
    audit: AuditExpansion | None
