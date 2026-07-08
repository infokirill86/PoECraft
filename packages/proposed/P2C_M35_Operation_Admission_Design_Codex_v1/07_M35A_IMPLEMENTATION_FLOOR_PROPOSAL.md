# Later M35-A Implementation Floor Proposal

## Proposed name

`M35-A Annulment Runtime Admission`

## Status

Not authorized by this package.

## Suggested scope if later authorized

M35-A should implement the narrowest useful Annulment runtime:

- base Annulment only;
- one removal;
- uniform selection over removable installed non-fractured modifier instances;
- exact/oracle enumeration;
- seeded MC comparison if stochastic MC path is included;
- deterministic replay;
- negative controls;
- no public numeric release.

## Required implementation evidence

M35-A should produce:

- exact/oracle removal-pool behavior proof;
- fractured exclusion proof;
- empty-pool no-transition proof;
- duplicate-instance terminal aggregation proof;
- deterministic replay proof;
- MC convergence proof if MC is part of the floor;
- regression proof that accepted `ordinary_add` behavior remains unchanged;
- fail-closed proof for unsupported operation variants.

## Suggested tests

Design-level suggested test groups:

1. `annulment_exact_oracle_uniformity`
2. `annulment_fractured_never_removed`
3. `annulment_empty_pool_no_transition`
4. `annulment_duplicate_instance_aggregation`
5. `annulment_replay_trace_determinism`
6. `annulment_fail_closed_unsupported_variant`
7. `ordinary_add_regression_unchanged`

These are suggestions for a later authorized implementation. They are not implemented in M35 design.

