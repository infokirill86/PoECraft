# Tests and Checks

## Focused runtime and integration

```text
python -m pytest -q tests/monte_carlo/test_m47a1_jawbone_placeholder_runtime.py tests/monte_carlo/test_m46a_fracture_core_runtime.py tests/monte_carlo/test_m43a_bounded_sequence_runtime.py tests/monte_carlo/test_m38a_operation_resolver.py
PASS — 63 passed
```

## Static foundation plus new runtime

```text
python -m pytest -q tests/static_data tests/monte_carlo/test_m47a1_jawbone_placeholder_runtime.py tests/monte_carlo/test_m46a_fracture_core_runtime.py
PASS — 57 passed
```

## Full regression

The first full run identified two stale tests whose exact admitted-operation sets did not yet include the newly authorized three rows. No runtime failure occurred. Those assertions were updated, and their focused rerun passed.

```text
python -m pytest -q
PASS — 324 passed
```

## Repository controls

```text
python tools/validate_active_task.py
python tools/update_sha256sums.py
python tools/check_sha256sums.py SHA256SUMS.txt
tools/hooks/pre-push
```

Results before commit: ACTIVE_TASK schema PASS; root manifest regenerated with 805 entries; root checksum check PASS; package checksum check PASS. The configured hook runs the same dispatcher/update/check sequence again during publication and must pass before Git permits the push.
