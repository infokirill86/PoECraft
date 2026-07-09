# Package Manifest

package_id: `P2C_M37A_ChaosLike_RemoveThenAdd_Runtime_Result_Codex_v1`
package_type: `IMPLEMENTATION_RESULT_PROPOSAL`
status: `proposed_for_claude_audit`
observed_repo_head: `3a9db200ac367e7c441074d27c6803f15a67c752`
observed_active_task_sha: `379e4bfcfda888f87db24599f7385035ec424926dfdb7f5f5188bef22c6513e6`

## Package files

| File | Status | Include reason | Future location |
|---|---|---|---|
| `00_README_FIRST.md` | new | Entry point, read receipt, plain-language summary | Proposed package only unless accepted |
| `01_MECHANICS_POLICY_ADOPTED.md` | new | Records accepted M37 project-model policy used by M37-A | Proposed package only unless accepted |
| `02_IMPLEMENTATION_SUMMARY.md` | new | Summarizes code/data/test changes | Proposed package only unless accepted |
| `03_EVIDENCE_TEST_MAP.md` | new | Maps requirements to tests/evidence | Proposed package only unless accepted |
| `04_COMMANDS_AND_RESULTS.md` | new | Records commands and validation results | Proposed package only unless accepted |
| `05_RISKS_AND_DEFERRED_ITEMS.md` | new | Records risks and gated exclusions | Proposed package only unless accepted |
| `06_CLAUDE_AUDIT_REQUEST.md` | new | Claude audit request | Proposed package only unless accepted |
| `PACKAGE_MANIFEST.md` | new | File inventory and package metadata | Proposed package only unless accepted |
| `SHA256SUMS.txt` | generated | Package integrity hashes | Proposed package only unless accepted |

## Repo files changed outside package

| File | Status | Include reason | Future location |
|---|---|---|---|
| `data/operations.yaml` | updated | Proposed runtime admission of base `chaos` only | Project data after audit/acceptance |
| `src/p2c_engine/monte_carlo/chaos_like.py` | new | M37-A runtime harness | Runtime after audit/acceptance |
| `src/p2c_engine/monte_carlo/__init__.py` | updated | Exports M37-A runtime symbols | Runtime after audit/acceptance |
| `tests/monte_carlo/test_m37a_chaoslike_remove_then_add_runtime.py` | new | M37-A focused test coverage | Tests after audit/acceptance |
| `tests/static_data/test_foundation_revision_v8_2.py` | updated | Reflects proposed `chaos` runtime admission | Tests after audit/acceptance |
| `tests/static_data/test_m7h1_governance_fingerprint.py` | updated | Pins new semantic fingerprint | Tests after audit/acceptance |
| `CURRENT_STATUS.md` | updated | Records mechanics/design accepted and M37-A pending audit | Current status |
| `ledger/DECISIONS.md` | updated | Records ChatGPT/User gate decision | Decisions ledger |
| `ledger/ACCEPTED_ARTIFACTS.md` | updated | Records M37 mechanics verification and design acceptance only | Accepted artifacts ledger |
| `work/active/ACTIVE_TASK.md` | updated | Routes next actor to Claude audit | Live dispatcher |
| `SHA256SUMS.txt` | generated | Root repository integrity hashes | Repo root |

