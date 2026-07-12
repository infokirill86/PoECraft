# Desecrated State Contract

## Unrevealed state

Use the existing dedicated `DesecratedPlaceholder`, not a fake modifier ID. It must:

- store its fixed side and source Jawbone context;
- consume one ordinary explicit slot on that side;
- contribute to total explicit-count checks where the later accepted operation explicitly says it counts;
- remain distinct from an installed mod for family/group, generation weight, and removal-pool purposes unless a later gate says otherwise;
- participate in canonical state hashing and deterministic replay;
- enforce the normal single-Desecrated limit.

## Revealed state

Reveal removes the placeholder and installs one canonical `ModifierInstance` with `desecrated: true`. The static modifier index remains the sole authority for side, family, groups, level, tags, and weight. The revealed modifier:

- consumes ordinary side capacity;
- blocks family/group conflicts;
- participates in canonical terminal identity and replay;
- is not crafted merely because it is Desecrated;
- is removable only under separately accepted operation rules;
- cannot gain `fractured: true` until PD-013 is explicitly decided.

The existing domain representation is sufficient; no new generalized state algebra is needed.
