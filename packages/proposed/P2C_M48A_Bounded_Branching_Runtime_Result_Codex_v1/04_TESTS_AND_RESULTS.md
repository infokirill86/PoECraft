# Tests and Results

## Focused evidence

```text
python -m pytest tests/monte_carlo/test_m48a_bounded_branching_runtime.py -q
21 passed in 1.19s
```

Coverage includes finite-DAG validation, cycle/unreachable/ceiling rejection, deterministic success classification, actual branch-state routing, exact mass, terminal aggregation, no-transition state preservation, structured exact overflow, deterministic replay, unsupported operation/predicate failures, evaluator/optimizer firewall, and explicit 64/128/8 limits.

## M43-A parity

```text
python -m pytest tests/monte_carlo/test_m43a_bounded_sequence_runtime.py tests/monte_carlo/test_m48a_bounded_branching_runtime.py -q
49 passed in 34.66s
```

Evidence includes:

- one-step exact and seeded parity;
- linear route exact projection parity;
- seeded parity across ordinary add, Annulment, Chaos, catalog single-add, Greater Essence, Perfect Essence, Alchemy, Fracture, Jawbone, and atomic Greater Exaltation executor paths;
- shared decision records for equal one-step/linear inputs.

## Full regression

```text
python -m pytest -q
350 passed in 161.15s
```

## Foundation

```text
python tools/validate_foundation.py
P2C_FOUNDATION_VALIDATION: PASS
SEMANTIC_FINGERPRINT: 6e7bc414416189d3d02941b63945457f4a35afafc475bc8bde54d0ddc1659a05

python tools/validate_m4.py
P2C_M4_VALIDATION: PASS
```

The semantic fingerprint is unchanged because M48-A changes no mechanics/data/config/admission truth.

Final ACTIVE_TASK/checksum/pre-push results are mechanically verified immediately before publication and recorded in the published Git state.
