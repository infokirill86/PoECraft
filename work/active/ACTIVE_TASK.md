---
schema_version: "2.0"
repo_head_at_last_update: "0e87c636b7e752041300829d51691fc99cc5efe3"
updated_at_utc: "2026-07-11T15:20:00Z"

status: "audited_pending_user_gate"
next_actor: "chatgpt_user"
active_task_id: "M43A_BOUNDED_ACCEPTED_OPERATION_SEQUENCE_RUNTIME"

allowed_next_action: "chatgpt_user_gate_decision_on_m43a_bounded_accepted_operation_sequence_runtime"
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
current_review_path: "reviews/P2C_M43A_Bounded_Accepted_Operation_Sequence_Runtime_Audit_Claude_v1.md"

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

Claude audit of M43-A Bounded Accepted-Operation Sequence Runtime: verdict GO. First multi-operation composition runtime - runs user-supplied 1-8 step sequences of already-accepted operations, re-resolving each step against the real current branch state. Verified by execution on all four anchors: (1) one-step exact+seeded parity for every accepted family (zero drift vs direct call); (2) branch-state load-bearing (no root-state reuse); (3) exact ceilings -> structured stop, no truncation/renorm/hidden-MC; (4) executor registry fails closed for admitted-without-executor and non-admitted. Plus MC<->exact convergence on mixed multi-step, deterministic 8-step replay, and schema fail-closed on modifiers/>8-steps/continue-policy (evaluator, NOT planner). Composition only: no new operation admission; foundation fingerprint unchanged (230dc88); the 3 accepted-file edits are behavior-preserving type-widenings (dict->Mapping, list->(list,tuple)) for frozen-data compatibility. 28 M43-A tests + 271 full suite pass.

Next: ChatGPT/User gate. Alchemy remains deferred; Omens/Fracture/Desecrate, longer/conditional sequences, planner/optimizer stay separate gates. Review: reviews/P2C_M43A_Bounded_Accepted_Operation_Sequence_Runtime_Audit_Claude_v1.md.

This is a proposed runtime delta only. It admits no new operation/modifier, builds no planner/optimizer/economics, releases no public numbers, enables no automation, and closes no MML/SOURCE-PROVENANCE/crafted-capacity/PD-013.
