#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(__file__).resolve().parents[1]
src = root / "src"
for candidate in (src, root):
    text = str(candidate)
    if text not in sys.path:
        sys.path.insert(0, text)

from p2c_engine.static_data import build_static_game_data, materialize_fractured_crit_state
from p2c_engine.legality import validate_item_state

static = build_static_game_data(root)
state = materialize_fractured_crit_state(static, 1)
result = validate_item_state(state, static)
assert result.ok, result.errors
print("P2C_FOUNDATION_VALIDATION: PASS")
print("STATIC_MODIFIER_INDEX_COUNT:", len(static.modifier_index))
print("SEMANTIC_FINGERPRINT:", static.semantic_fingerprint)
print("INITIAL_STATE_HASH:", state.state_hash())
