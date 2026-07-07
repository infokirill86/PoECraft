from pathlib import Path
import pytest
from p2c_engine.static_data import build_static_game_data, materialize_fractured_crit_state
from p2c_engine.domain.enums import Side
ROOT=Path(__file__).resolve().parents[2]

def test_all_allowed_tiers_materialize():
    static=build_static_game_data(ROOT)
    for tier in range(1,7):
        s=materialize_fractured_crit_state(static,tier)
        inst=s.modifiers[0]; mod=static.modifier_index[inst.mod_id]
        assert inst.fractured and not inst.crafted and not inst.desecrated
        assert mod.family_id=='value_to_critical_hit_chance'
        assert mod.side is Side.SUFFIX and mod.static_category=='ordinary'

def test_disallowed_tier_fails():
    static=build_static_game_data(ROOT)
    with pytest.raises(ValueError): materialize_fractured_crit_state(static,7)
