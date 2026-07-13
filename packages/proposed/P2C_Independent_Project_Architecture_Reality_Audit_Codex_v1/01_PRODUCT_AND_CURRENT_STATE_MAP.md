# Product and Current-State Map

## 1. Что в итоге строится

Целевой продукт — PoE2 crafting simulator для физического quarterstaff-маршрута, который должен последовательно пройти такие слои:

| Слой | Назначение | Реальность на audit pin |
|---|---|---|
| External evidence | официальные формулировки, PoE2DB, Craft of Exile, RePoE, player checks | есть, но provenance/freshness ещё не закрыты |
| Normalized game data | моды, family/group, tiers, levels, weights, currencies, Omens | есть для quarterstaff-подмножества |
| Item state + legality | rarity, affixes, capacity, fractured/crafted/desecrated, conflicts | исполняется |
| Operation compilation | currency + Omens + state → fail-closed plan | исполняется через `OperationResolver` |
| Mechanics execution | atomic transitions через accepted executors | исполняется для accepted surface |
| Probability engines | exact rational oracle + seeded MC + replay | исполняются |
| Sequence evaluation | заранее заданные accepted steps | исполняется для 1–8 шагов |
| Target evaluation | state → `TOP` / `ACCEPTABLE` / `NOT_SUCCESS` | YAML есть, executable classifier отсутствует |
| Adaptive scenario evaluation | caller-authored branches/stop conditions | design/proposal only |
| Strategy search | генерировать и сравнивать маршруты | отсутствует и gated |
| Economics | цены, attempts, budgets, EV | исторические/карантинные основания есть, текущий продуктовый слой отсутствует/gated |
| Advice/UI | объяснимые рекомендации пользователю | отсутствует/gated |

Иными словами, внутренний двигатель уже умеет «проигрывать заданный рецепт», но ещё не является помощником, который понимает цель и объясняет маршрут.

## 2. Что реально исполняется

### Ядро

- immutable `ItemState` и canonical hash;
- canonical modifier index;
- legality/capacity/family/group checks;
- единый ordinary weighted add pool;
- общий removal-pool по identity экземпляров;
- MML, side и removal-selector filters;
- exact weighted branching и deterministic SHA-256 rejection sampling;
- replay/decision IDs/traces;
- atomic no-transition/no-consumption failure semantics;
- fail-closed resolver и explicit executor registry.

### Исполнительная поверхность

- 35 accepted rows из `data/operations.yaml`;
- engine primitive `ordinary_add`, которого нет как currency row;
- 10 accepted executable Omens;
- fixed 1–8-step accepted-operation sequences;
- exact path/terminal aggregation с ceilings;
- seeded MC с теми же принятыми pool/executor contracts.

Проверка registry дала: `35 accepted catalog rows`, `0 missing`, плюс `ordinary_add` как вне-каталоговый primitive.

### Что является только данными/design/tooling

- `install_astrid`: admission candidate, не executable;
- `reveal_desecrated`: blocked/out-of-scope;
- 7 Abyss/Desecrated Omens: reference/blocked;
- D3–D5 Reveal sampling: proposed candidates, не mechanics truth;
- Reveal observation analyzer: evidence tooling, не crafting runtime;
- `config/success_criteria.yaml`: загружаемые данные, но не executable classifier;
- M48 branching evaluation: proposed design, не runtime;
- source/provenance, broad MML, crafted-capacity и PD-013: открыты.

## 3. Item и modifier foundation

### Принятая форма состояния

`ItemState` хранит:

- `item_class`, `rarity`, `item_level`;
- tuple установленных `ModifierInstance`;
- для экземпляра: `mod_id`, `crafted`, `desecrated`, `fractured`;
- необязательный `DesecratedPlaceholder` с side/Jawbone/MML/Lich constraint;
- augment socket counters и `astrid_installed`.

Явных объектов «пустой слот» нет. Занятые prefix/suffix считаются по canonical static modifier side, а свободные слоты выводятся из capacity.

### Capacity

| Rarity | Prefix | Suffix | Total |
|---|---:|---:|---:|
| Normal | 0 | 0 | 0 |
| Magic | 1 | 1 | 2 |
| Rare | 3 | 3 | 6 |

Placeholder занимает обычный слот своей стороны. Fractured modifier также занимает обычный слот. Desecrated limit сейчас равен одному hidden-or-revealed объекту.

### Static modifier surface

- ordinary quarterstaff rows: `158`;
- Desecrated rows: `16`;
- canonical modifier index после добавления Essence outputs: `188`;
- ordinary families: `23`;
- ordinary sides: `70 prefix`, `88 suffix`;
- modifier levels: `1..82`;
- все ordinary generation weights положительные.

`StaticModifier` содержит `family_id`, side, `group_ids`, tier, modifier level, tags и generation weight. Pool builder:

1. проверяет item class/rarity/level;
2. применяет side capacity;
3. блокирует installed families/groups;
4. применяет MML family fallback;
5. удаляет non-positive rows;
6. выбирает tier row по accepted weights.

### Сильные места

- family/group legality находится в общем kernel, а не копируется по валютам;
- fractured flag неизменяем для accepted removals;
- placeholder участвует в capacity и Fracture minimum count, но не target pool;
- canonical identity отделена от path identity;
- exact и MC используют общие pool contracts.

### Ограничения и допущения

- только quarterstaff;
- tier-level моделирование, без numeric affix rolls;
- нет base-stat/quality/socket/rune/corruption полного состояния;
- active product start и общая runtime ability расходятся (см. discrepancy D-03);
- Astrid/crafted-limit остаётся латентным спорным полем состояния (D-04);
- Reveal sampling и revealed-Desecrated/Fracture runtime остаются закрыты;
- success criteria загружаются, но пока не исполняются.

## 4. Техническая архитектура сегодня

Правильное разделение уже существует:

```text
static data
  -> ItemState / legality / pool builders
  -> OperationResolver + Omen compiler
  -> operation executors
  -> exact or seeded-MC outcome resolution
  -> fixed sequence evaluator
```

Но operation executors лежат в `monte_carlo/`, хотя многие реализуют одновременно exact, direct и MC behavior. Это название и зависимость устарели концептуально. Кроме того, `bounded_sequence.py` имеет собственные per-operation dispatch methods, а direct harnesses — свои; one-step parity tests защищают результат, но архитектура масштабируется через дублирование orchestration.

Отдельно существует старый `domain/action.py`/trace-v2 ActionPlan contour, почти не связанный с текущим `ResolvedOperationPlan`. Это два потенциальных plan vocabulary. До стратегии нужно выбрать канонический внутренний contract, а второй явно объявить legacy/reference либо адаптировать.
