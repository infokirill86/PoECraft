# Test and Smoke Report

Validation commands executed:

```text
python tools/validate_foundation.py
python tools/validate_m4.py
python -m pytest tests/monte_carlo/test_m32_seeded_mc_harness.py -q
python -m pytest -q
python examples/m32_seeded_mc_smoke.py
```

Results:

- foundation validator: PASS
- M4 validator: PASS
- targeted M32 pytest: PASS
- standard pytest: PASS
- real-data smoke example: PASS

Standard pytest is scoped by `pyproject.toml` to M32 tests for this delta. Legacy tests copied from the pre-GitHub local archive were not added to the commit because they require historical packages and examples that are not part of this M32 delta.

Smoke output policy:

- metadata only;
- no probability value;
- no percentage;
- no rational probability display;
- no optimizer or advice framing.
