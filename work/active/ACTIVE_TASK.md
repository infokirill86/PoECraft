---
schema_version: "2.0"
repo_head_at_last_update: "2bfc98f9a9042bf331422af94e8e033141019002"
updated_at_utc: "2026-07-08T14:48:06Z"

status: "ready_for_claude"
next_actor: "claude"
active_task_id: "M34B_DESIGN"

allowed_next_action: "claude_audit_m34b_design_package"
forbidden_next_actions:
  - "implement_m34b"
  - "start_m34b_runtime_or_tests"
  - "start_m34c"
  - "change_code_tests_mechanics"
  - "add_new_executable_operations"
  - "expand_beyond_accepted_ordinary_add"
  - "optimizer_advice_ranking_economics_ev"
  - "release_public_numeric_probabilities"
  - "close_source_provenance_mml_or_pd013"
  - "enable_supervised_auto_run"
  - "enable_github_actions"
  - "update_accepted_ledgers_as_accepted"

standing_boundaries_ref: "manifest/GitHub_Workflow_Protocol.md#standing-boundaries-for-active-task-dispatcher"
standing_boundaries_apply: true

current_result_path: "packages/proposed/P2C_M34B_Design_Codex_v1/"
current_review_path: "reviews/P2C_M34B_Design_Audit_Claude_v1.md"

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
  - "Stop if this task would require implementation, code, tests, mechanics, data, probabilities, or operation-behavior changes."
  - "Stop if M34-B implementation, M34-C, or operation expansion is started."
  - "Stop if automation or GitHub Actions enablement is attempted."
---

# P2C Active Task

Current live task: Claude audit of proposed M34-B design package.

Next actor: Claude.

Allowed next action: audit `packages/proposed/P2C_M34B_Design_Codex_v1/`.

M34-B implementation remains closed until explicit ChatGPT/User authorization.
