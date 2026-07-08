# Claude C1-C5 Incorporation

## C1 - tighter status enum

Implemented.

The schema uses six statuses only:

- `awaiting_user_gate`
- `ready_for_codex`
- `ready_for_claude`
- `audited_pending_user_gate`
- `blocked_for_human`
- `accepted_closed`

No intermediate "agent is working" states were added.

## C2 - prune mandatory field set

Implemented.

The schema uses the mandatory field set from the user gate. Optional draft fields such as `phase`, `milestone`, `builder`, `auditor`, `required_input_paths`, and `required_output_paths` were not added to `ACTIVE_TASK.md`.

## C3 - standing boundaries in manifest

Implemented.

Standing boundaries were added to `manifest/GitHub_Workflow_Protocol.md`.

`ACTIVE_TASK.md` now contains:

```yaml
standing_boundaries_ref: "manifest/GitHub_Workflow_Protocol.md#standing-boundaries-for-active-task-dispatcher"
standing_boundaries_apply: true
```

Task-specific forbidden actions remain in `ACTIVE_TASK.md`.

## C4 - read receipts in packages/reviews

Implemented.

`GitHub_Workflow_Protocol.md` now requires every Codex result package and Claude review to include:

- `observed_repo_head`
- `observed_active_task_sha`

This package includes both in `00_README_FIRST.md`.

## C5 - validator proposed, not built

Implemented.

`GitHub_Workflow_Protocol.md` includes a deferred validator section.

No code or tests were added.
