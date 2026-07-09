# Resolver Design Contract

## Purpose

The M38 resolver converts a user/action request into an executable operation plan when and only when all required runtime permissions and modifier layers are admitted.

```text
base currency + variant + active modifiers + item state -> resolved operation plan
```

The resolver is not the executor. It must not implement probability, sampling, or state mutation directly. It selects and parameterizes already accepted runtime primitives.

## Inputs

Proposed input shape:

```yaml
currency_id: chaos
variant_id: base | greater | perfect
active_modifier_ids:
  - whittling
  - sinistral_erasure
item_state_ref: current item state
mode:
  exact | monte_carlo | validation
```

The concrete runtime object can differ later, but it must preserve these concepts.

## Output

Proposed resolved plan shape:

```yaml
operation_group: chaos
base_operation_id: chaos
runtime_operation_id: chaos
primitive_sequence:
  - remove
  - add
filters:
  removal:
    exclude_fractured: true
    side_filter: null
    desecrated_only: false
    selection_policy: uniform_installed_instance
  add:
    pool_kind: ordinary_weighted
    side_filter: null
    mml_threshold: null
atomicity: no_partial_remove_only
runtime_permission: accepted_executable_runtime
source_labels:
  - PROJECT-MODEL ONLY
  - NOT SERVER-TRUTH
```

## Resolution phases

1. Parse request.
2. Resolve catalog row from `data/operations.yaml`.
3. Check runtime permission:
   - accepted engine primitive, or
   - `runtime_admission_status: accepted_executable_runtime`.
4. Resolve variant:
   - base;
   - Greater/Perfect only if separately admitted;
   - otherwise fail closed.
5. Resolve active modifiers:
   - each active modifier must be known in `data/omens.yaml` or later modifier registry;
   - each modifier must apply to the target operation group;
   - each modifier layer must be admitted for runtime;
   - incompatible modifier dimensions fail closed.
6. Compile filters into a resolved operation plan.
7. Validate plan invariants before execution.
8. Hand plan to an accepted executor.

## Fail-closed rules

The resolver must fail closed when:

- operation row is missing;
- operation row is not runtime-admitted and is not an accepted engine primitive;
- request tries to use `active_in_current_simulation` as runtime permission;
- variant exists in data but is not admitted;
- modifier exists in data but is not admitted;
- modifier applies to the wrong operation group;
- two modifiers set conflicting values in the same effect dimension;
- modifier combination semantics are not defined;
- item state violates preconditions;
- resolved plan would require an unaccepted primitive;
- resolved plan would change source/provenance, MML, or PD-013 status;
- resolved plan would produce public numeric output without a release gate.

## Compatibility model

M38 should use explicit effect dimensions rather than hardcoded names:

| Effect dimension | Examples | Combination rule |
|---|---|---|
| add count | Omen of Greater Exaltation | mutually exclusive with other add-count overrides unless explicitly approved |
| add side filter | Sinistral/Dextral Exaltation | mutually exclusive prefix vs suffix |
| removal side filter | Sinistral/Dextral Annulment or Erasure | mutually exclusive prefix vs suffix |
| removal subset filter | Omen of Light / desecrated-only | may combine only if resulting intersection is explicitly supported |
| removal selection policy | Whittling / lowest modifier-level | mutually exclusive with base uniform selection; replaces selection policy only when admitted |
| add MML filter | Greater/Perfect currency variants | one threshold per operation; variants mutually exclusive |
| Lich/reveal constraint | Jawbone/Lich Omens | blocked until relevant operation path is admitted |

## Why this is not a generalized algebra

The resolver should remain a small compiler over admitted primitives. It should not create a universal crafting DSL, symbolic planner, or optimizer. The point is to avoid hardcoded special functions while still keeping every new runtime behavior separately gated.

