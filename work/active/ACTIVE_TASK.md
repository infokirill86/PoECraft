---
schema_version: "2.0"
repo_head_at_last_update: "d63ce22dd1e394039b7b49ddf04cacf628a5744c"
updated_at_utc: "2026-07-13T08:56:05Z"

status: "ready_for_claude"
next_actor: "claude"
active_task_id: "M48A_BOUNDED_BRANCHING_RUNTIME"

allowed_next_action: "claude_audit_m48a_bounded_branching_runtime"
forbidden_next_actions:
  - "accept_m48a_without_explicit_chatgpt_user_gate"
  - "generate_search_compare_rank_improve_or_recommend_routes"
  - "add_predicate_score_probability_cost_ev_utility_desirability_or_ranking"
  - "invent_or_modify_success_criteria"
  - "truncate_renormalize_or_silently_replace_exact_results_with_monte_carlo"
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
  - "Stop if audit needs a new mechanic, operation admission, predicate rule, or source-policy decision."
  - "Stop if a predicate returns score, probability, cost, EV, utility, desirability, or ranking."
  - "Stop if route generation, search, comparison, ranking, recommendation, economics, or advice enters scope."
  - "Stop if exact mass is truncated, renormalized, or silently approximated."
  - "Stop if success criteria are invented or changed."
  - "Stop if Reveal, Astrid, D3-D5, PD-013, crafted-capacity, public numeric output, automation, or boundary closure enters scope."
---

# P2C Active Task

M48 design is accepted. M48-A bounded caller-authored branching runtime is implemented and proposed, not accepted. Claude should audit the result package, runtime diff, evaluator/optimizer firewall, exact/seeded behavior, parity, and fail-closed controls. ChatGPT/User remains the only acceptance authority.
