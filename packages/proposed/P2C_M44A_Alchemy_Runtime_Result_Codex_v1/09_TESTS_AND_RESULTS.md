# Tests and results

Commands run:

```text
python -m pytest -q tests/monte_carlo/test_m44a_alchemy_runtime.py
python -m pytest -q tests/monte_carlo/test_m44a_alchemy_runtime.py tests/monte_carlo/test_m43a_bounded_sequence_runtime.py tests/monte_carlo/test_m38a_operation_resolver.py tests/static_data/test_foundation_revision_v8_2.py
python -m pytest -q
python tools/validate_foundation.py
python tools/validate_m4.py
python tools/validate_active_task.py work/active/ACTIVE_TASK.md
python tools/check_public_numeric_leaks.py packages/proposed/P2C_M44A_Alchemy_Runtime_Result_Codex_v1
python tools/check_no_nested_zips.py packages/proposed/P2C_M44A_Alchemy_Runtime_Result_Codex_v1
python tools/update_sha256sums.py
python tools/check_sha256sums.py SHA256SUMS.txt
```

Results:

- M44-A focused suite: `11 passed`.
- M44-A plus resolver/sequence/static integration: `67 passed` after the final focused addition.
- full regression: `282 passed`.
- foundation validation: PASS.
- deterministic sampling/M4 validation: PASS.
- ACTIVE_TASK validation: PASS.
- proposed-package numeric leak and nested-ZIP checks: PASS.
- package and root SHA checks: PASS after final generation.
