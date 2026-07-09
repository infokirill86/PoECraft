# Chaos-like Candidate Semantics

## Candidate operation

The Chaos-like candidate is a game-facing operation candidate backed by the `remove_then_add` primitive.

## Required behavior

For each input state:

1. Validate that the operation row is executable-admitted. M37 design does not grant that status.
2. Build the removal pool from installed modifier instances.
3. Exclude fractured modifiers.
4. Select one removable non-fractured installed modifier instance.
5. Remove it on a branch-copy of the item.
6. Rebuild the ordinary add pool from that branch-specific post-removal item.
7. Select one legal add candidate.
8. Add the selected modifier.
9. Commit only the fully valid remove-plus-add result.

## Atomicity

The operation is atomic.

If a precondition fails, no resource is consumed and the original item state is not mutated.

If removal succeeds on a branch-copy but the branch-specific add pool is empty, the branch yields explicit no-transition/no-consumption to the original state.

## Path and terminal identity

Path identity includes:

- operation id;
- selected removal candidate key;
- selected removed mod id and duplicate ordinal;
- post-removal branch state hash;
- selected add candidate key;
- per-step pool fingerprints/digests;
- no-transition/failure marker, if any.

Terminal identity is canonical item-state identity.

Different paths may yield the same canonical terminal state and must be aggregated.

## Greater / Perfect modes

Greater and Perfect Chaos-like rows carry MML values in `data/operations.yaml`.

They should remain separately gated from the first M37-A base implementation unless ChatGPT/User explicitly authorizes them.

