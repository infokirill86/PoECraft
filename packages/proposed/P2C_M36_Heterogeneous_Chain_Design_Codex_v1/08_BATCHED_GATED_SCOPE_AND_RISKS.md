# Batched Scope, Gated Scope, Risks, and Stop Triggers

## What can be batched safely in M36-A

Safe to batch because it is reconstructible, automatically testable, and truth-neutral:

- fixed two-step heterogeneous chain representation;
- admission validation over accepted operations only;
- exact enumeration for small two-step fixtures;
- terminal canonical aggregation;
- seeded MC comparison to exact where tractable;
- replay/debug trace for two-step mixed chains;
- negative controls for unaccepted operations and active catalog rows.

## What remains separately gated

Separate gates are required for:

- M36 implementation authorization;
- chain length greater than 2;
- variable-length route planner;
- any new operation admission;
- Chaos runtime;
- Essence, Fracture, Desecrate, Jawbone, Reveal runtime;
- Annulment variants or omens;
- Exalted currency-wrapper runtime;
- public numeric release;
- optimizer/advice/ranking/economics/EV;
- SOURCE/PROVENANCE, MML, or PD-013 closure;
- automation/GitHub Actions.

## Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Chain layer accidentally admits active catalog rows | Unaccepted operations enter runtime | Require explicit runtime admission status or accepted primitive registry |
| M36 becomes a planner | Scope drift toward optimizer/advice | Fixed sequences only; no route choice |
| Exact enumeration explodes | Slow or incomplete validation | Pin ceilings and stop when exceeded |
| MC hides branch-specific legality errors | False confidence | Exact fixtures plus per-step marginal checks |
| Terminal identity confuses path order with final state | Wrong probability aggregation | Explicit path identity vs terminal identity rule |
| New operation admission sneaks in through chain tests | Mechanics expansion without gate | Negative controls and hard fail on unaccepted operation refs |

## Stop triggers

Stop if:

- implementation becomes required;
- a new executable operation would be admitted;
- a chain references Chaos or any other unaccepted operation as executable;
- public numeric output is requested;
- optimizer/economics/advice enters scope;
- source/provenance conflict requires user resolution;
- SOURCE/PROVENANCE, MML, or PD-013 closure enters scope;
- automation or GitHub Actions enter scope.
