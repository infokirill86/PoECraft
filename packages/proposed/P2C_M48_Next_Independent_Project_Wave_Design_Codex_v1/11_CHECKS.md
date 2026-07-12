# Checks

This is a documentation/design wave. Required checks before publication:

```text
python tools/validate_active_task.py
python tools/validate_foundation.py
python tools/update_sha256sums.py
python tools/check_sha256sums.py SHA256SUMS.txt
git diff --check
pre-push hook
```

Boundary check: no `src/`, runtime tests, operation/omen data, mechanics behavior, or runtime admission changes.

Results before publication:

- ACTIVE_TASK schema v2: **PASS**.
- Foundation validation: **PASS**.
- Semantic fingerprint: `6e7bc414416189d3d02941b63945457f4a35afafc475bc8bde54d0ddc1659a05` (unchanged).
- Full regression: **329 passed**.
- Package SHA, root SHA, staged diff, and pre-push results are finalized after staging.
