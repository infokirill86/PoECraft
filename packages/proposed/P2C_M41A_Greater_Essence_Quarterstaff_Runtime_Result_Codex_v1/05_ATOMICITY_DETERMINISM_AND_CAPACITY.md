# Atomicity, deterministic result, and crafted-capacity boundary

Successful behavior:

- input rarity is Magic;
- existing modifier instances and fractured flags are preserved;
- zero modifiers are removed;
- output rarity is Rare;
- exactly the declared guaranteed modifier is appended;
- there is no weighted pool and no random decision.

The transition is constructed on an immutable replacement state. Only a fully valid terminal state is returned. Invalid input rarity, family/group conflict, side capacity conflict, crafted-capacity conflict, or invalid source state returns `no_transition_no_consumption` with the original state hash.

General crafted-capacity semantics are explicitly `source_open_unverified_greater_only`. M41-A neither removes that check nor claims rules for stacking, replacement, multiple Essences, or Perfect Essences.
