# MML mechanics/source table

## Source hierarchy used

| Source | Role in this package | Observation |
|---|---|---|
| `data/operations.yaml` | Current project operation catalog | Greater/Perfect transmutation, augmentation, regal, exalted, and chaos rows encode `transition.add.mml` values; Essence rows do not use ordinary weighted MML add. |
| `data/mechanics_evidence.yaml` | Current project mechanics evidence and approved project-model rule | MML policy is `family_internal_threshold_with_strongest_family_fallback`; runtime status is `USER_APPROVED_PROJECT_RULE`; evidence remains `supported_empirically_server_unconfirmed`. |
| `data/sources.yaml` | Source policy | PoE2DB + Craft of Exile agreement is model truth, not server truth; conflicts require user approval. |
| PoE2DB Currency page | External current-data check | Greater/Perfect Transmutation, Augmentation, Regal, Exalted, and Chaos entries list modifier-level thresholds matching repo data. |
| Official Path of Exile 0.5.0 patch notes | Official wording support | Patch notes describe new Greater/Perfect currency tiers and use "minimum level" language for at least Greater/Perfect Transmutation and Augmentation. |
| Craft of Exile | Registered project source | Dynamic site was not used as line-level decisive evidence in this package. Existing repo policy still treats it as a required corroborating project source when available. |

## Trusted-source observations

PoE2DB current Currency page agrees with repo values:

| Operation family | Greater MML | Perfect MML | External observation |
|---|---:|---:|---|
| Transmutation | 44 | 70 | PoE2DB lists "Modifier Level 44/70". |
| Augmentation | 44 | 70 | PoE2DB lists "Modifier Level 44/70". |
| Regal | 35 | 50 | PoE2DB lists "Modifier Level 35/50". |
| Exalted | 35 | 50 | PoE2DB lists "Modifier Level 35/50". |
| Chaos | 35 | 50 | PoE2DB lists remove + augment wording with "Modifier Level 35/50". |

Official 0.5.0 patch notes corroborate the "minimum level" mechanic wording for newly introduced Greater/Perfect tiers. They also show that these thresholds can change by patch, so MML must stay source/provenance-open.

## Current repo MML implementation shape

Current ordinary add pool builder:

1. filters by item/base/radius applicability;
2. applies side capacity;
3. blocks installed family IDs;
4. blocks installed conflicting group IDs;
5. applies family-internal MML;
6. removes non-positive weights;
7. samples a weighted tier row.

Current `apply_family_mml` behavior:

- if `mml` is `null`, keep the pool unchanged;
- group candidate rows by `family_id`;
- within each family, keep rows whose `modifier_level >= mml`;
- if no row in a family reaches the threshold, keep the strongest tier row for that family;
- if a family has co-equal strongest rows, fail closed with `StaticDataDefect`.

This is a project-model rule, not a PoE2 server-truth claim.

