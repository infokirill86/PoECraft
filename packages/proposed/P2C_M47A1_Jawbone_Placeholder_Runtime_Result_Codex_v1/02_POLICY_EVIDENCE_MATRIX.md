# Policy and Evidence Matrix

| Contract | Implemented evidence | Hard boundary |
|---|---|---|
| Exact three-row inventory | Resolver allowlist, runtime IDs, admission data, and tests agree on Gnawed/Preserved/Ancient only | Reveal and every other row remain non-admitted |
| D1-A: only one free side | Candidate pool contains that side only and preserves every installed modifier | A full side is never selected while the opposite side is free |
| D1-A: both sides free | Candidate pool contains prefix and suffix with equal unit weights | No replacement candidates enter the pool |
| D2-A: fully occupied | Combined prefix/suffix installed-instance pool uses unit weights | Runs only when neither side has capacity |
| Fractured exclusion | Fractured installed instances are omitted from D2-A metadata and terminal invariants reject their removal | No Omen or alternate replacement selector |
| One-Desecrated invariant | Existing hidden placeholder or revealed `desecrated` instance fails before selection | No rune/Putrefaction bypass |
| Canonical placeholder | Dedicated object stores side, source Jawbone row, Reveal MML, null Lich constraint, and hidden state by type | No Reveal offer generation |
| Atomicity | Source item is immutable; failure terminal is byte-equivalent canonical state; D2 removal and install share one terminal construction | No partial removal state |
| Fracture minimum | Three installed modifiers plus one hidden placeholder satisfies the minimum | Placeholder is absent from the target candidates |
| Exact/oracle | Branch options use exact rational unit-weight masses and terminal aggregation by canonical state hash | No public probability values |
| Seeded replay | Same seed/run/input produces the same decisions, trajectories, and result hash | No hidden alternate RNG path |
| Sequence parity | One-step M43-A exact and seeded results match direct Jawbone execution | Evaluator remains non-planning |
| Negative control | A deliberately non-unit candidate weight raises a hard invariant failure | No silent normalization |

## Capacity / replacement matrix

| Prefix capacity | Suffix capacity | Runtime action |
|---|---|---|
| free | full | install prefix; remove nothing |
| full | free | install suffix; remove nothing |
| free | free | choose prefix/suffix uniformly; remove nothing |
| full | full | choose uniformly over all removable non-fractured installed instances; replace on selected instance side |
| full | full, no eligible replacement | no-transition/no-consumption; source unchanged |
