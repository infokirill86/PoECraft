# Branch-State and Pool-Rebuild Evidence

For each live exact branch and every MC trajectory:

1. the current `ItemState` is supplied to `OperationResolver`;
2. the returned single-operation plan is checked against the explicit executor registry;
3. that family harness rebuilds its pool, removal pool, feasible pool, or deterministic transition from the current state;
4. the next step receives the actual prior post-state.

Tests prove:

- add then Annulment rebuilds the removal pool from each selected add branch;
- all add paths aggregate back to one canonical terminal when Annulment removes the newly added non-fractured modifier;
- every adjacent trace has prior post-state hash equal to next pre-state hash;
- resolver-plan digests are branch-state-bound;
- a six-step mixed Essence, Chaos, Annulment, Exalted, Chaos, Annulment fixture completes through the expected executor sequence.

No root-state pool or resolved plan is reused after a state change.
