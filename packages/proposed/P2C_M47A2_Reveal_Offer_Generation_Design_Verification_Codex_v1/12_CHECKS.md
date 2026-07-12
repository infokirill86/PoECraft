# Checks

## Regression

```text
python -m pytest -q
PASS — 324 passed
```

This was a design/status wave. No runtime, test, operation-data, or offer-sampling behavior was changed.

## Dispatcher and repository integrity

```text
python tools/validate_active_task.py
python tools/update_sha256sums.py
python tools/check_sha256sums.py SHA256SUMS.txt
tools/hooks/pre-push
```

The dispatcher validation passed before packaging. Root checksum generation/check and the configured pre-push hook are run on the commit-ready index and must pass before publication.
