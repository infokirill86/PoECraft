# M33-P0 Acceptance and M33-P1 Limits

## Accepted from P0

ChatGPT/User accepted M33-P0 as a valid first rung:

- foundation tests accepted as partial;
- shared-kernel enforcement sufficient for P0;
- scope remained clean;
- accepted `ordinary_add` only;
- no new mechanics;
- no optimizer, advice, ranking, economics, or public numeric release.

## Not accepted from P0

The gate explicitly did not accept:

- full M33 oracle-convergence validation;
- any claim that Monte Carlo convergence is statistically proven.

## What P1 adds

P1 adds a stronger statistical test layer:

- per-branch tolerance derived from exact/oracle branch probability;
- sample-count tiers;
- fixed seed and hard divergence rules;
- broader skewed fixture.

## What P1 still does not claim

P1 does not claim server-truth probability.

P1 does not authorize public probability release.

P1 does not start M34.
