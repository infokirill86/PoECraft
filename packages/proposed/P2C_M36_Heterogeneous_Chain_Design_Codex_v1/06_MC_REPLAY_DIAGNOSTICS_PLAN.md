# MC / Replay / Diagnostics Plan

## Seeded MC shape

M36 MC must execute only accepted operations through the same legality/pool/removal kernels used by exact/oracle paths.

Required properties:

- fixed seed list;
- fixed sample tiers;
- deterministic replay for a given chain id, seed, run id, and fixture;
- no choosing sample sizes after seeing results;
- comparison to exact terminal distribution where tractable;
- property/invariant checks when exact is not tractable.

## Comparison targets

For M36-A two-step fixtures:

- terminal distribution against exact oracle;
- per-step marginal checks;
- operation-specific invariant checks;
- no-transition/failure mass handling;
- duplicate terminal aggregation behavior.

## Replay trace

Every sampled chain execution should be replayable from a compact trace:

- chain id;
- seed;
- run id;
- sample index;
- step index;
- operation ref;
- state hash before step;
- pool digest or removal-pool digest;
- selected transition key;
- state hash after step;
- terminal key if final;
- failure/no-transition code if applicable.

## Hard-fail diagnostics

Every failure must identify:

- fixture id;
- chain id;
- step index;
- operation id/ref;
- seed and run id if MC;
- state hash before failure;
- pool digest;
- expected vs actual invariant category;
- whether the failure was exact, MC, replay, validator, or boundary related.

## Negative controls

M36-A should include negative controls proving the suite fails when:

- a chain references `chaos`;
- a chain references an active catalog row without runtime admission;
- a chain references an Annulment variant/omen;
- a chain tries to infer permission from `active_in_current_simulation`;
- a replay trace is mutated;
- branch-specific pool rebuild is skipped.
