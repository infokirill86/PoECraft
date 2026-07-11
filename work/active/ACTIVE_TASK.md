---
schema_version: "2.0"
repo_head_at_last_update: "77c8418e2b80480d46af77ae55598ddb9e51ca51"
updated_at_utc: "2026-07-12T08:20:00Z"

status: "audited_pending_user_gate"
next_actor: "chatgpt_user"
active_task_id: "M46_FRACTURE_CORE_MECHANICS_DESIGN_VERIFICATION"

allowed_next_action: "chatgpt_user_gate_decision_on_m46_fracture_core_mechanics_design_verification"
forbidden_next_actions:
  - "implement_or_admit_fracturing_orb_runtime"
  - "resolve_revealed_desecrated_jawbone_reveal_or_pd013_behavior"
  - "admit_new_omens_operations_or_modifier_layers"
  - "change_accepted_operation_mechanics"
  - "add_conditional_retry_route_generation_planner_or_optimizer_behavior"
  - "release_public_numeric_probabilities"
  - "close_source_provenance_mml_crafted_capacity_or_pd013"
  - "enable_automation_or_github_actions"
  - "agent_self_acceptance"

standing_boundaries_ref: "manifest/GitHub_Workflow_Protocol.md#standing-boundaries-for-active-task-dispatcher"
standing_boundaries_apply: true

current_result_path: "packages/proposed/P2C_M46_Fracture_Core_Mechanics_Design_Verification_Codex_v1"
current_review_path: "reviews/P2C_M46_Fracture_Core_Mechanics_Design_Verification_Audit_Claude_v1.md"

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
  - "Stop if Fracture implementation or runtime admission begins."
  - "Stop if source conflict is silently resolved instead of surfaced."
  - "Stop if Revealed/Desecrated/Jawbone/Reveal or PD-013 behavior enters the clean core."
  - "Stop if planner/optimizer behavior, public numeric output, automation, or boundary closure enters scope."
---

# P2C Active Task

Claude audit of M46 Fracture Core Mechanics Design Verification: verdict GO (design-only; fracturing_orb stays disputed/candidate; nothing admitted). Clean-core matches Kirill's ground truth + accepted mechanics: rare input, >=4 explicit slots, no existing fracture, select ONE random instance from a COMBINED uniform pool (no side lottery, no weight), set fractured:true, atomic, fail-closed. Fractured-can-be-crafted captured (pool includes crafted; preserve crafted flag; ModifierInstance has independent crafted/fractured). Disputed Desecrated edge (the 1-of-3 trick) correctly EXCLUDED from the clean floor and kept as PD-013 (sources conflict: wiki ineligible-but-counts vs CoE eligible). Thorough fractured-immutability contract: accepted Annulment/Chaos removal + Perfect Essence feasible-removal keep excluding it, Alchemy fail-closed on fractured input, capacity still counts it, no op clears fractured without a gate. Honest source pass; project-model. Byte-confirmed operations.yaml fracturing_orb row + mechanics_evidence fracturing_revealed_desecrated conflict.

Watchpoints for M46-A: our pinned base is ALREADY fractured (fails no-existing-fracture) so Fracture applies to OTHER rare states in a route; uniform is 1-of-N (N>=4) over ALL instances; record clean-core in mechanics_evidence as source-open with the Desecrated conflict noted. Desecrated/Revealed/Jawbone/PD-013, multi-fracture, side-directed Fracture, other classes stay separate gates. Review: reviews/P2C_M46_Fracture_Core_Mechanics_Design_Verification_Audit_Claude_v1.md.

This is mechanics verification only. It admits no Fracture runtime, decides no Desecrated/PD-013 edge, releases no public numbers, and closes no MML/SOURCE-PROVENANCE/crafted-capacity/PD-013.
