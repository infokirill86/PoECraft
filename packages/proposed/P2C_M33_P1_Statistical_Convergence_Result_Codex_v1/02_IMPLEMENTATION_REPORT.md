# Implementation Report

## Scope

M33-P1 is a test-only delta.

It modifies the existing M33 oracle-convergence tests and does not touch runtime mechanics.

## Main changes

The previous loose tolerance was removed.

New helper logic was added to:

- compute a per-branch scaled deviation using integer arithmetic;
- compute a per-branch statistical tolerance from exact branch probability;
- assert every observed branch count is inside the declared tolerance;
- run increasing sample-count tiers;
- assert the largest tier shows the expected shrinkage direction compared with the smallest tier;
- exercise a broader skewed fixture with family, group, and capacity filters.

## Statistical policy

For each exact branch:

```text
tolerance = k * sqrt(n * p * (1 - p))
```

Where:

- `n` is the sample count;
- `p` is the exact/oracle branch probability;
- `k` is a fixed integer sigma multiplier defined before running the test.

The implementation compares integer-scaled count deviations and avoids floating-point probability comparison.

## Confidence and divergence rule

The confidence policy is a fixed multi-sigma envelope. It is intentionally conservative for foundation validation.

Divergence is a hard test failure if any branch exceeds its predeclared tolerance.

There is no manual eyeballing after results.

## Broader fixture

The broader fixture contains eight eligible ordinary-add branches plus rows excluded by:

- installed family;
- installed group;
- full suffix capacity.

This remains accepted `ordinary_add` only. It does not introduce a new operation or new mechanic.
