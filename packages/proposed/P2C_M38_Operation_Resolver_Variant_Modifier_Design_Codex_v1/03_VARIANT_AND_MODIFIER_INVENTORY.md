# Variant and Modifier Inventory

## Source/data basis checked

Local repo files inspected:

- `data/operations.yaml`
- `data/omens.yaml`
- `data/mechanics_evidence.yaml`
- `data/sources.yaml`
- `CURRENT_STATUS.md`
- accepted ledger files

This package does not perform a new external source capture and does not close SOURCE/PROVENANCE. It uses the local source registry and accepted project-model data currently in the repo. `data/sources.yaml` records the project source hierarchy and conflict policy; any future external conflict or changed data must still go to Kirill/ChatGPT for resolution.

## Greater/Perfect inventory

| Operation row | Group | Local primitive shape | Local MML | Runtime status | PoE2DB/source alignment | M38 classification |
|---|---|---|---:|---:|---|---|
| `greater_transmutation` | transmutation | ordinary add-like | 44 | data_reference_candidate | not live-checked for this package | variant candidate; not executable |
| `perfect_transmutation` | transmutation | ordinary add-like | 70 | data_reference_candidate | not live-checked for this package | variant candidate; not executable |
| `greater_augmentation` | augmentation | ordinary add-like | 44 | data_reference_candidate | not live-checked for this package | variant candidate; not executable |
| `perfect_augmentation` | augmentation | ordinary add-like | 70 | data_reference_candidate | not live-checked for this package | variant candidate; not executable |
| `greater_regal` | regal | ordinary add-like | 35 | data_reference_candidate | not live-checked for this package | variant candidate; not executable |
| `perfect_regal` | regal | ordinary add-like | 50 | data_reference_candidate | not live-checked for this package | variant candidate; not executable |
| `greater_exalted` | exalted | ordinary add-like | 35 | admission_candidate | local operations/evidence indicate MML threshold | appears MML-only for add behavior in repo data, but not admitted |
| `perfect_exalted` | exalted | ordinary add-like | 50 | admission_candidate | local operations/evidence indicate MML threshold | appears MML-only for add behavior in repo data, but not admitted |
| `greater_chaos` | chaos | remove_then_add | 35 | admission_candidate | local operations/evidence indicate MML threshold on add side | appears MML-on-add variant over base Chaos shape in repo data, but not admitted |
| `perfect_chaos` | chaos | remove_then_add | 50 | admission_candidate | local operations/evidence indicate MML threshold on add side | appears MML-on-add variant over base Chaos shape in repo data, but not admitted |

Design conclusion: Greater/Perfect rows in local repo data mostly appear to be MML/pool-filter variants for ordinary add-like or add-side behavior, not separate base primitives. However M38 must not assume all Greater/Perfect variants are identical across all currency families without per-row source/data confirmation.

Rows needing separate source/mechanics decisions before runtime admission:

- Transmutation/Augmentation/Regal variants: data-reference only; rarity/precondition semantics remain outside current runtime.
- Exalted variants: appear MML-only in local data, but Exalted currency runtime itself is not admitted.
- Chaos variants: appear MML-on-add over base remove_then_add in local data, but Greater/Perfect Chaos are not admitted.
- Essence/Jawbone/Reveal/Fracture/Desecrate-related rows: specialized mechanics, blocked/disputed/out-of-scope or admission candidates; not MML-only resolver work.

## Omen/modifier inventory

| Omen row | Applies to group | Local effect | Source alignment | Runtime status in M38 |
|---|---|---|---|---|
| `greater_exaltation` | exalted | add two modifiers, no partial execution | local repo evidence | modifier-layer candidate only |
| `sinistral_exaltation` | exalted | add prefix only | local repo evidence | modifier-layer candidate only |
| `dextral_exaltation` | exalted | add suffix only | local repo evidence | modifier-layer candidate only |
| `sinistral_annulment` | annulment | remove prefix only | local repo evidence | modifier-layer candidate only |
| `dextral_annulment` | annulment | remove suffix only | local repo evidence | modifier-layer candidate only |
| `light` | annulment | remove desecrated modifiers only | local repo evidence | modifier-layer candidate only |
| `sinistral_erasure` | chaos | Chaos removes prefix only | local repo evidence | modifier-layer candidate only |
| `dextral_erasure` | chaos | Chaos removes suffix only | local repo evidence | modifier-layer candidate only |
| `whittling` | chaos | Chaos removes lowest modifier-level modifier, uniform tie policy project-inferred | `mechanics_evidence.yaml` confirms lowest-level rule; tie behavior remains project policy | modifier-layer candidate only |
| `sinistral_crystallisation` / `dextral_crystallisation` | perfect_essence | removal side filter | local repo evidence | candidate only; depends on Essence admission |
| `sinistral_necromancy` / `dextral_necromancy` | jawbone | forced side | local repo evidence | blocked until Jawbone/Reveal path admitted |
| `liege` / `blackblooded` / `sovereign` | jawbone | Lich tag guarantee-one | user-approved project rule in data; not executable here | blocked until Jawbone/Reveal path admitted |
| `abyssal_echoes` | reveal | reveal offer-set reroll | local repo evidence | blocked until Reveal path admitted |

Design conclusion: Omens are independent modifier layers, not members of Chaos/Annulment/Exalted families. The resolver must compile them as active modifiers over a base currency request, not as separate hardcoded currency variants.
