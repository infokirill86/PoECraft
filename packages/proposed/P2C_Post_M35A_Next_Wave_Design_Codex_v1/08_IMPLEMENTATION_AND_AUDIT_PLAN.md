# Proposed Implementation and Audit Plan

## If this proposal is accepted

Next task:

```text
M36 Heterogeneous Accepted-Operation Chain Design
```

Still design-only.

## M36 design deliverables

M36 should define:

- accepted operation registry for chain design;
- fixed-chain input schema;
- exact/oracle path enumeration model;
- MC replay/validation model;
- no-transition propagation rule;
- terminal aggregation rule;
- diagnostics contract;
- negative controls;
- explicit non-goals.

## Later M36-A implementation evidence

If later authorized, M36-A should provide:

- exact/oracle fixtures for `ordinary_add -> annulment`;
- exact/oracle fixtures for `annulment -> ordinary_add`;
- no-transition-in-chain fixtures;
- branch-specific pool rebuild proof;
- deterministic replay proof;
- negative-control proof for unaccepted operation ids;
- regression proof that single-operation behavior remains unchanged.

## Claude audit request for this package

Claude should audit:

- whether M36 is the right strategic next wave;
- whether the proposal stays design-only;
- whether accepted-operation-only scope is clear;
- whether batching is safe;
- whether additional mechanics are correctly gated;
- whether the proposal avoids planner/optimizer drift.

