# Current Capability Map

## Accepted executable operations

| Capability | Current status |
|---|---|
| `ordinary_add` runtime | Accepted |
| `ordinary_add` exact/oracle | Accepted for scoped lanes |
| `ordinary_add` seeded MC | Accepted |
| Two-step homogeneous `ordinary_add` sequence | Accepted through M34-B1 |
| Base `annulment` runtime | Accepted through M35-A |
| Base `annulment` exact/oracle | Accepted through M35-A |
| Base `annulment` seeded MC / replay | Accepted through M35-A |

## Shared foundations

| Foundation | Current status |
|---|---|
| Static data loader and validation | Accepted project-model baseline |
| Ordinary add pool builder | Accepted shared kernel |
| Removal pool builder | Accepted shared kernel for M35-A |
| Exact rational oracle pattern | Accepted |
| Seeded MC harness pattern | Accepted |
| Replay/trace discipline | Accepted for existing lanes |
| ACTIVE_TASK schema v2 | Accepted workflow hygiene |

## What the runtime can express today

The runtime can evaluate isolated operation behavior and a homogeneous two-step accepted-`ordinary_add` sequence.

It does not yet have an accepted heterogeneous sequence design connecting `ordinary_add` and base `annulment`.

