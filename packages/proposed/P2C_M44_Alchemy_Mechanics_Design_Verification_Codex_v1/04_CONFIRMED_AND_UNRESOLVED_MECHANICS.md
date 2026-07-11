# Confirmed and unresolved mechanics

## Confirmed enough for the project basis

- Valid public input rarities: Normal and Magic.
- Output rarity: Rare.
- Magic input's original explicit modifiers are not retained.
- The result has four newly generated random explicit modifiers.
- Alchemy is currently a catalog/data-reference candidate, not accepted executable runtime.
- Ordinary Rare quarterstaff capacity and family/group/item-class legality remain governed by the accepted shared kernel.

## Proposed project-model rules for a later explicit gate

- Build from an isolated empty Rare working state that retains base identity and non-explicit item metadata.
- Generate four modifiers sequentially through the accepted ordinary weighted add pool.
- Rebuild legality and weights after every accepted draw.
- Require all four draws to succeed before commit.
- Treat an empty legal pool before the fourth draw as whole-operation no-transition/no-consumption.

These rules are mechanically auditable and reuse accepted kernels, but the public sources checked do not expose the server's internal four-modifier sampling algorithm. They remain project-model rules.

## Unresolved mechanics

### Fractured input

Public evidence supports both replacement of original Magic modifiers and immutability of fractured modifiers, but does not directly state Alchemy's behavior on a fractured Magic item. Required M44-A floor: reject any input containing a fractured explicit modifier, unchanged and unconsumed. A later source/gate may broaden this.

### Exact internal distribution

No checked source establishes whether the four modifiers are sampled by the same sequential weighted procedure as four ordinary additions, by a combined-set roll, or by another server-internal method. M44-A may adopt sequential accepted-pool sampling only as explicitly labelled project-model behavior.

### Non-equipment item classes

The project objective is quarterstaff crafting. Maps, jewels, and other special-capacity item classes are outside M44-A. Their Alchemy rules must not be inferred from this floor.
