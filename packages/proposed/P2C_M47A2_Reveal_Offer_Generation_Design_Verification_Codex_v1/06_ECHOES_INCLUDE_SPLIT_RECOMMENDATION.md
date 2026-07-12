# Echoes Include/Split Recommendation

## Recommendation

Design the seam now; split runtime admission from base Reveal.

## Confirmed contour

- Echoes must be active before the affected Reveal.
- The player can reroll the three offered modifiers once.
- The same modifier may reappear under the already ratified project rule.
- The hidden placeholder/item state remains the subject of the reveal until one offer is installed.

## Proposed architecture

`RevealSession` stores:

- immutable source item/placeholder identity;
- initial offer set and generation trace;
- `reroll_available` and `reroll_used` flags;
- optional replacement offer set;
- the final set from which the caller selects.

Echoes calls the same offer generator with a new decision namespace. If reroll is invoked, the initial set is discarded as selectable state, but retained in diagnostics/replay history. No offer from the first and second sets may be combined.

## Why implementation must split

The repository assumes all stored constraints persist. Multiple player reports show Ancient minimum-level behavior may not persist on an Echoes reroll. Public wording does not resolve whether this is a bug or intended behavior. That uncertainty changes the offer pool and probabilities materially.

Before Echoes runtime, ChatGPT/User must choose or verify:

- whether Jawbone MML is re-applied to the rerolled set;
- whether named-Lich constraints are re-applied;
- exact consumption point if reroll or generation fails;
- whether the second generation uses the same candidate policy with only a new RNG namespace.

Suggested later floor: `M47-A2E Echoes Constraint-Persistence Verification`, followed by an explicit runtime gate.
