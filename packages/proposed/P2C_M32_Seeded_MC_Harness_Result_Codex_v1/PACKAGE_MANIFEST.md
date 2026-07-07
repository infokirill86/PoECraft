# Package Manifest

Package: `P2C_M32_Seeded_MC_Harness_Result_Codex_v1`
Package type: `IMPLEMENTATION_RESULT_DELTA`
Status: ready for Claude audit

| Path | Status | Include reason | Future location |
|---|---|---|---|
| `00_README_FIRST.md` | new | orientation and boundaries | package record |
| `01_IMPLEMENTATION_SUMMARY.md` | new | implementation summary | package record |
| `02_SHARED_KERNEL_REPORT.md` | new | shared kernel evidence | package record |
| `03_SEED_REPLAY_AND_PRNG_REPORT.md` | new | deterministic replay evidence | package record |
| `04_RUNTIME_INVARIANTS_REPORT.md` | new | invariant enforcement evidence | package record |
| `05_TEST_AND_SMOKE_REPORT.md` | new | validation evidence summary | package record |
| `06_M33_ORACLE_CONVERGENCE_NEXT.md` | new | next-gate boundary | package record |
| `07_CLAUDE_AUDIT_REQUEST.md` | new, patched | audit request including M32 harness and baseline import review | reviews after Claude response |
| `BASELINE_IMPORT_INVENTORY.md` | new | documentation-only baseline import transparency for Claude audit | package record |
| `PACKAGE_MANIFEST.md` | new, patched | manifest including baseline import inventory | package record |
| `SHA256SUMS.txt` | generated, patched | package integrity after documentation-only correction | package record |

Related runtime files in repo delta:

- `src/p2c_engine/monte_carlo/__init__.py`
- `src/p2c_engine/monte_carlo/ordinary_add.py`
- `tests/monte_carlo/test_m32_seeded_mc_harness.py`
- `examples/m32_seeded_mc_smoke.py`
- `pyproject.toml`

No nested packages. No ZIP. No public probability values.
