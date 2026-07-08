# P2C - Open Blockers

Standing blockers remain open unless explicitly closed by a separate gate:

- Source/provenance closure.
- MML closure.
- PD-013 closure.
- Public numeric release.
- New executable mechanics beyond accepted ordinary_add and accepted base Annulment.
- Fractured-mod invariant changes.
- Optimizer / advice / ranking / EV-as-decision.
- Server-truth framing.

## Clarification after Layer A acceptance

GitHub Layer A import fidelity is no longer the blocker. The repo baseline import was accepted and pinned on 2026-07-08 as a project-model GitHub baseline after byte verification against the actual local origin working tree.

This does not close the broader SOURCE/PROVENANCE blocker. It only closes the GitHub migration/import-fidelity question.

M26-M30 operation-mechanics blueprint is currently context/open, not accepted source.

## Clarification after M33 acceptance

Full M33 oracle-convergence validation is accepted only for the accepted `ordinary_add` scope.

M33 acceptance does not close:

- Source/provenance closure.
- MML closure.
- PD-013 closure.
- Public numeric release.
- Future multi-seed convergence-rate validation.
- Future sequence / multi-step validation.
- Future operation-expansion validation.

## Clarification after M34-A acceptance

M34-A multi-seed hardening is accepted only for single-step accepted `ordinary_add`.

M34-A acceptance does not close:

- M34-B.
- Full M34.
- Multi-step / sequence validation.
- Source/provenance closure.
- MML closure.
- PD-013 closure.
- Public numeric release.
- Operation expansion beyond accepted `ordinary_add`.

## Clarification after operation inventory reconciliation

The operation inventory/admission reconciliation is accepted as a foundation finding: `active_in_current_simulation` is catalog/project-scope metadata and must not be treated as runtime execution authority.

This does not close:

- Source/provenance closure.
- MML closure.
- PD-013 closure.
- Public numeric release.
- Additional executable operation admission.
- Heterogeneous operation chains.

## Clarification after runtime admission metadata floor

`runtime_admission_status` is now the accepted field for separating operation catalog readiness from executable runtime admission. `active_in_current_simulation` must not be treated as executable runtime authorization.

This does not close:

- Source/provenance closure.
- MML closure.
- PD-013 closure.
- Public numeric release.
- Additional executable operation admission.
- Heterogeneous operation chains.
- Annulment variants or omens.

## Clarification after M36 design acceptance

M36 heterogeneous-chain design is accepted as design-only. It does not open M36-A implementation by itself.

This does not close:

- Source/provenance closure.
- MML closure.
- PD-013 closure.
- Public numeric release.
- Heterogeneous-chain runtime implementation.
- Additional executable operation admission.
- Optimizer / advice / ranking / EV-as-decision.
- Automation / GitHub Actions / supervised auto-run.

## Clarification after Repo Integrity SHA Floor acceptance

The deterministic root `SHA256SUMS.txt` updater and generated-manifest rule are accepted. Local pre-push hook enforcement is authorized as part of the M36-A implementation wave.

This does not close:

- Source/provenance closure.
- MML closure.
- PD-013 closure.
- Public numeric release.
- M36-A runtime acceptance.
- Additional executable operation admission.
- Optimizer / advice / ranking / EV-as-decision.
- GitHub Actions / watcher automation / supervised auto-run.
