# P2C M39-A MML Filter Interface Result — Codex v1

Package type: `IMPLEMENTATION_RESULT / PROPOSED_FOR_CLAUDE_AUDIT`

This package implements the M39-A authorization:

> fail-closed MML filter interface in the M38-A resolver only.

It does not admit Greater/Perfect runtime. It does not enable Greater/Perfect Exalted or Chaos. It does not close MML, SOURCE/PROVENANCE, or PD-013.

## Main result

The resolver now supports an explicit `mml` request field only for the accepted `ordinary_add` engine primitive. The resolver compiles that into `OrdinaryAddOperation(mml=...)` and records it in `ResolvedOperationFilters`.

All catalog operations with MML remain fail-closed in M39-A. Greater/Perfect rows remain not admitted because their `runtime_admission_status` is not `accepted_executable_runtime`.

## Files changed

- `src/p2c_engine/operations/resolver.py`
- `src/p2c_engine/operations/__init__.py`
- `tests/monte_carlo/test_m38a_operation_resolver.py`
- `CURRENT_STATUS.md`
- `ledger/ACCEPTED_ARTIFACTS.md`
- `ledger/DECISIONS.md`
- `work/active/ACTIVE_TASK.md`
- `SHA256SUMS.txt`

