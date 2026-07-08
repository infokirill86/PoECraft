# Test and Checks Report

## Commands run

```text
python -m pytest tests/monte_carlo/test_m35a_annulment_runtime.py -q
```

Result:

```text
10 passed
```

```text
python tools/validate_foundation.py
```

Result:

```text
P2C_FOUNDATION_VALIDATION: PASS
STATIC_MODIFIER_INDEX_COUNT: 188
SEMANTIC_FINGERPRINT: b268eb88389461d6cf5a435050278caaf0f36b3acfbf74e4bf1d29f9d2e14c3a
INITIAL_STATE_HASH: 6f50bd3a650f615821750eef8b8de8f1b18d63b8e024dda1091abb4009806b32
```

```text
python tools/validate_m4.py
```

Result:

```text
P2C_M4_VALIDATION: PASS
RNG_STREAM_VERSION: 1
SAMPLING_ALGORITHM_ID: p2c.sha256_rejection.v1
TRACE_SCHEMA_VERSION: 1
SELECTED_KEY: alpha
```

```text
python -m pytest tests/monte_carlo -q
```

Result:

```text
37 passed
```

```text
python -m pytest -q
```

Result:

```text
114 passed
```

## Notes

The package report does not include probability tables, public probability values, success chance tables, expected attempts, EV, ranking, or advice.

