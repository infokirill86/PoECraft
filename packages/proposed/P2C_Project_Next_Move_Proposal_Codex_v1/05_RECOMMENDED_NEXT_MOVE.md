# Recommended Next Move

## Recommendation

Start a design-only wave:

```text
M35 Operation Admission Framework and Annulment Candidate Design
```

## Why this is the right next move

P2C now has enough confidence in accepted `ordinary_add` MC/exact behavior to stop hardening only that operation.

The project needs to admit new executable operations in a controlled way. Otherwise, it remains a strong test harness but not a practical crafting simulator.

## Why Annulment is the best first candidate

Annulment is a good first non-add operation because:

- it is removal-only;
- it uses the existing `build_removal_pool` kernel support;
- it exercises a genuinely new state transition: removing an installed modifier;
- it avoids remove-then-add composition complexity;
- it avoids crafted guaranteed-mod semantics;
- it avoids placeholder/reveal/Lich/PD-013 complexity;
- it can be tested with small exact fixtures;
- it is route-relevant for crafting simulation.

## Recommended M35 design scope

M35 design should define:

- operation-admission criteria;
- required source/project-policy labels;
- required exact/oracle proof shape;
- required seeded MC proof shape if stochastic;
- required replay/trace fields;
- required failure/no-transition behavior;
- required negative controls;
- required boundary reports;
- first operation candidate: Annulment;
- why other operations are deferred.

## What M35 should not do yet

M35 design should not:

- implement Annulment;
- accept Annulment as executable;
- add new operation code;
- close source/provenance, MML, or PD-013;
- release numeric public values;
- add optimizer/economics/advice;
- enable automation.

## Implementation after design

If the M35 design passes Claude audit and ChatGPT/User authorization, the first implementation floor should be:

```text
M35-A Annulment Runtime Admission
```

That later implementation should be narrow and test-heavy.
