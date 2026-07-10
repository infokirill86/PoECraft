# Trusted-source comparison

Checked on: `2026-07-10`

Project interpretation: trusted-source agreement supports project-model truth only. It is not a PoE2 server-truth claim. External changes or conflicts must be surfaced and separately approved before runtime data changes.

## Sources

| Source | Role in this verification | Result |
|---|---|---|
| `data/operations.yaml` | Prepared operation contracts and thresholds | All ten rows have coherent input/output rarity, one ordinary add, and the expected MML values. |
| `data/mechanics_evidence.yaml` | Accepted project MML policy | Lists Transmutation, Augmentation, Regal, and Exalted as consumers of the shared family-internal MML policy; broader MML remains open. |
| `data/sources.yaml` | Project source hierarchy | PoE2DB is registered for exact displayed thresholds; Craft of Exile remains an independent pool comparison source. |
| [Official Content Update 0.3.0 notes](https://www.pathofexile.com/forum/view-thread/3826682) | Official introduction/context | Confirms Greater/Perfect Transmutation, Augmentation, Regal, and Exalted currencies and that each has its own minimum modifier level for the modifier it adds. |
| [PoE2DB Currency](https://poe2db.tw/us/Currency) | Exact displayed wording and thresholds | Confirms base effects plus `44/70` for Transmutation/Augmentation and `35/50` for Regal/Exalted. |
| [PoE2DB Crafting](https://poe2db.tw/us/Crafting) | Cross-family effect comparison | Confirms normal-to-magic +1, magic +1, magic-to-rare +1, and rare +1 shapes. |
| [PoE2 Wiki rarity](https://www.poe2wiki.net/wiki/Rarity) and [crafting](https://www.poe2wiki.net/wiki/Crafting) | Supporting capacity/context evidence | States that ordinary magic items support one prefix and one suffix and ordinary rare items three of each. Supporting only, not sole authority. |
| [PoE1 Augmentation discussion](https://www.pathofexile.com/forum/view-thread/19962) | PoE1 analogue | Supports the long-standing one-prefix/one-suffix magic capacity and forced remaining side. Analogy only; not PoE2 proof. |

## Agreement table

| Question | Repo data | Trusted-source result | Project-model conclusion |
|---|---|---|---|
| Transmutation effect | normal -> magic, add 1 | Matches PoE2DB wording | Confirmed for design. |
| Greater/Perfect Transmutation | same effect, MML 44/70 | Matches PoE2DB; official notes corroborate MML concept | Confirmed for design; broader MML remains open. |
| Augmentation effect | magic-only, add 1, max two explicit slots | Matches PoE2DB and supporting capacity sources | Confirmed for design. |
| Greater/Perfect Augmentation | same effect, MML 44/70 | Matches PoE2DB; official notes corroborate MML concept | Confirmed for design; broader MML remains open. |
| Regal effect | magic -> rare, add 1 | Matches PoE2DB wording | Confirmed for design. |
| Greater/Perfect Regal | same effect, MML 35/50 | Matches PoE2DB; official notes corroborate MML concept | Confirmed for design; broader MML remains open. |
| Base Exalted | rare, add 1 | Matches PoE2DB wording | Direct wrapper over accepted `ordinary_add`; no new mechanic. |

## Pool-build rarity conclusion

Public wording does not separately expose an internal timing step called `pool_build_rarity`. The project-model rule is nevertheless mechanically necessary and source-aligned:

- Transmutation says it upgrades to magic and adds a modifier. A normal item has no magic affix capacity, so the add pool must use the target magic state.
- Regal says it upgrades to rare and adds a modifier. A full two-mod magic item has no magic capacity, but the operation still adds a rare modifier, so the add pool must use the target rare state.

This is recorded as a project-model execution inference, not server implementation truth.

## Gaps and conflicts

- No contradictory trusted source was found for the scoped effects or thresholds.
- `data/sources.yaml` registers a later official patch reference, while the directly relevant introduction wording is in official update `0.3.0`. Future evidence maintenance should add the `0.3.0` source explicitly; this is a registry completeness gap, not a mechanics conflict.
- Craft of Exile is useful for later pool regression checks, but no stable line-level operation wording from it is load-bearing in this design.
- Broader MML fallback/source closure remains open by gate.
