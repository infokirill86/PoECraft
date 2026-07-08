# Implementation Report

## Scope used

M34-A implementation is test-only.

Added:

- `tests/monte_carlo/test_m34a_multi_seed_hardening.py`

No source runtime files were changed.

## Fixture

The main fixture is a broad skewed accepted-ordinary-add fixture.

It includes:

- eight eligible ordinary-add branches;
- rows blocked by installed family;
- rows blocked by installed group;
- rows blocked by suffix capacity.

This exercises accepted ordinary-add legality filtering without adding mechanics.

## Tests added

1. Execution contract pinning.
   - Confirms fixed seed list, sample tiers, and sigma multiplier.

2. Multi-seed single-step convergence hardening.
   - Runs the broad fixture across all fixed seeds and sample tiers.
   - Every branch must stay inside the predeclared envelope.

3. Deterministic replay.
   - Same seed and same run id must reproduce the same result hash and trajectory payload.

4. Negative-control failure reporting.
   - Forces a breach and asserts the diagnostic includes required fields.

## Numeric-output posture

The tests use counts, seeds, weights, and tolerance math internally.

The package does not publish observed probability values, success chances, percentages, decimal probability estimates, or public probability tables.
