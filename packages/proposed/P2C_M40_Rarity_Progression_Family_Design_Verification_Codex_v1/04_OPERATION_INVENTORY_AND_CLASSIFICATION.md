# Operation inventory and classification

All rows remain non-executable by this package. Proposed classifications describe a possible later M40-A gate only.

| Operation id | Input -> output | Add count | MML | Current runtime status | Future M40-A mapping |
|---|---|---:|---:|---|---|
| `transmutation` | normal -> magic | 1 | none | `data_reference_candidate` | shared rarity-transition add |
| `greater_transmutation` | normal -> magic | 1 | 44 | `data_reference_candidate` | same plan + MML |
| `perfect_transmutation` | normal -> magic | 1 | 70 | `data_reference_candidate` | same plan + MML |
| `augmentation` | magic -> magic | 1 | none | `data_reference_candidate` | shared in-place add |
| `greater_augmentation` | magic -> magic | 1 | 44 | `data_reference_candidate` | same plan + MML |
| `perfect_augmentation` | magic -> magic | 1 | 70 | `data_reference_candidate` | same plan + MML |
| `regal` | magic -> rare | 1 | none | `data_reference_candidate` | shared rarity-transition add |
| `greater_regal` | magic -> rare | 1 | 35 | `data_reference_candidate` | same plan + MML |
| `perfect_regal` | magic -> rare | 1 | 50 | `data_reference_candidate` | same plan + MML |
| `exalted` | rare -> rare | 1 | none | `admission_candidate` | direct accepted ordinary-add wrapper |

## Current repo-state observations

- `active_in_current_simulation` is false for the Transmutation, Augmentation, and Regal rows and true for `exalted`; none of those facts grants runtime permission.
- Runtime permission must continue to come only from `runtime_admission_status` and the accepted resolver registry.
- `config/project_scope.yaml` currently treats Transmutation, Augmentation, and Regal groups as reference-only and excludes a normal/magic starting route. A future implementation gate must update those declarations deliberately and test them; this design does not change them.
- `handler_declarations` currently lacks Transmutation, Augmentation, and Regal handlers. A future implementation should register a shared family handler/compiler, not three copied mechanics implementations.

## Classification conclusion

The rows are data-backed admission candidates for one later gate. They are not accepted executable runtime until implementation, Claude audit, and ChatGPT/User acceptance are complete.
