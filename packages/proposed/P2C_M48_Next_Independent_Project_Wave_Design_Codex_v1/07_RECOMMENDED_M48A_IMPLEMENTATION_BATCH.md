# Recommended Broad M48-A Implementation Batch

M48-A should be one implementation/audit batch, not multiple micro-gates, because all components share one evaluator contract.

## Include

1. **Accepted success classifier**
   - interpret the existing `success_criteria.yaml` for canonical quarterstaff states;
   - return only `TOP`, `ACCEPTABLE`, or `NOT_SUCCESS`;
   - fail closed on invalid/unsupported criteria shapes;
   - add known-answer and property tests.

2. **Finite route-DAG schema and validator**
   - operation, predicate-branch, and terminal nodes only;
   - unique IDs, complete references/cases, acyclic graph, reachability, and path-depth ceilings;
   - no arbitrary code/expressions.

3. **Exact evaluator**
   - reuse M43-A resolver/executor registry;
   - branch-state correctness, rational mass conservation, canonical terminal aggregation, and honest ceilings.

4. **Seeded MC and replay**
   - same operations and predicate results as exact execution;
   - deterministic traces and divergence diagnostics.

5. **Parity and negative controls**
   - one-node route equals direct operation;
   - linear DAG equals M43-A fixed sequence;
   - mixed branch fixtures prove actual-state routing;
   - unknown/unadmitted operation, modifier, predicate, cycle, missing edge, ceiling overflow, and attempted planner fields hard-fail.

6. **Internal-only reporting**
   - no public numeric probability output;
   - no advice/ranking/EV/cost fields.

## Suggested implementation name

`M48-A Bounded Caller-Authored Branching Sequence Runtime`

This package does not authorize M48-A. Claude audits the design first; ChatGPT/User decides the later implementation gate.
