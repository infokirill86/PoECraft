# Package Manifest

package_id: `P2C_M36A_Heterogeneous_Chain_Runtime_Result_Codex_v1`
package_type: `IMPLEMENTATION_RESULT_DELTA`
status: `proposed_for_claude_audit`
observed_repo_head: `382e53bb54e228bb9f4193ddc2d44c302c257a83`
observed_active_task_sha: `fefc441c4e9e5c2d2fe13d0fa24df41e39f4f67d36fdf46f353cca0fc56c4e7e`

| File | Status | Include reason | Future location |
|---|---|---|---|
| `00_README_FIRST.md` | new | Entry point, read receipt, plain-language summary | Proposed package only unless accepted |
| `01_HOOK_IMPLEMENTATION_SUMMARY.md` | new | Documents local pre-push enforcement | Proposed package only unless accepted |
| `02_M36A_IMPLEMENTATION_SUMMARY.md` | new | Documents M36-A implementation scope | Proposed package only unless accepted |
| `03_EVIDENCE_TEST_MAP.md` | new | Maps requirements to tests/evidence | Proposed package only unless accepted |
| `04_COMMANDS_AND_RESULTS.md` | new | Records commands and results | Proposed package only unless accepted |
| `05_RISKS_AND_DEFERRED_ITEMS.md` | new | Records boundaries and deferred work | Proposed package only unless accepted |
| `06_CLAUDE_AUDIT_REQUEST.md` | new | Claude audit request | Proposed package only unless accepted |
| `PACKAGE_MANIFEST.md` | new | File inventory and package metadata | Proposed package only unless accepted |
| `SHA256SUMS.txt` | generated | Package integrity hashes | Proposed package only unless accepted |

## Repo files changed outside package

| File | Status | Include reason | Future location |
|---|---|---|---|
| `tools/hooks/pre-push` | new | Local pre-push SHA enforcement | Repo tooling |
| `manifest/GitHub_Workflow_Protocol.md` | updated | Documents hook setup command and boundary | Workflow protocol |
| `src/p2c_engine/monte_carlo/heterogeneous_chain.py` | new | M36-A runtime implementation | Runtime source |
| `tests/monte_carlo/test_m36a_heterogeneous_chain_runtime.py` | new | M36-A evidence tests | Test suite |
| `CURRENT_STATUS.md` | updated | Records SHA floor acceptance and M36-A proposed state | Current status |
| `ledger/ACCEPTED_ARTIFACTS.md` | updated | Records accepted SHA floor | Accepted artifacts ledger |
| `ledger/DECISIONS.md` | updated | Records gate decision and authorization | Decisions ledger |
| `ledger/OPEN_BLOCKERS.md` | updated | Clarifies open blockers remain open | Open blockers ledger |
| `work/active/ACTIVE_TASK.md` | updated | Routes next actor to Claude audit under schema v2 | Live dispatcher |
| `SHA256SUMS.txt` | generated | Root repository integrity hashes | Repo root |
