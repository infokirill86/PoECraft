from __future__ import annotations
from pathlib import Path
from typing import Any
import yaml
from jsonschema import Draft202012Validator


def load_yaml(root: Path, rel: str) -> Any:
    path = root / rel
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def validate_schema(instance: Any, schema: dict[str, Any]) -> list[str]:
    validator = Draft202012Validator(schema)
    return [e.message for e in sorted(validator.iter_errors(instance), key=lambda e: list(e.absolute_path))]
