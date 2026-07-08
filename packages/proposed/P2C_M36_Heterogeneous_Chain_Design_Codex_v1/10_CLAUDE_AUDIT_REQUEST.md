# Claude Audit Request

Please audit `P2C_M36_Heterogeneous_Chain_Design_Codex_v1`.

## Requested verdict

Return:

- `GO`
- `GO WITH CHANGES`
- `NO-GO`

Also state whether this package is a safe basis for later M36-A implementation authorization.

## Audit focus

Please verify:

1. M36 design is appropriately timed after accepted runtime-admission metadata floor.
2. The participant critique is sound and not executor-mode.
3. Scope is design-only.
4. Accepted operation set is limited to:
   - accepted `ordinary_add` engine primitive;
   - accepted base `annulment`.
5. No new operation is admitted.
6. Chain representation is fixed-sequence, not planner/optimizer.
7. Per-step branch expansion, state transition, and legality/pool rebuild are specified.
8. Exact/oracle plan uses exact rational path mass multiplication and terminal aggregation.
9. MC/replay/diagnostics plan is sufficient for later implementation.
10. Fail-closed rules correctly use `runtime_admission_status` and do not rely on `active_in_current_simulation`.
11. M36-A implementation proposal is bounded enough.
12. Public numeric release, optimizer/economics/advice, source/server-truth claims, SOURCE/PROVENANCE/MML/PD-013 closure, and automation remain closed.

## Specific audit questions

1. Should M36-A be limited to exactly two steps, or is a bounded N-step design safe at first implementation?
2. Is the proposed no-transition chain policy correct for first implementation, or should it be revised before M36-A?
3. Is an accepted engine primitive registry required before implementation, or can M36-A hard-code `ordinary_add` as the only primitive for the first floor?
