# Operation Classification Table

Source: `data/operations.yaml`

This table applies the accepted reconciliation classification to all existing operation rows.

| operation_id | active_in_current_simulation | runtime_admission_status |
|---|---:|---|
| `transmutation` | false | `data_reference_candidate` |
| `greater_transmutation` | false | `data_reference_candidate` |
| `perfect_transmutation` | false | `data_reference_candidate` |
| `augmentation` | false | `data_reference_candidate` |
| `greater_augmentation` | false | `data_reference_candidate` |
| `perfect_augmentation` | false | `data_reference_candidate` |
| `regal` | false | `data_reference_candidate` |
| `greater_regal` | false | `data_reference_candidate` |
| `perfect_regal` | false | `data_reference_candidate` |
| `exalted` | true | `admission_candidate` |
| `greater_exalted` | true | `admission_candidate` |
| `perfect_exalted` | true | `admission_candidate` |
| `annulment` | true | `accepted_executable_runtime` |
| `chaos` | true | `admission_candidate` |
| `greater_chaos` | true | `admission_candidate` |
| `perfect_chaos` | true | `admission_candidate` |
| `alchemy` | false | `data_reference_candidate` |
| `fracturing_orb` | false | `disputed_or_requires_user_resolution` |
| `install_astrid` | true | `admission_candidate` |
| `greater_essence_abrasion` | false | `data_reference_candidate` |
| `greater_essence_flames` | false | `data_reference_candidate` |
| `greater_essence_ice` | false | `data_reference_candidate` |
| `greater_essence_electricity` | false | `data_reference_candidate` |
| `greater_essence_battle` | false | `data_reference_candidate` |
| `greater_essence_haste` | false | `data_reference_candidate` |
| `greater_essence_seeking` | false | `data_reference_candidate` |
| `greater_essence_infinite` | false | `data_reference_candidate` |
| `perfect_essence_abrasion` | true | `admission_candidate` |
| `perfect_essence_flames` | true | `admission_candidate` |
| `perfect_essence_ice` | true | `admission_candidate` |
| `perfect_essence_electricity` | true | `admission_candidate` |
| `perfect_essence_battle` | true | `admission_candidate` |
| `perfect_essence_haste` | true | `admission_candidate` |
| `gnawed_jawbone` | true | `blocked_or_out_of_scope` |
| `preserved_jawbone` | true | `blocked_or_out_of_scope` |
| `ancient_jawbone` | true | `blocked_or_out_of_scope` |
| `reveal_desecrated` | true | `blocked_or_out_of_scope` |

## Runtime admission interpretation

- `annulment` is admitted executable runtime, base-only, project-model semantics.
- `ordinary_add` is accepted runtime as an engine primitive, not an `operations.yaml` row.
- Exalted-like rows are not executable merely because they map conceptually to add behavior.
- Chaos-like rows are candidates only.
- Perfect Essences are candidates only.
- Jawbone/Reveal remain blocked/out of scope.
- Fracturing remains disputed/requires user resolution.
