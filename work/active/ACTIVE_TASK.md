---
schema_version: "2.0"
repo_head_at_last_update: "3a9db200ac367e7c441074d27c6803f15a67c752"
updated_at_utc: "2026-07-09T12:34:10Z"

status: "ready_for_claude"
next_actor: "claude"
active_task_id: "M37A_CHAOSLIKE_REMOVE_THEN_ADD_RUNTIME"

allowed_next_action: "claude_audit_m37a_chaoslike_remove_then_add_runtime"
forbidden_next_actions:
  - "self_accept_m37a"
  - "implement_whittling_runtime"
  - "implement_omen_runtime"
  - "implement_greater_or_perfect_chaos"
  - "implement_essence_fracture_desecrate_jawbone_or_reveal_runtime"
  - "implement_annulment_variants"
  - "implement_chains_longer_than_accepted_m36a_scope"
  - "implement_route_planner"
  - "optimizer_advice_ranking_economics_ev"
  - "release_public_numeric_probabilities"
  - "claim_server_truth"
  - "close_source_provenance_mml_or_pd013"
  - "enable_github_actions"
  - "enable_supervised_auto_run_or_watcher_automation"

standing_boundaries_ref: "manifest/GitHub_Workflow_Protocol.md#standing-boundaries-for-active-task-dispatcher"
standing_boundaries_apply: true

current_result_path: "packages/proposed/P2C_M37A_ChaosLike_RemoveThenAdd_Runtime_Result_Codex_v1/"
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
  - "Stop if M37-A audit would require implementation changes without a new Codex gate."
  - "Stop if public numeric output, optimizer/economics/advice, automation, SOURCE/PROVENANCE closure, MML closure, or PD-013 closure enters scope."
---

# P2C Active Task

Current live task: Claude audit of the proposed M37-A base Chaos-like remove-then-add runtime package.

Next actor: Claude.

Allowed next action: audit `packages/proposed/P2C_M37A_ChaosLike_RemoveThenAdd_Runtime_Result_Codex_v1/`.

M37-A is proposed, not accepted. Base Chaos-like runtime is the only new proposed executable path. Whittling, Omens, Greater/Perfect Chaos, additional operations, public numeric release, optimizer/economics/advice, automation, and SOURCE/PROVENANCE/MML/PD-013 closure remain closed pending separate explicit ChatGPT/User gates.
