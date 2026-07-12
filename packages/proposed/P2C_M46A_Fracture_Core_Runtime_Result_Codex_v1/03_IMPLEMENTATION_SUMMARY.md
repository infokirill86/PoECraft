# Implementation Summary

## Runtime

- `src/p2c_engine/monte_carlo/fracture.py` implements pool construction, exact enumeration, seeded sampling, replay evidence, diagnostics, and invariants.
- `src/p2c_engine/operations/resolver.py` compiles only the admitted base `fracturing_orb` row and validates its pinned data contract.
- `src/p2c_engine/monte_carlo/bounded_sequence.py` adds the explicit accepted-executor registry entry and direct/exact/seeded dispatch.

## Data and scope

- `data/operations.yaml` admits only base `fracturing_orb` and pins combined-side unit-weight selection plus clean-core preconditions.
- `config/project_scope.yaml` activates only the Fracture clean-core group/mechanic.
- `data/mechanics_evidence.yaml` records M46-A as user-authorized proposed runtime pending audit, project-model/source-open.
- `data/sources.yaml` records the trusted references inherited from the accepted M46 mechanics verification.

## Acceptance boundary

The ledger records M46 design acceptance and M46-A authorization only. It does not record M46-A runtime as accepted.
