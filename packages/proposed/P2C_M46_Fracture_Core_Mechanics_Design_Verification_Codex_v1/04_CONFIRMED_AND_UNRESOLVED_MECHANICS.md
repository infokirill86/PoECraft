# Confirmed and Unresolved Mechanics

## Proposed clean-core contract

Preconditions:

- item class is `quarterstaff`;
- rarity is `rare`;
- installed explicit modifier instance count is at least four;
- fractured modifier count is zero;
- there is no unrevealed Desecrated placeholder;
- there is no installed modifier with `desecrated: true`;
- every installed modifier resolves through the canonical modifier index.

Candidate pool:

- all canonical installed non-Desecrated explicit modifier instances;
- ordinary and `crafted: true` instances are included;
- no side-first selection and no generation-weight weighting;
- selection is uniform over instance identities.

Commit:

- set `fractured: true` only on the selected instance;
- preserve mod ID, side, crafted flag, values represented by the canonical row, rarity, item level, item class, and every unselected instance;
- consume only on a successful transition.

Failure:

- return explicit no-transition/no-consumption;
- preserve the original state exactly;
- provide a stable diagnostic category.

## Unresolved and excluded

| Question | M46 status |
|---|---|
| Revealed Desecrated target eligibility | disputed; excluded from clean core |
| Unrevealed placeholder count/eligibility | excluded from clean core |
| Jawbone/Reveal interaction | separately gated |
| PD-013 closure | forbidden |
| New Omen control over Fracture | not designed or admitted |
| Multiple fractures | forbidden by precondition and current item wording |
| Non-quarterstaff item classes | mechanically general in the game wording, but outside the first implementation floor |
| Crafted-capacity after fracturing a crafted modifier | remains source-open; fracturing preserves the existing crafted flag and changes no capacity policy |
