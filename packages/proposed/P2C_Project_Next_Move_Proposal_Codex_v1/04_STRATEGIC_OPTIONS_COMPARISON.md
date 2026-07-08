# Strategic Options Comparison

| Option | Description | Value | Risk | Recommendation |
|---|---|---:|---:|---|
| Continue M34 hardening | More `ordinary_add` sequence/property work. | Medium | Low | Do only if directly needed by operation admission. |
| Bounded N-step ordinary-add infrastructure | Generalize fixed-length sequence helper for accepted `ordinary_add`. | Medium | Medium | Defer; useful but not the highest-value next move. |
| Operation-admission framework | Define how new operations become executable. | High | Low-medium | Recommended next move. |
| First new real operation design | Design Annulment or another first operation. | High | Medium | Include as candidate selection under admission framework. |
| First new real operation implementation now | Implement Annulment immediately. | High | Medium-high | Too early without admission contract/audit. |
| ACTIVE_TASK freshness checker | Build schema validator/checker. | Low-medium | Low | Defer unless workflow drift recurs. |
| Public numeric release | Release probability values. | Product-visible but risky | High | Not now. |
| Optimizer/economics/advice | Strategy layer. | Future high | Very high now | Not now. |

## Option evaluation

### Continue M34 hardening

Useful if the goal is confidence in sequence infrastructure. But after M34-B1, more ordinary-add-only hardening risks becoming infrastructure work detached from the product goal.

### Bounded N-step ordinary-add infrastructure

Technically safe, but strategically second-best. It strengthens the runway but does not expand simulator capability.

### Operation-admission framework

Best next move. It is truth-neutral if kept design-only and gives the project a repeatable gate for admitting Annulment, Chaos, Perfect Essence, and later Jawbone/Reveal.

### First new real operation design

Good if paired with the admission framework. Annulment is the best first candidate because it is removal-only, uses existing removal pool infrastructure, and does not require add+remove composition yet.

### First new real operation implementation now

Not recommended. Implementation without a prior admission contract would reintroduce ad hoc gates and increase audit ambiguity.

## Codex recommendation

Move to:

```text
M35 Operation Admission Framework + First Operation Candidate Selection
```

Recommended first candidate:

```text
Annulment
```
