---
schema_version: "2.0"
repo_head_at_last_update: "27d580b5f84286a7d508e1a6b32ab99e50853c12"
updated_at_utc: "2026-07-12T18:12:11Z"

status: "ready_for_claude"
next_actor: "claude"
active_task_id: "M48_NEXT_INDEPENDENT_PROJECT_WAVE_DESIGN"

allowed_next_action: "claude_audit_m48_next_independent_project_wave_design"
forbidden_next_actions:
  - "accept_or_promote_d3_d5_from_observations_without_explicit_chatgpt_user_gate"
  - "implement_or_admit_reveal_or_echoes_runtime"
  - "implement_omen_of_light_necromancy_lich_or_putrefaction"
  - "admit_multiple_placeholders_or_revealed_desecrated_fracture_runtime"
  - "implement_m48_or_add_branching_sequence_runtime"
  - "add_route_generation_search_ranking_optimizer_economics_or_advice"
  - "publish_captured_probability_results_or_crafting_advice"
  - "add_conditional_retry_route_generation_planner_or_optimizer_behavior"
  - "release_public_numeric_probabilities"
  - "close_source_provenance_mml_crafted_capacity_or_pd013"
  - "enable_automation_or_github_actions"
  - "agent_self_acceptance"

standing_boundaries_ref: "manifest/GitHub_Workflow_Protocol.md#standing-boundaries-for-active-task-dispatcher"
standing_boundaries_apply: true

current_result_path: "packages/proposed/P2C_M48_Next_Independent_Project_Wave_Design_Codex_v1"
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
  - "Stop if a D3-D5 candidate or limited observation set is represented as accepted mechanics."
  - "Stop if M48 design turns into implementation, route generation, planner, optimizer, economics, or advice."
  - "Stop if a new operation, modifier, predicate rule, or mechanics policy would be admitted."
  - "Stop if an external-source conflict is silently resolved."
  - "Stop if revealed-Desecrated Fracture runtime or PD-013 closure enters scope."
  - "Stop if planner/optimizer behavior, public numeric output, automation, or boundary closure enters scope."
---

# P2C Active Task

M47-A2V Reveal Sampling Verification & Decision Support is accepted after Claude GO audit as internal quarantined evidence tooling only. D3-D5 and Reveal/Echoes runtime remain unaccepted; real observations and a later User gate are still required.

Codex created the proposed M48 independent next-wave design. It compares Omen of Light, Echoes, Putrefaction, revealed-Desecrated Fracture, Astrid/crafted capacity, more sequence infrastructure, and a bounded caller-authored branching evaluator. The recommendation is a finite acyclic branching-sequence evaluator over accepted operations: the caller supplies the complete graph, while P2C only evaluates it through accepted resolver/executor, exact/MC, replay, and named success predicates. It contains no route generation, ranking, costs, advice, optimizer, new mechanics, or runtime implementation.

Next: Claude audits `packages/proposed/P2C_M48_Next_Independent_Project_Wave_Design_Codex_v1/`, including whether the selected boundary remains an evaluator and whether Omen of Light or Astrid should instead be the next clean wave. All D3-D5, Echoes, Putrefaction, Omen of Light, Astrid/crafted-capacity, revealed-Fracture/PD-013, public numeric release, optimizer/economics/advice, and automation remain separately gated.
