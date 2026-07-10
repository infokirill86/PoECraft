# Commands and results

## Validation

```text
python tools/validate_foundation.py
P2C_FOUNDATION_VALIDATION: PASS
SEMANTIC_FINGERPRINT: 90e4b017325f6949490377358fff6538d36c1c845ad7c52fdb85a2d363b64678

python tools/validate_m4.py
P2C_M4_VALIDATION: PASS

python -m pytest -q
160 passed
```

## Focused M39-B evidence

```text
python -m pytest tests/monte_carlo/test_m39b_greater_perfect_exalted_chaos_runtime.py -q
9 passed

python tools/check_no_nested_zips.py packages/proposed/P2C_M39B_GreaterPerfect_Exalted_Chaos_Runtime_Result_Codex_v1
PASS

python tools/check_public_numeric_leaks.py packages/proposed/P2C_M39B_GreaterPerfect_Exalted_Chaos_Runtime_Result_Codex_v1
PASS
```

## Repo integrity

The final commit flow must run after all package/status files are staged:

```text
git config --get core.hooksPath
tools/hooks

python tools/update_sha256sums.py
python tools/check_sha256sums.py SHA256SUMS.txt
```

Final checksum result is recorded by the committed root manifest and push hook. No public numeric probability values were produced.
