# Full Operation Inventory Table

Source: `data/operations.yaml`

Inventory facts:

- `operations.yaml` row count: 37.
- Rows with `active_in_current_simulation: true`: 18.
- Rows with `active_in_current_simulation: false`: 19.
- Accepted executable runtime today: accepted `ordinary_add` engine primitive plus accepted base `annulment`.

Classification vocabulary used here:

- `accepted_executable_runtime`: accepted runtime may execute this operation in the accepted scope.
- `engine_primitive`: runtime primitive rather than a game-facing currency/catalog row.
- `data_reference_candidate`: structured catalog/reference row, not executable-admitted.
- `admission_candidate`: plausible future admission candidate, but not executable-accepted.
- `blocked_or_out_of_scope`: known boundary/dependency prevents admission now.
- `disputed_or_requires_user_resolution`: source or policy conflict requires explicit user-approved resolution.

Important: `ordinary_add` is an accepted executable engine primitive, but it is not a direct row in `data/operations.yaml`.

| # | operation_id | group | active_in_current_simulation | transition shape | classification | runtime interpretation / note |
|---:|---|---|---:|---|---|---|
| 1 | `transmutation` | `transmutation` | false | ordinary weighted add, count 1, normal to magic | `data_reference_candidate` | Reference/catalog row. Uses add primitive shape, but not in accepted runtime scope. |
| 2 | `greater_transmutation` | `transmutation` | false | ordinary weighted add, count 1, MML 44 | `data_reference_candidate` | Reference/catalog row. MML remains project-model assumption. |
| 3 | `perfect_transmutation` | `transmutation` | false | ordinary weighted add, count 1, MML 70 | `data_reference_candidate` | Reference/catalog row. MML remains project-model assumption. |
| 4 | `augmentation` | `augmentation` | false | ordinary weighted add, count 1, magic slot rule | `data_reference_candidate` | Reference/catalog row. Not accepted executable runtime. |
| 5 | `greater_augmentation` | `augmentation` | false | ordinary weighted add, count 1, MML 44 | `data_reference_candidate` | Reference/catalog row. Not accepted executable runtime. |
| 6 | `perfect_augmentation` | `augmentation` | false | ordinary weighted add, count 1, MML 70 | `data_reference_candidate` | Reference/catalog row. Not accepted executable runtime. |
| 7 | `regal` | `regal` | false | ordinary weighted add, count 1, magic to rare | `data_reference_candidate` | Reference/catalog row. Not accepted executable runtime. |
| 8 | `greater_regal` | `regal` | false | ordinary weighted add, count 1, MML 35 | `data_reference_candidate` | Reference/catalog row. Not accepted executable runtime. |
| 9 | `perfect_regal` | `regal` | false | ordinary weighted add, count 1, MML 50 | `data_reference_candidate` | Reference/catalog row. Not accepted executable runtime. |
| 10 | `exalted` | `exalted` | true | ordinary weighted add, count 1, rare | `admission_candidate` | Active project-scope catalog row. The underlying `ordinary_add` primitive is accepted, but the Exalted currency wrapper/omen variants are not separately accepted as executable runtime. |
| 11 | `greater_exalted` | `exalted` | true | ordinary weighted add, count 1, MML 35 | `admission_candidate` | Same as `exalted`; MML remains project-model assumption. |
| 12 | `perfect_exalted` | `exalted` | true | ordinary weighted add, count 1, MML 50 | `admission_candidate` | Same as `exalted`; MML remains project-model assumption. |
| 13 | `annulment` | `annulment` | true | uniform installed-instance remove, excludes fractured | `accepted_executable_runtime` | Accepted as base Annulment runtime only. Annulment variants/omens remain closed unless separately gated. |
| 14 | `chaos` | `chaos` | true | remove then rebuild ordinary add pool then add | `admission_candidate` | Future remove_then_add candidate. Not accepted executable runtime. |
| 15 | `greater_chaos` | `chaos` | true | remove then add, MML 35 | `admission_candidate` | Future remove_then_add candidate. MML and Whittling interactions remain gated. |
| 16 | `perfect_chaos` | `chaos` | true | remove then add, MML 50 | `admission_candidate` | Future remove_then_add candidate. Not accepted executable runtime. |
| 17 | `alchemy` | `alchemy` | false | discard all explicit, sequential ordinary add x4 | `data_reference_candidate` | Reference/catalog row. Multi-add shell creation not accepted runtime. |
| 18 | `fracturing_orb` | `fracture` | false | target installed instance, set fractured flag | `disputed_or_requires_user_resolution` | Disabled and source-disputed for revealed Desecrated eligibility. Requires explicit user-approved resolution before admission. |
| 19 | `install_astrid` | `support_augment` | true | support augment state mutation | `admission_candidate` | Active project-scope catalog row. Not accepted executable runtime. |
| 20 | `greater_essence_abrasion` | `greater_essence` | false | guaranteed crafted flat physical, magic to rare | `data_reference_candidate` | Reference/catalog row. Essence runtime not accepted. |
| 21 | `greater_essence_flames` | `greater_essence` | false | guaranteed crafted flat fire, magic to rare | `data_reference_candidate` | Reference/catalog row. Essence runtime not accepted. |
| 22 | `greater_essence_ice` | `greater_essence` | false | guaranteed crafted flat cold, magic to rare | `data_reference_candidate` | Reference/catalog row. Essence runtime not accepted. |
| 23 | `greater_essence_electricity` | `greater_essence` | false | guaranteed crafted flat lightning, magic to rare | `data_reference_candidate` | Reference/catalog row. Essence runtime not accepted. |
| 24 | `greater_essence_battle` | `greater_essence` | false | guaranteed crafted accuracy, magic to rare | `data_reference_candidate` | Reference/catalog row. Essence runtime not accepted. |
| 25 | `greater_essence_haste` | `greater_essence` | false | guaranteed crafted attack speed, magic to rare | `data_reference_candidate` | Reference/catalog row. Essence runtime not accepted. |
| 26 | `greater_essence_seeking` | `greater_essence` | false | guaranteed crafted critical chance, magic to rare | `data_reference_candidate` | Reference/catalog row. Essence runtime not accepted. |
| 27 | `greater_essence_infinite` | `greater_essence` | false | guaranteed crafted attribute, magic to rare | `data_reference_candidate` | Reference/catalog row. Essence runtime not accepted. |
| 28 | `perfect_essence_abrasion` | `perfect_essence` | true | remove one non-fractured, install guaranteed crafted mod | `admission_candidate` | Active project-scope catalog row. Essence remove-plus-guaranteed-install runtime not accepted. |
| 29 | `perfect_essence_flames` | `perfect_essence` | true | remove one non-fractured, install guaranteed crafted mod | `admission_candidate` | Active project-scope catalog row. Not accepted executable runtime. |
| 30 | `perfect_essence_ice` | `perfect_essence` | true | remove one non-fractured, install guaranteed crafted mod | `admission_candidate` | Active project-scope catalog row. Not accepted executable runtime. |
| 31 | `perfect_essence_electricity` | `perfect_essence` | true | remove one non-fractured, install guaranteed crafted mod | `admission_candidate` | Active project-scope catalog row. Not accepted executable runtime. |
| 32 | `perfect_essence_battle` | `perfect_essence` | true | remove one non-fractured, install guaranteed crafted mod | `admission_candidate` | Active project-scope catalog row. Not accepted executable runtime. |
| 33 | `perfect_essence_haste` | `perfect_essence` | true | remove one non-fractured, install guaranteed crafted mod | `admission_candidate` | Active project-scope catalog row. Not accepted executable runtime. |
| 34 | `gnawed_jawbone` | `jawbone` | true | create unrevealed Desecrated placeholder | `blocked_or_out_of_scope` | Active project-scope catalog row, but Jawbone placeholder mechanics remain closed for runtime admission in this wave. |
| 35 | `preserved_jawbone` | `jawbone` | true | create unrevealed Desecrated placeholder | `blocked_or_out_of_scope` | Same as `gnawed_jawbone`. |
| 36 | `ancient_jawbone` | `jawbone` | true | create unrevealed Desecrated placeholder, reveal MML 40 | `blocked_or_out_of_scope` | Same as Jawbone plus MML dependency. Not accepted executable runtime. |
| 37 | `reveal_desecrated` | `reveal` | true | generate offer set and replace placeholder | `blocked_or_out_of_scope` | Reveal/Lich/Abyssal/PD-013-related mechanics remain separately gated. Not accepted executable runtime. |

## Current classification counts

| Classification | Count | Members |
|---|---:|---|
| `accepted_executable_runtime` | 1 | `annulment` |
| `engine_primitive` | 0 rows | `ordinary_add` exists outside `operations.yaml` as accepted runtime primitive |
| `data_reference_candidate` | 18 | transmutation/augmentation/regal variants, `alchemy`, greater essences |
| `admission_candidate` | 13 | Exalted variants, Chaos variants, `install_astrid`, Perfect Essences |
| `blocked_or_out_of_scope` | 4 | Jawbones, `reveal_desecrated` |
| `disputed_or_requires_user_resolution` | 1 | `fracturing_orb` |
