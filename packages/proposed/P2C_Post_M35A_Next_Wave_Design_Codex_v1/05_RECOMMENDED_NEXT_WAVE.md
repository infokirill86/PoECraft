# Recommended Next Wave

## Recommendation

Authorize design-only:

```text
M36 Heterogeneous Accepted-Operation Chain Design
```

## Scope

M36 should design how to validate short chains over only:

- accepted `ordinary_add`;
- accepted base `annulment`.

Allowed sequence shapes for design:

- fixed length 2;
- optionally fixed length 3 if design remains simple;
- explicit operation list, not a route planner;
- branch-specific state after every step;
- pool rebuild for each operation from the branch-specific state;
- exact/oracle path products where tractable;
- seeded MC comparison where exact oracle exists or can be bounded.

## Why this is the widest safe batch

It is wide enough to move P2C from isolated operation runtime toward actual crafting simulation.

It is safe because:

- it uses only accepted operations;
- it is design-only;
- it does not change source truth;
- it does not release numeric outputs;
- it can be tested later with deterministic fixtures;
- it can fail closed on unaccepted operations.

## Suggested later implementation floor

If M36 design passes audit and ChatGPT/User authorization, a later implementation floor could be:

```text
M36-A Mixed Accepted-Operation Chain Runtime
```

M36-A should still be narrow:

- fixed short chain;
- accepted operations only;
- no planner;
- no optimizer;
- no user advice.

