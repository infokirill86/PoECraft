from __future__ import annotations

import hashlib
from typing import Any

from .json import canonical_json_bytes


def sha256_bytes(data: bytes) -> bytes:
    """Sole raw SHA-256 primitive for the engine."""
    return hashlib.sha256(data).digest()


def sha256_canonical(value: Any, *, schema_version: int = 1) -> str:
    return sha256_bytes(canonical_json_bytes(value, schema_version=schema_version)).hex()
