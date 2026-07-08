# Commands and Results

## Hook / checksum

```text
git config core.hooksPath tools/hooks
```

Result: PASS.

```text
git push --dry-run origin HEAD:main
```

Result: EXPECTED BLOCK. The hook ran, regenerated `SHA256SUMS.txt`, detected that it changed, and told the actor to stage/commit the regenerated file.

```text
python tools/update_sha256sums.py
python tools/check_sha256sums.py SHA256SUMS.txt
```

Result: PASS.

## Focused M36-A tests

```text
python -m pytest tests/monte_carlo/test_m36a_heterogeneous_chain_runtime.py -q
```

Result: PASS, 10 passed.

## Neighbor accepted-operation regression

```text
python -m pytest tests/monte_carlo/test_m34b1_two_step_sequence.py tests/monte_carlo/test_m35a_annulment_runtime.py tests/monte_carlo/test_m36a_heterogeneous_chain_runtime.py -q
```

Result: PASS, 28 passed.

## Foundation validators

```text
python tools/validate_foundation.py
python tools/validate_m4.py
```

Result: PASS / PASS.

## Full test suite

```text
python -m pytest -q
```

Result: PASS, 128 passed.
