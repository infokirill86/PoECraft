from __future__ import annotations
import json
from typing import Any
from .normalize import normalize_primitive


def canonical_json_text(value: Any, *, schema_version: int = 1) -> str:
    envelope = {"schema_version": schema_version, "value": normalize_primitive(value)}
    return json.dumps(envelope, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def canonical_json_bytes(value: Any, *, schema_version: int = 1) -> bytes:
    return canonical_json_text(value, schema_version=schema_version).encode("utf-8")
