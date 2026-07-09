---
schema_version: "2.0"
repo_head_at_last_update: "9f4aae3f9f1aab5a13a6dcfcf754e6ce64d6c5ef"
updated_at_utc: "2026-07-09T10:04:58Z"

status: "awaiting_user_gate"
next_actor: "chatgpt_user"
active_task_id: "POST_M36A_NEXT_GATE"

allowed_next_action: "chatgpt_user_decide_next_chain_or_operation_admission_wave"
forbidden_next_actions:
  - "implement_chains_longer_than_two"
  - "implement_route_planner"
  - "implement_chaos_runtime"
  - "implement_essence_fracture_desecrate_jawbone_or_reveal_runtime"
  - "implement_new_executable_operation"
  - "implement_annulment_variants_or_omens"
  - "optimizer_advice_ranking_economics_ev"
  - "release_public_numeric_probabilities"
  - "close_source_provenance_mml_or_pd013"
  - "enable_github_actions"
  - "enable_supervised_auto_run_or_watcher_automation"

standing_boundaries_ref: "manifest/GitHub_Workflow_Protocol.md#standing-boundaries-for-active-task-dispatcher"
standing_boundaries_apply: true

current_result_path: ""
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
  - "Stop if any next wave would start without explicit ChatGPT/User authorization."
  - "Stop if chains longer than two, route planning, a new operation, public numeric release, optimizer/economics/advice, GitHub Actions, watcher automation, SOURCE/PROVENANCE closure, MML closure, or PD-013 closure appears without a separate gate."
---

# P2C Active Task

Current live task: ChatGPT/User next gate after M36-A acceptance.

Next actor: ChatGPT/User.

Allowed next action: decide the next chain or operation-admission wave.

M36-A is accepted. Full M36 beyond M36-A, longer chains, route planning, additional operations, public numeric release, optimizer/economics/advice, automation, and SOURCE/PROVENANCE/MML/PD-013 closure remain closed pending separate explicit gates.
