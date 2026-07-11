# Source and evidence table

Checked 2026-07-11. External evidence is used as project-model input, not a server-truth claim.

| Source | Finding | Confidence / use |
|---|---|---|
| Official Content Update 0.3.0: `https://www.pathofexile.com/forum/view-thread/3826682` | Perfect Essences remove a random modifier and augment a Rare item with a guaranteed modifier | Primary confirmation of family shape; does not define removal domain or side-capacity handling |
| Official 0.5 patch notes: `https://www.pathofexile.com/forum/view-thread/3932540` | Items can have only one crafted modifier at a time; guaranteed crafting outputs are crafted | Primary current-rule evidence for a single crafted slot; replacement behavior is not specified |
| PoE2DB Essence: `https://poe2db.tw/us/Essence` | Current Perfect wording and item-specific outputs | Trusted project-model cross-check |
| PoE2DB Perfect Abrasion: `https://poe2db.tw/us/Perfect_Essence_of_Abrasion` | Quarterstaff physical prefix and modifier level | Confirms prepared prefix row |
| PoE2DB Perfect Haste: `https://poe2db.tw/us/Perfect_Essence_of_Haste` | Quarterstaff Onslaught suffix and modifier level | Confirms prepared suffix row |
| PoE2 Wiki Essence: `https://www.poe2wiki.net/wiki/Essence` | Repeats remove-random-plus-guaranteed-add family wording | Secondary corroboration |
| GGG forum community reports: `https://www.pathofexile.com/forum/view-thread/3853903` and `https://www.pathofexile.com/forum/view-thread/3894843` | Reports indicate removal is constrained when the guaranteed side is full | Supporting behavior evidence only; not sufficient alone for exact probability truth |
| Craft of Exile PoE2 | Useful emulator comparison, but PoE2 behavior is not primary authority | Audit aid only |
| `data/operations.yaml` | Proposes uniform removal, fractured exclusion, Omen side filter, and prevalidation | Unaccepted model hypothesis, not proof |
| `data/essence_outputs.yaml` | Six exact outputs and a one-crafted-capacity model | Internally consistent prepared data; crafted-capacity remains unaccepted |
| `data/sources.yaml` / `data/mechanics_evidence.yaml` | Official 0.5 source is registered, but no accepted Perfect Essence removal/repeat contract exists | Confirms a decision gate is still required |

PoE1 Essence rerolls are mechanically different and are not used to define PoE2 Perfect Essence. PoE1 contributes only the general warning that “crafted modifier” capacity rules are system-level constraints.
