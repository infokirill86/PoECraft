---
schema_version: "2.0"
repo_head_at_last_update: "587c9963a62807c0419bfb9ff6e2faa92d9e989f"
updated_at_utc: "2026-07-08T14:31:54Z"

status: "awaiting_user_gate"
next_actor: "chatgpt_user"
active_task_id: "M34B_AUTHORIZATION_GATE"

allowed_next_action: "chatgpt_user_decide_whether_to_authorize_m34b_design_or_choose_another_task"
forbidden_next_actions:
  - "start_m34b_without_explicit_later_gate"
  - "design_m34b_without_explicit_later_gate"
  - "implement_m34b_without_explicit_later_gate"
  - "multi_step_sequence_validation_without_explicit_later_gate"
  - "change_code_tests_mechanics_without_explicit_later_gate"
  - "enable_supervised_auto_run"
  - "enable_github_actions"
  - "update_accepted_truth_without_explicit_later_gate"
  - "release_public_numeric_probabilities"

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
  - "Stop if this task would require code, tests, mechanics, data, probabilities, or operation-behavior changes."
  - "Stop if M34-B, sequence validation, or multi-step validation is started or designed without explicit later authorization."
  - "Stop if automation or GitHub Actions enablement is attempted."
---

# P2C Active Task

Current state: `ACTIVE_TASK_SCHEMA_V2` is accepted as workflow hygiene.

Next actor: ChatGPT/User.

Allowed next action: decide whether to authorize M34-B design or choose another task.

M34-B and full M34 remain closed until an explicit later gate.
