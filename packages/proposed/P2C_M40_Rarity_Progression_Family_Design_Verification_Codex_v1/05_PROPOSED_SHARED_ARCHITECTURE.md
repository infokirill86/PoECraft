# Proposed shared architecture

## Design objective

Compile all ten rows into a lean one-add operation plan instead of creating one function per currency.

Suggested plan shape:

```text
CatalogSingleAddPlan
  operation_id
  required_input_rarity
  pool_build_rarity
  output_rarity
  add_count = 1
  mml = null | integer
  atomic = true
```

This is not a generalized operation algebra. It is a narrow compiler/executor seam for catalog operations whose only stochastic mechanic is one accepted ordinary weighted add.

## Compilation

1. Look up the currency row through the accepted operation registry.
2. Require `runtime_admission_status: accepted_executable_runtime` after a future admission gate.
3. Reject unsupported variants, Omens, side filters, and extra modifiers before execution.
4. Read input rarity, output rarity, pool-build rarity, add count, and MML from the row.
5. Validate that the row matches the admitted one-add schema; fail closed on drift.

## Execution order

1. Validate item invariants and input rarity without mutation.
2. Validate operation-specific capacity/preconditions.
3. Create an isolated working state using `pool_build_rarity`:
   - magic for Transmutation;
   - current magic for Augmentation;
   - rare for Regal;
   - current rare for Exalted.
4. Call the accepted ordinary-add pool builder with that working state and the row MML.
5. If no legal add exists, return explicit no-transition/no-consumption with the original state.
6. Exact/oracle path: use exact rational ordinary-add weights. MC path: use the accepted seeded weighted sampler.
7. Apply the selected modifier to the isolated target state.
8. Validate capacity, family/group exclusion, rarity, and canonical state.
9. Commit the target rarity and modifier together as one atomic transition.

## Shared components

- accepted M38-A resolver/admission seam;
- accepted ordinary-add legality and weight builder;
- accepted M39-A MML interface and current project fallback policy;
- existing item-state rarity and canonicalization;
- existing exact rational and seeded sampling kernels;
- existing no-transition normalization and diagnostic conventions.

## Capacity model

- normal: no explicit modifier capacity;
- magic Quarterstaff: one prefix and one suffix;
- rare Quarterstaff: three prefixes and three suffixes.

Augmentation requires no special “choose opposite side” randomizer. The ordinary combined legal pool plus magic side capacities naturally removes the occupied side. With zero installed modifiers, both sides remain eligible. With one prefix, only suffix candidates remain; with one suffix, only prefix candidates remain.

## Exalted wrapper

Base `exalted` should compile to the same plan with rare input/output, rare pool-build rarity, one add, and no MML. Existing Omen parameters in the catalog must remain unsupported and fail closed; admitting the base wrapper does not admit any Omen behavior.
