# Claude Audit Request - ACTIVE_TASK_SCHEMA_V2

Please audit this ACTIVE_TASK_SCHEMA_V2 workflow-hygiene result.

## Requested verdict

Return one of:

- GO
- GO WITH CHANGES
- NO-GO

## Audit questions

Check whether:

- `ACTIVE_TASK.md` is now a strict thin dispatcher;
- the machine-readable block is first;
- there is exactly one live state;
- there is one `status`, one `next_actor`, and one `allowed_next_action`;
- old task history was removed;
- human summary does not introduce new state;
- standing boundaries are referenced instead of repeated;
- `GitHub_Workflow_Protocol.md` now carries standing boundaries and read-receipt rules;
- Claude C1-C5 were incorporated;
- automation remains manual and disabled;
- no code/tests/mechanics/data/probability behavior changed;
- M34-B was not started or designed;
- SOURCE/PROVENANCE, MML, and PD-013 remain open;
- this package correctly includes `observed_repo_head` and `observed_active_task_sha`.

## Key files to inspect

- `work/active/ACTIVE_TASK.md`
- `manifest/GitHub_Workflow_Protocol.md`
- `packages/proposed/P2C_ACTIVE_TASK_SCHEMA_V2_Result_Codex_v1/`

## Expected clean outcome

If clean, recommend ChatGPT/User acceptance of ACTIVE_TASK_SCHEMA_V2 as the workflow-hygiene standard.

Do not treat this audit as authorization to start M34-B.
