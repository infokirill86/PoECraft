# Runtime Invariants Report

Every simulated transition checks:

- operation id is exactly `ordinary_add`;
- mode id remains unchanged;
- fractured suffix remains present and unchanged;
- fractured installed modifier remains a suffix;
- prefix capacity is not exceeded;
- suffix capacity is not exceeded;
- total affix capacity is not exceeded;
- installed family duplicates are rejected;
- installed group intersections are rejected;
- unknown installed modifier ids are rejected.

Invariant violations raise `M32InvariantViolation` and are defects, not discarded samples.

Evidence:

- `test_runtime_invariants_fail_on_fractured_change`
- `test_runtime_invariants_fail_on_unsupported_operation`
- `test_runtime_invariants_fail_on_capacity_family_and_group`
