# Risks and Deferred Items

## Risks

| Risk | Mitigation |
|---|---|
| Accidentally treating Whittling as base Chaos | M37-A code has no Whittling selector; tests and docs keep Whittling gated. |
| Accidentally using side-first add selection | M37-A calls the accepted combined `build_ordinary_add_pool`; test verifies weight behavior. |
| Partial remove-only state after add failure | Exact and MC paths return original state on post-removal add-pool failure. |
| Fractured modifier removal | Shared removal pool excludes fractured modifiers; negative control proves leaked fractured candidate fails. |
| Chaos row self-accepted by code commit | Status/ledger/package say M37-A is proposed pending Claude/User acceptance. |

## Deferred

- Whittling / lowest-modifier-level runtime.
- Side/desecrated Omen layers.
- Greater/Perfect Chaos MML modes.
- Chaos in longer routes beyond already accepted M36-A scope.
- Public numeric probability release.
- Optimizer/economics/advice.
- Server-truth closure.
- SOURCE/PROVENANCE, MML, PD-013 closure.

## Required next step

Claude audit must review this proposed implementation. ChatGPT/User must decide whether to accept M37-A after audit.

