# Package Manifest

package_id: `P2C_Repo_Integrity_SHA_Floor_Codex_v1`
package_type: `REPO_HYGIENE_RESULT_DELTA`
status: `proposed_for_claude_audit`
observed_repo_head: `4e560c6b7a20e9b1cee6d79e52b68b7eaabd9aff`
observed_active_task_sha: `6e1f7bc1e20076e1aa002a886f079ad84132d1174a13db68f90ddcbf8f98c043`

| File | Status | Include reason | Future location |
|---|---|---|---|
| `00_README_FIRST.md` | new | Entry point, read receipt, plain-language summary | Proposed package only unless accepted |
| `01_IMPLEMENTATION_SUMMARY.md` | new | Documents repo hygiene tool and scope | Proposed package only unless accepted |
| `02_COMMANDS_AND_CHECKS.md` | new | Records required commands and check results | Proposed package only unless accepted |
| `03_BOUNDARY_REPORT.md` | new | Confirms M36-A/runtime boundaries remain closed | Proposed package only unless accepted |
| `04_CLAUDE_AUDIT_REQUEST.md` | new | Claude audit request | Proposed package only unless accepted |
| `PACKAGE_MANIFEST.md` | new | File inventory and metadata | Proposed package only unless accepted |
| `SHA256SUMS.txt` | generated | Package integrity hashes | Proposed package only unless accepted |

## Repo files changed outside package

| File | Status | Include reason | Future location |
|---|---|---|---|
| `tools/update_sha256sums.py` | new | Deterministic root SHA256SUMS updater | Repo tool |
| `manifest/GitHub_Workflow_Protocol.md` | updated | Adds root SHA update/check pre-push rule | Workflow protocol |
| `CURRENT_STATUS.md` | updated | Records M36 design acceptance and SHA floor state | Current status |
| `ledger/ACCEPTED_ARTIFACTS.md` | updated | Records accepted M36 design artifact | Accepted artifacts ledger |
| `ledger/DECISIONS.md` | updated | Records gate decision and boundaries | Decisions ledger |
| `ledger/OPEN_BLOCKERS.md` | updated | Clarifies M36 design does not close blockers | Open blockers ledger |
| `work/active/ACTIVE_TASK.md` | updated | Routes next actor to Claude audit under schema v2 | Live dispatcher |
| `SHA256SUMS.txt` | generated | Root repository integrity hashes | Repo root |

