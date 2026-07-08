# M36 Design Contract

## Scope

M36 designs heterogeneous-chain execution over accepted executable operations only.

Accepted operation sources:

- accepted engine primitive: `ordinary_add`;
- accepted operation row: base `annulment` with `runtime_admission_status: accepted_executable_runtime`.

Allowed chain examples:

- `ordinary_add -> annulment`
- `annulment -> ordinary_add`
- later bounded fixed sequences using only accepted operations, if separately authorized.

## Non-scope

M36 design does not authorize:

- implementation;
- heterogeneous-chain runtime;
- M36-A execution;
- new executable operations;
- Chaos runtime;
- Essence, Fracture, Desecrate, Jawbone, Reveal runtime;
- Annulment variants or omens;
- Exalted currency-wrapper admission;
- planner / route strategy;
- optimizer / advice / ranking;
- economics / EV / expected attempts;
- public numeric probability release;
- source-truth or server-truth claims;
- SOURCE/PROVENANCE, MML, or PD-013 closure;
- automation or GitHub Actions.

## Required invariant

Runtime permission is never inferred from `active_in_current_simulation`.

An operation may enter a chain only if it is:

1. an accepted engine primitive, or
2. an `operations.yaml` row with `runtime_admission_status: accepted_executable_runtime`.

Everything else fails closed.

## Design target

The design target is a deterministic, auditable chain evaluator contract:

- fixed sequence in;
- branch-expanded terminal distribution out;
- exact path mass where tractable;
- seeded MC comparison where needed;
- replay/debug traces sufficient to reproduce any branch or failure.
