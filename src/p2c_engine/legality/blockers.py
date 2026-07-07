from __future__ import annotations
from p2c_engine.domain.evidence import BlockerEvidence
from p2c_engine.domain.item_state import ItemState
from p2c_engine.static_data.game_data import StaticGameData

def installed_blockers(state: ItemState, static: StaticGameData) -> BlockerEvidence:
    families=[]; groups=[]
    for instance in state.modifiers:
        mod=static.modifier_index[instance.mod_id]
        families.append(mod.family_id); groups.extend(mod.group_ids)
    return BlockerEvidence(tuple(sorted(families)), tuple(sorted(set(groups))))
