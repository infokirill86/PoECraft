# Final ACTIVE_TASK Schema V2

## Mandatory fields

- `schema_version`
- `repo_head_at_last_update`
- `updated_at_utc`
- `status`
- `next_actor`
- `active_task_id`
- `allowed_next_action`
- `forbidden_next_actions`
- `standing_boundaries_ref`
- `standing_boundaries_apply`
- `current_result_path`
- `current_review_path`
- `acceptance_authority`
- `automation`
- `freshness_rules`
- `stop_conditions`

## Allowed status values

- `awaiting_user_gate`
- `ready_for_codex`
- `ready_for_claude`
- `audited_pending_user_gate`
- `blocked_for_human`
- `accepted_closed`

## Allowed next_actor values

- `chatgpt_user`
- `codex`
- `claude`
- `blocked`

## Consistency rules

- `awaiting_user_gate` requires `next_actor: chatgpt_user`.
- `ready_for_codex` requires `next_actor: codex`.
- `ready_for_claude` requires `next_actor: claude`.
- `audited_pending_user_gate` requires `next_actor: chatgpt_user`.
- `blocked_for_human` requires `next_actor: chatgpt_user` or `next_actor: blocked`.
- `accepted_closed` requires `next_actor: chatgpt_user` or `next_actor: blocked`.
- `automation.enabled: false` requires `automation.max_handoffs: 0`.

## Human summary rule

A short human summary may follow the YAML frontmatter.

It must not introduce state not present in the machine block.

## Accepted-truth rule

`ACTIVE_TASK.md` may reference accepted truth, packages, and reviews.

It must not itself establish accepted truth.
