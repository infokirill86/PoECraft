---
schema_version: "2.0"
repo_head_at_last_update: "5abc11c0b85c8b500adca99c2826f19d30d0f961"
updated_at_utc: "2026-07-12T09:20:00Z"

status: "audited_pending_user_gate"
next_actor: "chatgpt_user"
active_task_id: "M46A_FRACTURE_CORE_RUNTIME"

allowed_next_action: "chatgpt_user_gate_decision_on_m46a_fracture_core_runtime"
forbidden_next_actions:
  - "chatgpt_user_accept_m46a_before_claude_audit"
  - "resolve_desecrated_revealed_jawbone_reveal_or_pd013_behavior"
  - "admit_multiple_side_directed_non_quarterstaff_or_variant_fracture"
  - "admit_new_omens_operations_or_modifier_layers"
  - "change_accepted_operation_mechanics"
  - "add_conditional_retry_route_generation_planner_or_optimizer_behavior"
  - "release_public_numeric_probabilities"
  - "close_source_provenance_mml_crafted_capacity_or_pd013"
  - "enable_automation_or_github_actions"
  - "agent_self_acceptance"

standing_boundaries_ref: "manifest/GitHub_Workflow_Protocol.md#standing-boundaries-for-active-task-dispatcher"
standing_boundaries_apply: true

current_result_path: "packages/proposed/P2C_M46A_Fracture_Core_Runtime_Result_Codex_v1"
current_review_path: "reviews/P2C_M46A_Fracture_Core_Runtime_Audit_Claude_v1.md"

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
  - "Stop if M46-A implementation is treated as accepted before Claude audit and a later User gate."
  - "Stop if a source conflict is silently resolved instead of surfaced."
  - "Stop if Desecrated/Revealed/Jawbone/Reveal or PD-013 behavior enters the clean core."
  - "Stop if planner/optimizer behavior, public numeric output, automation, or boundary closure enters scope."
---

# P2C Active Task

Claude audit of M46-A Fracture Core Runtime: verdict GO. First Fracture runtime - only fracturing_orb admitted. Preconditions fail-closed: <4 explicit, existing fracture, unrevealed placeholder, or any desecrated instance rejected (clean floor; PD-013 stays open). Uniform combined-pool selection (Candidate weight 1, no side-first, no generation weight; crafted eligible); one-bit atomic mutation preserving crafted (fractured+crafted). Fractured immutability verified across accepted Annulment/Chaos removal + capacity + Alchemy fail-closed. Direct/resolver/M43-A parity + MC<->exact convergence. mechanics_evidence fracture_core_m46a = project_model_source_open (uniform_without_generation_weights). bounded_sequence change is additive fracture executor registration. 16 M46-A tests + 316 full suite pass; fingerprint 2e5e4454 self-consistent (pinned-fingerprint tests pass). Closes the Fracture mechanic.

Watchpoints: pinned base already fractured -> Fracture applies to OTHER rare states; Desecrated<->Fracture interaction deferred to the Desecrate wave (rules recorded). Next: ChatGPT/User gate. Review: reviews/P2C_M46A_Fracture_Core_Runtime_Audit_Claude_v1.md.

This is a proposed runtime delta only. It admits only base fracturing_orb, decides no Desecrated/PD-013 edge, builds no planner/optimizer, releases no public numbers, and closes no crafted-capacity/MML/SOURCE-PROVENANCE/PD-013.
