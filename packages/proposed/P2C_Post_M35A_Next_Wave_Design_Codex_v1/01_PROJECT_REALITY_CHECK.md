# Project Reality Check

## 1. What can the simulator actually do today?

In simple terms, P2C can now simulate two accepted project-model operations:

- `ordinary_add`: add one ordinary modifier through the accepted shared pool/legality/weight kernel;
- base `annulment`: remove one removable non-fractured installed modifier instance uniformly.

The simulator has:

- exact/oracle enumeration for narrow accepted lanes;
- seeded MC sampling;
- deterministic replay;
- validation against exact/oracle behavior;
- protection for the fixed fractured modifier;
- no-transition behavior for empty legal pools;
- package/audit workflow discipline.

## 2. What is still missing before it becomes useful as a real crafting simulator?

Major missing pieces:

- heterogeneous operation chains, e.g. add then remove, remove then add;
- a shared chain evaluator that can sequence accepted operations without turning into a planner;
- exact-vs-MC validation for mixed accepted-operation chains;
- replay/debug traces across mixed operation steps;
- target success over multi-step states;
- user-facing safe outputs;
- later operation admission for more mechanics;
- optimizer/economics/advice, which remains deliberately last.

## 3. Are we ready for heterogeneous chains?

Yes, for design only.

Implementation should still be gated, but the design frontier is ready because two accepted executable operations exist and both are project-model accepted:

- `ordinary_add` mutates by adding an installed modifier;
- base `annulment` mutates by removing a removable installed modifier.

The next design question is no longer "can one operation work?" but "can accepted operations compose safely?"

## 4. Should we add or harden another operation first?

Not as the default next move.

Adding another operation before mixed-chain design risks creating isolated handlers with no accepted sequence model. Hardening only the two individual operations risks infrastructure drift. The highest-value next step is a design-only chain boundary over already accepted operations.

