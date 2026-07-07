from __future__ import annotations

from dataclasses import dataclass

from p2c_engine.domain.action import ActionIdentityEnvelope, ActionPlan, ActionPlanSemanticProjection
from p2c_engine.domain.action_fingerprint import action_fingerprint
from p2c_engine.domain.defects import ActionFingerprintMismatch, TraceSchemaVersionMismatch

TRACE_SCHEMA_VERSION_V2 = 2


@dataclass(frozen=True, slots=True)
class TraceV2Envelope:
    trace_schema_version: int
    semantic_fingerprint: str
    action_identity: ActionIdentityEnvelope
    action_projection: ActionPlanSemanticProjection | None
    compact: bool


def build_trace_v2_envelope(action_plan: ActionPlan, *, compact: bool = False) -> TraceV2Envelope:
    projection = action_plan.semantic_projection()
    if action_fingerprint(projection) != action_plan.action_fingerprint:
        raise ActionFingerprintMismatch("action projection does not match action fingerprint")
    envelope = TraceV2Envelope(
        trace_schema_version=TRACE_SCHEMA_VERSION_V2,
        semantic_fingerprint=action_plan.static_semantic_fingerprint,
        action_identity=action_plan.identity_envelope(),
        action_projection=None if compact else projection,
        compact=compact,
    )
    verify_trace_v2_envelope(envelope)
    return envelope


def verify_trace_v2_envelope(envelope: TraceV2Envelope) -> None:
    if envelope.trace_schema_version != TRACE_SCHEMA_VERSION_V2:
        raise TraceSchemaVersionMismatch(
            f"Trace schema mismatch: expected {TRACE_SCHEMA_VERSION_V2}, got {envelope.trace_schema_version}"
        )
    if envelope.action_projection is None:
        return
    projected = action_fingerprint(envelope.action_projection)
    if projected != envelope.action_identity.action_fingerprint:
        raise ActionFingerprintMismatch("trace v2 action projection fingerprint mismatch")
