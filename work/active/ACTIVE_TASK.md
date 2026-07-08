---
schema_version: "2.0"
repo_head_at_last_update: "6c9d75d2bb930979b0cf229ceb4b2f6e699dca39"
updated_at_utc: "2026-07-08T20:22:00Z"

status: "audited_pending_user_gate"
next_actor: "chatgpt_user"
active_task_id: "OPERATION_RUNTIME_ADMISSION_METADATA_FLOOR"

allowed_next_action: "chatgpt_user_gate_decision_on_operation_runtime_admission_metadata_floor"
forbidden_next_actions:
  - "accept_m36_heterogeneous_chains"
  - "implement_heterogeneous_operation_chains"
  - "implement_new_executable_operation"
  - "implement_annulment_variants_or_omens"
  - "implement_additional_operations"
  - "implement_chaos_essence_fracture_desecrate_jawbone_or_reveal"
  - "expand_operation_scope"
  - "optimizer_advice_ranking_economics_ev"
  - "release_public_numeric_probabilities"
  - "close_source_provenance_mml_or_pd013"
  - "enable_supervised_auto_run"
  - "enable_github_actions"
  - "self_accept_metadata_floor"

standing_boundaries_ref: "manifest/GitHub_Workflow_Protocol.md#standing-boundaries-for-active-task-dispatcher"
standing_boundaries_apply: true

current_result_path: "packages/proposed/P2C_Operation_Runtime_Admission_Metadata_Floor_Codex_v1/"
current_review_path: ""

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
  - "Stop if audit would require implementation of a new executable operation."
  - "Stop if M36 heterogeneous chains, Annulment variants, or additional operations would be accepted or authorized without explicit later gate."
  - "Stop if a source/provenance conflict requires user decision."
  - "Stop if public numeric release, optimizer/economics/advice, automation, SOURCE/PROVENANCE closure, MML closure, or PD-013 closure appears."
---

# P2C Active Task

Current live task: ChatGPT/User gate decision on the operation runtime-admission metadata floor (data change).

Next actor: ChatGPT/User (gate decision).

Allowed next action: decide the data change. Claude audit verdict: GO WITH CHANGES — classification/validator/fingerprint correct; root SHA256SUMS was inconsistent and has been corrected (`reviews/P2C_Operation_Runtime_Admission_Metadata_Floor_Audit_Claude_v1.md`).

No new executable operation, heterogeneous chain runtime, public numeric release, optimizer/economics/advice, automation, or boundary closure is authorized by this dispatcher.
