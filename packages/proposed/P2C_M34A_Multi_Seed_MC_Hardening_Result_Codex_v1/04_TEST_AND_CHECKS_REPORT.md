# Test and Checks Report

## Commands run

```text
python -m pytest tests/monte_carlo/test_m34a_multi_seed_hardening.py -q
python -m pytest tests/monte_carlo -q
python tools/validate_foundation.py
python tools/validate_m4.py
python -m pytest -q
python tools/check_public_numeric_leaks.py packages/proposed/P2C_M34A_Multi_Seed_MC_Hardening_Result_Codex_v1
python tools/check_sha256sums.py packages/proposed/P2C_M34A_Multi_Seed_MC_Hardening_Result_Codex_v1/SHA256SUMS.txt
python tools/check_sha256sums.py SHA256SUMS.txt
git diff --check
```

## Results

| Check | Status |
|---|---|
| M34-A isolated test file | PASS |
| Monte Carlo test suite | PASS |
| Foundation validator | PASS |
| M4 validator | PASS |
| Full pytest suite | PASS |
| Public numeric leak scan on M34-A package | PASS |
| M34-A package SHA verification | PASS |
| Root SHA verification | PASS |
| Git whitespace check | PASS |

## Notes

Runtime tests were run because M34-A is a test implementation floor.

No public probability values are included in this report.
