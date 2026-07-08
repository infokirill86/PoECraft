# Chain Model

## Chain representation

A chain is a fixed ordered list of accepted operation invocations.

Example design shape:

```yaml
chain_id: m36_two_step_add_then_annul
chain_scope_label: PROJECT-MODEL HARDENING FIXTURE
steps:
  - step_index: 0
    operation_ref:
      kind: engine_primitive
      id: ordinary_add
    mode_id: add_no_side_filter
  - step_index: 1
    operation_ref:
      kind: operation_row
      id: annulment
    mode_id: base_annulment
```

## Step execution model

For every branch state at step `i`:

1. Validate that the operation is accepted executable runtime.
2. Build the legal pool for that exact branch state.
3. Enumerate or sample a transition.
4. Apply the operation to produce state `S(i+1)`.
5. Preserve path identity.
6. Rebuild legality/pool from `S(i+1)` before the next step.

No step may use a pool built from the root state unless the branch state is still the root state.

## Branch identity vs terminal identity

Path identity includes:

- chain id;
- step index sequence;
- selected transition key at each step;
- no-transition markers;
- per-step operation id/mode id;
- branch-specific state hashes.

Terminal identity is canonical and unordered where appropriate:

- installed modifier identity/multiset;
- stable item fields;
- flags relevant to accepted runtime;
- no irrelevant path order.

Different paths may produce the same terminal state. Their exact masses must be aggregated.

## No-transition behavior

If a step has no legal transition:

- the step emits the accepted operation's explicit no-transition result;
- the chain continues or terminates according to a pinned chain policy;
- M36-A should start with "continue after no-transition" disabled unless explicitly justified.

Recommended M36-A policy:

- a no-transition at any step becomes a terminal chain failure/no-transition state for that chain path;
- no later step executes after that failure;
- mass remains conserved.

This policy must be audited before implementation.
