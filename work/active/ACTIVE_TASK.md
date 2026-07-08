---
schema_version: "2.0"
repo_head_at_last_update: "a3fabef923227cc1eabae719b0b7c4abe6a4eff8"
updated_at_utc: "2026-07-08T19:07:08Z"

status: "awaiting_user_gate"
next_actor: "chatgpt_user"
active_task_id: "POST_M35A_NEXT_GATE"

allowed_next_action: "chatgpt_user_decide_next_operation_or_hardening_wave"
forbidden_next_actions:
  - "start_next_work_without_explicit_gate"
  - "accept_full_m35"
  - "implement_annulment_variants_or_omens"
  - "implement_additional_operations"
  - "implement_chaos_essence_fracture_desecrate_jawbone_or_reveal"
  - "start_heterogeneous_operation_chains"
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

current_result_path: ""
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
  - "Stop if any work beyond recording M35-A acceptance would be started."
  - "Stop if full M35 or any additional operation would be accepted or authorized without explicit later gate."
  - "Stop if public numeric release, optimizer/economics/advice, automation, or boundary closure appears."
---

# P2C Active Task

Current live task: ChatGPT/User gate after M35-A Annulment Runtime Admission acceptance.

Next actor: ChatGPT/User.

Allowed next action: decide the next operation or hardening wave.

M35-A base Annulment runtime is accepted. Full M35, Annulment variants, additional operations, heterogeneous chains, public numeric release, optimizer/economics/advice, automation, and boundary closure remain closed until a later explicit gate.
