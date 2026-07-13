# Final Implementation Contract

## Caller request

`BoundedBranchingRequest` contains:

- a caller-owned `route_id` and `start_node_id`;
- an explicit tuple of operation, predicate-branch, and terminal nodes;
- explicit node, edge, and root-to-leaf operation-step ceilings.

Pinned accepted maxima:

| Ceiling | Maximum |
|---|---:|
| Nodes | 64 |
| Edges | 128 |
| Operation nodes per root-to-leaf path | 8 |

The graph must be finite, fully referenced, acyclic, reachable from the start, and end at unambiguous caller-labeled terminal nodes. Cycles, missing targets, duplicate nodes/terminal labels, unreachable nodes, incomplete predicate cases, excessive depth, and ceilings above the accepted maxima fail closed with structured codes.

## Node behavior

- Operation node: invokes one `BoundedSequenceStep` through the accepted M43-A resolver/executor seam and declares separate transition/no-transition edges.
- Predicate node: invokes a named accepted state predicate and declares complete categorical cases.
- Terminal node: records the caller label and canonical terminal state; it executes no action.

Each operation resolves from the actual current branch `ItemState`. A post-mutation branch never reuses the root plan, legality, pool, or state digest.

## Exact evaluation

- Multiplication uses `Fraction` path mass only.
- Deterministic predicate edges do not split probability.
- Execution terminals aggregate by terminal node/label, canonical state identity, and final operation outcome.
- State-only projection is separate.
- Candidate/path/terminal overflow returns `ceiling_exceeded` with empty paths/terminals: no truncation, renormalization, or hidden MC fallback.
- Completed path and terminal mass must each equal exactly one.

## Seeded evaluation and replay

Seeded traversal reuses the same accepted step executor and one recording decision source. Trace events identify node, state digests, chosen edge, resolver/operation trace, predicate result, terminal label, no-transition reason, and decisions. Same route, state, seed, sample count, and run ID replay byte-equivalently at the result-object level.

## Explicit stop/failure behavior

- Operation no-transition follows the caller's `on_no_transition` edge and preserves prior committed state.
- Unsupported operations/predicates and malformed graphs raise structured admission errors.
- Exact overflow is a structured non-completed result.
- There is no implicit retry, route repair, or alternate action.
