# Implementation Report

## Runtime support added

File changed:

- `src/p2c_engine/monte_carlo/ordinary_add.py`

Added support for:

- exact two-step sequence path enumeration;
- exact terminal distribution aggregation;
- seeded two-step sequence sampling;
- per-step trace records;
- sequence run result hashes;
- no-transition step records;
- exact path ceiling failure.

The implementation reuses the existing `OrdinaryAddMonteCarloHarness` and its injected ordinary-add pool builder.

## Important implementation boundaries

The implementation does not add a new operation family.

The implementation does not add a planner.

The implementation does not implement variable-length sequences.

The implementation does not change accepted ordinary-add mechanics.

## Exact/oracle behavior

Exact two-step enumeration:

1. Builds the step-one pool from the initial state.
2. Applies each accepted ordinary-add branch to create a branch-specific state.
3. Rebuilds the step-two pool from that branch-specific state.
4. Sums path products into terminal canonical state identities.

Exact probabilities are represented internally as exact numerator and denominator fields.

## MC behavior

Seeded MC two-step execution:

1. Samples step one from the current state.
2. Applies the selected ordinary modifier.
3. Samples step two from the changed state.
4. Records a per-step trace and final terminal state hash.

## Diagnostics

The tests require diagnostics to identify:

- fixture id;
- seed;
- run id;
- sample tier;
- branch or terminal key;
- deviation category;
- tolerance category.
