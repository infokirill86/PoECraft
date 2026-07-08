# Test and Checks Report

## Commands run

```text
python -m pytest tests/monte_carlo/test_m34b1_two_step_sequence.py -q
python -m pytest tests/monte_carlo -q
python tools/validate_foundation.py
python tools/validate_m4.py
python -m pytest -q
python tools/check_public_numeric_leaks.py packages/proposed/P2C_M34B1_Result_Codex_v1
python tools/check_sha256sums.py packages/proposed/P2C_M34B1_Result_Codex_v1/SHA256SUMS.txt
python tools/check_sha256sums.py SHA256SUMS.txt
git diff --check
```

## Results

| Check | Status |
|---|---|
| M34-B1 isolated test file | PASS |
| Monte Carlo test suite | PASS |
| Foundation validator | PASS |
| M4 validator | PASS |
| Full pytest suite | PASS |
| Public numeric leak scan on M34-B1 package | PASS |
| M34-B1 package SHA verification | PASS |
| Root SHA verification | PASS |
| Git whitespace check | PASS |

## Observed test counts

| Check | Result |
|---|---|
| M34-B1 isolated tests | `8 passed` |
| Monte Carlo suite | `27 passed` |
| Full pytest suite | `104 passed` |

## Notes

Runtime tests were run because M34-B1 is an implementation floor.

This report does not release public probability values.
