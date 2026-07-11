---
schema_version: "2.0"
repo_head_at_last_update: "35e0b3b748dbda3716eb1b48bd85059a5c345e35"
updated_at_utc: "2026-07-11T19:56:46Z"

status: "ready_for_claude"
next_actor: "claude"
active_task_id: "M45_NEXT_PROJECT_WAVE_DESIGN"

allowed_next_action: "claude_audit_m45_next_project_wave_design"
forbidden_next_actions:
  - "implement_or_admit_any_m45_runtime_operation_or_modifier"
  - "admit_omens_whittling_fracture_desecrate_jawbone_or_reveal"
  - "change_accepted_m44a_or_other_runtime_mechanics"
  - "add_conditional_retry_route_generation_planner_or_optimizer_behavior"
  - "release_public_numeric_probabilities"
  - "close_source_provenance_mml_crafted_capacity_or_pd013"
  - "enable_automation_or_github_actions"
  - "agent_self_acceptance"

standing_boundaries_ref: "manifest/GitHub_Workflow_Protocol.md#standing-boundaries-for-active-task-dispatcher"
standing_boundaries_apply: true

current_result_path: "packages/proposed/P2C_M45_Next_Project_Wave_Design_Codex_v1"
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
  - "Stop if the M45 design is treated as runtime admission or implementation authority."
  - "Stop if source/catalogue drift is resolved without a ChatGPT/User gate."
  - "Stop if planner/optimizer behavior, public numeric output, automation, or boundary closure enters scope."
---

# P2C Active Task

M44-A base Alchemy runtime is accepted after Claude GO and the ChatGPT/User gate.

Claude should audit the proposed M45 next-wave design. Codex recommends a clean independent Omen modifier layer over already accepted currencies, with historical, disputed, Desecrated, Jawbone, Reveal, multi-remove, and all runtime-admission questions kept behind later explicit gates.
