# Tests, Fingerprint, and Checks

## Test commands

- `python -m pytest -q tests/monte_carlo/test_m46a_fracture_core_runtime.py tests/monte_carlo/test_m43a_bounded_sequence_runtime.py`
- impacted accepted-operation and static-data regression selection
- `python -m pytest -q`
- `python tools/validate_foundation.py`
- `python tools/validate_m4.py`
- `python tools/validate_active_task.py work/active/ACTIVE_TASK.md`
- `python tools/update_sha256sums.py`
- `python tools/check_sha256sums.py SHA256SUMS.txt`
- `python -m compileall -q src tests`
- `git diff --check`
- `tools/hooks/pre-push`

## Results

- focused Fracture plus bounded-sequence tests: PASS;
- full regression surface: PASS (`316 passed`);
- foundation and M4 validators: PASS;
- compilation and diff hygiene: PASS;
- ACTIVE_TASK, checksum, and pre-push results are finalized immediately before publication.

## Semantic fingerprint

The semantic fingerprint changes because exactly one operation row, its project-scope group, and its clean-core evidence become runtime-active/proposed. The expected final fingerprint is recorded by the pinned governance test. No unrelated modifier, weight, Essence output, Omen, or accepted operation semantic changed.
