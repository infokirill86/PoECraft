# Commands and results

Commands run before packaging:

```text
python -m pytest tests/monte_carlo/test_m38a_operation_resolver.py -q
```

Result:

```text
8 passed
```

```text
python tools/validate_foundation.py
```

Result:

```text
P2C_FOUNDATION_VALIDATION: PASS
STATIC_MODIFIER_INDEX_COUNT: 188
SEMANTIC_FINGERPRINT: 18339351096e3e925907f2901763f36d69325e4e76bc47ab5db8fbe75c719203
INITIAL_STATE_HASH: 6f50bd3a650f615821750eef8b8de8f1b18d63b8e024dda1091abb4009806b32
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
67 passed
```

```text
python -m pytest -q
```

Result:

```text
148 passed
```

Repo integrity commands are run after this package is created and before commit/push:

```text
git config core.hooksPath tools/hooks
python tools/update_sha256sums.py
python tools/check_sha256sums.py SHA256SUMS.txt
```

Result:

```text
UPDATED SHA256SUMS.txt: 433 entries
PASS
```
