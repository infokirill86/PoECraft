# Shared Primitive and Resolver Architecture

## Lean operation plan

M41-A should extend the accepted single-operation resolver with one Essence-specific plan shape, not a universal operation algebra:

```text
GreaterEssencePlan
  operation_id
  input_rarity = magic
  target_rarity = rare
  guaranteed_mod_id
  guaranteed_family_id
  guaranteed_side
  crafted = true
  retain_existing_modifiers = true
```

## Compilation

1. Load the operation row and matching output row.
2. Require the operation id to be in the explicitly authorized eight-row set.
3. Require the operation group to be `greater_essence`.
4. Require operation/output ids, family, side, and crafted flag to agree across files.
5. Require `runtime_admission_status` appropriate to the current gate.
6. Reject variants, Omens, side overrides, Perfect Essence, and unknown fields fail-closed.

## Execution

1. Validate Magic input and static output applicability.
2. Prevalidate family/group absence and crafted capacity.
3. Create an isolated Rare working copy.
4. Install the exact guaranteed modifier instance on its declared side.
5. Run accepted state/capacity validation on the complete working state.
6. Commit the working state and consume the Essence only if every check passes.

No ordinary weighted draw occurs. The modifier is guaranteed by the selected Essence row.

## Reuse

- M40-A atomic target-rarity working-copy pattern;
- existing normalized static modifier index;
- existing family/group conflict rules;
- existing crafted-capacity and side-capacity validation;
- M38 resolver admission checks;
- existing canonical terminal-state identity and diagnostics conventions.
