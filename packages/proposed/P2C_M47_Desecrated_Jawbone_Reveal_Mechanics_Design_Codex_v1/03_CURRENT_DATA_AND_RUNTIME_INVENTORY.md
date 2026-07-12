# Current Data and Runtime Inventory

## Operation rows

| Row | Prepared contour | Runtime admission |
|---|---|---|
| `gnawed_jawbone` | Rare weapon/quiver; project row carries item-level ceiling; hidden placeholder | blocked/reference only |
| `preserved_jawbone` | Rare weapon/quiver; hidden placeholder | blocked/reference only |
| `ancient_jawbone` | Rare weapon/quiver; hidden placeholder; MML | blocked/reference only |
| `reveal_desecrated` | fixed placeholder side; ordinary plus exclusive pool; three offers; atomic replacement | blocked/reference only |

All four rows are catalog-active but not executable-admitted. `active_in_current_simulation` remains project-scope metadata and grants no runtime permission.

## State and pool foundations

- `DesecratedPlaceholder` already stores side, Jawbone identity, reveal MML, and optional Lich constraint.
- `ModifierInstance` already has independent `desecrated`, `crafted`, and `fractured` flags.
- canonical state hashing includes the complete placeholder context and installed flags.
- capacity code counts a placeholder on its stored side.
- `build_reveal_base_pool` already provides a prepared union/filter pipeline for ordinary and exclusive Desecrated rows.
- existing Reveal-pool tests are foundation prototypes, not accepted runtime evidence.

## Relevant modifier rows

| Modifier | Prepared effect | Current admission |
|---|---|---|
| Sinistral/Dextral Necromancy | force Jawbone prefix/suffix | blocked/reference only |
| Liege/Blackblooded/Sovereign | named-Lich constraint | blocked/reference only |
| Abyssal Echoes | reroll Reveal offers once | blocked/reference only |
| Light | Annulment restricted to Desecrated | blocked/reference only |
| Putrefaction | replace all modifiers with multiple placeholders and corrupt | blocked; explicitly outside clean M47 |

No currently accepted M45-A Omen directly authorizes Jawbone or Reveal behavior. The accepted modifier compiler can be reused later, but admission remains separate.
