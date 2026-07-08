# Validation and Test Report

## Commands run

```text
python tools/validate_foundation.py
python tools/validate_m4.py
python -m pytest tests/static_data -q
python -m pytest -q
python tools/check_sha256sums.py packages/proposed/P2C_Operation_Runtime_Admission_Metadata_Floor_Codex_v1/SHA256SUMS.txt
python tools/check_sha256sums.py SHA256SUMS.txt
python tools/check_no_nested_zips.py packages/proposed/P2C_Operation_Runtime_Admission_Metadata_Floor_Codex_v1
```

## Results

| Check | Result |
|---|---|
| Foundation validator | PASS |
| Static modifier count | 188 |
| Semantic fingerprint | `acc50b83bd6b94835fe9544266ebf7863c67938957a4aa0408d4262765ee7c25` |
| Initial state hash | `6f50bd3a650f615821750eef8b8de8f1b18d63b8e024dda1091abb4009806b32` |
| M4 validator | PASS |
| Static-data pytest suite | 31 passed |
| Full pytest suite | 118 passed |
| Package SHA check | PASS |
| Root SHA check | PASS |
| Nested ZIP check | PASS |

## New/updated test coverage

Added or updated tests proving:

- missing `runtime_admission_status` fails validation;
- all 37 operation rows carry explicit status and only `annulment` is executable-admitted in `operations.yaml`;
- inactive rows cannot be marked executable-admitted;
- active catalog candidates such as `chaos` no longer affect runtime semantic projection;
- accepted runtime `annulment` still affects runtime semantic projection;
- Perfect Essence and Jawbone catalog changes are source changes but not runtime semantic changes until admitted.

## Semantic fingerprint note

The semantic fingerprint changed from the previous pinned value because the runtime semantic projection now excludes active catalog rows that are not executable-admitted.

This is intended behavior for this floor.
