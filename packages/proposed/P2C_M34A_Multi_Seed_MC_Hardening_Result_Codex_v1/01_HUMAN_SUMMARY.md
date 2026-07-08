# Human Summary

## What was done

M34-A added a test-only hardening layer for Monte Carlo.

M33 checked that seeded Monte Carlo converges against the exact/oracle layer. M34-A asks a stronger practical question: does this still behave correctly across several fixed seeds, and does the system fail loudly with useful debug information if a branch violates the tolerance rule?

## Why it matters

Monte Carlo is random-looking by design, even though our version is deterministic for a fixed seed. A single seed can pass while hiding a bad edge case. M34-A makes the foundation more trustworthy by checking a fixed seed set and requiring deterministic replay for each seed.

## What changed

Added:

- `tests/monte_carlo/test_m34a_multi_seed_hardening.py`

Added package:

- `packages/proposed/P2C_M34A_Multi_Seed_MC_Hardening_Result_Codex_v1/`

No runtime mechanics were changed.

## What was tested

M34-A tests:

- the execution contract is pinned;
- a broad single-step accepted-ordinary-add fixture passes across fixed seeds and sample tiers;
- same seed plus same run id replays exactly;
- a negative-control forced breach raises a diagnostic failure with required fields.

## What remains proposed

M34-A remains proposed until Claude audit and ChatGPT/User gate decision.

M34-B and full M34 are not accepted by this package.

## Who is next

Next actor: Claude.
