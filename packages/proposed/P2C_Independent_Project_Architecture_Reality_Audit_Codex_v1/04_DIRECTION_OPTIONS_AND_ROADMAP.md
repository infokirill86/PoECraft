# Project Direction, Options, and Roadmap

## 1. Архитектурный вердикт

Проект не потерял направление, но приблизился к новой точке риска: mechanics engine уже достаточно широк, а всё последующее планирование продолжает вести себя так, будто главный дефицит — ещё одна валюта.

Сильная сторона текущего пути — принятые операции опираются на общие legality/pool kernels, exact/MC/replay и fail-closed admission. Слабая — продуктовый feedback loop не закрыт: нет executable target semantics, adaptive user-supplied evaluation и интерфейса результата. Поэтому добавление новых операций теперь даёт меньшую предельную ценность, чем вертикальный evaluator slice.

## 2. Strategic options

| Направление | Ценность сейчас | Риск | Вердикт |
|---|---|---|---|
| Ещё accepted operations | medium; закрывает отдельные route edges | Reveal/Astrid/PD-013 source gates | не immediate default |
| Дополнительно harden MC | low | infrastructure drift | отложить до нового statistical need |
| Source refresh/reconciliation | high foundation | может превратиться в бесконечный data project | обязательный параллельный floor, но не вместо продукта |
| Unified executor protocol | medium/high maintainability | чистый refactor может съесть milestone | включить минимально в product wave |
| Success classifier + caller DAG evaluator | highest | criteria требуют explicit gate; опасность незаметно стать planner | recommended immediate wave |
| Conditional/retry language | medium later | циклы/policy semantics быстро превращаются в optimizer | после finite DAG |
| Strategy search/optimizer | будущая высокая ценность | слишком рано: нет goal/runtime product seam, costs/source freshness | отдельный high-risk blueprint позже |
| Economics/advice/UI | конечная ценность | source/time/public-output gates | после evaluator и release policy |

## 3. Recommended immediate wave

### Gate 0 — два коротких human decisions

До кода ChatGPT/Kirill должны:

1. ратифицировать либо исправить `config/success_criteria.yaml` как project-model target contract;
2. определить active-start product contract (fixed fractured start versus multi-start/progression).

Это genuine accepted-truth gates; их нельзя скрыть внутри implementation.

### M48-A-equivalent: Goal-Aware Bounded Evaluation Vertical Slice

Одна широкая, но coherent implementation wave:

1. **Deterministic success classifier**
   - input: canonical `ItemState`;
   - output только `TOP`, `ACCEPTABLE`, `NOT_SUCCESS`;
   - никакого score, probability, cost или ranking;
   - unsupported criteria shape fails closed.

2. **Finite caller-authored DAG evaluator**
   - пользователь заранее задаёт все nodes/edges;
   - predicates только deterministic state-based;
   - bounded, acyclic, no retries/loops/generation;
   - каждое действие проходит accepted `OperationResolver` и registry.

3. **Shared executor seam consolidation**
   - один internal adapter/protocol для direct, exact, MC и sequence calls;
   - one-step parity остаётся hard invariant;
   - никаких mechanics changes.

4. **Internal scenario report**
   - terminal class counts/masses, stop reason, replay metadata;
   - numeric evidence остаётся quarantined/internal;
   - не выдавать advice и «лучший путь».

5. **Evidence**
   - hand fixtures для TOP/ACCEPTABLE/NOT_SUCCESS;
   - exact mass conservation/ceiling honesty;
   - seeded replay;
   - branch-current-state correctness;
   - negative controls for score/cost/ranking predicates;
   - full registry parity and regression.

Это широкая безопасная волна: она не вводит новую игровую механику, не генерирует маршруты и не меняет accepted operations. Она превращает движок из «проигрывателя списка валют» в «оценщик пользовательского crafting-сценария относительно цели».

## 4. Broad roadmap

### Wave R0 — Truth reconciliation (короткий gate + documentary delta)

- active starts/scope;
- success criteria semantics;
- Astrid/crafted capacity disposition;
- target patch/league/source snapshot policy;
- repair stale status/evidence labels.

### Wave R1 — Goal-aware evaluator (immediate implementation)

- classifier;
- bounded caller DAG;
- shared executor adapter;
- internal scenario report;
- exact/MC/replay evidence.

### Wave R2 — Source-backed operation completion

- ingest current quarterstaff-relevant candidate inventory (including new current-patch crafting families) as proposed data;
- Reveal D3–D5 after real observations;
- Omen of Light/Echoes only after dependencies;
- resolve or retire Astrid legacy contour;
- no blanket «all game operations» expansion.

### Wave R3 — Strategy prerequisites

- canonical action/plan vocabulary consolidation;
- failure/consumption and attempt semantics over goal-aware paths;
- price-source contract with timestamps/league;
- strategy-search blueprint with explicit objective and human gate.

### Wave R4 — Search, economics, and product release

- route generation/search only after separate optimizer gate;
- economics/EV only after source/time contract;
- explanatory UI/API;
- public numeric release with uncertainty, source labels and release-specific leak checks;
- advice remains separately authorized.

## 5. Что нельзя смешивать

- Reveal sampling decision с generic evaluator;
- source data updates с silent runtime acceptance;
- finite caller DAG с route generation;
- classifier label с score/ranking;
- internal numeric evidence с public release;
- executor refactor с mechanics change;
- current-quarterstaff vertical slice с all-item-class expansion.

## 6. Против micro-stepping

Для truth-neutral implementation больше не нужны отдельные milestones на schema, exact, MC, replay и diagnostics, если они составляют один контракт и имеют общую test surface. Отдельный gate нужен только на mechanics truth, public output, optimizer/economics/advice, automation и boundary closure.
