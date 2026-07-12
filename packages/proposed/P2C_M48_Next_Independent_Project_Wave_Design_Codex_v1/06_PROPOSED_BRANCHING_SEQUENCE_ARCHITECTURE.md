# Proposed Branching-Sequence Architecture

## Request model

```yaml
policy_id: caller_supplied_id
start_node_id: step_1
max_operation_steps_per_path: 8
nodes:
  - node_id: step_1
    kind: operation
    operation_request: accepted_resolver_request
    on_transition: classify_1
    on_no_transition: stopped_no_transition
  - node_id: classify_1
    kind: predicate_branch
    predicate_id: accepted_success_class
    cases:
      TOP: accepted_terminal
      ACCEPTABLE: accepted_terminal
      NOT_SUCCESS: recovery_step
  - node_id: accepted_terminal
    kind: terminal
    terminal_label: caller_label_only
```

Names are illustrative; the later M48-A gate must pin the exact schema before implementation.

## Required contracts

### Finite graph

- DAG only; cycles fail validation.
- Every referenced node exists; unreachable nodes and duplicate IDs fail closed.
- Every root-to-leaf path contains at most eight operation nodes for parity with M43-A.
- A retry must be explicitly unrolled as distinct nodes; no `repeat`, `until`, or back-edge.

### Predicates

- Only a registry of named, versioned, data-backed predicates.
- M48-A floor: transition/no-transition plus classification against accepted `config/success_criteria.yaml`.
- No arbitrary expression language, Python callback, dynamic plugin, cost predicate, or probability predicate.
- Unknown predicate IDs or incomplete case coverage fail closed.

### Operation execution

- Every operation compiles through accepted `OperationResolver` against the current branch `ItemState`.
- Every executor comes from the accepted fail-closed registry.
- No root-state plan/pool reuse after mutation.
- No new operation/modifier admission through policy syntax.

### Exact evaluation

- Multiply exact rational path masses through operation and branch edges.
- Deterministic predicates split by state, not probability.
- Aggregate execution terminals by path terminal label plus canonical terminal state; expose state-only projection separately.
- Enforce explicit path/terminal ceilings with structured stop; no truncation, renormalization, or hidden MC substitution.

### MC/replay

- Use the same accepted executors and predicate registry.
- Fixed seed/run ID replays exactly.
- Trace node ID, operation plan, decision records, state digest, predicate result, chosen edge, terminal label, and stop reason.

### No-transition

No-transition follows the caller-declared `on_no_transition` edge while preserving all state produced by earlier successful nodes. It is not silently reinterpreted as retry or success.
