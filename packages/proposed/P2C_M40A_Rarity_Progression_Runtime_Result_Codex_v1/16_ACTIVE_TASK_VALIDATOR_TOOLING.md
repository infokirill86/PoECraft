# ACTIVE_TASK validator tooling companion

The same commit includes a truth-neutral dispatcher guard:

- `tools/validate_active_task.py` rejects missing/invalid frontmatter, duplicate YAML keys/live-state blocks, missing schema-v2 fields, inconsistent status/actor pairs, unsafe or missing referenced paths, and malformed thin-dispatcher state.
- `tools/hooks/pre-push` runs the validator before regenerating/checking `SHA256SUMS.txt`.
- `tests/tools/test_active_task_validator.py` includes positive and negative controls.
- `AGENTS.md` and `CLAUDE.md` now define completion as pushed bytes, remote `main == HEAD`, and commit-pinned ACTIVE_TASK routing to the intended actor.

For `ready_for_claude`, `current_result_path` must exist. `current_review_path` stays empty until an audit file exists; once a non-empty review path is referenced, it must exist. `audited_pending_user_gate` requires an existing review path.

This tooling does not accept M40-A, change crafting mechanics, enable GitHub Actions, or grant agents gate authority.
