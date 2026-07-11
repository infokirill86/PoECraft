# Exact, Monte Carlo, Replay, and Acceptance Plan

## Exact/oracle

- Multiply per-step exact rational masses along every path.
- Aggregate by execution-terminal identity.
- Require total terminal mass to sum exactly to one, including explicit early no-transition terminals.
- Require per-step marginal reconciliation for tractable fixtures.
- Use the same accepted operation pools and transition functions as seeded MC.

Proposed M43-A ceilings, pinned before execution:

| Ceiling | Proposed value |
|---|---:|
| Maximum sequence steps | 8 |
| Maximum candidate branches from one pool | 256 |
| Maximum exact paths | 65,536 |
| Maximum exact execution terminals | 65,536 |

If exact ceilings are exceeded, exact execution must stop with a structured ceiling result. It must not silently truncate or renormalize.

## Seeded Monte Carlo

- Fixed seeds: `43001`, `43002`, `43003`.
- Fixed sample tiers: `512`, `2048`, `8192`.
- Reuse the M33/M34 statistical envelope policy rather than inventing a post-result tolerance.
- Compare to exact execution-terminal and per-step marginals where exact fits.
- Where exact does not fit, require deterministic replay plus operation and mass-conservation invariants; do not claim convergence proof from property checks alone.

These are execution-count metadata, not released probability values.

## Replay trace

Every sampled path must record:

- sequence id and semantic fingerprint;
- seed, run id, and sample index;
- step index/id and currency id;
- state hash before and after;
- resolved-operation schema/fingerprint or equivalent digest;
- pool/removal/feasible-pool digest;
- selected transition key;
- no-transition/failure code;
- final execution-terminal key.

Same sequence, static fingerprint, seed, run id, and sample index must replay exactly.

## Required tests for later M43-A

1. One-step parity against every accepted operation-family harness.
2. Three-to-eight-step constructed fixtures covering rarity transition, deterministic Essence, remove, add, and remove-then-add.
3. Branch-specific re-resolution and pool rebuild proof.
4. Exact rational mass conservation and duplicate terminal aggregation.
5. Early no-transition preserves earlier committed state and blocks later steps.
6. Deterministic replay and mutated-trace negative control.
7. Fail-closed unadmitted operation/modifier/unsupported-executor controls.
8. Exact ceiling hard-stop and no silent truncation.
9. Regression suite for all accepted single-operation floors and M36-A.
10. Public-report leak scan: no probability values released.
