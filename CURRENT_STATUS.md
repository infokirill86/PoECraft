# P2C — CURRENT STATUS

last_updated: 2026-07-07

Keep this file tiny. Stable rules live in START_HERE.md and manifest/Operating_Manifest_v4.md.

## Where we are
- Operating Manifest v4: accepted operating baseline.
- Participant Voice Charter: accepted; folds into START_HERE / workflow.
- GitHub repo migration: active. Goal is to make GitHub the shared project workspace so Kirill is no longer the file courier.
- M31 Monte Carlo policy: accepted after C-1 correction. M26-M30 is open/context only, not accepted source.
- M32 seeded MC harness (Layer B): **accepted** (User gate 2026-07-07, on Claude GO audit `reviews/M32_Audit_Claude_v1.md`).
- GitHub baseline import (Layer A): **PROPOSED, not accepted** — pending A1 (deps) + A2 (kernel tests/pin).

## Next gate
- M32_A1_A2_BASELINE_HYGIENE (Codex): declare reproducible deps + import M32 load-bearing kernel tests
  and re-establish the prior accepted package SHA/pin. Baseline hygiene only; no new mechanics; M33 not started.
- After that delta is audited + gated, the imported baseline can be considered for acceptance, then M33 (oracle convergence).

## Not authorized
New executable mechanics; optimizer/advice/ranking; public numeric release; source/provenance, MML, or PD-013 closure; MC execution of unaccepted operations.
