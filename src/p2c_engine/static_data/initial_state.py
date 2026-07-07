from __future__ import annotations
from p2c_engine.domain.enums import Rarity, Side
from p2c_engine.domain.item_state import ItemState, ModifierInstance
from p2c_engine.domain.defects import StaticDataDefect
from .game_data import StaticGameData
from .admission import admit_item_state_payload


def materialize_fractured_crit_state(static: StaticGameData, tier: int, *, item_level: int = 82) -> ItemState:
    active = next(s for s in static.initial_states['states'] if s['enabled'])
    template = active['state_template']
    allowed = tuple(template['required_modifier_tier']['allowed_tiers'])
    if tier not in allowed:
        raise ValueError(f"Crit tier must be one of {allowed}, got {tier}")
    pattern = static.initial_states['canonical_materialization_contract']['fractured_crit_mod_id_pattern']
    mod_id=pattern.format(tier=tier)
    mod=static.modifier_index.get(mod_id)
    expected_side = Side(template['required_side'])
    if mod is None:
        raise StaticDataDefect(f"Unknown fractured Crit mod_id: {mod_id}")
    if mod.family_id != template['required_modifier_family'] or mod.side is not expected_side or mod.static_category != 'ordinary':
        raise StaticDataDefect(f"Invalid static Crit contract for {mod_id}")
    flags = static.initial_states['canonical_materialization_contract']['instance_flags']
    state = ItemState(
        item_class=template['item_class'], rarity=Rarity(template['rarity']), item_level=item_level,
        modifiers=(ModifierInstance(mod_id=mod_id, crafted=flags['crafted'], desecrated=flags['desecrated'], fractured=flags['fractured']),),
        unrevealed_desecrated=None, augment_socket_capacity=template['augment_socket_capacity'],
        augment_socket_used=template['augment_socket_used'], astrid_installed=template['astrid_installed'],
    )
    admit_item_state_payload(state.canonical_payload(), dict(static.item_state_schema))
    return state
