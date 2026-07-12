# Proposed Reveal Contract

This is the structural contract; the exact offer algorithm remains gated by `M47-D3` through `M47-D5`.

## Preconditions

- Rare quarterstaff;
- exactly one valid unrevealed placeholder;
- canonical Jawbone context;
- no invalid capacity/family/group state;
- no unsupported Omen bundle in base M47-A.

## Pool

- fixed to placeholder side;
- union of accepted ordinary and quarterstaff-exclusive Desecrated rows;
- item-class and item-level legality;
- installed family/group exclusion;
- Jawbone MML with accepted family fallback;
- canonical static modifier index only.

## Offer set

The later runtime must pin before execution:

- exclusive-offer guarantee policy;
- weighted sampling unit;
- without-replacement and compatibility order;
- insufficient-pool behavior;
- whether displayed order has mechanical meaning.

No result-dependent tuning is allowed. Exact and seeded execution must share this one offer builder.

## Commit

User selection replaces the placeholder with exactly one offered canonical modifier on the same side and sets `desecrated: true`. The transition is atomic; failure leaves the placeholder and entire original item unchanged and consumes nothing.
