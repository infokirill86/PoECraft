# Validator / Fail-Closed Requirements

## Runtime admission gate

Before any chain executes, every step must pass an admission check.

Allowed:

- accepted engine primitive: `ordinary_add`;
- accepted operation row: `annulment` with `runtime_admission_status: accepted_executable_runtime`.

Forbidden:

- any operation row with `admission_candidate`;
- any operation row with `data_reference_candidate`;
- any operation row with `blocked_or_out_of_scope`;
- any operation row with `disputed_or_requires_user_resolution`;
- any active catalog row admitted only because `active_in_current_simulation: true`;
- any missing or unknown operation id.

## Proposed chain validation steps

1. Parse chain spec.
2. Require fixed ordered sequence.
3. Reject empty sequence.
4. Reject sequence length above the current floor ceiling.
5. Resolve every operation ref.
6. Check runtime admission status or accepted primitive registry.
7. Check operation-specific mode/scope.
8. Reject variants/omens unless explicitly accepted in a later gate.
9. Pin exact/MC execution contract before running.

## Boundary checks

The chain layer must fail closed if:

- `data/operations.yaml` marks a row active but not runtime-admitted;
- an operation id exists in catalog but is not accepted executable runtime;
- a primitive id exists in code but is not in the accepted primitive registry;
- operation mode requests unsupported variant behavior;
- a chain spec implies route choice or planner behavior;
- a chain step requires source/provenance, MML, or PD-013 closure.

## Validator test proposal

M36-A should include tests for:

- accepted `ordinary_add -> annulment`;
- accepted `annulment -> ordinary_add`;
- rejected `ordinary_add -> chaos`;
- rejected Exalted catalog row as a direct executable step;
- rejected Annulment omen/variant;
- rejected unknown operation;
- rejected chain length above M36-A ceiling.
