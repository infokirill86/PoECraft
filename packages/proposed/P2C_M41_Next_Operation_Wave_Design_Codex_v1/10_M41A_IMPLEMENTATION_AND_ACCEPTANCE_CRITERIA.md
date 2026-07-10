# Proposed M41-A Implementation and Acceptance Criteria

## One broad safe batch

Implement all eight prepared Greater Essence quarterstaff rows through one shared, data-driven executor and the accepted resolver.

## Required evidence

1. All eight rows compile from operation and output data without per-row mechanics branches.
2. Magic becomes Rare and the exact row-declared guaranteed modifier is installed.
3. Existing modifiers and fractured flags are preserved.
4. Family/group, crafted-capacity, side-capacity, and item-class checks use shared accepted validation.
5. Rarity plus modifier commit atomically.
6. Every precondition failure is no-transition/no-consumption with original state unchanged.
7. Exact distribution is normalized and deterministic.
8. Seeded execution replays identically and matches exact terminal identity.
9. Unsupported Essence tiers, Perfect Essence, Omens, and undeclared rows fail closed.
10. Accepted M40-A and all prior regression tests remain passing.
11. Runtime admission metadata changes only for the explicitly authorized rows and remains proposed until User acceptance.

## Implementation gate shape

A future User authorization should explicitly name the eight row ids, permit only Greater Essence runtime, and keep Perfect Essence and all Omen behavior closed. Claude must audit row/data consistency, atomicity, fail-closed behavior, and absence of copied per-row mechanics before acceptance.
