---
schema_version: "2.0"
repo_head_at_last_update: "6f9f97f9804db4900fedf76cb07e883bc41ab53c"
updated_at_utc: "2026-07-11T11:40:00Z"

status: "audited_pending_user_gate"
next_actor: "chatgpt_user"
active_task_id: "M43_NEXT_PROJECT_WAVE_DESIGN"

allowed_next_action: "chatgpt_user_gate_decision_on_m43_next_project_wave_design"
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
current_review_path: "reviews/P2C_M43_Next_Project_Wave_Design_Audit_Claude_v1.md"

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

Current live task: ChatGPT/User gate decision on the audited M43 Next Project Wave design.

Next actor: ChatGPT/User (gate decision).

Allowed next action: decide. Claude verdict: GO on the design. It selects a BOUNDED FIXED-SEQUENCE EVALUATOR (1-8 user-supplied accepted-operation steps) as the next wave - the bridge from currency emulators to a crafting-route simulator, generalizing the accepted M36-A seam. Verified it is an evaluator, NOT a planner: runs the user's supplied route, explicit exclusions of planner/ranking/retry/conditional/economics/discovery, stop_on_no_transition pinned, dispatch only to accepted executors (admitted-but-no-executor fails closed), exact-under-ceilings with honest structured-stop. Design-only, nothing admitted. KEY DIRECTION DECISION for the gate: this DEFERS Alchemy (which Kirill earlier wanted next) in favor of sequence composition - a conscious strategic pivot, both legitimate; Claude leans for M43 (route-evaluator is the real product) but it is Kirill's/ChatGPT's call. Optimizer/planner/economics and all other mechanics stay gated (`reviews/P2C_M43_Next_Project_Wave_Design_Audit_Claude_v1.md`).

This is design/selection verification only. It does not implement M43-A, admit any operation, build a planner/optimizer, release public numeric output, or authorize automation, and does not close MML, SOURCE/PROVENANCE, crafted-capacity, or PD-013.
