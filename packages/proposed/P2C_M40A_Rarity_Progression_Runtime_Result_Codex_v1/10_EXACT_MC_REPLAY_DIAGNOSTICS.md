# Exact/oracle, MC, replay, and diagnostics evidence

## Exact/oracle

- Every eligible pool candidate becomes an exact rational path from the accepted generation weight.
- Exact path and terminal mass sum exactly to one.
- No-transition is an explicit exact path with mass one when the operation cannot execute.
- Exact tests cover each distinct class: Transmutation, Augmentation, Regal, and Exalted.

## Seeded MC and replay

- All four distinct classes run through the accepted seeded decision source.
- Same seed, run id, state, operation, and data reproduce byte-equivalent result objects and result hashes.
- Every sampled terminal hash belongs to the exact terminal set for the same fixture.

## Diagnostics

Each trajectory records operation id, source/pool/output rarity, pre/post state hashes, decision id, selected modifier id, candidate count/digest, and no-transition reason. Public summaries remain numeric-probability-free.

## Negative controls

- target-rarity plan drift fails hard;
- non-admitted Alchemy fails closed;
- Whittling/active modifier injection fails closed;
- full or empty legal pool returns explicit no-transition/no-consumption.
