---
schema_version: "2.0"
repo_head_at_last_update: "9e1019ddd0a03745e07db8b38ada10288fe5caf3"
updated_at_utc: "2026-07-08T14:26:08Z"

status: "audited_pending_user_gate"
next_actor: "chatgpt_user"
active_task_id: "ACTIVE_TASK_SCHEMA_V2"

allowed_next_action: "chatgpt_user_gate_decision_on_active_task_schema_v2"
forbidden_next_actions:
  - "start_m34b"
  - "design_m34b"
  - "implement_m34b"
  - "multi_step_sequence_validation"
  - "change_code_tests_mechanics"
  - "add_new_mailbox_or_write_location"
  - "enable_supervised_auto_run"
  - "enable_github_actions"
  - "accept_schema_without_chatgpt_user_gate"

standing_boundaries_ref: "manifest/GitHub_Workflow_Protocol.md#standing-boundaries-for-active-task-dispatcher"
standing_boundaries_apply: true

current_result_path: "packages/proposed/P2C_ACTIVE_TASK_SCHEMA_V2_Result_Codex_v1/"
current_review_path: "reviews/P2C_ACTIVE_TASK_SCHEMA_V2_Audit_Claude_v1.md"

acceptance_authority: "chatgpt_user"

automation:
  mode: "manual"
  enabled: false
  max_handoffs: 0
  current_handoff_count: 0
  human_gate_required: true
  allowed_next_actors:
    - "codex"
    - "claude"
  stop_on:
    - "NO_GO"
    - "GO_WITH_CHANGES_REQUIRES_DESIGN_DECISION"
    - "scope_expansion"
    - "missing_required_bytes"
    - "sha_mismatch"
    - "test_failure"
    - "dependency_or_provenance_uncertainty"
    - "builder_auditor_conflict"
    - "accepted_truth_update_needed"
    - "milestone_transition"
    - "max_handoffs_reached"

freshness_rules:
  must_verify_repo_head: true
  must_record_visible_head: true
  stop_if_head_unverified: true
  stop_if_raw_cache_suspected: true
  prefer_commit_pinned_urls_for_recent_updates: true

stop_conditions:
  - "Stop if current repo HEAD cannot be verified."
  - "Stop if ACTIVE_TASK.md frontmatter is invalid or missing mandatory fields."
  - "Stop if status and next_actor are inconsistent."
  - "Stop if accepted/proposed/current state is ambiguous."
  - "Stop if standing boundaries are missing or unclear."
  - "Stop if this task requires code, tests, mechanics, data, probabilities, or operation-behavior changes."
  - "Stop if M34-B, sequence validation, or multi-step validation is started or designed."
  - "Stop if automation or GitHub Actions enablement is attempted."
---

# P2C Active Task

Current live task: `ACTIVE_TASK_SCHEMA_V2` workflow hygiene.

Next actor: ChatGPT/User (gate decision).

Allowed next action: decide acceptance of the SCHEMA_V2 result. Claude audit verdict: GO
(`reviews/P2C_ACTIVE_TASK_SCHEMA_V2_Audit_Claude_v1.md`).

This dispatcher is routing/control only. It is not evidence, not a ledger, and not accepted truth.
