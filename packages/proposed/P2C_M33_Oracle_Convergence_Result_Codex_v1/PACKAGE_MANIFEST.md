# Package Manifest

Package: `P2C_M33_Oracle_Convergence_Result_Codex_v1`

Package type: `ORACLE_CONVERGENCE_RESULT_DELTA`

Status: proposed for Claude audit.

Base commit: `a27d09a`

## Files

| Path | Status | Include reason | Future location |
|---|---|---|---|
| `00_README_FIRST.md` | new | Entry point and scope boundary | Proposed package |
| `01_HUMAN_SUMMARY.md` | new | Plain-language summary for human review | Proposed package |
| `02_IMPLEMENTATION_REPORT.md` | new | Describes the test-only implementation delta | Proposed package |
| `03_ORACLE_CONVERGENCE_TEST_PLAN.md` | new | Documents seed, sample count, tolerance logic, pass criteria, and limitations without public probability values | Proposed package |
| `04_TEST_AND_CHECKS_REPORT.md` | new | Captures validation command statuses | Proposed package |
| `05_BOUNDARY_REPORT.md` | new | Confirms forbidden scope was not entered | Proposed package |
| `06_NUMERIC_QUARANTINE_REPORT.md` | new | Documents public numeric-release posture | Proposed package |
| `07_CLAUDE_AUDIT_REQUEST.md` | new | External audit request | Proposed package |
| `PACKAGE_MANIFEST.md` | new | Package file inventory | Proposed package |
| `SHA256SUMS.txt` | generated | Byte-level package integrity evidence | Proposed package |

## Repo files changed outside this package

| Path | Status | Include reason |
|---|---|---|
| `tests/monte_carlo/test_m33_oracle_convergence.py` | new | M33 oracle-convergence tests |
| `CURRENT_STATUS.md` | updated | Records M33 ready-for-Claude status |
| `work/active/ACTIVE_TASK.md` | updated | Routes next actor to Claude |
| `SHA256SUMS.txt` | updated | Root repository integrity file |
