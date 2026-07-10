# Commands and results

Focused M41-A plus adjacent regression command:

`python -m pytest tests/monte_carlo/test_m41a_greater_essence_runtime.py tests/monte_carlo/test_m40a_rarity_progression_runtime.py tests/monte_carlo/test_m39b_greater_perfect_exalted_chaos_runtime.py tests/static_data/test_m7h1_governance_fingerprint.py -q --basetemp .pytest_tmp_m41a_focus -p no:cacheprovider`

Result: PASS, 59 tests.

Other completed checks:

| Command | Result |
|---|---|
| `python tools/validate_foundation.py` | PASS; semantic fingerprint `251bf97728e97c1907f6d59229120544852053dd20eba728a98aabd9ac453158` |
| `python tools/validate_m4.py` | PASS |
| `python -m pytest -q --basetemp .pytest_tmp_m41a_full_retry -p no:cacheprovider` | PASS; 220 tests |
| `python tools/validate_active_task.py` | PASS; ready for Claude |
| `python tools/update_sha256sums.py` | PASS; deterministic root manifest regenerated from staged Git-normalized bytes |
| `python tools/check_sha256sums.py SHA256SUMS.txt` | PASS |

The configured pre-push hook reruns the ACTIVE_TASK and checksum guards during publication.
