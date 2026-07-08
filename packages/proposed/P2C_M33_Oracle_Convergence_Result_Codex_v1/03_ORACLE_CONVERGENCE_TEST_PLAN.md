# Oracle Convergence Test Plan

## Objective

Validate that accepted seeded Monte Carlo behavior tracks exact/oracle branch expectations for accepted `ordinary_add` under controlled fake fixtures.

## Oracle source

The oracle path is the existing exact enumeration helper:

- `OrdinaryAddMonteCarloHarness.enumerate_outcomes()`
- `p2c_engine.sampling.exact.branch_options()`

This keeps exact/oracle expectations tied to the same candidate ordering and branch semantics used by the accepted kernel.

## Monte Carlo source

The sampled path is:

- `OrdinaryAddMonteCarloHarness.run()`
- `SeededDecisionSource`
- accepted weighted sampling kernel

## Determinism

Each fixture uses an explicit fixed seed and run id. Same seed plus same run id must remain reproducible under the M32 deterministic sampling contract.

## Fixtures

Fixtures are fake and narrow by design:

- two-branch `ordinary_add` fixture;
- three-branch `ordinary_add` fixture;
- empty-pool no-transition fixture;
- shared-builder fixture proving exact/oracle and Monte Carlo paths use the same injected builder path.

## Tolerance logic

The tests compare integer counts against exact/oracle branch weights by cross multiplication. No floating-point probability comparison is used.

The tolerance is an absolute count tolerance derived from sample count by a fixed divisor. This is intentionally conservative for a foundation validation test and is not a server-truth claim.

## Pass and fail criteria

Pass requires:

- exact/oracle branch keys match the fixture's known candidate keys;
- seeded Monte Carlo produces only oracle-known selected keys for non-empty pools;
- total observed rows equal the configured sample count;
- every observed count is within the configured integer tolerance of the exact/oracle expectation;
- empty exact/oracle pools produce no-transition Monte Carlo rows;
- the shared-builder spy proves exact and sampled paths call the same injected pool-builder route.

Fail occurs if:

- any non-ordinary operation is introduced;
- exact/oracle and Monte Carlo paths diverge in candidate identity;
- observed counts exceed tolerance;
- empty pool behavior transitions when it should not;
- the shared-builder proof fails.

## Limitations

This is not a public numeric release.

This is not a server-truth probability claim.

This does not validate optimizer behavior, economics, expected attempts, or operation expansion.
