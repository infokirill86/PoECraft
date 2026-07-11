# Edge Cases, Stop Conditions, and Separate Gates

## Edge cases M43-A must define

| Case | Required behavior |
|---|---|
| Later step rejects current rarity | Explicit no-transition at that step; earlier committed state retained; later steps skipped |
| Deterministic Essence step | Single transition through its accepted executor; no synthetic weighted branch |
| Perfect Essence feasible pool empty | Inherit accepted no-transition/no-consumption for that step |
| Fractured modifier present | Preserve every accepted operation's fracture protection |
| Different paths reach same item but at different failure steps | Keep separate execution terminals; optional state-only projection may merge later |
| Exact ceiling exceeded | Structured stop; no truncation, renormalization, or hidden MC substitution |
| Row admitted in data but executor unsupported | Fail closed; do not infer a generic handler |
| Omen/modifier supplied | Fail closed until separate modifier admission |

## Stop conditions during implementation

Stop and return to ChatGPT/User if:

- a sequence needs conditional branching, retry, fallback, or route selection;
- an operation needs mechanics changes rather than adapter/dispatch work;
- an accepted single-operation result differs under one-step sequence parity;
- operation admission and executor support become ambiguous;
- exact execution would be silently approximated;
- public probability output, optimizer/economics/advice, automation, or boundary closure enters scope.

## Work that remains separately gated

- Omen inventory reconciliation and runtime admission;
- Fracture runtime and its disputed Desecrated edge;
- Alchemy multi-add;
- Essence replacement/stacking/repeat and Astrid/rune capacity;
- Desecrate/Jawbone/Reveal and PD-013;
- sequences longer than the first bounded floor;
- conditional policies, retry loops, planner, route comparison, optimizer, economics, and advice;
- public numeric probability release;
- SOURCE/PROVENANCE, broader MML, crafted-capacity, or PD-013 closure;
- automation/GitHub Actions.
