# Package Manifest

package_id: `P2C_Operation_Runtime_Admission_Metadata_Floor_Codex_v1`
package_type: `METADATA_CORRECTION_RESULT`
status: `proposed_for_claude_audit`
observed_repo_head: `d01cd80c6e21e9f66b001b25e9a4958011c454df`
observed_active_task_sha: `84e4f29a1f25560e0bfca5c09592c19ce59a0118ec89faf64db40c8f45b34878`

| File | Status | Include reason | Future location |
|---|---|---|---|
| `00_README_FIRST.md` | new | Entry point, read receipt, plain-language summary | Proposed package only unless accepted |
| `01_IMPLEMENTATION_SUMMARY.md` | new | Metadata/validator/documentation summary | Proposed package only unless accepted |
| `02_OPERATION_CLASSIFICATION_TABLE.md` | new | Full operation status table | Proposed package only unless accepted |
| `03_VALIDATION_AND_TEST_REPORT.md` | new | Test/check evidence | Proposed package only unless accepted |
| `04_BOUNDARY_REPORT.md` | new | Boundary and risk statement | Proposed package only unless accepted |
| `05_CLAUDE_AUDIT_REQUEST.md` | new | Claude audit request | Proposed package only unless accepted |
| `PACKAGE_MANIFEST.md` | new | File inventory and package metadata | Proposed package only unless accepted |
| `SHA256SUMS.txt` | generated | Package integrity hashes | Proposed package only unless accepted |

## Repo files changed outside package

| File | Status | Include reason | Future location |
|---|---|---|
| `data/operations.yaml` | updated | Adds runtime admission metadata to all operation rows | Runtime/data baseline after audit acceptance |
| `src/p2c_engine/static_data/checks.py` | updated | Validates operation runtime admission metadata | Runtime/data validation |
| `src/p2c_engine/static_data/semantic.py` | updated | Projects only executable-admitted operation semantics | Runtime/data semantic fingerprinting |
| `tests/static_data/test_foundation_revision_v8_2.py` | updated | Adds/updates metadata correction tests | Test suite |
| `tests/static_data/test_m7h1_governance_fingerprint.py` | updated | Pins corrected semantic fingerprint | Test suite |
| `manifest/GitHub_Workflow_Protocol.md` | updated | Documents active catalog vs runtime admission distinction | Workflow protocol |
| `CURRENT_STATUS.md` | updated | Records accepted reconciliation and metadata floor status | Status |
| `ledger/ACCEPTED_ARTIFACTS.md` | updated | Records accepted reconciliation artifact | Ledger |
| `ledger/DECISIONS.md` | updated | Records user gate and metadata floor authorization | Ledger |
| `ledger/OPEN_BLOCKERS.md` | updated | Clarifies blockers remain open | Ledger |
| `work/active/ACTIVE_TASK.md` | updated | Routes next actor to Claude audit | Live dispatcher |
| `SHA256SUMS.txt` | updated | Root repository integrity file | Repo root |
