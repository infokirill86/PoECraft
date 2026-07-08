# Implementation Report

## Scope

Implemented M33 as test-only validation for the accepted M32 seeded Monte Carlo harness.

Allowed scope used:

- accepted `ordinary_add` only;
- accepted shared pool, legality, weight, and sampling kernel;
- deterministic seeded Monte Carlo;
- small known-answer artificial fixtures;
- exact/oracle comparison through the existing `enumerate_outcomes()` path.

Forbidden scope avoided:

- no new operation semantics;
- no operation expansion;
- no optimizer, advice, ranking, or economics;
- no public numeric probability release;
- no server-truth claim;
- no closure of SOURCE/PROVENANCE, MML, or PD-013.

## Files changed

Added:

- `tests/monte_carlo/test_m33_oracle_convergence.py`

Updated:

- `CURRENT_STATUS.md`
- `work/active/ACTIVE_TASK.md`
- `SHA256SUMS.txt`

Added package directory:

- `packages/proposed/P2C_M33_Oracle_Convergence_Result_Codex_v1/`

## Test design

The test file uses fake `StaticGameData` fixtures. It does not load real project data and does not create new mechanics.

For each non-empty fixture:

- exact/oracle branches are created by `OrdinaryAddMonteCarloHarness.enumerate_outcomes()`;
- seeded Monte Carlo uses `OrdinaryAddMonteCarloHarness.run()`;
- both paths use the same accepted ordinary-add pool builder route;
- selected outcomes are counted;
- counts are compared against exact/oracle branch weights using integer arithmetic and a fixed count tolerance.

The empty-pool fixture checks that exact/oracle has no branch options and Monte Carlo returns no-transition rows.

## Numeric publication posture

The tests necessarily use weights, seeds, sample counts, and count tolerances. Those are test configuration and validation mechanics, not a public probability release.

This result package does not publish observed estimates, exact probability values, percentages, decimal renderings, rational renderings, or Python fraction-constructor renderings.
