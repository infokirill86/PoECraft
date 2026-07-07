import dataclasses
import pytest
from p2c_engine.domain.enums import Rarity
from p2c_engine.domain.item_state import ItemState, ModifierInstance

def state(mods):
    return ItemState('quarterstaff',Rarity.RARE,82,tuple(mods),None,2,0,False)

def test_state_frozen():
    s=state([])
    with pytest.raises(dataclasses.FrozenInstanceError): s.item_level=83

def test_hash_order_independent():
    a=ModifierInstance('a'); b=ModifierInstance('b',fractured=True)
    assert state([a,b]).state_hash()==state([b,a]).state_hash()

def test_hash_changes_semantically():
    assert state([ModifierInstance('a')]).state_hash()!=state([ModifierInstance('a',fractured=True)]).state_hash()

def test_modifier_has_only_canonical_fields():
    assert set(ModifierInstance.__dataclass_fields__)=={'mod_id','crafted','desecrated','fractured'}
