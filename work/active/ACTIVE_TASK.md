---
schema_version: "2.0"
repo_head_at_last_update: "ee9ca03efeff104c009d17171819f203a6d5f0f8"
updated_at_utc: "2026-07-11T11:05:04Z"

status: "ready_for_claude"
next_actor: "claude"
active_task_id: "M43_NEXT_PROJECT_WAVE_DESIGN"

allowed_next_action: "claude_audit_m43_next_project_wave_design"
forbidden_next_actions:
  - "implement_m43a_or_any_new_runtime"
  - "admit_omen_whittling_fracture_alchemy_or_other_mechanics"
  - "implement_essence_replacement_stacking_repeat_or_astrid_rune_capacity"
  - "implement_desecrate_jawbone_reveal_or_close_pd013"
  - "create_planner_optimizer_economics_advice_or_ranking"
  - "release_public_numeric_probabilities"
  - "close_source_provenance_mml_crafted_capacity_or_pd013"
  - "enable_automation_or_github_actions"
  - "agent_self_acceptance"

standing_boundaries_ref: "manifest/GitHub_Workflow_Protocol.md#standing-boundaries-for-active-task-dispatcher"
standing_boundaries_apply: true

current_result_path: "packages/proposed/P2C_M43_Next_Project_Wave_Design_Codex_v1"
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
  - "Stop if audit would turn into implementation or operation admission."
  - "Stop if public numeric output, optimizer/economics/advice, automation, or boundary closure enters scope."
---

# P2C Active Task

M43 design proposes bounded fixed-sequence evaluation over already accepted operations. Claude audits the package next. M43-A implementation and every new mechanic remain closed pending a later ChatGPT/User gate.
