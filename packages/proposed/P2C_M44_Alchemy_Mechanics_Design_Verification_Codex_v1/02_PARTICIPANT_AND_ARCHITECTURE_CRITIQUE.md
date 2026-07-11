# Participant and architecture critique

## Is Alchemy the correct next move?

Yes. M43-A completed safe composition of already accepted operations. Another sequence-only hardening wave would now add less simulator value than admitting a coherent new currency. Alchemy directly extends the item-generation surface and exercises a genuinely new, but bounded, atomic multi-add shape.

## Is base Alchemy one coherent wave?

Yes, with one boundary correction. The clean core is:

- non-fractured Normal or Magic equipment input;
- discard existing explicit modifiers;
- create an isolated Rare working state;
- generate exactly four legal ordinary weighted modifiers;
- commit only after the fourth successful generation.

Fractured Magic input should not be bundled. "Original modifiers are not retained" and "fractured modifiers cannot be removed or modified" are individually supported, but their joint Alchemy behavior was not directly documented by the sources checked. Guessing would turn a clean operation admission into an unapproved source/mechanics decision.

## Better alternative?

No broader alternative is safer. Omens change other operations and require a modifier-layer gate. Fracture introduces target locking and more source-sensitive eligibility. More chain hardening would drift back toward infrastructure. Base non-fractured Alchemy is the widest coherent next floor.

## Architecture objection to avoid

Do not implement Alchemy as four calls that mutate the caller's live item. The four draws are one currency action. A failure after any intermediate draw must roll back the entire action. The implementation should use an isolated Rare working copy and one final commit.
