# Commands and results

- `python -m pytest tests/monte_carlo/test_m40a_rarity_progression_runtime.py tests/static_data/test_m40a_mechanics_evidence.py -q`: PASS, `34 passed`.
- `python tools/validate_foundation.py`: PASS.
- `python tools/validate_m4.py`: PASS.
- `python -m pytest tests/tools/test_active_task_validator.py tests/tools/test_sha256sums_tools.py -q`: PASS, `9 passed`.
- `python tools/validate_active_task.py work/active/ACTIVE_TASK.md`: PASS; `ready_for_claude / claude / M40A_RARITY_PROGRESSION_RUNTIME`.
- `python -m pytest -q`: PASS, `204 passed`.
- semantic fingerprint after authorized runtime-surface retune: `cc39128cef59e699a1c530c7a9aab7169b2a19f8c5d8656af072cfc32c2dea69`.
- `python tools/update_sha256sums.py`: PASS, `521 entries` from final staged Git-normalized bytes.
- `python tools/check_sha256sums.py SHA256SUMS.txt`: PASS.
- `git diff --cached --check`: PASS.
