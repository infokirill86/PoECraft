# Complete Operation and Currency Classification

## Классификационные правила

- `engine primitive`: исполняемая внутренняя операция, не обязательно currency row.
- `accepted executable operation`: currency/catalog row с accepted runtime admission и registered executor.
- `currency mapping over primitives`: accepted currency компилируется из общих primitive/pool layers.
- `design/data/evidence only`: есть описание или инструмент, но runtime admission отсутствует.
- `blocked`: механика или evidence недостаточны либо gate явно закрыт.

Все 37 catalog rows имеют `active_in_current_simulation: true`; это **не** execution authority. Канонический authority — `runtime_admission_status` плюс explicit resolver/executor support.

## Engine primitives и shared effects

| Primitive/effect | Статус | Использование |
|---|---|---|
| `ordinary_add` | accepted engine primitive | weighted legal tier-row add |
| uniform installed-instance removal | accepted shared pool/effect | Annulment, Chaos, Perfect Essence feasibility |
| rarity transition | accepted shared effect | Transmutation/Regal/Essence/Alchemy |
| sequential add with branch rebuild | accepted shared effect | Greater Exaltation, Alchemy, sequences |
| remove-then-add atomic composition | accepted composite | Chaos family |
| guaranteed canonical install | accepted shared effect | Greater/Perfect Essence |
| set fractured flag on selected instance | accepted effect | Fracturing Orb |
| placeholder install/replace | accepted effect | Jawbone family |
| Omen filter/compiler | accepted modifier layer | 10 accepted Omens |
| Reveal offer generation | design/evidence only | D3–D5 unresolved |
| Astrid crafted-capacity augmentation | data candidate only | source-open/conflicting |

## Все 37 operation rows

| # | `operation_id` | Классификация | Executor / primitive mapping | Примечание |
|---:|---|---|---|---|
| 1 | `transmutation` | accepted executable currency mapping | `catalog_single_add` | Normal→Magic, add 1 |
| 2 | `greater_transmutation` | accepted executable variant | `catalog_single_add` + MML 44 | data-driven |
| 3 | `perfect_transmutation` | accepted executable variant | `catalog_single_add` + MML 70 | data-driven |
| 4 | `augmentation` | accepted executable currency mapping | `catalog_single_add` | Magic capacity resolves side |
| 5 | `greater_augmentation` | accepted executable variant | `catalog_single_add` + MML 44 | data-driven |
| 6 | `perfect_augmentation` | accepted executable variant | `catalog_single_add` + MML 70 | data-driven |
| 7 | `regal` | accepted executable currency mapping | target-Rare `catalog_single_add` | Magic→Rare atomically |
| 8 | `greater_regal` | accepted executable variant | same + MML 35 | data-driven |
| 9 | `perfect_regal` | accepted executable variant | same + MML 50 | data-driven |
| 10 | `exalted` | accepted executable currency mapping | accepted add kernel | Rare add 1 |
| 11 | `greater_exalted` | accepted executable variant | `ordinary_add` + MML 35 | shared kernel |
| 12 | `perfect_exalted` | accepted executable variant | `ordinary_add` + MML 50 | shared kernel |
| 13 | `annulment` | accepted executable operation | uniform non-fractured removal | Omen side filters supported |
| 14 | `chaos` | accepted executable composite | uniform removal → rebuilt add | atomic |
| 15 | `greater_chaos` | accepted executable variant | Chaos + post-removal MML 35 | removal unchanged |
| 16 | `perfect_chaos` | accepted executable variant | Chaos + post-removal MML 50 | removal unchanged |
| 17 | `alchemy` | accepted executable composite | discard explicits → 4 sequential adds | Normal/Magic, non-fractured floor |
| 18 | `fracturing_orb` | accepted executable operation | uniform eligible instance → set flag | clean non-Desecrated core |
| 19 | `install_astrid` | proposed candidate / inconsistent foundation | none | active catalog flag, not admitted; crafted-limit conflict/open |
| 20 | `greater_essence_abrasion` | accepted executable guaranteed operation | Greater Essence executor | Magic→Rare, deterministic mod |
| 21 | `greater_essence_flames` | accepted executable guaranteed operation | Greater Essence executor | same family contract |
| 22 | `greater_essence_ice` | accepted executable guaranteed operation | Greater Essence executor | same family contract |
| 23 | `greater_essence_electricity` | accepted executable guaranteed operation | Greater Essence executor | same family contract |
| 24 | `greater_essence_battle` | accepted executable guaranteed operation | Greater Essence executor | same family contract |
| 25 | `greater_essence_haste` | accepted executable guaranteed operation | Greater Essence executor | same family contract |
| 26 | `greater_essence_seeking` | accepted executable guaranteed operation | Greater Essence executor | same family contract |
| 27 | `greater_essence_infinite` | accepted executable guaranteed operation | Greater Essence executor | same family contract |
| 28 | `perfect_essence_abrasion` | accepted executable composite | feasible removal → guaranteed install | temporary `crafted_count==0` floor |
| 29 | `perfect_essence_flames` | accepted executable composite | same Perfect Essence executor | source-open crafted floor |
| 30 | `perfect_essence_ice` | accepted executable composite | same Perfect Essence executor | source-open crafted floor |
| 31 | `perfect_essence_electricity` | accepted executable composite | same Perfect Essence executor | source-open crafted floor |
| 32 | `perfect_essence_battle` | accepted executable composite | same Perfect Essence executor | source-open crafted floor |
| 33 | `perfect_essence_haste` | accepted executable composite | same Perfect Essence executor | source-open crafted floor |
| 34 | `gnawed_jawbone` | accepted executable placeholder operation | Jawbone D1-A/D2-A executor | Rare weapon, ilvl ceiling |
| 35 | `preserved_jawbone` | accepted executable placeholder operation | same Jawbone executor | Rare weapon |
| 36 | `ancient_jawbone` | accepted executable placeholder operation | same Jawbone executor | stored MML 40 |
| 37 | `reveal_desecrated` | design + evidence tooling, runtime blocked | no accepted executor | D3–D5 and real observations open |

