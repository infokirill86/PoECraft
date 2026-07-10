# Shared-kernel and atomicity contract

## Exalted variants

1. Resolver loads the admitted row.
2. Resolver validates the row as one atomic ordinary weighted add on a rare item.
3. Resolver loads MML from the row.
4. Resolver emits `OrdinaryAddOperation(mml=...)`.
5. The accepted ordinary add builder performs legality, capacity, family/group blocking, MML filtering, and weighting.

## Chaos variants

1. Resolver validates the row as an atomic uniform eligible removal followed by one ordinary weighted add.
2. Base Chaos removal builds the same combined eligible non-fractured removal pool as before.
3. Each removal is applied only to a branch copy.
4. The ordinary add pool is rebuilt from that branch-specific post-removal state.
5. Row-declared MML is applied to that rebuilt add pool.
6. A completed remove+add terminal is committed atomically.
7. If the rebuilt add pool is empty, the original state is returned as no-transition/no-consumption; no remove-only terminal is exposed.

Path identity remains distinct from canonical terminal identity. Duplicate terminal states continue to aggregate through the existing exact/oracle code path.
