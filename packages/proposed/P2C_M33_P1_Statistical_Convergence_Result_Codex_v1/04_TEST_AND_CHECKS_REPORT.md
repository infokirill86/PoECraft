# Test and Checks Report

## Commands run

```text
python -m pytest tests/monte_carlo/test_m33_oracle_convergence.py -q
python -m pytest tests/monte_carlo -q
python tools/validate_foundation.py
python tools/validate_m4.py
python -m pytest -q
python tools/check_public_numeric_leaks.py packages/proposed/P2C_M33_P1_Statistical_Convergence_Result_Codex_v1
python tools/check_sha256sums.py packages/proposed/P2C_M33_P1_Statistical_Convergence_Result_Codex_v1/SHA256SUMS.txt
python tools/check_sha256sums.py SHA256SUMS.txt
git diff --check
```

## Results

| Check | Status |
|---|---|
| M33 oracle-convergence tests | PASS |
| Monte Carlo test suite | PASS |
| Foundation validator | PASS |
| M4 validator | PASS |
| Full pytest suite | PASS |
| Public numeric leak scan on M33-P1 package | PASS |
| M33-P1 package SHA verification | PASS |
| Root SHA verification | PASS |
| Git whitespace check | PASS |

## Public numeric posture

No public probability values were added to this package.

The package describes statistical rules and pass/fail status. It does not publish observed probability estimates, exact probability values, percentages, decimal renderings, rational probability renderings, or success chance tables.
