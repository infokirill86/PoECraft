---
schema_version: "2.0"
repo_head_at_last_update: "2f1a6b5e75ca873f0e32aa44ebc2ab1569be4d64"
updated_at_utc: "2026-07-11T08:54:21Z"

status: "ready_for_claude"
next_actor: "claude"
active_task_id: "M42A_PERFECT_ESSENCE_QUARTERSTAFF_RUNTIME"

allowed_next_action: "claude_audit_m42a_perfect_essence_quarterstaff_runtime"
forbidden_next_actions:
  - "accept_m42a_without_chatgpt_user_gate"
  - "admit_perfect_essence_seeking_or_infinite"
  - "implement_essence_replacement_stacking_or_repeat_application"
  - "change_greater_lesser_or_corrupted_essence_runtime"
  - "accept_whittling_omen_or_side_filter_runtime"
  - "implement_alchemy_fracture_desecrate_jawbone_or_reveal"
  - "implement_longer_chains_or_planner"
  - "optimizer_economics_advice"
  - "release_public_numeric_probabilities"
  - "close_crafted_capacity_source_provenance_mml_or_pd013"
  - "enable_automation_or_github_actions"
  - "agent_self_acceptance"

standing_boundaries_ref: "manifest/GitHub_Workflow_Protocol.md#standing-boundaries-for-active-task-dispatcher"
standing_boundaries_apply: true

current_result_path: "packages/proposed/P2C_M42A_Perfect_Essence_Quarterstaff_Runtime_Result_Codex_v1"
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
  - "Stop if implementation requires replacement/repeat semantics, Omen behavior, or an unprepared Essence row."
  - "Stop if public numeric output, optimizer/economics/advice, automation, or boundary closure enters scope."
---

# P2C Active Task

M42-A is proposed and ready for Claude audit. Exactly six prepared Perfect Essence quarterstaff rows use one shared atomic executor with uniform terminal-feasible non-fractured removal and a `crafted_count == 0` precondition. Replacement, stacking, repeat application, and broader crafted-capacity remain source-open and unimplemented.
