# Risks and Stop Triggers

## Risks

- Confusing the `remove_then_add` engine primitive with accepted Chaos Orb runtime.
- Treating `active_in_current_simulation` as runtime permission.
- Accidentally including Greater/Perfect MML modes in the first base implementation.
- Letting Whittling or Omen rules enter scope through `operations.yaml` fields.
- Committing a remove-only partial result when the post-removal add pool is empty.
- Failing to aggregate original-state terminals when remove-then-add recreates the original item state.

## Stop triggers

Stop if:

- source/data status becomes ambiguous;
- design requires a server-truth claim;
- runtime implementation would begin;
- any Chaos-like row would be marked accepted executable runtime;
- Whittling, Omen, Greater/Perfect MML, or variants enter M37-A without a new gate;
- public numeric output, optimizer/economics/advice, automation, SOURCE/PROVENANCE closure, MML closure, or PD-013 closure enters scope.

