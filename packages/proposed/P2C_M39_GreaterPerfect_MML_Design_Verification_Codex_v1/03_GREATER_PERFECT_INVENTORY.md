# Greater/Perfect inventory

Source: `data/operations.yaml` at observed repo head `963a61f110a56ee72477a1266d0f6c35ca177a96`.

## Summary

Total Greater/Perfect operation rows found: 24.

The rows divide into two different categories:

1. MML ordinary-add / remove-then-add variants: 10 rows.
2. Essence guaranteed-output mechanics: 14 rows.

The essence rows must not be treated as MML-only variants.

## MML ordinary-add / remove-then-add variants

| operation_id | group | active_in_current_simulation | runtime_admission_status | base shape | MML | Codex classification |
|---|---:|---:|---|---|---:|---|
| `greater_transmutation` | transmutation | false | data_reference_candidate | normal -> magic, add ordinary weighted | 44 | MML-like, but base transmutation wrapper not accepted runtime |
| `perfect_transmutation` | transmutation | false | data_reference_candidate | normal -> magic, add ordinary weighted | 70 | MML-like, but base transmutation wrapper not accepted runtime |
| `greater_augmentation` | augmentation | false | data_reference_candidate | magic add ordinary weighted with magic-side capacity rule | 44 | MML-like, but base augmentation wrapper not accepted runtime |
| `perfect_augmentation` | augmentation | false | data_reference_candidate | magic add ordinary weighted with magic-side capacity rule | 70 | MML-like, but base augmentation wrapper not accepted runtime |
| `greater_regal` | regal | false | data_reference_candidate | magic -> rare, add ordinary weighted using rare pool | 35 | MML-like, but base regal wrapper not accepted runtime |
| `perfect_regal` | regal | false | data_reference_candidate | magic -> rare, add ordinary weighted using rare pool | 50 | MML-like, but base regal wrapper not accepted runtime |
| `greater_exalted` | exalted | true | admission_candidate | rare add ordinary weighted | 35 | best future MML batch candidate after M39 audit |
| `perfect_exalted` | exalted | true | admission_candidate | rare add ordinary weighted | 50 | best future MML batch candidate after M39 audit |
| `greater_chaos` | chaos | true | admission_candidate | remove uniformly, rebuild ordinary add pool, add ordinary weighted | 35 | best future MML batch candidate after M39 audit |
| `perfect_chaos` | chaos | true | admission_candidate | remove uniformly, rebuild ordinary add pool, add ordinary weighted | 50 | best future MML batch candidate after M39 audit |

## Greater Essence rows

| operation_id | group | active_in_current_simulation | runtime_admission_status | shape | Codex classification |
|---|---:|---:|---|---|---|
| `greater_essence_abrasion` | greater_essence | false | data_reference_candidate | guaranteed crafted output, no ordinary weighted MML add | separate Essence admission |
| `greater_essence_flames` | greater_essence | false | data_reference_candidate | guaranteed crafted output, no ordinary weighted MML add | separate Essence admission |
| `greater_essence_ice` | greater_essence | false | data_reference_candidate | guaranteed crafted output, no ordinary weighted MML add | separate Essence admission |
| `greater_essence_electricity` | greater_essence | false | data_reference_candidate | guaranteed crafted output, no ordinary weighted MML add | separate Essence admission |
| `greater_essence_battle` | greater_essence | false | data_reference_candidate | guaranteed crafted output, no ordinary weighted MML add | separate Essence admission |
| `greater_essence_haste` | greater_essence | false | data_reference_candidate | guaranteed crafted output, no ordinary weighted MML add | separate Essence admission |
| `greater_essence_seeking` | greater_essence | false | data_reference_candidate | guaranteed crafted output, no ordinary weighted MML add | separate Essence admission |
| `greater_essence_infinite` | greater_essence | false | data_reference_candidate | guaranteed crafted output, no ordinary weighted MML add | separate Essence admission |

## Perfect Essence rows

| operation_id | group | active_in_current_simulation | runtime_admission_status | shape | Codex classification |
|---|---:|---:|---|---|---|
| `perfect_essence_abrasion` | perfect_essence | true | admission_candidate | remove uniform installed instance, then guaranteed crafted output | separate Essence admission |
| `perfect_essence_flames` | perfect_essence | true | admission_candidate | remove uniform installed instance, then guaranteed crafted output | separate Essence admission |
| `perfect_essence_ice` | perfect_essence | true | admission_candidate | remove uniform installed instance, then guaranteed crafted output | separate Essence admission |
| `perfect_essence_electricity` | perfect_essence | true | admission_candidate | remove uniform installed instance, then guaranteed crafted output | separate Essence admission |
| `perfect_essence_battle` | perfect_essence | true | admission_candidate | remove uniform installed instance, then guaranteed crafted output | separate Essence admission |
| `perfect_essence_haste` | perfect_essence | true | admission_candidate | remove uniform installed instance, then guaranteed crafted output | separate Essence admission |

## Important interpretation

`active_in_current_simulation: true` is not runtime authorization. Runtime permission must come from `runtime_admission_status: accepted_executable_runtime` or an accepted engine primitive.

No Greater/Perfect row is accepted executable runtime by this package.

