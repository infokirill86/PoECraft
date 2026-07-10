# Atomicity and target-rarity proof

## Mechanical proof points

- Transmutation resolver plans carry `pool_build_rarity: magic` and `output_rarity: magic`.
- Regal resolver plans carry `pool_build_rarity: rare` and `output_rarity: rare`.
- A spy builder test records the actual rarity passed to the shared pool builder for both families.
- Applied exact paths hash the state produced by changing rarity and adding exactly the selected modifier together.
- An injected empty pool produces one exact no-transition/no-consumption path with mass exactly one and the original state hash.
- Seeded trajectories under the same empty-pool condition retain identical pre/post hashes.
- A negative control changes a compiled Transmutation plan to build under normal rarity; contract validation fails hard before execution.

## Failure contract

Wrong source rarity, invalid source capacity, or empty legal pool returns explicit `no_transition_no_consumption`. Because `ItemState` is immutable and the working state is isolated, no partially changed rarity can leak into the result.
