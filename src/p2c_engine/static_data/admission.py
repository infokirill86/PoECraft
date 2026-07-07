from __future__ import annotations
from typing import Any
from p2c_engine.domain.defects import StaticDataDefect
from .loaders import validate_schema


def admit_item_state_payload(payload: Any, schema: dict[str, Any]) -> Any:
    errors = validate_schema(payload, schema)
    if errors:
        raise StaticDataDefect('Invalid ItemState payload: ' + '; '.join(errors))
    return payload
