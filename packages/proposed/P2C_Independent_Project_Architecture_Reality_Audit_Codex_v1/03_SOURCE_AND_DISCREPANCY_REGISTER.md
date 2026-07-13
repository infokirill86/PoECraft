# Source Foundation and Discrepancy Register

## 1. Источники и их реальная роль

| Источник | Что проверено 2026-07-13 | Правильная роль | Ограничение |
|---|---|---|---|
| [Official 0.2 patch](https://www.pathofexile.com/forum/view-thread/3740562/page/1) | Fracturing Orb: random mod, Rare, минимум 4 | primary mechanics contour | не раскрывает RNG и Desecrated edge |
| [Official 0.3 patch](https://www.pathofexile.com/forum/view-thread/3826682) | Greater/Perfect families и MML concept | primary feature contour | exact thresholds не перечислены |
| [Official 0.3.1 patch](https://www.pathofexile.com/forum/view-thread/3862213/page/1) | Alchemy на Magic, старые mods не сохраняются | primary contour | не раскрывает 4-add sampling internals |
| [Official 0.5 patch](https://www.pathofexile.com/forum/view-thread/3932540) | crafted/Desecrated limits, changed outputs, new crafting families | current primary change source | repo surface не полностью reconciled |
| [PoE2DB Currency](https://poe2db.tw/us/Currency) | currency wording и MML 44/70, 35/50 | trusted project-model display data | не server truth |
| [PoE2DB Quarterstaves](https://poe2db.tw/Quarterstaves) | class/tier/mod applicability surface | trusted project-model data | динамический сайт, snapshot не pinned |
| [PoE2DB Fracturing Orb](https://poe2db.tw/us/Fracturing_Orb) | current text + cannot use on fractured | corroboration | не раскрывает disputed edges |
| [PoE2DB Abyss](https://poe2db.tw/us/Abyss) | Jawbones, Omens, three-offer contour | trusted contour | не раскрывает D3–D5 sampling |
| [Craft of Exile PoE2](https://www.craftofexile.com/?game=poe2) | intended independent pool/weight comparison | model corroboration | repo прямо признаёт extrapolated weights; exact snapshot отсутствует |
| [RePoE PoE2](https://repoe-fork.github.io/poe2/) | structural IDs/tags; live page reports version `4.5.4.3` | structural support | version/hash не записан в `sources.yaml` |
| PoE Ninja | пока не используется runtime | future economics/time-series source | назван в hierarchy, но source entry/pin отсутствуют |
| Kirill in-game | Whittling tie contour: 2 tests | project-rule evidence | Reveal D3–D5 observations ещё отсутствуют |

Принцип repo разумный: agreement trusted sources = project-model truth, не server truth; conflict нельзя переписывать автоматически. Проблема не в политике, а в слабой воспроизводимости source snapshots.

## 2. Discrepancy register

| ID | Severity | Расхождение | Риск / действие |
|---|---|---|---|
| D-01 | medium | `ACTIVE_TASK` = audited/user gate, а `CURRENT_STATUS` live paragraph всё ещё говорит ready for Claude | routing не сломан, но человек/модель получают разные ответы; snapshot надо обновлять при следующем разрешённом gate |
| D-02 | high-cognitive | все 37 operations имеют `active_in_current_simulation: true`, включая `install_astrid` и blocked Reveal; `project_scope` также называет их active | permission технически защищён `runtime_admission_status`, но naming вводит в заблуждение; переименовать/разделить prepared scope и executable scope в отдельной metadata wave |
| D-03 | high-product | `CURRENT_STATUS` говорит, что Normal/Magic starts вошли в simulator scope, но `project_scope` и `initial_states` по-прежнему объявляют sole fixed fractured-Rare start и не моделируют получение fracture | требуется Kirill gate: это один fixed-route product или multi-start simulator; после решения синхронизировать config/status |
| D-04 | high-foundation | `ItemState`/capacity разрешают `crafted_limit=1+astrid_installed`, а official 0.5 говорит: один crafted modifier, Desecrated отдельно max 1; `install_astrid` не admitted, но latent state semantics остаются | accepted runtime пока защищён, но до strategy layer нужно решить: удалить/заморозить legacy Astrid semantics или дать актуальное подтверждение |
| D-05 | low/medium | `omens.yaml` всё ещё помечает Whittling uniform tie-break как unpublished policy, тогда как `mechanics_evidence.yaml` фиксирует user player-confirmed contour | behavior одинаков, но evidence labels расходятся; documentary reconciliation later |
| D-06 | high-source | `sources.yaml` имеет общий `checked_at: 2026-06-25`, URL и `status: checked`, но нет per-source checked_at, content hash/version/snapshot | нельзя воспроизвести, какие именно bytes дали 158 ordinary rows и weights; SOURCE/PROVENANCE закономерно остаётся open |
| D-07 | medium/product-scope | official 0.5 добавляет новые crafting families (например 13 Alloys) и меняет значения; prepared operation DB содержит 37 выбранных rows, но не является полной current-game inventory | это не runtime defect, но название «complete database» нужно понимать как prepared quarterstaff scope; нужен current-patch candidate inventory до широкого product claim |
| D-08 | high-product | `success_criteria.yaml` имеет `status: READY` и загружается, но нет executable classifier и нет ясного отдельного acceptance row для semantics | нельзя строить adaptive evaluator, пока пользователь явно не ратифицирует criteria contract |
| D-09 | medium-architecture | direct operation harnesses и `bounded_sequence.py` имеют отдельную per-operation orchestration; one-step parity ловит drift, но новый operation требует правок в нескольких местах | перед branching evaluator ввести единый internal executor protocol или адаптер, без mechanics changes |
| D-10 | positive | 35 admitted catalog rows полностью совпадают с executor registry; extra entry только `ordinary_add` | runtime admission foundation согласован |
| D-11 | low-navigation | 54 directories в `packages/proposed`, хотя многие ledger-accepted; 56 reviews | ledger делает truth корректной, но onboarding тяжёл; не перемещать evidence без отдельной cleanup wave |
| D-12 | medium-architecture | `domain/action.py` ActionPlan/trace-v2 contour и текущий `ResolvedOperationPlan` живут параллельно | выбрать канонический plan vocabulary до planner/strategy; не удалять молча |
| D-13 | low-status | `CURRENT_STATUS` сохраняет историческую фразу «base Exalted remains not admitted» в M39-B bullet, хотя M40-A позже его admitted | хронологически верно, как current snapshot двусмысленно |
| D-14 | low-governance | Participant Voice Charter footer говорит `final candidate`, accepted ledger — accepted | authority у ledger, но stale footer снижает доверие к first-read docs |
| D-15 | medium-release | leak scan является broad candidate scanner и выдаёт множество expected internal candidates, затем PASS; это не точный public-release proof | перед реальным public numeric gate нужен allowlist/context-aware release checker |

## 3. Где есть реальный конфликт, а где только открытая область

### Реальный/материальный конфликт

- Astrid/crafted capacity against current official 0.5 contour (D-04).
- Active start/scope contract между config и status (D-03).
- `READY` success data без принятого executable meaning (D-08).

### Открыто, но корректно fail-closed

- Reveal D3–D5;
- Echoes interaction;
- revealed Desecrated + Fracture/PD-013;
- broad MML/source closure;
- public numeric output;
- optimizer/economics/advice.

### Repo блокирует работу излишне

- дальнейшая MC-hardening для уже accepted operations не нужна перед goal-aware evaluator: 329-test suite, exact oracle, deterministic replay и registry parity дают достаточный implementation floor;
- branching evaluation over accepted operations не требует нового mechanics gate;
- Omen of Light contour хорошо описан внешне, но его runtime dependency на accepted revealed-Desecrated path остаётся реальной причиной блокировки, а не недостаток текста источника.

## 4. Explicit Kirill/ChatGPT decisions и in-game checks

1. **Product start contract:** fixed purchased fractured staff only, либо также Normal/Magic starts и путь получения fracture.
2. **Success contract:** принять/исправить `TOP`, `ACCEPTABLE`, order и origin/crafted treatment до classifier implementation.
3. **Astrid/crafted state:** official-0.5 one-crafted rule делает старую +1-capacity модель подозрительной. Нужен explicit retire/retain decision; если retain — скрин/актуальный item text и воспроизводимый in-game test.
4. **Target patch/league:** зафиксировать, какую версию PoE2 моделирует repo и когда source snapshot считается stale.
5. **Reveal D3–D5:** использовать уже принятый observation protocol; реальные screenshots/IDs остаются обязательными.
6. **Economics later:** перед ценами выбрать league/realm/timestamp и зарегистрировать PoE Ninja/source snapshot; сейчас не открывать.
