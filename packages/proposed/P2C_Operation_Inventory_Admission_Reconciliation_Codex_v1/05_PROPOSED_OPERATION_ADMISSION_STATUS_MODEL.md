# Proposed Operation Admission Status Model

## Goal

Prevent `active_in_current_simulation` from being misread as executable runtime authorization.

## Proposed field

Add an explicit per-operation field:

```yaml
runtime_admission_status: accepted_executable_runtime | engine_primitive | data_reference_candidate | admission_candidate | blocked_or_out_of_scope | disputed_or_requires_user_resolution
```

For `operations.yaml` rows, the most common values will be:

- `accepted_executable_runtime`
- `data_reference_candidate`
- `admission_candidate`
- `blocked_or_out_of_scope`
- `disputed_or_requires_user_resolution`

`engine_primitive` should be used for primitive registry/docs, not necessarily for game-facing currency rows. For example, accepted `ordinary_add` is an engine primitive but not an `operations.yaml` row today.

## Optional supporting fields

These fields would reduce future ambiguity:

```yaml
runtime_admission_scope: base_only | variants_excluded | not_executable | proposed_only
runtime_admission_note: "Short human-readable scope note."
primitive_relationship:
  primary_primitive: ordinary_add | remove_one_non_fractured | remove_then_add | guaranteed_install | placeholder_create | reveal_offer_set | state_mutation | fracture_mutation
  relationship_status: accepted | candidate | blocked | disputed
source_policy_status: project_model | source_open | disputed | server_truth_forbidden
```

## Proposed initial status assignment

This is a proposal only. It is not applied to `data/operations.yaml` in this package.

| operation_id | proposed runtime_admission_status |
|---|---|
| `transmutation` | `data_reference_candidate` |
| `greater_transmutation` | `data_reference_candidate` |
| `perfect_transmutation` | `data_reference_candidate` |
| `augmentation` | `data_reference_candidate` |
| `greater_augmentation` | `data_reference_candidate` |
| `perfect_augmentation` | `data_reference_candidate` |
| `regal` | `data_reference_candidate` |
| `greater_regal` | `data_reference_candidate` |
| `perfect_regal` | `data_reference_candidate` |
| `exalted` | `admission_candidate` |
| `greater_exalted` | `admission_candidate` |
| `perfect_exalted` | `admission_candidate` |
| `annulment` | `accepted_executable_runtime` |
| `chaos` | `admission_candidate` |
| `greater_chaos` | `admission_candidate` |
| `perfect_chaos` | `admission_candidate` |
| `alchemy` | `data_reference_candidate` |
| `fracturing_orb` | `disputed_or_requires_user_resolution` |
| `install_astrid` | `admission_candidate` |
| `greater_essence_abrasion` | `data_reference_candidate` |
| `greater_essence_flames` | `data_reference_candidate` |
| `greater_essence_ice` | `data_reference_candidate` |
| `greater_essence_electricity` | `data_reference_candidate` |
| `greater_essence_battle` | `data_reference_candidate` |
| `greater_essence_haste` | `data_reference_candidate` |
| `greater_essence_seeking` | `data_reference_candidate` |
| `greater_essence_infinite` | `data_reference_candidate` |
| `perfect_essence_abrasion` | `admission_candidate` |
| `perfect_essence_flames` | `admission_candidate` |
| `perfect_essence_ice` | `admission_candidate` |
| `perfect_essence_electricity` | `admission_candidate` |
| `perfect_essence_battle` | `admission_candidate` |
| `perfect_essence_haste` | `admission_candidate` |
| `gnawed_jawbone` | `blocked_or_out_of_scope` |
| `preserved_jawbone` | `blocked_or_out_of_scope` |
| `ancient_jawbone` | `blocked_or_out_of_scope` |
| `reveal_desecrated` | `blocked_or_out_of_scope` |

## Validator proposal for later

A later audited metadata-correction floor should add a fail-closed check:

- runtime code may execute only operations with `runtime_admission_status: accepted_executable_runtime`, or internal primitives from an accepted primitive registry;
- `active_in_current_simulation: true` alone must never authorize runtime execution;
- variants/omens require their own explicit accepted scope even if their base operation is accepted.

This validator is not implemented in this package.
