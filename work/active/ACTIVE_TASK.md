---
schema_version: "2.0"
repo_head_at_last_update: "ca7ac2bfec5a967bcbae6df99532fb9d351b77d2"
updated_at_utc: "2026-07-11T21:58:51Z"

status: "ready_for_claude"
next_actor: "claude"
active_task_id: "M46_FRACTURE_CORE_MECHANICS_DESIGN_VERIFICATION"

allowed_next_action: "claude_audit_m46_fracture_core_mechanics_design_verification"
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
  - "Stop if Fracture implementation or runtime admission begins."
  - "Stop if source conflict is silently resolved instead of surfaced."
  - "Stop if Revealed/Desecrated/Jawbone/Reveal or PD-013 behavior enters the clean core."
  - "Stop if planner/optimizer behavior, public numeric output, automation, or boundary closure enters scope."
---

# P2C Active Task

M45-A Independent Omen Layer Runtime and the Whittling documentary evidence bump are accepted by ChatGPT/User after Claude GO.

M46 is design/mechanics verification only. Claude should audit the fresh source comparison, the clean Fracture candidate-pool and immutability contract, the deliberate fail-closed exclusion of all Desecrated/Revealed states, and the proposed later M46-A implementation boundary. No Fracture runtime is authorized by this package.