Итог: `35/37` catalog rows admitted and registered, `2/37` not admitted. Доказанных obsolete или duplicate rows нет. `install_astrid` является потенциально stale/inconsistent candidate, но объявлять его obsolete без user gate нельзя.

## Все 17 Omen rows

| Omen | Классификация | Effect / зависимость |
|---|---|---|
| `greater_exaltation` | accepted executable modifier | Exalted add-count 2, atomic |
| `sinistral_exaltation` | accepted executable modifier | prefix-only add |
| `dextral_exaltation` | accepted executable modifier | suffix-only add |
| `sinistral_annulment` | accepted executable modifier | prefix-only removal |
| `dextral_annulment` | accepted executable modifier | suffix-only removal |
| `sinistral_erasure` | accepted executable modifier | Chaos prefix removal filter |
| `dextral_erasure` | accepted executable modifier | Chaos suffix removal filter |
| `whittling` | accepted executable modifier | lowest modifier-level, uniform tied minimum |
| `sinistral_crystallisation` | accepted executable modifier | Perfect Essence prefix-removal filter |
| `dextral_crystallisation` | accepted executable modifier | Perfect Essence suffix-removal filter |
| `light` | data/reference; blocked | requires revealed Desecrated Annulment path |
| `sinistral_necromancy` | data/reference; blocked | Jawbone/Reveal modifier layer |
| `dextral_necromancy` | data/reference; blocked | Jawbone/Reveal modifier layer |
| `liege` | data/reference + accepted project-rule contour; runtime blocked | Lich-tag constraint depends on Reveal |
| `blackblooded` | same | depends on Reveal |
| `sovereign` | same | depends on Reveal |
| `abyssal_echoes` | data/reference; runtime blocked | Reveal reroll, D3–D5/Ancient MML interaction open |

## Consistency result

- Положительный результат: accepted runtime registry полностью покрывает 35 admitted catalog rows и отдельно `ordinary_add`.
- Resolver не выводит permission из `active_in_current_simulation` и проверяет `runtime_admission_status`.
- Отрицательный результат: prepared-scope flags и тексты всё ещё выглядят как execution scope, хотя юридически им не являются. Это остаётся источником человеческой ошибки.
- Hardcoded allowlists существуют одновременно в resolver, operation modules и executor registry. Тесты ловят drift, но один централизованный executor protocol/table был бы надёжнее перед дальнейшим ростом.
