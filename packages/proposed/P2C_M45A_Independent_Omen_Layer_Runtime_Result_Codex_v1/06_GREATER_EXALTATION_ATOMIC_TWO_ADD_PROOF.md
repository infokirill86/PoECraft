# Greater Exaltation Atomic Two-Add Proof

Implementation: `src/p2c_engine/monte_carlo/greater_exaltation.py`.

Verified behavior:

- exactly two sequential draws use the accepted ordinary weighted pool builder;
- the second pool is rebuilt from the actual first-add branch state;
- side and currency MML filters remain load-bearing on both draws;
- all work occurs on immutable/private branch states;
- insufficient initial capacity fails before a draw;
- an empty later pool returns the original state with no-transition/no-consumption;
- no one-modifier partial terminal exists;
- exact path mass is multiplied across the two draws;
- canonical duplicate terminals are aggregated;
- exact total mass conservation is PASS;
- seeded execution replays byte-for-byte deterministically;
- per-add pool fingerprints, candidate digests, decision IDs, and selected IDs are recorded.

The harness accepts only the ratified two-add count and an admitted Exalted-family source currency. It is not a general add-count engine.
