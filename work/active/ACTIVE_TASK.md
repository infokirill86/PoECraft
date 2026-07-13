---
schema_version: "2.0"
repo_head_at_last_update: "fcdb2e1be3302f934bdda27d4c9573c75ade2212"
updated_at_utc: "2026-07-13T09:16:13Z"

status: "audited_pending_user_gate"
next_actor: "chatgpt_user"
active_task_id: "M48A_BOUNDED_BRANCHING_RUNTIME"

allowed_next_action: "chatgpt_user_gate_m48a_after_claude_go"
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
  - "Stop if audit needs a new mechanic, operation admission, predicate rule, or source-policy decision."
  - "Stop if a predicate returns score, probability, cost, EV, utility, desirability, or ranking."
  - "Stop if route generation, search, comparison, ranking, recommendation, economics, or advice enters scope."
  - "Stop if exact mass is truncated, renormalized, or silently approximated."
  - "Stop if success criteria are invented or changed."
  - "Stop if Reveal, Astrid, D3-D5, PD-013, crafted-capacity, public numeric output, automation, or boundary closure enters scope."
---

# P2C Active Task

M48 design is accepted. Claude audited the proposed M48-A bounded caller-authored branching runtime with verdict **GO** (`reviews/P2C_M48A_Bounded_Branching_Runtime_Audit_Claude_v1.md`): the evaluator↔optimizer firewall holds in code (closed `success_class.v1` registry, `PredicateDecision` carries only categorical result, no optimizer/route-generation surface, classifier interprets `success_criteria.yaml` and fails closed on shape change); caller owns the whole finite acyclic DAG; exact mass each equals 1 with overflow→empty `ceiling_exceeded` (no truncation/renorm/hidden MC); reuses the accepted M43-A seam (behavior-preserving refactor, M43-A parity 48 passed); fingerprint unchanged; 21 M48-A tests pass. Proposed, not accepted.

Next: ChatGPT/User acceptance gate. M48-A remains proposed. Route generation/search/ranking/optimizer/economics/advice, scoring predicates, new operations/criteria, Reveal/Astrid/D3-D5/PD-013/crafted-capacity, public numeric release, and automation remain separately gated.
