from __future__ import annotations

from p2c_engine.canonical.hashes import sha256_canonical
from p2c_engine.canonical.normalize import normalize_primitive

from .action import ActionPlanSemanticProjection

ACTION_SCHEMA_VERSION = 1
ACTION_FINGERPRINT_VERSION = 1


def action_fingerprint(projection: ActionPlanSemanticProjection) -> str:
    return sha256_canonical(
        normalize_primitive(projection),
        schema_version=ACTION_FINGERPRINT_VERSION,
    )
