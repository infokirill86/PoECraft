# Candidate Models

These are alternatives for explicit later selection, not accepted policy.

## D1 — side choice

- `D1-A source-conservative`: if only one side has capacity, use it without removal; if both have capacity, choose uniformly between sides.
- `D1-B prepared-YAML`: choose uniformly over every side that is free or has a removable replacement, even when another side is free.
- `D1-C data-first`: admit no runtime until both-free and mixed-capacity behavior is observed.

## D2 — full-item replacement

- `D2-A combined-instance`: choose uniformly over all removable non-fractured installed instances; placeholder inherits the removed instance side.
- `D2-B side-first`: choose a legal side, then choose uniformly within that side.
- `D2-C unknown server / explicit project policy`: use D2-A for project-model simplicity while leaving server truth open.

## D3 — exclusive composition

- `D3-A guaranteed-exclusive`: reserve at least one compatible exclusive Desecrated offer, then fill remaining slots from the general legal pool.
- `D3-B shared-mixture`: draw every offer from one weighted ordinary-plus-exclusive pool with no guarantee.
- `D3-C staged-mixture`: first draw offer category composition, then draw rows inside each category.

## D4 — offer sampling

- `D4-A prepared sequential model`: tier-row weighting; sequential weighted draws without replacement; after each draw block its family/groups; display positions are presentation-only.
- `D4-B family-first model`: draw family/type before tier row.
- `D4-C independent-with-rejection`: draw independently and reject duplicates/conflicts until the set is complete.
- `D4-D data-first`: defer runtime until a structured dataset distinguishes the candidate models.

## D5 — incomplete compatible set

- `D5-A atomic fail-closed`: no-transition/no-consumption; original placeholder and state unchanged.
- `D5-B reduced offer set`: present fewer than the normal number of offers.
- `D5-C fallback relaxation`: relax MML or compatibility until a complete set exists.

D5-A is safest for simulator integrity, but still requires explicit User approval because sources do not reveal the server edge.
