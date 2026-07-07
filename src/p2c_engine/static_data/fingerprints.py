from __future__ import annotations
from pathlib import Path
from typing import Any
from p2c_engine.canonical import sha256_canonical


def semantic_fingerprint(value: Any) -> str:
    return sha256_canonical(value, schema_version=1)


def source_fingerprint(root: Path, rel_paths: tuple[str, ...]) -> str:
    payload = []
    for rel in sorted(rel_paths):
        payload.append({"path": rel, "text": (root / rel).read_text(encoding="utf-8")})
    return sha256_canonical(payload, schema_version=1)
