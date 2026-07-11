---
schema_version: "2.0"
repo_head_at_last_update: "79c48129a3e0b90a5682148cde9701e485b5e7da"
updated_at_utc: "2026-07-11T19:15:00Z"

status: "audited_pending_user_gate"
next_actor: "chatgpt_user"
active_task_id: "M44A_ALCHEMY_RUNTIME"

allowed_next_action: "chatgpt_user_gate_decision_on_m44a_alchemy_runtime"
forbidden_next_actions:
  - "accept_m44a_without_chatgpt_user_gate"
  - "admit_alchemy_variants_omens_whittling_or_other_item_classes"
  - "admit_fractured_input_alchemy"
  - "change_accepted_ordinary_add_legality_capacity_or_weighting"
  - "expose_internal_alchemy_adds_as_caller_visible_sequence_steps"
  - "add_conditional_retry_route_generation_planner_or_optimizer_behavior"
  - "release_public_numeric_probabilities"
  - "close_source_provenance_mml_crafted_capacity_or_pd013"
  - "enable_automation_or_github_actions"
  - "agent_self_acceptance"

standing_boundaries_ref: "manifest/GitHub_Workflow_Protocol.md#standing-boundaries-for-active-task-dispatcher"
standing_boundaries_apply: true

current_result_path: "packages/proposed/P2C_M44A_Alchemy_Runtime_Result_Codex_v1"
current_review_path: "reviews/P2C_M44A_Alchemy_Runtime_Audit_Claude_v1.md"

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
  - "Stop if Alchemy does not rebuild the accepted ordinary pool after every internal add."
  - "Stop if any failed intermediate add exposes a partial Rare state or consumes the operation."
  - "Stop if direct/resolver or M43-A one-step parity fails."
  - "Stop if fractured input, variants, Omens, other item classes, planner/optimizer behavior, public numeric output, automation, or boundary closure enters scope."
---

# P2C Active Task

Claude audit of M44-A Alchemy Runtime: verdict GO. First executable Alchemy - only the alchemy row admitted. Atomic four-modifier multi-add over the accepted ordinary-weighted-add kernel: isolated empty-Rare working copy, 4 sequential adds with pool rebuild each step, caller item commits once after the 4th success; any failure / fractured / unrevealed-desecrated input -> no-transition/no-consumption, original unchanged. Verified by execution: weight-driven distribution covers 3-1/2-2/1-3 (never 4-0 - answers the 2-2/3-1 question); resolver-direct == M43-A one-step parity; seeded MC converges to exact + deterministic replay; exact ceilings structured-stop. bounded_sequence change is additive alchemy executor registration (M43-A anchors hold). Sampling recorded in mechanics_evidence as project_model_source_open / server_truth_claimed:false (the ratified model). 11 M44-A tests + 282 full suite pass; fingerprint reproduces package-pinned fcc79311.

Next: ChatGPT/User gate. Closes the basic-currency set. Fractured-input Alchemy, variants, Omens, other item classes stay separate gates. Review: reviews/P2C_M44A_Alchemy_Runtime_Audit_Claude_v1.md.

This is a proposed runtime delta only. It admits only base alchemy, builds no planner/optimizer, releases no public numbers, enables no automation, and closes no crafted-capacity/MML/SOURCE-PROVENANCE/PD-013.
