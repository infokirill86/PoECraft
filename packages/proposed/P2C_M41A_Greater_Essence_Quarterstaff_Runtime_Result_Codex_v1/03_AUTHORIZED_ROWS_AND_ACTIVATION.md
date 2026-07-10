# Authorized rows and activation

Only these rows changed to `active_in_current_simulation: true` and `runtime_admission_status: accepted_executable_runtime`:

| Operation | Guaranteed modifier | Family | Side |
|---|---|---|---|
| `greater_essence_abrasion` | `crafted_greater_abrasion_flat_physical` | `adds_value_to_value_physical_damage` | prefix |
| `greater_essence_flames` | `crafted_greater_flames_flat_fire` | `adds_value_to_value_fire_damage` | prefix |
| `greater_essence_ice` | `crafted_greater_ice_flat_cold` | `adds_value_to_value_cold_damage` | prefix |
| `greater_essence_electricity` | `crafted_greater_electricity_flat_lightning` | `adds_value_to_value_lightning_damage` | prefix |
| `greater_essence_battle` | `crafted_greater_battle_accuracy` | `value_to_accuracy_rating` | prefix |
| `greater_essence_haste` | `crafted_greater_haste_attack_speed` | `value_increased_attack_speed` | suffix |
| `greater_essence_seeking` | `crafted_greater_seeking_critical_hit_chance` | `value_to_critical_hit_chance` | suffix |
| `greater_essence_infinite` | `crafted_greater_infinite_attribute` | `value_to_attribute_choice` | suffix |

`config/project_scope.yaml` activates only the `greater_essence` group/mechanic. Perfect Essence remains non-admitted. Tests compare the admitted set to the exact eight-row constant.
