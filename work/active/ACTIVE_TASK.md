---
schema_version: "2.0"
repo_head_at_last_update: "d088e4e386b88706054b1b6c7da47216dcdd2df7"
updated_at_utc: "2026-07-08T15:58:13Z"

status: "awaiting_user_gate"
next_actor: "chatgpt_user"
active_task_id: "M34_NEXT_GATE"

allowed_next_action: "chatgpt_user_decide_next_m34_step_or_choose_another_task"
forbidden_next_actions:
  - "start_m34c_without_explicit_later_gate"
  - "implement_sequences_longer_than_two_steps_without_explicit_later_gate"
  - "add_variable_length_route_planner"
  - "add_new_executable_operations"
  - "expand_beyond_accepted_ordinary_add"
  - "optimizer_advice_ranking_economics_ev"
  - "release_public_numeric_probabilities"
  - "close_source_provenance_mml_or_pd013"
  - "enable_supervised_auto_run"
  - "enable_github_actions"
  - "self_accept_later_milestone"

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
  - "Stop if this task would require mechanics, code, tests, data, probability release, or operation-behavior changes."
  - "Stop if M34-C, longer sequences, route planning, operation expansion, or optimizer/economics work starts without explicit later authorization."
  - "Stop if public numeric probability release, automation, or boundary closure appears."
---

# P2C Active Task

Current state: M34-B1 implementation is accepted after Claude GO audit and ChatGPT/User gate.

Next actor: ChatGPT/User.

Allowed next action: decide the next M34 step or choose another task.

Full M34, M34-C, sequences longer than two steps, route planning, operation expansion, optimizer/economics/advice, public numeric release, automation, and boundary closure remain closed until explicit later authorization.
