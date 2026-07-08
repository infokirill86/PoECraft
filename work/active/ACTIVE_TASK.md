---
schema_version: "2.0"
repo_head_at_last_update: "2a2d55be76b798b5c5aa738c1c2c2c920f2eac27"
updated_at_utc: "2026-07-08T18:02:00Z"

status: "audited_pending_user_gate"
next_actor: "chatgpt_user"
active_task_id: "M35A_ANNULMENT_RUNTIME"

allowed_next_action: "chatgpt_user_gate_decision_on_m35a_annulment_runtime"
forbidden_next_actions:
  - "accept_annulment_as_executable"
  - "self_accept_m35a"
  - "implement_additional_operations"
  - "implement_chaos_essence_fracture_desecrate_jawbone_or_reveal"
  - "change_mechanics_data_or_source_truth"
  - "expand_operation_scope"
  - "optimizer_advice_ranking_economics_ev"
  - "release_public_numeric_probabilities"
  - "close_source_provenance_mml_or_pd013"
  - "enable_supervised_auto_run"
  - "enable_github_actions"
  - "update_accepted_ledgers_as_accepted"

standing_boundaries_ref: "manifest/GitHub_Workflow_Protocol.md#standing-boundaries-for-active-task-dispatcher"
standing_boundaries_apply: true

current_result_path: "packages/proposed/P2C_M35A_Annulment_Runtime_Result_Codex_v1/"
current_review_path: "reviews/P2C_M35A_Annulment_Runtime_Audit_Claude_v1.md"

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
  - "Stop if audit would require new implementation, code, tests, mechanics, data, probabilities, or operation-behavior changes."
  - "Stop if M35-A would be accepted without ChatGPT/User gate."
  - "Stop if operation expansion beyond base Annulment, public numeric release, optimizer/economics/advice, automation, or boundary closure appears."
---

# P2C Active Task

Current live task: ChatGPT/User gate decision on the M35-A Annulment runtime.

Next actor: ChatGPT/User (gate decision).

Allowed next action: decide acceptance of Annulment runtime. Claude audit verdict: GO (`reviews/P2C_M35A_Annulment_Runtime_Audit_Claude_v1.md`).

Annulment runtime is proposed only and is not accepted until Claude audit and ChatGPT/User gate.
