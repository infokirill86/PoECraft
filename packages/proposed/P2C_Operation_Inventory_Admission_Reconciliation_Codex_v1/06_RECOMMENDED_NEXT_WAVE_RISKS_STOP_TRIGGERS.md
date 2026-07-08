# Recommended Next Wave, Risks, and Stop Triggers

## Recommended next wave after Claude audit

Recommended immediate next step if Claude returns GO or GO WITH CHANGES:

1. Create a small metadata-correction floor.
2. Add `runtime_admission_status` or equivalent to `data/operations.yaml`.
3. Add or update validation so runtime executability cannot be inferred from `active_in_current_simulation`.
4. Keep all new operation execution closed.

Only after that should the project return to M36 heterogeneous chain design over already accepted operations:

- accepted `ordinary_add`;
- accepted base Annulment.

## Why this should be before heterogeneous chains

Heterogeneous chains depend on a clear operation registry. If the registry confuses "catalog active" with "runtime accepted," then a chain evaluator could accidentally admit Chaos, Perfect Essence, Jawbone, Reveal, or other unaccepted mechanics.

The next safe value is therefore not more ordinary-add hardening and not immediate M36 implementation. It is a small operation-admission metadata correction that makes future runtime gates mechanically legible.

## What is safe to batch

Safe to batch in the metadata-correction floor:

- add the status field;
- classify all current operation rows;
- add schema/validation checks for the new field;
- document the distinction between project-scope catalog rows and accepted executable runtime;
- add tests that active catalog rows cannot be treated as executable merely because they are active.

This is reconstructible, automatically testable, and truth-neutral if it does not accept new operations.

## What must remain gated

Separate gates are required for:

- accepting any additional executable operation;
- M36 heterogeneous chain implementation;
- Annulment variants/omens;
- Chaos, Essence, Fracture, Desecrate, Jawbone, Reveal runtime;
- source/provenance conflict resolution;
- MML closure;
- PD-013 closure;
- public numeric release;
- optimizer/economics/advice/ranking;
- automation or GitHub Actions.

## Risks

| Risk | Impact | Mitigation |
|---|---|---|
| `active_in_current_simulation` is treated as executable authorization | Unaccepted operations may enter runtime paths | Add explicit `runtime_admission_status` and fail-closed validation |
| Overcorrecting by deleting active catalog rows | Loses prepared project data and context | Keep active flag as project-scope metadata; add a separate runtime status |
| Building a broad generalized operation algebra | Infrastructure drift and complexity | Keep the model lean and admission-driven |
| Moving directly to M36 chains | Chain evaluator may inherit ambiguous operation status | Complete metadata reconciliation first |
| Treating project-model evidence as server truth | Overclaims correctness | Preserve labels and blockers |

## Stop triggers for the next floor

Stop if:

- a data change would imply accepting a new executable operation;
- validators would require runtime implementation of unaccepted operations;
- source/provenance conflict resolution is needed;
- MML, PD-013, or server-truth closure enters scope;
- public numeric output or optimizer/advice enters scope;
- operation status cannot be classified without user decision.
