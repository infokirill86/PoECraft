# Governance Execution and Validation

## 1. Достаточны ли существующие правила

Да. Participant Voice Charter, `AGENTS.md`, `CLAUDE.md` и Agent Role Pack уже требуют participant critique, project-direction review и human gate. Новый charter не нужен.

Проблема была не в отсутствии правил, а в их исполнении:

- длинные ChatGPT prompts часто заранее фиксировали решение, файлы и микрограницы;
- Codex participant critique нередко превращался в формальный файл после того, как boundary уже задан;
- Claude всё чаще проверял direction, но сам workflow поощрял diff-audit;
- ChatGPT стал единственным постоянным planner, а Codex/Claude — последовательными builder/auditor;
- Kirill видел множество `PASS` и milestone names, но мало цельной продуктовой карты.

Положительные изменения уже есть: live dispatcher один, read order исправлен, agent role files приняты, а последние design waves требуют direction critique. Однако `CURRENT_STATUS`, config scope и historical wording всё ещё позволяют восстановить разные «реальности».

## 2. Минимальное operational improvement без process bloat

Не создавать новый файл или charter. Добавить в обычный handoff только один обязательный видимый блок из трёх строк:

```text
Direction: aligned | adjust | stop
Material objection: none | <one concise objection>
Recommended boundary: <widest safe batch>
```

Правило применяется **до** implementation/audit и показывается Кириллу в chat update, а не прячется только в package. ChatGPT prompts должны задавать цель и hard gates, но не расписывать внутреннюю реализацию, если она reconstructible. Claude должен отдельно оценивать `direction`, даже когда технический verdict GO.

Этого достаточно, чтобы активировать уже принятый charter; новый governance слой не требуется.

## 3. Audit method

- remote `main` fetch/pull и exact pin;
- live ACTIVE validation и byte hash;
- accepted ledger/status/manifest reconstruction;
- static data, item model, legality, resolver, executor registry и tests inspected;
- 37 operations и 17 Omens parsed from YAML;
- accepted catalog rows compared to runtime registry;
- source pages re-opened on 2026-07-13;
- current external wording compared with repo contracts;
- other model's audit file deliberately not read.

## 4. Commands and results

| Check | Result |
|---|---|
| `git fetch --all --prune` + `git pull --ff-only` | local = `origin/main` at audit pin |
| `python tools/validate_active_task.py work/active/ACTIVE_TASK.md` | PASS |
| operations/registry comparison | 35 accepted rows, 0 missing; `ordinary_add` is expected extra primitive |
| `python tools/validate_foundation.py` | PASS; modifier index 188; semantic fingerprint `6e7bc414416189d3d02941b63945457f4a35afafc475bc8bde54d0ddc1659a05` |
| `python tools/validate_m4.py` | PASS |
| `python -m pytest -q` | PASS |
| `python -m pytest --collect-only -q` | 329 tests collected |
| `python tools/check_sha256sums.py SHA256SUMS.txt` | PASS before audit package creation |
| `python tools/check_public_numeric_leaks.py` | PASS; broad candidate list remains internal review noise |
| single tracked `work/active` dispatcher | PASS: only `ACTIVE_TASK.md` |

`check_no_nested_zips.py` reports the three deliberately preserved source-bundle ZIPs under the accepted byte-verification evidence package. No new nested archive was created.

## 5. Boundaries preserved

Этот пакет:

- не меняет runtime, data, config, mechanics или tests;
- не меняет accepted ledgers/status/ACTIVE_TASK;
- не принимает M48 или другой milestone;
- не закрывает SOURCE/PROVENANCE, MML, crafted-capacity или PD-013;
- не публикует numeric crafting probabilities;
- не вводит optimizer/economics/advice/automation;
- предлагает decisions и roadmap, но оставляет authority Кириллу/ChatGPT.
