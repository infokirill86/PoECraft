# Proposed atomic multi-add architecture

## Resolver plan

The accepted single-operation resolver should compile admitted base `alchemy` to one plan, not to a public four-step user sequence:

1. Validate operation admission, item class, Normal/Magic rarity, and the non-fractured M44-A floor.
2. Clone the item into an isolated working state.
3. Remove all existing explicit modifiers from the working state only.
4. Set the working rarity to Rare.
5. Invoke the accepted ordinary-add pool builder and weighted-selection kernel four times in sequence.
6. After each selected modifier, update the working state and rebuild the next legal pool from that state.
7. Commit the completed Rare state only after all four installations succeed.

## Shared-kernel requirements

- Use the canonical modifier index.
- Use accepted item-class, required-level, family/group, prefix/suffix capacity, and weight rules.
- Do not copy pool-building or weighting logic into an Alchemy-specific implementation.
- Do not compile Alchemy through M43-A as four caller-visible currency steps; Alchemy has one consumption boundary and one atomic result.

## Failure contract

Every invalid precondition, canonical-data failure, empty intermediate pool, ceiling stop, or unsupported state returns explicit no-transition/no-consumption. The caller's original item is byte/structure-equivalent to its pre-call state. There is no partially Rare item and no state with fewer than four newly generated modifiers.

## Capacity and conflict behavior

The empty Rare quarterstaff starts with full ordinary Rare capacity. Each subsequent pool rebuild removes candidates made illegal by side capacity, family/group conflicts, item class, item level, or already installed state. The fourth selection must be legal under the state created by the first three selections.
