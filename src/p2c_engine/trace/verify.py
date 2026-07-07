from __future__ import annotations

from p2c_engine.domain.versions import TRACE_SCHEMA_VERSION
from p2c_engine.domain.defects import (
    ActionFingerprintMismatch,
    SemanticFingerprintMismatch,
    TraceSchemaVersionMismatch,
)

from .schema import ReplayContext


def verify_replay_context(
    recorded: ReplayContext,
    *,
    semantic_fingerprint: str,
    action_fingerprint: str,
    pre_state_hash: str,
) -> None:
    if recorded.trace_schema_version != TRACE_SCHEMA_VERSION:
        raise TraceSchemaVersionMismatch(
            f"trace schema {recorded.trace_schema_version} != {TRACE_SCHEMA_VERSION}"
        )
    if recorded.semantic_fingerprint != semantic_fingerprint:
        raise SemanticFingerprintMismatch("semantic fingerprint mismatch")
    if (
        recorded.action_fingerprint != action_fingerprint
        or recorded.pre_state_hash != pre_state_hash
    ):
        raise ActionFingerprintMismatch("action fingerprint or pre-state hash mismatch")
