# Implementation Summary

M32 adds a seeded Monte Carlo harness over the accepted `ordinary_add` operation.

Implemented files:

- `src/p2c_engine/monte_carlo/__init__.py`
- `src/p2c_engine/monte_carlo/ordinary_add.py`
- `tests/monte_carlo/test_m32_seeded_mc_harness.py`
- `examples/m32_seeded_mc_smoke.py`
- `pyproject.toml`

Runtime foundation imported into GitHub for M32:

- `src/p2c_engine/`
- `data/`
- `config/`
- `schemas/`
- `tools/validate_foundation.py`
- `tools/validate_m4.py`

The import was necessary because the GitHub bootstrap repo did not yet contain the accepted engine/data kernel needed by M32. M32 does not reimplement ordinary-add legality or weights; it delegates pool construction to the existing accepted ordinary-add pool builder.
