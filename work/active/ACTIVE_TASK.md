---
schema_version: "2.0"
repo_head_at_last_update: "d26fb94cdc61be6a0e449b35a4087dd501fd5ad0"
updated_at_utc: "2026-07-13T09:30:43Z"

status: "awaiting_user_gate"
next_actor: "chatgpt_user"
active_task_id: "POST_M48A_NEXT_GATE"

allowed_next_action: "chatgpt_user_decide_next_project_wave"
forbidden_next_actions:
  - "start_any_next_runtime_mechanics_or_operation_wave_without_explicit_chatgpt_user_gate"
  - "generate_search_compare_rank_improve_or_recommend_routes"
  - "add_automatic_retry_conditional_strategy_invention_or_planner_behavior"
  - "add_predicate_score_probability_cost_ev_utility_desirability_or_ranking"
  - "invent_or_modify_success_criteria"
  - "implement_or_admit_reveal_echoes_omen_of_light_putrefaction_or_astrid"
  - "promote_d3_d5_or_resolve_revealed_desecrated_fracture_pd013_or_crafted_capacity"
  - "admit_new_operation_omen_modifier_predicate_mechanics_or_source_policy"
  - "publish_numeric_probabilities_crafting_advice_economics_or_optimizer_output"
  - "close_source_provenance_mml_crafted_capacity_or_pd013"
  - "enable_automation_or_github_actions"
  - "agent_self_acceptance"

standing_boundaries_ref: "manifest/GitHub_Workflow_Protocol.md#standing-boundaries-for-active-task-dispatcher"
standing_boundaries_apply: true

current_result_path: "packages/proposed/P2C_M48A_Bounded_Branching_Runtime_Result_Codex_v1"
current_review_path: "reviews/P2C_M48A_Bounded_Branching_Runtime_Audit_Claude_v1.md"

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
  - "Stop if the next wave would begin without an explicit ChatGPT/User gate."
  - "Stop if route generation, search, comparison, ranking, recommendation, economics, advice, or public numeric output enters scope."
  - "Stop if a new operation, Omen, modifier, predicate mechanic, source policy, automation, or boundary closure enters scope without an explicit gate."
---

# P2C Active Task

M48-A bounded caller-authored branching runtime is accepted after Claude GO audit and ChatGPT/User gate. The next project wave remains closed pending an explicit ChatGPT/User decision.
