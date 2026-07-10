# Trusted Source and Repo Evidence

Checked on 2026-07-10. These sources support project-model design, not PoE2 server-truth closure.

| Evidence | Location | Finding | Design use |
|---|---|---|---|
| Official Content Update 0.3.0 | https://www.pathofexile.com/forum/view-thread/3826682 | Essences have four tiers; specific outputs depend on tier/item type; Greater can upgrade Magic to Rare and add a guaranteed modifier; Perfect removes random then adds guaranteed | Confirms family-level transition split |
| PoE2DB Greater Essence of Abrasion | https://poe2db.tw/us/Greater_Essence_of_Abrasion | Magic-to-Rare; guaranteed two-handed physical-damage prefix; Quarterstaves listed | Confirms selected physical row and item applicability |
| PoE2DB Essence overview | https://poe2db.tw/us/Essence | Greater is Magic-to-Rare; Perfect is remove-and-guaranteed-add | Cross-checks official wording |
| PoE2 Wiki Perfect Essence of Abrasion | https://www.poe2wiki.net/wiki/Perfect_Essence_of_Abrasion | Random removal plus guaranteed physical prefix on Rare item | Confirms Perfect family shape but not capacity-conditioned removal |
| Craft of Exile | https://www.craftofexile.com/?game=poe2 | Independent crafting model; site itself labels PoE2 weighting/features as work in progress | Supporting comparison only, not sole authority |
| Repo operation registry | `data/operations.yaml` | Eight Greater rows are `data_reference_candidate`; six Perfect rows are `admission_candidate`; neither family is executable | Admission boundary is intact |
| Repo output registry | `data/essence_outputs.yaml` | Exact quarterstaff output ids, families, sides, groups, tags, and crafted-capacity cost are prepared | Load-bearing proposed row data |
| Repo scope | `config/project_scope.yaml` | Perfect Essence is active-scope data; Greater Essence route is currently reference-only | M41-A is a separately gated scope expansion, not silent accepted truth |

## Source conflict / drift surfaced

Current PoE2DB Omen listings include entries not present in `data/omens.yaml`, including Alchemy/Coronation and Greater Annulment examples. Therefore a future broad Omen wave must begin with inventory/version reconciliation. No external data is copied into project truth by this package.

## PoE1 analogy

PoE1 Essences also guarantee a named modifier family, so they support the architectural idea of a data-selected guaranteed output. Their full-item reroll behavior is not the PoE2 Greater Essence mechanic and is not used as executable evidence. The PoE2-specific official 0.3 wording and current PoE2DB row remain load-bearing.

## Perfect Essence unresolved rule

Trusted wording does not define the probability semantics when random removal leaves no capacity on the guaranteed modifier's side. Community reports suggest capacity-conditioned selection or no-consumption failure attempts, but community reports are supporting evidence only. Required future gate question:

> Does the project model condition Perfect Essence removal on removals that permit the guaranteed add, or include invalid removal branches as no-transition/no-consumption outcomes?
