# Current Accepted Runtime and Taxonomy

## Accepted executable runtime today

| Runtime capability | Repo representation | Status | Notes |
|---|---|---:|---|
| `ordinary_add` | engine primitive outside `data/operations.yaml` | accepted executable primitive | Adds one legal ordinary modifier from the accepted weighted pool. |
| base Annulment | `operation_id: annulment` | `accepted_executable_runtime` | Removes one eligible non-fractured installed modifier instance uniformly. |
| base Chaos-like remove_then_add | `operation_id: chaos` | `accepted_executable_runtime` | Removes one eligible non-fractured instance uniformly, rebuilds ordinary add pool, adds one legal modifier. |

## Catalog rows are not executable permission

`active_in_current_simulation` is catalog/scope readiness only. Runtime permission must come from:

- accepted engine primitive status, or
- `runtime_admission_status: accepted_executable_runtime` for operation rows.

The resolver must never infer runtime permission from `active_in_current_simulation`.

## Engine primitives

M38 should recognize these primitive concepts:

| Primitive | Current status | Purpose |
|---|---:|---|
| `add` | accepted as `ordinary_add` primitive | Build legal ordinary weighted pool and add selected mod. |
| `remove` | accepted through base Annulment runtime | Build eligible removal pool and remove selected non-fractured installed instance. |
| `remove_then_add` | accepted through base Chaos-like runtime | Remove on branch copy, rebuild add pool, add, commit atomically. |
| `pool_filter` / `mml_filter` | modeled/project-approved but not broadly executable as variant runtime | Restrict add pool by modifier level threshold semantics. |
| `removal_side_filter` | data/evidence modeled; runtime not admitted as Omen layer | Restrict removal pool to prefix/suffix. |
| `minimum_modifier_level_selection` | data/evidence modeled for Whittling; runtime not admitted | Select lowest modifier-level removable instance; tie policy remains project-model inference. |
| `desecrated_only_filter` | data/evidence modeled for Omen of Light; runtime not broadly admitted | Restrict removal to desecrated modifiers. |

Future primitives may be added only through separate admission gates.

## Base currency operation mapping

| Currency family | Primitive shape | Current admission |
|---|---|---:|
| Exalted-like | `add` | catalog/admission candidate only; accepted executable behavior exists as `ordinary_add` engine primitive, not as Exalted currency runtime. |
| Annulment-like | `remove` | base `annulment` accepted executable runtime. |
| Chaos-like | `remove_then_add` | base `chaos` accepted executable runtime. |
| Transmutation/Augmentation/Regal | add-like with rarity preconditions | data reference candidates only. |
| Essence/Jawbone/Reveal/Fracture/Desecrate | specialized candidates or blocked/disputed | not admitted as executable runtime. |

