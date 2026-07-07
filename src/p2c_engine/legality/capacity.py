from __future__ import annotations
from collections import Counter
from p2c_engine.domain.evidence import CapacitySnapshot
from p2c_engine.domain.item_state import ItemState
from p2c_engine.static_data.game_data import StaticGameData

CAPACITY={"normal":{"prefix":0,"suffix":0},"magic":{"prefix":1,"suffix":1},"rare":{"prefix":3,"suffix":3}}

def capacity_snapshot(state: ItemState, static: StaticGameData) -> CapacitySnapshot:
    counts=Counter()
    for instance in state.modifiers:
        counts[static.modifier_index[instance.mod_id].side.value]+=1
    if state.unrevealed_desecrated:
        counts[state.unrevealed_desecrated.side.value]+=1
    rarity=state.rarity.value
    crafted=sum(m.crafted for m in state.modifiers)
    desecrated=sum(m.desecrated for m in state.modifiers)+int(state.unrevealed_desecrated is not None)
    return CapacitySnapshot(
        rarity=rarity, prefix_used=counts['prefix'], suffix_used=counts['suffix'],
        total_used=len(state.modifiers)+int(state.unrevealed_desecrated is not None),
        prefix_capacity=CAPACITY[rarity]['prefix'], suffix_capacity=CAPACITY[rarity]['suffix'],
        total_capacity=sum(CAPACITY[rarity].values()), crafted_count=crafted,
        crafted_limit=1+int(state.astrid_installed), desecrated_count=desecrated, desecrated_limit=1,
    )
