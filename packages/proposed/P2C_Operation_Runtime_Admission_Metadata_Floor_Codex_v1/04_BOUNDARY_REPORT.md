# Boundary Report

## Held boundaries

This floor did not:

- add new executable operation runtime;
- implement Chaos, Essence, Fracture, Desecrate, Jawbone, Reveal, or Annulment variants/omens;
- implement heterogeneous operation chains;
- add optimizer/advice/ranking/economics/EV;
- release public numeric probabilities;
- claim PoE2 server truth;
- close SOURCE/PROVENANCE, MML, or PD-013;
- enable automation or GitHub Actions.

## What changed and why it is allowed

This floor changed metadata and validation around the operation catalog:

- `data/operations.yaml` now labels each row with `runtime_admission_status`.
- validators require the field and fail on invalid/missing status.
- semantic projection now uses explicit runtime admission instead of active catalog status.

This is within the authorized metadata-correction scope.

## What remains proposed

This result package is proposed pending Claude audit and ChatGPT/User acceptance.

The following remain closed:

- M36 heterogeneous chains;
- any additional executable operation;
- Annulment variants/omens;
- source/provenance closure;
- MML closure;
- PD-013 closure;
- public numeric release;
- optimizer/economics/advice.

## Main risk for Claude to check

The main audit question is whether filtering runtime semantic projection by `runtime_admission_status: accepted_executable_runtime` is the correct mechanical interpretation of the accepted reconciliation.

Codex position: yes. It is the only effective way to ensure `active_in_current_simulation` cannot silently authorize runtime semantics.
