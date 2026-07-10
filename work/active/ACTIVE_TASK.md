---
schema_version: "2.0"
repo_head_at_last_update: "150021e5a0a75727bd8d1c81965b52cef6b229a5"
updated_at_utc: "2026-07-10T22:25:13Z"

status: "awaiting_user_gate"
next_actor: "chatgpt_user"
active_task_id: "POST_M41A_NEXT_GATE"

allowed_next_action: "chatgpt_user_decide_next_operation_or_modifier_wave"
forbidden_next_actions:
  - "start_next_mechanics_or_runtime_wave_without_explicit_gate"
  - "admit_perfect_lesser_or_corrupted_essence_runtime"
  - "decide_multiple_essence_stacking_replacement_or_capacity_semantics"
  - "accept_whittling_or_omen_runtime"
  - "implement_alchemy_fracture_desecrate_jawbone_or_reveal"
  - "implement_longer_chains_or_planner"
  - "optimizer_economics_advice"
  - "release_public_numeric_probabilities"
  - "close_source_provenance_mml_or_pd013"
  - "enable_automation_or_github_actions"
  - "agent_self_acceptance"

standing_boundaries_ref: "manifest/GitHub_Workflow_Protocol.md#standing-boundaries-for-active-task-dispatcher"
standing_boundaries_apply: true

current_result_path: "packages/proposed/P2C_M41A_Greater_Essence_Quarterstaff_Runtime_Result_Codex_v1"
current_review_path: "reviews/P2C_M41A_Greater_Essence_Quarterstaff_Runtime_Audit_Claude_v1.md"

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
  - "Stop if any new mechanics/runtime wave starts without explicit ChatGPT/User authorization."
  - "Stop if crafted-capacity, SOURCE/PROVENANCE, broader MML, or PD-013 closure is implied."
  - "Stop if public numeric output, optimizer/economics/advice, automation, or an unauthorized operation enters scope."
---

# P2C Active Task

M41-A Greater Essence Quarterstaff Runtime is accepted for exactly eight audited rows. Crafted-capacity remains source-open/unverified, and no multiple-Essence, stacking, replacement, or Perfect-Essence semantics are accepted. The next project move requires an explicit ChatGPT/User gate.
