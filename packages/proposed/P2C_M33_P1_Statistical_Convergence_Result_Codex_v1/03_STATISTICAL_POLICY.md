# Statistical Policy

## Fixed policy before running

M33-P1 uses a deterministic policy:

- fixed seed per fixture;
- fixed run id per fixture;
- fixed sample-count tiers;
- fixed integer sigma multiplier;
- fixed pass/fail assertions;
- no result-dependent tolerance adjustment.

## Exact/oracle reference

The exact/oracle reference comes from:

- `OrdinaryAddMonteCarloHarness.enumerate_outcomes()`;
- `p2c_engine.sampling.exact.branch_options()`;
- the accepted ordinary-add pool builder path.

## Tolerance calculation

For each branch, exact/oracle gives numerator and denominator for branch probability.

The test checks:

```text
abs(observed_count * denominator - sample_count * numerator)
<= k * ceil_sqrt(sample_count * numerator * (denominator - numerator))
```

This is the integer-scaled version of:

```text
k * sqrt(n * p * (1 - p))
```

## Sample-count tiers

The P1 tier test uses increasing sample counts and records hard assertions in code.

The largest tier must improve over the smallest tier in the direction predicted by square-root convergence. The assertion is deliberately conservative: it requires clear shrinkage direction without claiming proof of full convergence.

## What this does not prove

This does not prove server-truth probabilities.

This does not prove all future operations.

This does not release public numeric probability values.

This does not make M33 fully accepted by itself.
