# Implementation summary

## Runtime

- Added `src/p2c_engine/monte_carlo/alchemy.py`.
- Added one `AlchemyOperation` plan and one shared `AlchemyHarness`.
- Added direct exact enumeration, canonical terminal aggregation, seeded sampling, deterministic replay, internal per-add traces, diagnostics, and exact ceilings.
- Added atomic rollback for invalid inputs and any failed intermediate add.

## Admission and resolver

- Base `alchemy` is the only newly admitted operation row.
- Added the `alchemy` active operation group and handler declaration.
- Added a resolver compiler that validates the exact admitted row shape.
- Added an explicit `alchemy` executor to the M43-A registry.
- Unsupported variants and active modifiers still fail closed.

## Project-model evidence

`data/mechanics_evidence.yaml` records the sequential four-add model as User-approved, source-open project behavior. It explicitly does not claim that the server's internal sampling algorithm has been verified.

## Existing mechanics

The accepted ordinary add pool builder, family/group blockers, item-class rules, side capacities, weights, exact branching, and seeded decision source were reused. No accepted single-add mechanic was changed.
