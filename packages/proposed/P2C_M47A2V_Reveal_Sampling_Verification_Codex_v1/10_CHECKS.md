# Checks

Commands and results:

```text
python -m pytest -q tests/tools/test_reveal_observation_analysis.py
python -m pytest -q
python tools/validate_active_task.py
python tools/validate_foundation.py
python tools/update_sha256sums.py
python tools/check_sha256sums.py SHA256SUMS.txt
tools/hooks/pre-push
```

- Focused analyzer tests: **5 passed**.
- Full regression: **329 passed**.
- ACTIVE_TASK schema v2 validation: **PASS**.
- Foundation validation: **PASS**.
- Semantic fingerprint: `6e7bc414416189d3d02941b63945457f4a35afafc475bc8bde54d0ddc1659a05` (unchanged).
- Root checksum and pre-push results are finalized after staging.
- Boundary diff: no crafting runtime source file changed.
