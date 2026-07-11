# Proposed M46-A Implementation Boundary

## One broad coherent batch

M46-A should implement exactly one base `fracturing_orb` executor for clean Rare quarterstaff states.

Required components:

- change only the `fracturing_orb` runtime admission after a separate implementation gate;
- compile through the accepted single-operation resolver;
- register one explicit accepted executor in the M43-A registry;
- reuse canonical `ModifierInstance` identity and canonical-state hashing;
- use one shared candidate builder for direct, resolver, exact, MC, replay, and sequence execution;
- keep all special/disputed states fail-closed.

Required tests/evidence:

- Rare and four-plus preconditions;
- fewer-than-four, wrong-rarity, existing-fracture, unknown-mod, and Desecrated-state failures;
- uniform exact instance paths and exact mass conservation;
- duplicate-instance terminal aggregation;
- prefix/suffix combined-pool proof;
- ordinary and crafted candidate coverage;
- one-bit atomic mutation and rollback/no-consumption;
- fractured immutability through accepted Annulment, Chaos, Perfect Essence, and capacity logic;
- deterministic seeded MC/replay and negative-control diagnostics;
- direct/resolver/M43-A one-step parity;
- bounded accepted-operation sequence compatibility without expanding route semantics;
- full regression and semantic-fingerprint delta limited to the Fracture admission surface.

## Explicit non-goals

No Desecrated/Revealed/Jawbone/Reveal behavior, PD-013 decision, Omen, multi-fracture, planner, optimizer, economics/advice, public numeric release, automation, or boundary closure belongs in M46-A.
