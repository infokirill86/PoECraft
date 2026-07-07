from __future__ import annotations
from collections import Counter
from typing import Any
from p2c_engine.domain.enums import FailureCode
from p2c_engine.domain.evidence import StateValidation, Violation
from p2c_engine.domain.item_state import ItemState
from p2c_engine.static_data.game_data import StaticGameData
from .capacity import capacity_snapshot
from .blockers import installed_blockers


def validate_item_state(state: ItemState, static: StaticGameData) -> StateValidation:
    errors=[]
    resolved=[]
    for i,instance in enumerate(state.modifiers):
        mod=static.modifier_index.get(instance.mod_id)
        if mod is None:
            errors.append(Violation(FailureCode.UNKNOWN_MOD_ID, ('modifiers',i,'mod_id'), {'mod_id':instance.mod_id}))
        else:
            resolved.append((i,instance,mod))
    if errors:
        return StateValidation(False, tuple(errors), None, None)

    cap=capacity_snapshot(state, static)
    if cap.prefix_used>cap.prefix_capacity:
        errors.append(Violation(FailureCode.SIDE_CAPACITY_EXCEEDED, ('modifiers',), {'side':'prefix','used':cap.prefix_used,'capacity':cap.prefix_capacity}))
    if cap.suffix_used>cap.suffix_capacity:
        errors.append(Violation(FailureCode.SIDE_CAPACITY_EXCEEDED, ('modifiers',), {'side':'suffix','used':cap.suffix_used,'capacity':cap.suffix_capacity}))
    if cap.total_used>cap.total_capacity:
        errors.append(Violation(FailureCode.TOTAL_CAPACITY_EXCEEDED, ('modifiers',), {'used':cap.total_used,'capacity':cap.total_capacity}))
    if cap.crafted_count>cap.crafted_limit:
        errors.append(Violation(FailureCode.CRAFTED_CAPACITY_EXCEEDED, ('modifiers',), {'used':cap.crafted_count,'capacity':cap.crafted_limit}))
    if cap.desecrated_count>cap.desecrated_limit:
        errors.append(Violation(FailureCode.DESECRATED_LIMIT_EXCEEDED, ('unrevealed_desecrated',), {'used':cap.desecrated_count,'capacity':1}))

    families=[mod.family_id for _,_,mod in resolved]
    duplicates=sorted(k for k,v in Counter(families).items() if v>1)
    if duplicates:
        errors.append(Violation(FailureCode.DUPLICATE_FAMILY_BLOCKED, ('modifiers',), {'family_ids':duplicates}))
    seen=set()
    for i,_,mod in resolved:
        overlap=sorted(seen.intersection(mod.group_ids))
        if overlap:
            errors.append(Violation(FailureCode.GROUP_CONFLICT_BLOCKED, ('modifiers',i), {'group_ids':overlap}))
            break
        seen.update(mod.group_ids)

    if state.astrid_installed and state.augment_socket_used<1:
        errors.append(Violation(FailureCode.ASTRID_SOCKET_UNAVAILABLE, ('astrid_installed',), {'augment_socket_used':state.augment_socket_used}))
    if state.augment_socket_used>state.augment_socket_capacity:
        errors.append(Violation(FailureCode.AUGMENT_SOCKET_CAPACITY_EXCEEDED, ('augment_socket_used',), {'used':state.augment_socket_used,'capacity':state.augment_socket_capacity}))

    blockers=installed_blockers(state, static)
    return StateValidation(not errors, tuple(errors), cap, blockers)
