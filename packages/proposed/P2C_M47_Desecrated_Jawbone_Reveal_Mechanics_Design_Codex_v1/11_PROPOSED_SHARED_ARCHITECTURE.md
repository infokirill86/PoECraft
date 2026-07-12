# Proposed Shared Architecture

## Resolver seam

`currency + active modifier bundle + current ItemState -> resolved single-operation plan`

The resolver must read runtime admission metadata, validate combination compatibility, and fail closed. Catalog activity never grants execution permission.

## Executors

- one data-driven Jawbone executor parameterized by row item-level/MML data;
- one Reveal executor using the canonical shared offer-pool builder;
- no copied executor per Jawbone;
- no route planning or policy selection inside either executor.

## State transition

Jawbone emits a canonical placeholder. Reveal consumes that placeholder and emits a canonical installed modifier. Both are atomic operations and can later participate in M43-A only after separate runtime admission.

## Modifier layers

Use the accepted M45 compiler pattern later:

- Necromancy filters the Jawbone side stage;
- named-Lich effects attach a stored Reveal constraint at Jawbone compilation;
- Abyssal Echoes modifies the Reveal offer-set stage;
- Omen of Light filters accepted Annulment removal candidates after revealed-removal semantics are decided.

Unsupported combinations, Putrefaction, and every unadmitted modifier fail closed.

## Validation

Exact/oracle and seeded MC must share the same state transition, pool builder, compatibility rules, and operation executors. Diagnostics must identify operation row, side policy, replacement pool digest, placeholder context, Reveal pool stages, offer-set digest, selected offer, and terminal hash without publishing numeric probabilities.
