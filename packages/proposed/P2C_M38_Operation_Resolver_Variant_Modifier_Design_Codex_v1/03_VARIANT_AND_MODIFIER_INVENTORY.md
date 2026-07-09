# Variant and Modifier Inventory

## Source/data basis checked

Local repo files inspected:

- `data/operations.yaml`
- `data/omens.yaml`
- `data/mechanics_evidence.yaml`
- `data/sources.yaml`
- `CURRENT_STATUS.md`
- accepted ledger files

External trusted source pages checked for this design:

- PoE2DB Chaos Orb: `https://poe2db.tw/us/Chaos_Orb`
- PoE2DB Greater Chaos Orb: `https://poe2db.tw/us/Greater_Chaos_Orb`
- PoE2DB Perfect Chaos Orb: `https://poe2db.tw/us/Perfect_Chaos_Orb`
- PoE2DB Exalted Orb: `https://poe2db.tw/us/Exalted_Orb`
- PoE2DB Greater Exalted Orb: `https://poe2db.tw/us/Greater_Exalted_Orb`
- PoE2DB Perfect Exalted Orb: `https://poe2db.tw/us/Perfect_Exalted_Orb`
- PoE2DB Orb of Annulment: `https://poe2db.tw/us/Orb_of_Annulment`
- PoE2DB Omen of Whittling: `https://poe2db.tw/us/Omen_of_Whittling`
- PoE2DB Omen of Sinistral Erasure: `https://poe2db.tw/us/Omen_of_Sinistral_Erasure`
- PoE2DB Omen of Dextral Erasure: `https://poe2db.tw/us/Omen_of_Dextral_Erasure`
- PoE2DB Omen of Sinistral Annulment: `https://poe2db.tw/us/Omen_of_Sinistral_Annulment`
- PoE2DB Omen of Light: `https://poe2db.tw/us/Omen_of_Light`
- PoE2DB Omen of Greater Exaltation: `https://poe2db.tw/us/Omen_of_Greater_Exaltation`

No external source conflict was found that requires a user decision for this design package. This does not close SOURCE/PROVENANCE.

## Greater/Perfect inventory

| Operation row | Group | Local primitive shape | Local MML | Runtime status | PoE2DB/source alignment | M38 classification |
|---|---|---|---:|---:|---|---|
| `greater_transmutation` | transmutation | ordinary add-like | 44 | data_reference_candidate | not live-checked for this package | variant candidate; not executable |
| `perfect_transmutation` | transmutation | ordinary add-like | 70 | data_reference_candidate | not live-checked for this package | variant candidate; not executable |
| `greater_augmentation` | augmentation | ordinary add-like | 44 | data_reference_candidate | not live-checked for this package | variant candidate; not executable |
| `perfect_augmentation` | augmentation | ordinary add-like | 70 | data_reference_candidate | not live-checked for this package | variant candidate; not executable |
| `greater_regal` | regal | ordinary add-like | 35 | data_reference_candidate | not live-checked for this package | variant candidate; not executable |
| `perfect_regal` | regal | ordinary add-like | 50 | data_reference_candidate | not live-checked for this package | variant candidate; not executable |
| `greater_exalted` | exalted | ordinary add-like | 35 | admission_candidate | PoE2DB shows Minimum Modifier Level 35 and add-one-random-modifier wording | appears MML-only for add behavior, but not admitted |
| `perfect_exalted` | exalted | ordinary add-like | 50 | admission_candidate | PoE2DB shows Minimum Modifier Level 50 and add-one-random-modifier wording | appears MML-only for add behavior, but not admitted |
| `greater_chaos` | chaos | remove_then_add | 35 | admission_candidate | PoE2DB shows Minimum Modifier Level 35 and remove-random/add-random wording | appears MML-on-add variant over base Chaos shape, but not admitted |
| `perfect_chaos` | chaos | remove_then_add | 50 | admission_candidate | PoE2DB shows Minimum Modifier Level 50 and remove-random/add-random wording | appears MML-on-add variant over base Chaos shape, but not admitted |

Design conclusion: Greater/Perfect rows checked here appear to be MML/pool-filter variants for the add side, not separate base primitives. However M38 must not assume all Greater/Perfect variants are identical across all currency families without per-row source/data confirmation.

## Omen/modifier inventory

| Omen row | Applies to group | Local effect | Source alignment | Runtime status in M38 |
|---|---|---|---|---|
| `greater_exaltation` | exalted | add two modifiers, no partial execution | PoE2DB wording says next Exalted adds two random modifiers | modifier-layer candidate only |
| `sinistral_exaltation` | exalted | add prefix only | local repo evidence; not live-checked here | modifier-layer candidate only |
| `dextral_exaltation` | exalted | add suffix only | local repo evidence; not live-checked here | modifier-layer candidate only |
| `sinistral_annulment` | annulment | remove prefix only | PoE2DB wording says next Annulment removes only prefix modifiers | modifier-layer candidate only |
| `dextral_annulment` | annulment | remove suffix only | local counterpart to sinistral; not live-opened here | modifier-layer candidate only |
| `light` | annulment | remove desecrated modifiers only | PoE2DB wording says next Annulment removes only Desecrated modifiers | modifier-layer candidate only |
| `sinistral_erasure` | chaos | Chaos removes prefix only | PoE2DB wording says next Chaos removes only prefix modifiers | modifier-layer candidate only |
| `dextral_erasure` | chaos | Chaos removes suffix only | PoE2DB wording says next Chaos removes only suffix modifiers | modifier-layer candidate only |
| `whittling` | chaos | Chaos removes lowest modifier-level modifier, uniform tie policy project-inferred | PoE2DB wording confirms lowest-level removal; tie behavior remains project policy | modifier-layer candidate only |
| `sinistral_crystallisation` / `dextral_crystallisation` | perfect_essence | removal side filter | local repo evidence | candidate only; depends on Essence admission |
| `sinistral_necromancy` / `dextral_necromancy` | jawbone | forced side | local repo evidence | blocked until Jawbone/Reveal path admitted |
| `liege` / `blackblooded` / `sovereign` | jawbone | Lich tag guarantee-one | user-approved project rule in data; not executable here | blocked until Jawbone/Reveal path admitted |
| `abyssal_echoes` | reveal | reveal offer-set reroll | local repo evidence | blocked until Reveal path admitted |

Design conclusion: Omens are independent modifier layers, not members of Chaos/Annulment/Exalted families. The resolver must compile them as active modifiers over a base currency request, not as separate hardcoded currency variants.

