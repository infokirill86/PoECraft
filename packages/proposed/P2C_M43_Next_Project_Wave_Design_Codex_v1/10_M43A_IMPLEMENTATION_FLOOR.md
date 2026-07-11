# Proposed M43-A Implementation Floor

## Floor name

`M43-A Bounded Accepted-Operation Sequence Runtime`

## Proposed batch

Implement in one coherent wave:

1. A fixed sequence request schema with one-to-eight steps.
2. Per-branch, per-step compilation through the accepted `OperationResolver`.
3. Explicit executor registry covering all currently accepted operation families and `ordinary_add`.
4. Exact rational enumeration under pinned ceilings.
5. Seeded MC execution using the same step executors.
6. Execution-terminal aggregation and optional state-only projection.
7. Early no-transition termination with prior-step state preservation.
8. Deterministic sequence replay and hard-fail diagnostics.
9. One-step parity tests, mixed multi-step fixtures, negative controls, full regression, and leak scan.

## Why this batch is safe to keep together

All parts are reconstruction and validation of composition. They do not modify operation semantics or admit a new mechanic. Splitting schema, exact, MC, replay, and diagnostics into separate micro-gates would create partially usable sequence infrastructure and weaken cross-engine parity.

## Acceptance criteria

- all accepted operation families pass one-step parity;
- mixed fixed sequences execute only admitted operations;
- branch state is load-bearing for every later resolver/pool call;
- exact mass sums exactly to one within ceilings;
- MC deterministically replays and satisfies the pinned comparison policy where exact is tractable;
- early no-transition behavior is explicit and tested;
- ceilings fail closed;
- no current operation regression;
- no new operation/modifier admission;
- no public probability values;
- Claude audit followed by ChatGPT/User acceptance.

This design does not authorize M43-A implementation.
