---
schema_version: "2.0"
repo_head_at_last_update: "486039718288df844a62917515471452a65efc20"
updated_at_utc: "2026-07-11T14:51:52Z"

status: "ready_for_claude"
next_actor: "claude"
active_task_id: "M43A_BOUNDED_ACCEPTED_OPERATION_SEQUENCE_RUNTIME"

allowed_next_action: "claude_audit_m43a_bounded_accepted_operation_sequence_runtime"
forbidden_next_actions:
  - "accept_m43a_without_chatgpt_user_gate"
  - "add_conditional_retry_repeat_fallback_or_route_generation"
  - "create_planner_optimizer_ranking_recommendation_economics_ev_or_advice"
  - "admit_new_operation_variant_modifier_or_alchemy"
  - "hide_exact_overflow_with_truncation_renormalization_or_monte_carlo"
  - "move_delete_or_rewrite_existing_packages_reviews_or_history"
  - "release_public_numeric_probabilities"
  - "close_source_provenance_mml_crafted_capacity_or_pd013"
  - "enable_automation_or_github_actions"
  - "agent_self_acceptance"

standing_boundaries_ref: "manifest/GitHub_Workflow_Protocol.md#standing-boundaries-for-active-task-dispatcher"
standing_boundaries_apply: true

current_result_path: "packages/proposed/P2C_M43A_Bounded_Accepted_Operation_Sequence_Runtime_Result_Codex_v1"
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
  - "Stop if one-step sequence parity differs from direct accepted execution."
  - "Stop if a later step reuses root-state resolver or pool data."
  - "Stop if an admitted row lacks an explicit accepted executor."
  - "Stop if exact overflow is approximated, truncated, or renormalized."
  - "Stop if planner/optimizer behavior, new mechanics, public numeric output, automation, or boundary closure enters scope."
---

# P2C Active Task

Claude audits the proposed M43-A bounded accepted-operation sequence runtime. The evaluator runs caller-supplied fixed one-to-eight-step sequences only, re-resolves every branch step against current state, uses an explicit accepted executor registry, returns structured exact ceiling stops, and supports seeded replay. M43-A is proposed; Alchemy, new mechanics/modifiers, conditional routes, planner/optimizer behavior, public numeric release, automation, and boundary closures remain closed.
