# Package Manifest

Package: `P2C_M33_P1_Statistical_Convergence_Result_Codex_v1`

Package type: `STATISTICAL_CONVERGENCE_RESULT_DELTA`

Status: proposed for Claude audit.

Base commit: `f8b8f13`

## Files

| Path | Status | Include reason | Future location |
|---|---|---|---|
| `00_README_FIRST.md` | new | Entry point and scope boundary | Proposed package |
| `01_HUMAN_SUMMARY.md` | new | Plain-language summary for human review | Proposed package |
| `02_IMPLEMENTATION_REPORT.md` | new | Describes the test-only P1 delta | Proposed package |
| `03_STATISTICAL_POLICY.md` | new | Documents tolerance, seed, tiers, and divergence policy | Proposed package |
| `04_TEST_AND_CHECKS_REPORT.md` | new | Captures validation command statuses | Proposed package |
| `05_BOUNDARY_REPORT.md` | new | Confirms forbidden scope was not entered | Proposed package |
| `06_P0_ACCEPTANCE_AND_P1_LIMITS.md` | new | Separates P0 partial acceptance from proposed P1 | Proposed package |
| `07_CLAUDE_AUDIT_REQUEST.md` | new | External audit request | Proposed package |
| `PACKAGE_MANIFEST.md` | new | Package file inventory | Proposed package |
| `SHA256SUMS.txt` | generated | Byte-level package integrity evidence | Proposed package |

## Repo files changed outside this package

| Path | Status | Include reason |
|---|---|---|
| `tests/monte_carlo/test_m33_oracle_convergence.py` | modified | M33-P1 statistical convergence tests |
| `CURRENT_STATUS.md` | updated | Records P0 partial acceptance and P1 ready-for-Claude status |
| `ledger/ACCEPTED_ARTIFACTS.md` | updated | Records P0 partial acceptance only |
| `ledger/DECISIONS.md` | updated | Records gate decision and P1 scope |
| `work/active/ACTIVE_TASK.md` | updated | Routes next actor to Claude |
| `SHA256SUMS.txt` | updated | Root repository integrity file |
