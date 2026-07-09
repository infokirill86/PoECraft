# Participant Critique

## Did the previous M37 design silently assume mechanics?

Yes.

The previous M37 design treated the remove stage like the accepted Annulment removal pool unless a later Whittling/Omen gate was opened. That direction is probably correct for base Chaos after source checking, but it was not safe to leave implicit.

The design should have said plainly:

- base Chaos-like removal is source-checked as "random modifier" behavior;
- Whittling is a separate Omen modifier over Chaos behavior;
- "random" is interpreted by the project model as uniform over eligible installed modifier instances unless later source evidence or in-game testing disproves it.

Without that explicit verification, exact/MC calculations could be internally rigorous while modeling the wrong operation.

## Is this verification task the right next move?

Yes.

M37-A must not start until the base removal selection rule is pinned. The project now has enough engine structure to compose remove-plus-add, but composition is only useful if the source mechanics are correct.

This is a foundation correctness checkpoint, not an implementation delay for its own sake.

## Corrected boundary

The safer boundary is:

- M37 mechanics verification now;
- Claude audit of this verification;
- ChatGPT/User decision on the project-model rule;
- then a corrected M37 design acceptance or patch;
- only then M37-A base Chaos-like runtime, if explicitly authorized.

M37-A should remain base `chaos` only unless later gates explicitly add Whittling, side Omens, Greater/Perfect MML, or variants.

