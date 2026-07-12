# Selection and Install Contract

Offer generation and player selection must be separate API calls.

## Selection request

`RevealSelectionRequest` contains:

- the exact offer-set ID;
- the unchanged pre-selection item state hash;
- one caller-selected offered modifier ID.

The engine must not choose the preferred offer, rank offers, or infer player intent. A selection outside the referenced set fails closed.

## Atomic commit

After validation:

1. Reconfirm the item/placeholder state hash matches the offer-set input.
2. Resolve the chosen offer through the canonical modifier index.
3. Reconfirm side, item class, item level, family/group, and capacity validity.
4. Replace the hidden placeholder with one installed `ModifierInstance` on the same side.
5. Set `desecrated: true`; preserve all unrelated item/modifier flags and state.
6. Commit once.

Any stale offer set, changed item, missing row, incompatible choice, or invariant failure leaves the hidden placeholder and original item unchanged. No random or weighted selection is made on behalf of the user.

## Exact/MC representation

The stochastic engine evaluates offer-set generation. The chosen offer is an explicit caller decision, not an RNG branch and not optimizer behavior. Test fixtures may enumerate all legal selections for invariant coverage, but no result may be ranked or recommended.
