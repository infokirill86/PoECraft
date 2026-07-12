# D3-D5 Evidence and Candidate Models

All selected recommendations below remain **PROPOSED** until an explicit ChatGPT/User gate names them.

| Decision | Evidence-backed contour | Candidate models | Recommended project-base candidate | Status |
|---|---|---|---|---|
| D3 exclusive composition | At least one exclusive offer when a compatible row exists; more than one may appear | A: reserve one compatible exclusive, then fill from the remaining combined pool; B: one shared independent mixture; C: fixed category slots | D3-A | explicit User decision required |
| D4 candidate unit | Offers are tier-specific modifier outcomes; ordinary and exclusive rows have different weight evidence | A: canonical eligible tier row; B: family first then tier; C: independent draws with rejection | D4-A tier-row unit | explicit User decision required |
| D4 weighting/order | Ordinary weights appear conventional; exclusive weights uneven; exact server order unpublished | A: sequential current-pool weight-proportional draws without replacement, blocking family/groups after each selection; B: category/family stage before weights | D4-A prepared sequential model | explicit User decision required |
| D4 display order | No reliable evidence that position changes mechanics | A: presentation-only permutation after the set exists; B: position-specific generation | D4-A presentation-only | explicit User decision required |
| D5 insufficient set | The game can report "Could not generate mod" and show no usable set | A: atomic fail/no consumption/source unchanged; B: show fewer offers; C: relax filters | D5-A fail-closed | explicit User decision required |

## D3-A precise candidate

If at least one compatible exclusive row exists, select one exclusive offer first from the exclusive eligible pool. Remove its family/group conflicts. Fill the remaining positions sequentially from the combined remaining ordinary-plus-exclusive eligible pool. This guarantees at least one exclusive while allowing more than one.

## D4-A precise candidate

The sampling unit is one canonical modifier tier row. At every draw, weights are read from the current remaining eligible rows. Selected rows are removed, and all rows conflicting by family/group are blocked before the next draw. The final set is unordered mechanically; display order is a deterministic presentation permutation derived from the same decision trace.

## D5-A precise candidate

If a complete compatible set cannot be constructed, return structured `NO_TRANSITION_NO_CONSUMPTION`; preserve the hidden placeholder and the entire source item. No reduced set, MML relaxation, or compatibility relaxation occurs.
