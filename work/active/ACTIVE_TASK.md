---
schema_version: "2.0"
repo_head_at_last_update: "bd40cd14a8feb25f9b69b907d5864294c48b74f0"
updated_at_utc: "2026-07-12T07:57:55Z"

status: "ready_for_claude"
next_actor: "claude"
active_task_id: "M46A_FRACTURE_CORE_RUNTIME"

allowed_next_action: "claude_audit_m46a_fracture_core_runtime"
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
  - "Stop if M46-A implementation is treated as accepted before Claude audit and a later User gate."
  - "Stop if a source conflict is silently resolved instead of surfaced."
  - "Stop if Desecrated/Revealed/Jawbone/Reveal or PD-013 behavior enters the clean core."
  - "Stop if planner/optimizer behavior, public numeric output, automation, or boundary closure enters scope."
---

# P2C Active Task

Audit the proposed M46-A clean base Fracture runtime. Verify the combined uniform installed-instance pool, crafted-flag preservation, atomic one-flag mutation, exact/seeded evidence, accepted-operation immutability regressions, resolver/M43-A parity, and fail-closed exclusion of every disputed or unauthorized edge.

M46 design is accepted. M46-A runtime is proposed only and requires Claude audit followed by a separate ChatGPT/User acceptance gate.
