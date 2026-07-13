# Risks and Remaining Gates

| Risk | Implemented control |
|---|---|
| Evaluator drifts into planner | Caller supplies the complete finite graph; no generation/comparison/recommendation API |
| Predicate becomes hidden score | Closed categorical state registry; forbidden value/field tests |
| Stale branch state | Every node resolves/classifies the actual current branch state and records hashes |
| Exact result is quietly approximated | Structured empty-result ceiling stop; MC is a separate explicit call |
| Newly admitted operation executes accidentally | Existing explicit M43-A executor registry remains required |
| Malformed graph produces ambiguous behavior | Unique/reachable/acyclic/full-reference/full-case validation and unique terminal labels |
| Internal probabilities leak as advice | Public payloads omit probability values and declare numeric release false |

## Still separately gated

- M48-A acceptance itself.
- Any route generation, search, comparison, selection, ranking, recommendation, score, cost, economics, EV, advice, conditional retry language, or cyclic policy.
- Any public numeric probability release.
- Reveal and D3-D5, Echoes, Omen of Light, Putrefaction, Astrid/crafted capacity, revealed-Desecrated Fracture, and PD-013.
- New operation, Omen, modifier, predicate mechanics, source-policy admission, SOURCE/PROVENANCE closure, broader MML closure, crafted-capacity closure, automation, or GitHub Actions.

## Audit watchpoints

1. Confirm the exposed accepted-step seam preserves M43-A direct/executor behavior.
2. Hostile-test graph validation and exact overflow for partial-mass leakage.
3. Confirm the strict success classifier matches the accepted config and fails on unsupported shapes.
4. Confirm no public payload or predicate surface can carry optimizer vocabulary or values.
5. Confirm `CURRENT_STATUS`/ledgers record only design acceptance and implementation authorization, not M48-A acceptance.
