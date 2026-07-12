# Proposed Jawbone Install Contract

This is the recommended later M47-A shape after `M47-D1` and `M47-D2` are decided.

## Inputs

- one of the three prepared quarterstaff-compatible Jawbone rows;
- Rare quarterstaff;
- item level allowed by the row;
- no existing placeholder and no installed Desecrated modifier;
- no unsupported modifier bundle.

## Planning

1. Validate the row and current immutable state.
2. Determine legal placeholder side and any required replacement using the explicitly gated side/replacement policy.
3. Exclude fractured instances from every replacement pool.
4. Build the complete terminal transition before drawing or mutating.
5. Store canonical placeholder context: side, Jawbone identity, reveal MML, and no Lich constraint in base M47-A.

## Commit

- if capacity is available, preserve all installed modifiers and add the placeholder capacity state;
- if a full-item replacement is required, remove exactly the selected eligible instance and add the placeholder on the resulting side;
- commit removal plus placeholder installation atomically;
- any empty pool or invalid state returns no-transition/no-consumption and preserves the original state.

No side Omen, Lich Omen, Putrefaction, or Fracture behavior belongs in base M47-A.
