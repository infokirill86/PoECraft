# Package Manifest

Package: `P2C_M32_A1_A2_Baseline_Hygiene_Result_Codex_v1`
Package type: `BASELINE_HYGIENE_RESULT_PROPOSED`
Status: ready for Claude audit

| Path | Status | Include reason | Future location |
|---|---|---|---|
| `00_README_FIRST.md` | new | orientation and boundaries | package record |
| `01_A1_DEPENDENCY_DECLARATION_REPORT.md` | new | dependency declaration evidence | package record |
| `02_A2_KERNEL_TEST_RESTORATION_REPORT.md` | new | restored kernel test coverage evidence | package record |
| `03_BASELINE_PIN_RECONCILIATION.md` | new | prior baseline SHA/pin reconciliation | package record |
| `04_VALIDATION_REPORT.md` | new | validation evidence | package record |
| `05_CLAUDE_AUDIT_REQUEST.md` | new | audit request | reviews after Claude response |
| `PACKAGE_MANIFEST.md` | new | manifest | package record |
| `SHA256SUMS.txt` | generated | package integrity | package record |

Related repo delta files:

- `pyproject.toml`
- `tests/decisions/test_decision_sources.py`
- `tests/domain/test_canonical_state.py`
- `tests/legality/test_m5_audit_additions_claude.py`
- `tests/legality/test_m5_pool_builders.py`
- `tests/sampling/test_sampling_contract.py`
- `tests/static_data/test_foundation_revision_v8_1.py`
- `tests/static_data/test_foundation_revision_v8_2.py`
- `tests/static_data/test_initial_state.py`
- `tests/static_data/test_m7h1_governance_fingerprint.py`
- `tests/static_data/test_static_game_data.py`
- `work/active/M32_A1_A2_Baseline_Hygiene_Task.md`
- `work/active/ACTIVE_TASK.md`

No nested packages. No ZIP. No public probability values. No accepted-ledger update.
