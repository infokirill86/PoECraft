# M32 A1/A2 Baseline Hygiene Delta

Package: `P2C_M32_A1_A2_Baseline_Hygiene_Result_Codex_v1`
Package type: `BASELINE_HYGIENE_RESULT_PROPOSED`
Status: ready for Claude audit

This package responds only to Claude's Layer A required changes A1 and A2 after the M32 audit.

Boundary:

- M32 Layer B is treated as passed by the user gate.
- GitHub baseline import Layer A remains proposed, not accepted truth.
- This delta does not start M33.
- This delta does not add new executable mechanics.
- This delta does not release public numeric probabilities.
- This delta does not add optimizer, advice, ranking, EV, budget, or expected-attempt logic.
- This delta does not close source/provenance, MML, or PD-013.

## Files changed by this delta

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
- this proposed result package

## Audit focus

Claude should verify that A1 and A2 are cleared without accepting the imported baseline as project truth.
