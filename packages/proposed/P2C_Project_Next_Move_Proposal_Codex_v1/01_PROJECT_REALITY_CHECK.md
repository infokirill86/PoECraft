# Project Reality Check

## 1. What are we actually building?

P2C is a project-model Path of Exile 2 crafting simulator for a narrow first domain:

- physical quarterstaff;
- fixed fractured critical suffix;
- item state transitions;
- stochastic crafting operations;
- exact rational oracle for narrow lanes;
- seeded Monte Carlo as the scalable runtime direction;
- optimizer/economics/advice later, separately gated.

It is not intended to remain a test harness for one add operation.

## 2. What is already accepted and implemented?

Accepted project state includes:

- GitHub Layer A runtime/data/config/schema/tool baseline;
- accepted `ordinary_add` executable runtime;
- shared legality/pool/weight kernel for ordinary add;
- static data loading, normalization, validation, and fingerprints;
- removal and reveal pool builders as kernel support;
- seeded MC harness for accepted `ordinary_add`;
- exact/oracle comparison for accepted `ordinary_add`;
- M34-A multi-seed single-step hardening;
- M34-B1 two-step accepted-ordinary-add sequence hardening.

## 3. What can the simulator actually do today?

Today the simulator can:

- load project-model static data;
- validate foundation/M4 invariants;
- build ordinary add pools;
- build removal pools;
- build reveal base pools;
- execute accepted `ordinary_add` through exact/oracle and seeded MC paths;
- execute exactly two sequential accepted `ordinary_add` steps as a hardening fixture;
- produce deterministic replay/debug traces for the accepted ordinary-add MC path.

## 4. What major simulator capabilities are still missing?

Still missing:

- executable runtime admission for non-add operations;
- operation handlers for removal-only mechanics such as Annulment;
- operation handlers for remove-then-add mechanics such as Chaos;
- operation handlers for guaranteed crafted mods such as Perfect Essence;
- operation handlers for placeholder mechanics such as Jawbone and Reveal;
- a generalized operation execution interface across accepted operations;
- plan/sequence execution over heterogeneous real operations;
- target success aggregation over real operation results;
- user-facing route evaluation;
- costs/economics/EV;
- optimizer/advice/ranking.

## 5. Are we drifting?

There is a real drift risk.

M31-M34 were valuable because they proved the MC/exact foundation over accepted `ordinary_add`. After M34-B1, another pure `ordinary_add` hardening wave is lower value unless it directly supports operation admission.

The project should pivot from “more confidence in ordinary add” to “controlled admission of the first additional real operation.”

## 6. Is more ordinary-add hardening still the highest-value next move?

No.

More ordinary-add hardening is useful only as support work. It is not the highest-value project move because the simulator still cannot execute most real crafting mechanics.

The highest-value safe move is to design the operation-admission path, then admit the first new operation under that framework.
