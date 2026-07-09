# Source Table

checked_at_utc: `2026-07-09`

| Source | URL / repo path | Scope checked | Evidence summary | Load-bearing use |
|---|---|---|---|---|
| PoE2DB Chaos Orb | `https://poe2db.tw/us/Chaos_Orb` | base Chaos wording | Says Chaos removes a random modifier and augments a rare item with a new random modifier. | Primary support for base Chaos random-removal wording. |
| PoE2DB Currency page | `https://poe2db.tw/us/Currency` | currency list cross-check | Lists Chaos / Greater Chaos / Perfect Chaos as random removal plus random add; lists Orb of Annulment as random removal; lists Exalted as random add. | Cross-check against individual pages. |
| PoE2DB Orb of Annulment | `https://poe2db.tw/us/Orb_of_Annulment` | Annulment wording | Says Orb of Annulment removes a random modifier from an item. | Primary support for base Annulment random-removal wording. |
| PoE2DB Exalted Orb | `https://poe2db.tw/us/Exalted_Orb` | Exalted-like add wording | Says Exalted Orb augments a rare item with a new random modifier and rare items can have up to six random modifiers. | Primary support for ordinary_add / Exalted-like random-add wording. |
| PoE2DB Omen of Whittling | `https://poe2db.tw/us/Omen_of_Whittling` | Whittling/Omen interaction | Says the next Chaos Orb removes the lowest level modifier. | Primary support that lowest-level selection is an Omen-over-Chaos modifier, not base Chaos wording. |
| PoE2 Wiki Chaos Orb | `https://www.poe2wiki.net/wiki/Chaos_Orb` | community source cross-check | Describes base Chaos as random remove + random add; lists Whittling under related Omens. | Supporting evidence only. |
| PoE2 Wiki Omen of Whittling | `https://www.poe2wiki.net/wiki/Omen_of_Whittling` | community source cross-check | Describes Whittling with Chaos as removing the modifier with the lowest item-level requirement; notes this is unrelated to tier. | Supporting detail for Whittling semantics. |
| PoE2 Wiki Orb of Annulment | `https://www.poe2wiki.net/wiki/Orb_of_Annulment` | community source cross-check | Describes Annulment as random modifier removal; lists side/desecrated Omens separately. | Supporting evidence only. |
| PoE2 Wiki Exalted Orb | `https://www.poe2wiki.net/wiki/Exalted_Orb` | community source cross-check | Describes Exalted add; lists side Omens as add-only-prefix/add-only-suffix modifiers. | Supporting evidence for side Omens as filters. |
| Craft of Exile PoE2 | `https://www.craftofexile.com/?game=poe2` | project secondary source availability | Public HTML confirms PoE2 support, experimental/disclaimer status, and that Omens narrow currency behavior. No specific base Chaos remove-rule text was accessible in static HTML. | Support only; not sole authority for this verification. |
| RePoE PoE2 | `https://repoe-fork.github.io/poe2/` | structural export availability | Provides datamined structural exports. No direct currency behavior rule was used from this check. | Structural support only. |
| Official patch 0.5.0 notes | `https://www.pathofexile.com/forum/view-thread/3932540` | official wording search | No direct base Chaos / Whittling equipment-crafting rule was found in the checked patch page. It mentions some Chaos-related Waystone Omens. | Context only; not load-bearing for base equipment Chaos. |
| Repo operations | `data/operations.yaml` | operation rows | `chaos`, `greater_chaos`, and `perfect_chaos` are `admission_candidate`; all include remove_then_add-like sequence and Omen filters. | Repo-state grounding. |
| Repo omens | `data/omens.yaml` | Omen mappings | `whittling` applies to `chaos` group with `selection: minimum_modifier_level`; tie breaker is project policy. | Clarifies Whittling is Omen metadata. |
| Repo mechanics evidence | `data/mechanics_evidence.yaml` | project evidence state | Whittling is `PROJECT_ADOPTED_INFERENCE`; tie behavior is not published. MML applies to greater/perfect chaos addition. | Identifies unresolved/project-policy parts. |
| Repo source policy | `data/sources.yaml` | source hierarchy | PoE2DB + Craft of Exile agreement is project-model truth, not server truth; conflicts require user resolution. | Governing policy. |

