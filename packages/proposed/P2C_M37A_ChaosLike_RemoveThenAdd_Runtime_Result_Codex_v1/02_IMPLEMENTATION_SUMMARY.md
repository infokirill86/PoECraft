# Implementation Summary

## Runtime code

Added:

- `src/p2c_engine/monte_carlo/chaos_like.py`

Updated:

- `src/p2c_engine/monte_carlo/__init__.py`

The new `ChaosLikeMonteCarloHarness` implements exact/oracle and seeded MC execution for base Chaos-like `remove_then_add`.

## Data metadata

Updated:

- `data/operations.yaml`

Only base `chaos` was changed from `admission_candidate` to `accepted_executable_runtime` as part of the proposed M37-A implementation path.

Still not admitted:

- `greater_chaos`;
- `perfect_chaos`;
- Whittling;
- side Omens;
- any other operation.

## Test updates

Added:

- `tests/monte_carlo/test_m37a_chaoslike_remove_then_add_runtime.py`

Updated:

- `tests/static_data/test_foundation_revision_v8_2.py`
- `tests/static_data/test_m7h1_governance_fingerprint.py`

The semantic fingerprint changed because base `chaos` is now part of the proposed runtime-admitted operation surface.

## Shared-kernel discipline

The implementation reuses existing accepted builders/helpers:

- `build_removal_pool`;
- `build_ordinary_add_pool`;
- existing branch enumeration;
- existing seeded decision source;
- existing canonical state hashes.

It does not add a parallel removal-pool or ordinary-add-pool implementation.

