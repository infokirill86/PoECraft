# In-Game Verification Matrix

The repetition counts below are test sample sizes, not released probability results. All trials must be logged before results are inspected. Record item text, item level, prefix/suffix occupancy, fractured flags, Jawbone, Omens, hidden side, complete Reveal window, and final action outcome.

| Question | Required setup | Exact action and observable | Minimum repetitions | Models distinguished |
|---|---|---|---|---|
| D1 single free side | Rare quarterstaff with one side full and the opposite side having capacity; no Desecrated state; no Omen | apply Preserved Jawbone; record hidden side and whether any modifier was removed; repeat with mirrored occupancy | ten per mirrored setup | free-side-only/no-removal versus prepared free-or-replaceable-side lottery |
| D1 both sides free | equivalent Rare quarterstaves with capacity on both sides; no Omen | apply Preserved Jawbone; record hidden side | one hundred | deterministic/weight-driven bias versus approximately symmetric side choice; cannot prove exact server uniformity |
| D2 full replacement | full Rare quarterstaff; one fractured installed modifier; known side/identity for every other instance | apply Preserved Jawbone; record removed identity and hidden side | one hundred twenty | combined eligible-instance selection versus side-first selection; fractured exclusion is a mandatory invariant |
| D3 exclusive guarantee | high-item-level quarterstaff with a placeholder side known to have at least one compatible exclusive Desecrated row | reveal and record all offers without selecting based on value | thirty per side | guaranteed-exclusive versus shared mixture; one zero-exclusive valid window falsifies the guarantee model |
| D4 offer composition and weighting screen | fixed item class, item level, side, installed blockers, and Jawbone tier; new equivalent item for each trial | capture every offer mod ID, tier, category, family/groups, and displayed position | five hundred windows | gross category composition, duplicate/conflict behavior, position patterns, tier-row versus family-first fit; screening only |
| D4 high-confidence model comparison | same protocol with machine-readable logging and pre-registered analysis | compare complete observed offer sets against candidate likelihood models | five thousand windows | meaningful discrimination of low-frequency rows and competing weighted algorithms; still project evidence, not server proof |
| D5 insufficient pool | engineer the smallest legal quarterstaff pool using low item level, fixed side, and installed family/group blockers; verify expected pool independently from repo data | attempt Reveal and record whether it fails, presents fewer offers, or relaxes constraints | ten equivalent setups; stop earlier only on a deterministic repeatable error with preserved currency/state | fail-closed versus reduced-set versus fallback-relaxation |

## Practical warning

D4 is not a reasonable casual manual test. If Kirill does not want a large structured collection, the honest alternative is an explicit project-model policy gate for D4-A with SOURCE/PROVENANCE left open.
