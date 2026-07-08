# Strategic Options Compared

| Option | Value | Risk | Recommendation |
|---|---|---|---|
| Continue hardening individual `ordinary_add` | Low-medium | Infrastructure drift; diminishing returns | Do not choose as default |
| Broaden accepted-operation sequence infrastructure | High | Can become generic planner if overbuilt | Choose as design-only, tightly bounded |
| M36 heterogeneous chain design over accepted `ordinary_add` + base Annulment | Highest | Manageable if design-only and accepted-ops-only | Recommended |
| Add next operation admission candidate after Annulment | Medium-high later | Isolated handler growth before composition model | Defer until chain design exists |
| Hardening/replay/diagnostics around two accepted operations | Medium | Useful but too narrow alone | Batch into M36 design as requirements |
| ACTIVE_TASK freshness checker / validator | Low right now | Hygiene can distract from simulator progress | Defer unless workflow failures recur |

## Why M36 is the recommended option

M36 uses only already accepted executable operations and asks the next simulator-level question:

```text
Can accepted operations compose safely and reproducibly?
```

This gives product progress without opening new mechanics or source-truth claims.

## Why not a third operation now

A third operation would expand breadth but leave a structural gap: no accepted model for mixed operation chains. Real crafting simulation needs chains. It is better to prove composition over two accepted operations before admitting more mechanics.

