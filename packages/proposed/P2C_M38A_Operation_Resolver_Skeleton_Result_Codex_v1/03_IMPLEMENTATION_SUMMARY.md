# Implementation summary

Files added:

- `src/p2c_engine/operations/__init__.py`
- `src/p2c_engine/operations/resolver.py`
- `tests/monte_carlo/test_m38a_operation_resolver.py`

Core objects:

- `OperationResolverRequest`
- `ResolvedOperationFilters`
- `ResolvedOperationPlan`
- `OperationResolver`
- `M38AResolverAdmissionError`

Resolver behavior:

1. Reject non-base variants.
2. Reject active modifier layers.
3. Resolve `ordinary_add` as an accepted engine primitive outside `data/operations.yaml`.
4. For catalog operations, require `runtime_admission_status: accepted_executable_runtime`.
5. Dispatch only:
   - `annulment` -> `AnnulmentOperation`;
   - `chaos` -> `ChaosLikeOperation`.
6. Reject active catalog rows such as `exalted`, `greater_chaos`, and `perfect_chaos`.

Important non-change:

- No existing operation semantics were changed.
- The resolver does not execute operations.
- The resolver is not a chain planner.

