# Edge cases and failure semantics

## Common rules

- Unsupported or non-admitted operation id, variant, modifier bundle, or schema drift: fail closed before execution.
- Known admitted currency applied to the wrong rarity or without required capacity: explicit no-transition/no-consumption.
- Empty legal add pool: explicit no-transition/no-consumption.
- No failure may leave a rarity-only transition or consume the currency.
- Input state must remain byte-equivalent/canonically identical on no-transition.
- Exact terminal mass, including no-transition, must sum exactly to one when the later runtime is evaluated.

## Transmutation

- Input must be normal.
- A corrupted/internally inconsistent normal state containing explicit modifiers is an invariant failure, not a valid probability branch.
- Pool is built under target magic rarity.
- Selected side may be prefix or suffix from one combined legal weighted pool.
- Empty pool rolls back the proposed rarity change.

## Augmentation

- Input must be magic.
- Zero installed explicit modifiers: both prefix and suffix candidates are eligible.
- One installed prefix: suffix only through ordinary capacity filtering.
- One installed suffix: prefix only through ordinary capacity filtering.
- Two installed modifiers, or otherwise full relevant capacity: no-transition/no-consumption.
- MML changes eligible tier rows within the accepted family fallback policy; it does not override side capacity.

## Regal

- Input must be magic.
- Pool is built under target rare rarity so rare capacity and legality govern the added modifier.
- Existing magic modifiers remain installed.
- The rarity transition and added modifier commit together.
- Empty pool leaves the item magic and unchanged.

## Exalted

- Input must be rare.
- Base wrapper uses no MML and one accepted ordinary add.
- Full relevant capacity or empty pool yields no-transition/no-consumption.
- Omen parameters and multi-add overrides remain unsupported.

## Exact and MC evidence required later

- Exact rational per-row path weights and exact mass normalization.
- Target-rarity pool-build proof for Transmutation and Regal.
- Capacity-derived side forcing proof for Augmentation.
- Deterministic replay for every admitted row.
- Negative controls for wrong rarity, full capacity, unsupported modifiers, missing admission status, and deliberately wrong pool-build rarity.
- Regression proof for accepted ordinary_add, Annulment, Chaos-like, M36-A, M38-A, M39-A, and M39-B behavior.
