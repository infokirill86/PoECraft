# Risk Register

| Risk ID | Risk | Severity | Mitigation |
|---|---|---:|---|
| R-M34B-001 | M34-B accidentally becomes a generic sequence engine. | High | Pin M34-B1 to exactly two accepted `ordinary_add` steps. |
| R-M34B-002 | Step 1 pool is built from the original state instead of the branch state. | High | Require step linkage and branch-state pool digest evidence. |
| R-M34B-003 | MC and exact/oracle comparison use different kernels. | High | Require shared accepted pool/transition kernel for both paths. |
| R-M34B-004 | Terminal comparison treats ordered path text as terminal identity. | Medium | Use canonical final item state identity for terminal aggregation. |
| R-M34B-005 | Diagnostics identify only the run, not the failing step. | Medium | Require fixture id, sequence id, seed, run id, sample tier, step index, pool digest, and state hashes. |
| R-M34B-006 | Public reports leak probability values. | High | Keep public docs numeric-probability-free and require leak scan. |
| R-M34B-007 | Fixture becomes too large for exact/oracle audit. | Medium | Set ceilings and stop if exceeded. |
| R-M34B-008 | Negative-control path is omitted, so the suite may not prove it can fail. | Medium | Require explicitly marked negative-control failure proof. |
| R-M34B-009 | New mechanics slip in under sequence terminology. | High | Accepted inputs allow `ordinary_add` only; all other operation families are forbidden. |
| R-M34B-010 | M34-B acceptance is implied by design package existence. | Medium | Package is proposed only; ChatGPT/User gate remains required. |

## Residual risk

The largest residual risk is that later implementation may need small runtime support for sequence traces. That support is allowed only if a future gate authorizes implementation and the support does not change mechanics.
