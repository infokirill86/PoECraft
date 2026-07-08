# P2C Operation Runtime Admission Metadata Floor - Codex v1

package_id: `P2C_Operation_Runtime_Admission_Metadata_Floor_Codex_v1`
package_type: `METADATA_CORRECTION_RESULT`
status: `proposed_for_claude_audit`

observed_repo_head: `d01cd80c6e21e9f66b001b25e9a4958011c454df`
observed_active_task_sha: `84e4f29a1f25560e0bfca5c09592c19ce59a0118ec89faf64db40c8f45b34878`

## Plain-language summary for Kirill

This floor fixes a naming/control problem in the operation database.

Before this patch, `operations.yaml` had many operations marked `active_in_current_simulation: true`. That could look like "the engine may execute this operation." That reading is unsafe.

After this patch:

- `active_in_current_simulation` means: this operation is part of prepared project-scope/catalog data.
- `runtime_admission_status` means: whether runtime is allowed to execute it.

Only base `annulment` is marked `accepted_executable_runtime` in `operations.yaml`.

Accepted `ordinary_add` remains an engine primitive outside `operations.yaml`.

Everything else remains candidate, reference-only, blocked/out of scope, or disputed. No new operation became executable.

## Important result

The semantic fingerprint changed to:

`acc50b83bd6b94835fe9544266ebf7863c67938957a4aa0408d4262765ee7c25`

This is expected because the semantic projection now excludes active catalog rows that are not runtime-admitted.

## Files changed

- `data/operations.yaml`
- `src/p2c_engine/static_data/checks.py`
- `src/p2c_engine/static_data/semantic.py`
- `tests/static_data/test_foundation_revision_v8_2.py`
- `tests/static_data/test_m7h1_governance_fingerprint.py`
- `manifest/GitHub_Workflow_Protocol.md`
- `CURRENT_STATUS.md`
- `ledger/ACCEPTED_ARTIFACTS.md`
- `ledger/DECISIONS.md`
- `ledger/OPEN_BLOCKERS.md`
- `work/active/ACTIVE_TASK.md`
- `SHA256SUMS.txt`

## Not changed

- no runtime operation implementation added;
- no Chaos/Essence/Fracture/Desecrate/Jawbone/Reveal runtime;
- no heterogeneous chains;
- no optimizer/economics/advice;
- no public numeric release;
- no SOURCE/PROVENANCE, MML, or PD-013 closure.
