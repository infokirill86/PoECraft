# Selected M41 Wave and Inventory

## Selected boundary

M41-A should implement the **Greater Essence quarterstaff core only**.

All eight rows share these mechanics:

- input rarity: Magic;
- output rarity: Rare;
- retain existing modifiers;
- remove count: zero;
- add exactly one row-declared guaranteed crafted modifier;
- validate family/group conflict, crafted capacity, item-class applicability, and target-side Rare capacity before commit;
- commit rarity and modifier atomically;
- no legal result means no-transition/no-consumption.

## Eight proposed rows

| Operation id | Guaranteed family | Side | Direct structural relevance |
|---|---|---|---|
| `greater_essence_abrasion` | flat physical damage | prefix | Physical quarterstaff route |
| `greater_essence_flames` | flat fire damage | prefix | Weapon damage family coverage |
| `greater_essence_ice` | flat cold damage | prefix | Weapon damage family coverage |
| `greater_essence_electricity` | flat lightning damage | prefix | Weapon damage family coverage |
| `greater_essence_battle` | accuracy | prefix | Attack-family coverage |
| `greater_essence_haste` | attack speed | suffix | Attack-speed coverage |
| `greater_essence_seeking` | critical hit chance | suffix | Quarterstaff critical-family coverage |
| `greater_essence_infinite` | attribute choice | suffix | Attribute-family coverage |

The rows are proposed together because mechanics are identical and behavior is entirely data-selected. The batch does not include Lesser, Normal, Perfect, Corrupted, or newly observed external Essence rows not present in the accepted project dataset.

## Runtime admission discipline

During a later implementation floor, only these eight rows may move from `data_reference_candidate` to proposed executable admission. They become accepted executable runtime only after Claude audit and ChatGPT/User gate.
