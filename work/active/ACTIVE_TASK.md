---
schema_version: "2.0"
repo_head_at_last_update: "d73130cdc5f051cfbfb541b19b330d350f769f4c"
updated_at_utc: "2026-07-09T13:43:50Z"

status: "awaiting_user_gate"
next_actor: "chatgpt_user"
active_task_id: "POST_M37A_NEXT_GATE"

allowed_next_action: "chatgpt_user_decide_next_operation_or_omen_layer_or_chain_wave"
forbidden_next_actions:
  - "implement_whittling_runtime_without_explicit_gate"
  - "implement_omen_runtime_without_explicit_gate"
  - "implement_greater_or_perfect_chaos_without_explicit_gate"
  - "implement_chaos_variants_without_explicit_gate"
  - "implement_essence_fracture_desecrate_jawbone_or_reveal_runtime_without_explicit_gate"
  - "implement_annulment_variants_without_explicit_gate"
  - "implement_chains_longer_than_accepted_m36a_scope_without_explicit_gate"
  - "implement_route_planner_without_explicit_gate"
  - "optimizer_advice_ranking_economics_ev"
  - "release_public_numeric_probabilities"
  - "claim_server_truth"
  - "close_source_provenance_mml_or_pd013"
  - "enable_github_actions"
  - "enable_supervised_auto_run_or_watcher_automation"

standing_boundaries_ref: "manifest/GitHub_Workflow_Protocol.md#standing-boundaries-for-active-task-dispatcher"
standing_boundaries_apply: true

current_result_path: "packages/proposed/P2C_M37A_ChaosLike_RemoveThenAdd_Runtime_Result_Codex_v1/"
current_review_path: "reviews/P2C_M37A_ChaosLike_RemoveThenAdd_Runtime_Audit_Claude_v1.md"

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
  - "Stop if a next wave would require a new mechanics, operation-expansion, public-output, optimizer/economics, automation, SOURCE/PROVENANCE, MML, or PD-013 closure gate."
---

# P2C Active Task

Current live state: M37-A base Chaos-like Remove-Then-Add Runtime is accepted after Claude GO WITH CHANGES audit and ChatGPT/User gate.

Next actor: ChatGPT/User.

Allowed next action: decide the next operation, Omen layer, chain wave, or other project move.

Accepted runtime now includes `ordinary_add`, base Annulment, and base Chaos-like remove-then-add. Whittling, Omens, Greater/Perfect Chaos, Chaos variants, additional operations, public numeric release, optimizer/economics/advice, automation, and SOURCE/PROVENANCE/MML/PD-013 closure remain closed pending separate explicit ChatGPT/User gates.
