# A1 Dependency Declaration Report

Status: implemented as proposed repo configuration; not accepted truth.

## Change

`pyproject.toml` now declares:

- package metadata for the source-layout `p2c_engine` package;
- runtime dependencies for YAML loading and JSON Schema validation;
- a dev dependency for pytest execution;
- pytest discovery paths for the restored kernel test set and the existing M32 test set.

## Purpose

Claude's A1 finding was that a clean clone could not reproduce the validation/test result without the auditor discovering dependencies manually.

This delta makes the clean-clone reproduction path explicit:

```text
python -m pip install -e ".[dev]"
python tools/validate_foundation.py
python tools/validate_m4.py
python -m pytest -q
```

## Boundary

No runtime mechanics were changed. Dependency declaration does not accept the imported baseline as project truth.
