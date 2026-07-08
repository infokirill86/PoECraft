# Accepted and Forbidden Inputs

## Accepted inputs

M34-B1 may use:

- accepted `ordinary_add` operation semantics;
- accepted ordinary-add legality and pool-building kernel;
- accepted weighted sampling kernel;
- accepted exact/oracle branch layer where tractable;
- accepted `StaticGameData` loading path already present in the GitHub baseline;
- accepted item-state and static-modifier domain objects;
- fake fixtures or small project-model fixtures when explicitly labeled;
- real project data only if the active gate explicitly authorizes it for the M34-B1 implementation floor.

## Required input labels

Every fixture or dataset used by later M34-B1 implementation should identify:

- fixture id;
- source type: fake fixture, project-model fixture, or real project data;
- operation sequence id;
- step count;
- operation ids;
- source fingerprint when real/static project data is used;
- semantic fingerprint when real/static project data is used.

## Forbidden inputs

M34-B1 must not use:

- operations other than accepted `ordinary_add`;
- Reveal mechanics;
- Lich mechanics;
- Abyssal mechanics;
- Whittling mechanics;
- optimizer-generated plans;
- economics, EV, cost, budget, or expected-attempt inputs;
- source-capture or live-fetch inputs;
- public numeric probability release files;
- accepted-truth updates as input authority.

## Fail-closed rule

If a later implementation cannot prove that all executed steps are accepted `ordinary_add` steps, it must stop instead of running a broader sequence.
