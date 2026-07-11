# Tests and Commands

Completed before final checksum/push:

- `git ls-files work/active`: exactly `work/active/ACTIVE_TASK.md`.
- `python tools/validate_active_task.py`: PASS, `ready_for_claude / claude`.
- `python -m pytest tests/tools/test_active_task_validator.py -q`: 10 passed, including the extra-tracked-file negative test.
- full `python -m pytest -q`: 241 passed.
- `python tools/validate_foundation.py`: PASS.
- `python tools/validate_m4.py`: PASS.
- `git diff --check`: PASS.
- first-read stale-claim scan: no new competing current-runtime inventory; remaining matches are scoped historical acceptance statements.

Final publication checks:

- `python tools/update_sha256sums.py`;
- `python tools/check_sha256sums.py SHA256SUMS.txt`;
- existing pre-push hook;
- remote-main/local-HEAD equality.

Any failure blocks publication as a successful cleanup result.
