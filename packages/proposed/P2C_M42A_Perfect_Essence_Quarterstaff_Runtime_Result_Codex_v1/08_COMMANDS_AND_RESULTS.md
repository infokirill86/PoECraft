# Commands and results

| Command | Result |
|---|---|
| `python -m pytest tests/monte_carlo/test_m42a_perfect_essence_runtime.py -q` | PASS; 19 tests |
| `python tools/validate_foundation.py` | PASS; proposed semantic fingerprint reproduced |
| `python tools/validate_m4.py` | PASS |
| `python -m pytest -q --basetemp .pytest_tmp_m42a_full_final -p no:cacheprovider` | PASS; 239 tests |
| `python tools/validate_active_task.py` | PASS; ready for Claude |
| `python tools/update_sha256sums.py` | PASS; root manifest regenerated from staged Git-normalized bytes |
| `python tools/check_sha256sums.py SHA256SUMS.txt` | PASS |

The configured pre-push hook reruns ACTIVE_TASK and checksum validation during publication.
