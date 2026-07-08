# Package Manifest

Package: `P2C_M34A_Multi_Seed_MC_Hardening_Result_Codex_v1`

Package type: `MC_HARDENING_RESULT_DELTA`

Status: proposed for Claude audit.

Base commit: `cd2f28e`

## Files

| Path | Status | Include reason | Future location |
|---|---|---|---|
| `00_README_FIRST.md` | new | Entry point and scope boundary | Proposed package |
| `01_HUMAN_SUMMARY.md` | new | Plain-language summary | Proposed package |
| `02_EXECUTION_CONTRACT.md` | new | Pins seed list, sample tiers, tolerance, breach, and diagnostics contract | Proposed package |
| `03_IMPLEMENTATION_REPORT.md` | new | Documents test-only implementation | Proposed package |
| `04_TEST_AND_CHECKS_REPORT.md` | new | Captures validation command statuses | Proposed package |
| `05_DIAGNOSTICS_AND_FAILURE_REPORTING.md` | new | Documents failure reporting and negative-control proof | Proposed package |
| `06_BOUNDARY_REPORT.md` | new | Confirms forbidden scope was not entered | Proposed package |
| `07_CLAUDE_AUDIT_REQUEST.md` | new | External audit request | Proposed package |
| `PACKAGE_MANIFEST.md` | new | Package inventory | Proposed package |
| `SHA256SUMS.txt` | generated | Package integrity evidence | Proposed package |

## Repo files changed outside this package

| Path | Status | Include reason |
|---|---|---|
| `tests/monte_carlo/test_m34a_multi_seed_hardening.py` | new | M34-A multi-seed single-step hardening tests |
| `CURRENT_STATUS.md` | updated | Records M34-A ready-for-Claude status |
| `work/active/ACTIVE_TASK.md` | updated | Routes next actor to Claude |
| `SHA256SUMS.txt` | updated | Root repository integrity file |
