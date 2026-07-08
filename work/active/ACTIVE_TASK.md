---
schema_version: "2.0"
repo_head_at_last_update: "3bb1c555e367af6c1e9ffda7b0954ae60bba0968"
updated_at_utc: "2026-07-08T19:12:32Z"

status: "ready_for_claude"
next_actor: "claude"
active_task_id: "POST_M35A_NEXT_WAVE_DESIGN"

allowed_next_action: "claude_audit_post_m35a_next_wave_design"
forbidden_next_actions:
  - "accept_full_m35"
  - "implement_next_wave"
  - "implement_heterogeneous_operation_chains"
  - "implement_annulment_variants_or_omens"
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

current_result_path: "packages/proposed/P2C_Post_M35A_Next_Wave_Design_Codex_v1/"
current_review_path: "reviews/P2C_Post_M35A_Next_Wave_Design_Audit_Claude_v1.md"

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
  - "Stop if audit would require implementation, code, tests, mechanics, data, probabilities, or operation-behavior changes."
  - "Stop if full M35, heterogeneous chains, Annulment variants, or additional operations would be accepted or authorized without explicit later gate."
  - "Stop if public numeric release, optimizer/economics/advice, automation, SOURCE/PROVENANCE closure, MML closure, or PD-013 closure appears."
---

# P2C Active Task

Current live task: Claude audit of the post-M35A next-wave design proposal.

Next actor: Claude.

Allowed next action: audit `packages/proposed/P2C_Post_M35A_Next_Wave_Design_Codex_v1/`.

No implementation, heterogeneous chain runtime, new operation, public numeric release, optimizer/economics/advice, automation, or boundary closure is authorized by this dispatcher.
