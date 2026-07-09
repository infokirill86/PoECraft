# Commands and results

## Initial sync/read receipt

```text
git rev-parse HEAD
be84534bd0908b49e911d258d457ea0b53b3cd5a

SHA-256(work/active/ACTIVE_TASK.md)
2c9f4593200f1440f0834c8e3c9d90dde90c6d9dcd4080f61a052b694167eaaf
```

## Test commands

```text
python tools/validate_foundation.py
P2C_FOUNDATION_VALIDATION: PASS

python tools/validate_m4.py
P2C_M4_VALIDATION: PASS

python -m pytest tests/monte_carlo/test_m38a_operation_resolver.py tests/legality/test_m5_pool_builders.py -q
22 passed in 0.21s

python -m pytest -q
151 passed in 96.21s
```

## Integrity commands

```text
git config core.hooksPath tools/hooks
error: could not lock config file C:/Users/infok/Documents/GitHub/PoECraft/.git/config: Permission denied

git config --get core.hooksPath
tools/hooks
```

Interpretation: this linked worktree already reports `tools/hooks` as the active hook path. The attempted write failed because the common Git config is outside the current writable root.

```text
python tools/update_sha256sums.py
UPDATED SHA256SUMS.txt: 459 entries

python tools/check_sha256sums.py SHA256SUMS.txt
PASS
```
