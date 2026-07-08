# M34-A Execution Contract

The M34-A contract is pinned before execution and is not chosen after seeing results.

## Seed list

Fixed deterministic seed identifiers:

- `34001`
- `34002`
- `34003`

Replay rule:

- same seed plus same run id must replay exactly.

## Sample tiers

Fixed sample-count tiers:

- `512`
- `2048`
- `8192`

## Tolerance policy

M34-A uses the M33-P1 binomial tolerance shape:

```text
k * sqrt(n * p * (1 - p))
```

The fixed multiplier is:

- `k = 6`

Implementation uses integer-scaled comparison and avoids floating-point probability comparison.

## Breach rule

Any non-negative-control branch/tier/seed breach is a hard test failure.

Negative-control cases are explicitly marked and must prove that the suite can fail.

## Diagnostics rule

Every breach diagnostic must identify:

- fixture id;
- seed;
- run id;
- sample tier;
- branch/key;
- pool digest or equivalent;
- deviation category;
- tolerance category.
