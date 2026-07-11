# Files Changed and Removed

## Routing and first-read documents

- `AGENTS.md`, `CLAUDE.md`: verified HEAD and live `ACTIVE_TASK.md` now precede volatile orientation/status prose.
- `README.md`, `START_HERE.md`, `manifest/Agent_Role_Pack.md`: canonical entry order and truth ownership clarified.
- `manifest/GitHub_Workflow_Protocol.md`: reduced to stable workflow rules; time-sensitive project history removed.
- `manifest/Operating_Manifest_v4.md`, `ledger/OPEN_BLOCKERS.md`: stale runtime/invariant wording replaced by canonical references.
- `CURRENT_STATUS.md`: records the accepted audit and proposed cleanup state.
- `ledger/ACCEPTED_ARTIFACTS.md`, `ledger/DECISIONS.md`: record acceptance of the audit and authorization of Wave A+B, not acceptance of this result.

## Current-tree removals

- `work/active/LayerA_Source_Bundle_Byte_Verification_Task.md`
- `work/active/M32_A1_A2_Baseline_Hygiene_Task.md`
- `work/active/M32_Seeded_MC_Harness_Task.md`

These were historical task records, not evidence packages. Their committed history remains retrievable through Git. Existing package/review evidence and references were not changed.

## Tooling

- `tools/validate_active_task.py`: requires exactly one tracked path under `work/active/`, specifically `work/active/ACTIVE_TASK.md`.
- `tests/tools/test_active_task_validator.py`: proves an extra tracked sibling fails while an untracked local note does not create a second tracked dispatcher.
