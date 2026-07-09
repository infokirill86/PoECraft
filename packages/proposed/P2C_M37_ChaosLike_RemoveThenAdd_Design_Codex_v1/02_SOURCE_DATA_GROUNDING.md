# Source / Data Grounding

## Files inspected

- `data/operations.yaml`
- `data/sources.yaml`
- `data/mechanics_evidence.yaml`
- `CURRENT_STATUS.md`
- accepted ledgers
- standing workflow boundaries

## Current operation metadata

`data/operations.yaml` contains three Chaos-like rows:

| operation_id | group | active_in_current_simulation | runtime_admission_status | add mml |
|---|---|---|---|---|
| `chaos` | `chaos` | true | `admission_candidate` | null |
| `greater_chaos` | `chaos` | true | `admission_candidate` | 35 |
| `perfect_chaos` | `chaos` | true | `admission_candidate` | 50 |

These rows are catalog/source-model candidates only. They are not accepted executable runtime.

`active_in_current_simulation: true` means the row is in prepared project-scope/catalog data. It does not authorize runtime execution.

Runtime executability must come from `runtime_admission_status: accepted_executable_runtime`, and the Chaos-like rows do not currently have that status.

## Relevant operation-row semantics

The Chaos-like rows specify:

- rare item input;
- atomic operation;
- remove one installed modifier instance;
- exclude fractured modifiers from removal;
- rebuild the add pool after removal on the branch-copy;
- add one ordinary weighted modifier;
- no-transition/no-consumption on failed precondition.

## Source policy

`data/sources.yaml` states that PoE2DB plus Craft of Exile agreement is accepted as project-model truth, not server truth.

`data/mechanics_evidence.yaml` states:

- MML applies to greater/perfect chaos addition as a user-approved project rule;
- Whittling has a project-adopted inference, but tie behavior is not fully published.

M37 must not close SOURCE/PROVENANCE, MML, or PD-013.

