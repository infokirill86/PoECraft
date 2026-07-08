# Human Summary

## What was done

M33-P1 strengthened the previous M33-P0 oracle test.

P0 checked that Monte Carlo was broadly following the exact/oracle branch structure. P1 replaces the loose hand-set tolerance with a statistical rule.

In plain language: for each branch, the exact layer says how often that branch should appear in the long run. Monte Carlo samples a fixed number of times with a fixed seed. P1 now checks whether the observed branch counts are inside a pre-declared statistical envelope.

## Why it matters

This reduces the risk of a test passing just because the tolerance was too forgiving. It also forces the project to state the convergence rule before looking at results.

## What changed

Modified:

- `tests/monte_carlo/test_m33_oracle_convergence.py`

Added:

- `packages/proposed/P2C_M33_P1_Statistical_Convergence_Result_Codex_v1/`

## What was tested

M33-P1 covers:

- per-branch statistical tolerance derived from exact branch probability;
- increasing sample-count tiers;
- deterministic replay through fixed seed and run id;
- hard failure if observed counts exceed the declared envelope;
- a broader skewed fixture with eight eligible branches;
- family, group, and suffix-capacity filtering inside accepted `ordinary_add`.

## What remains proposed

M33-P1 remains proposed until Claude audit and ChatGPT/User decision.

This is not full M33 acceptance yet.

## Who is next

Next actor: Claude.

## Human decision required

Yes. Claude audit should happen first, then ChatGPT/User decides whether M33-P1 is accepted.
