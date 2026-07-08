# M34-B1 Execution Contract

## Contract status

Pinned before execution.

## Sequence contract

- Sequence length: exactly two steps.
- Step shape: accepted `ordinary_add`, then accepted `ordinary_add`.
- Fixture label: constructed project-model hardening fixture, not a real crafting route.
- Operation expansion: none.
- Planner behavior: none.

## Seed contract

Fixed seed identifiers:

- `34001`
- `34002`
- `34003`

Replay rule: same fixture, seed, run id, and sample tier must replay exactly.

## Sample-tier contract

Fixed sample-count tiers:

- `512`
- `2048`
- `8192`

Sample tiers were not chosen after seeing results.

## Exact enumeration ceiling

Fixed exact path ceiling:

- `64`

If the exact path ceiling is exceeded, the implementation fails loudly instead of skipping the oracle.

## Tolerance contract

The implementation keeps the accepted M34-A tolerance shape:

```text
k * sqrt(n * p * (one minus p))
```

Pinned multiplier:

- `6`

The comparison uses integer-scaled exact rational fields. Public package docs do not print probability values.

## Negative-control contract

M34-B1 includes a forced-breach negative control proving the diagnostic path can fail.
