# Commands and Results

Commands run by Codex:

```text
python -m pytest tests/monte_carlo/test_m37a_chaoslike_remove_then_add_runtime.py -q
```

Result:

```text
12 passed
```

```text
python -m pytest tests/monte_carlo/test_m37a_chaoslike_remove_then_add_runtime.py tests/static_data/test_m7h1_governance_fingerprint.py tests/static_data/test_foundation_revision_v8_2.py -q
```

Result:

```text
30 passed
```

```text
python tools/validate_foundation.py
```

Result:

```text
P2C_FOUNDATION_VALIDATION: PASS
STATIC_MODIFIER_INDEX_COUNT: 188
SEMANTIC_FINGERPRINT: 18339351096e3e925907f2901763f36d69325e4e76bc47ab5db8fbe75c719203
```

```text
python tools/validate_m4.py
```

Result:

```text
P2C_M4_VALIDATION: PASS
```

```text
python -m pytest tests/monte_carlo -q
```

Result:

```text
59 passed
```

```text
python -m pytest -q
```

Result:

```text
140 passed
```

Final repo-integrity commands will be rerun before commit/push:

```text
python tools/update_sha256sums.py
python tools/check_sha256sums.py SHA256SUMS.txt
```

