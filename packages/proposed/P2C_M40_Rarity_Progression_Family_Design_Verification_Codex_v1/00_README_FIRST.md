# P2C M40 Rarity Progression Family Design Verification — Codex v1

Package type: `DESIGN_MECHANICS_VERIFICATION / PROPOSED`

This package designs and verifies a shared rarity-progression family before any runtime admission:

- base, Greater, and Perfect Transmutation;
- base, Greater, and Perfect Augmentation;
- base, Greater, and Perfect Regal;
- the base Exalted currency wrapper.

## Recommendation

The boundary is right-sized. These ten catalog rows are one coherent family: each performs one ordinary weighted add, with an optional rarity transition and an optional MML filter. A future M40-A may batch them through one shared plan/executor seam, subject to Claude audit and a separate ChatGPT/User implementation gate.

The design contains one important correction: Transmutation and Regal cannot build their add pool under the input rarity. They must build against an isolated working state at the target rarity, then commit the rarity change and selected modifier atomically. A failed pool or add must leave the original state and currency unchanged.

No runtime code, operation admission, data semantics, accepted truth, public numeric output, or broader MML closure is included here.
