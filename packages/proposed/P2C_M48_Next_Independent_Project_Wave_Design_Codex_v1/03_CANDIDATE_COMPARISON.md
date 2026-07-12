# Candidate Comparison

| Candidate | Quarterstaff value | Source/mechanics certainty | Open dependency | Architecture fit | Decision |
|---|---|---|---|---|---|
| Omen of Light | High after a Reveal result: lets Annulment remove only Desecrated modifiers | Wording is clear | Accepted runtime cannot yet create the revealed target state | Reuses M45 removal filtering | Defer until Reveal is usable, or admit later as a small companion gate |
| Abyssal Echoes | High for rerolling Reveal choices | One-reroll contour clear | Exact Reveal sampler plus Ancient-MML persistence conflict | Reuses future Reveal offer generator | Blocked by D4/conflict |
| Putrefaction | Potentially broad Desecrated route | Contour clear but edge behavior is version/conflict-heavy | Multi-placeholder state, corrupt state, MML behavior, no Reveal runtime | Requires new multi-placeholder/multi-reveal architecture | Separate major mechanics wave |
| Revealed Desecrated + Fracture | High for protected special modifiers | User ratified part of contour, sources conflict | PD-013 and runtime extension explicitly open | Fits current flags only after gate | Blocked |
| Astrid / crafted capacity | High for two crafted modifiers and Essence routes | Current item wording strongly supports +1 capacity | Replacement/removal persistence and accepted Essence preconditions remain open | Prepared operation/state contour exists | Separate focused mechanics verification |
| More fixed-length steps | Low | High | None | M43-A already supports 1-8 | Infrastructure drift |
| Bounded caller-authored branching evaluation | **High now**: uses all accepted operations and can stop/fallback by actual result | Truth-neutral architecture; no new game mechanic | None of D3-D5/Echoes/PD-013 | Direct extension of M43-A exact/MC/replay | **Selected** |

## Broadest coherent batch

The safe unit is not "conditional syntax" alone. It is:

1. deterministic classification of actual terminal state against accepted success criteria;
2. validation of a finite caller-authored route DAG;
3. exact and seeded-MC traversal through the existing executor registry;
4. replay, diagnostics, mass conservation, and linear-sequence parity.

These parts are jointly reconstructible and automatically testable. Search, ranking, costs, and cyclic retry language are not part of the batch.
