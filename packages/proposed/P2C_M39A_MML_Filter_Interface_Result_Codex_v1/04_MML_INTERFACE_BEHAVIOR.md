# MML interface behavior

## Accepted in M39-A

| Request | Result |
|---|---|
| `ordinary_add` with `mml: null` | accepted ordinary_add, unchanged |
| `ordinary_add` with positive integer `mml` | accepted ordinary_add with explicit MML filter |

## Rejected in M39-A

| Request | Rejection reason |
|---|---|
| `ordinary_add` with `mml: 0` | invalid MML threshold |
| `ordinary_add` with negative/non-integer/bool MML | invalid MML threshold |
| base `chaos` with explicit MML | MML filters are admitted only for explicit ordinary_add in M39-A |
| `greater_chaos` with or without MML | not executable-admitted by `runtime_admission_status` |
| `chaos` with `variant_id: greater` | variants are not executable-admitted |
| any active Omen/modifier layer | modifier layers are not executable-admitted |

## Add-pool narrowing proof

The test fixture creates two modifier families:

- one family has a high-level row above MML;
- one family has no row above MML, so the existing strongest-family fallback applies.

The resolver compiles `ordinary_add + mml: 50`, then the shared ordinary add pool builder narrows the candidate pool to the MML-filtered/fallback rows.

This proves the resolver can carry MML into the accepted shared add-pool path without admitting Greater/Perfect currency runtime.

