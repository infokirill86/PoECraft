---
schema_version: "2.0"
repo_head_at_last_update: "17089680b1149cff8f05d1b84b9b55e247d64452"
updated_at_utc: "2026-07-08T15:40:23Z"

status: "ready_for_claude"
next_actor: "claude"
active_task_id: "M34B1_IMPLEMENTATION"

allowed_next_action: "claude_audit_m34b1_implementation"
forbidden_next_actions:
  - "accept_m34b1_without_chatgpt_user_gate"
  - "start_m34c"
  - "implement_sequences_longer_than_two_steps"
  - "add_variable_length_route_planner"
  - "add_new_executable_operations"
  - "expand_beyond_accepted_ordinary_add"
  - "optimizer_advice_ranking_economics_ev"
  - "release_public_numeric_probabilities"
  - "close_source_provenance_mml_or_pd013"
  - "enable_supervised_auto_run"
  - "enable_github_actions"

standing_boundaries_ref: "manifest/GitHub_Workflow_Protocol.md#standing-boundaries-for-active-task-dispatcher"
standing_boundaries_apply: true

current_result_path: "packages/proposed/P2C_M34B1_Result_Codex_v1/"
current_review_path: "reviews/P2C_M34B1_Implementation_Audit_Claude_v1.md"

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
  - "Stop if M34-B1 implementation would be self-accepted."
  - "Stop if M34-C, longer sequences, route planning, operation expansion, or optimizer/economics work appears."
  - "Stop if public numeric probability release or boundary closure appears."
---

# P2C Active Task

Current live task: Claude audit of proposed M34-B1 implementation.

Next actor: Claude.

Allowed next action: audit `packages/proposed/P2C_M34B1_Result_Codex_v1/`.

M34-B1 is proposed only until Claude audit and ChatGPT/User acceptance.
