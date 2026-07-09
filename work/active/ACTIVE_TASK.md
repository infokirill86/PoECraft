---
schema_version: "2.0"
repo_head_at_last_update: "1947c735b453b0fadcd3088bdda95479a03c98b7"
updated_at_utc: "2026-07-09T11:20:00Z"

status: "audited_pending_user_gate"
next_actor: "chatgpt_user"
active_task_id: "M37_MECHANICS_VERIFICATION"

allowed_next_action: "chatgpt_user_gate_decision_on_m37_mechanics_verification"
forbidden_next_actions:
  - "implement_m37a"
  - "implement_chaos_runtime"
  - "mark_chaos_or_chaoslike_rows_accepted_executable_runtime"
  - "pin_base_chaos_to_whittling_without_user_gate"
  - "pin_base_chaos_to_uniform_random_without_source_audit"
  - "implement_essence_fracture_desecrate_jawbone_or_reveal_runtime"
  - "implement_annulment_variants_or_omens"
  - "implement_new_executable_operation"
  - "implement_chains_longer_than_two"
  - "implement_route_planner"
  - "optimizer_advice_ranking_economics_ev"
  - "release_public_numeric_probabilities"
  - "claim_server_truth"
  - "close_source_provenance_mml_or_pd013"
  - "enable_github_actions"
  - "enable_supervised_auto_run_or_watcher_automation"

standing_boundaries_ref: "manifest/GitHub_Workflow_Protocol.md#standing-boundaries-for-active-task-dispatcher"
standing_boundaries_apply: true

current_result_path: "packages/proposed/P2C_M37_Mechanics_Verification_Codex_v1/"
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
  - "Stop if standing boundaries are missing or unclear."
  - "Stop if source evidence and repo evidence conflict in a way requiring ChatGPT/User decision."
  - "Stop if M37-A implementation or Chaos runtime implementation would begin."
  - "Stop if any Chaos-like row would be marked accepted executable runtime."
  - "Stop if public numeric output, optimizer/economics/advice, automation, SOURCE/PROVENANCE closure, MML closure, or PD-013 closure enters scope."
---

# P2C Active Task

Current live task: ChatGPT/User gate decision on the M37 mechanics-verification package.

Next actor: ChatGPT/User (gate decision).

Allowed next action: decide (adopt as project-model policy). Claude audit verdict: GO — removal=uniform combined pool, add=combined generation_weight pool (side=capacity filter, not 50/50), Omens/Whittling are separate layers; project-model policy, not server truth (`reviews/P2C_M37_Mechanics_Verification_Audit_Claude_v1.md`).

M37 mechanics verification is source/provenance design work only. M37-A, Chaos runtime, executable Chaos admission, public numeric release, optimizer/economics/advice, automation, and SOURCE/PROVENANCE/MML/PD-013 closure remain closed pending separate explicit ChatGPT/User gates.
