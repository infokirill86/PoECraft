# Sequence Model Definition

## Sequence object

An M34-B1 sequence is an ordered list of two accepted ordinary-add invocations:

```text
S0 --ordinary_add(step_0)--> S1 --ordinary_add(step_1)--> S2
```

Where:

- `S0` is the initial item state;
- `S1` is the branch state after step 0;
- `S2` is the terminal state after step 1;
- each step uses accepted `ordinary_add` semantics only.

## Step identity

Each step must have stable identifiers:

- `sequence_id`;
- `step_index`;
- `operation_id`;
- `mode_id`;
- `pre_state_hash`;
- `pool_digest`;
- `selected_mod_id` when a transition occurs;
- `post_state_hash`;
- `decision_id`.

## Pool rebuild rule

The pool for each step must be built from that step's actual pre-state.

The step 1 pool must not be reused from step 0 and must not be built from `S0`.

## Terminal identity

Terminal identity should be the canonical final item state after the full sequence, including stable item fields and installed modifier identity.

Ordering belongs to the trace. Terminal comparison should use canonical state identity, not path text.

## No-transition behavior

If a step has no legal candidates, the design must specify whether the sequence stops as a no-transition terminal or records a failed step. The recommended M34-B1 behavior is:

- record the no-transition step explicitly;
- keep the state unchanged for that step;
- do not silently fabricate a transition;
- include the stop reason in diagnostics.

## Public report boundary

Public M34-B1 reports may include counts, hashes, pass/fail status, seed ids, tier ids, and diagnostic categories.

They must not include public probability values, percentages, fractions, expected attempts, route advice, or ranking.
