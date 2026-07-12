---
schema_version: "2.0"
repo_head_at_last_update: "74d9fcb25e213feff706cc97682fbe9e31238c60"
updated_at_utc: "2026-07-12T10:33:05Z"

status: "audited_pending_user_gate"
next_actor: "chatgpt_user"
active_task_id: "M47A1_JAWBONE_PLACEHOLDER_RUNTIME"

allowed_next_action: "chatgpt_user_gate_m47a1_after_claude_go"
forbidden_next_actions:
  - "accept_m47a1_without_chatgpt_user_gate"
  - "implement_reveal_or_select_d3_d5_sampling_policy"
  - "implement_echoes_omen_of_light_necromancy_lich_or_putrefaction"
  - "admit_multiple_placeholders_or_revealed_desecrated_fracture_runtime"
  - "add_conditional_retry_route_generation_planner_or_optimizer_behavior"
  - "release_public_numeric_probabilities"
  - "close_source_provenance_mml_crafted_capacity_or_pd013"
  - "enable_automation_or_github_actions"
  - "agent_self_acceptance"

standing_boundaries_ref: "manifest/GitHub_Workflow_Protocol.md#standing-boundaries-for-active-task-dispatcher"
standing_boundaries_apply: true

current_result_path: "packages/proposed/P2C_M47A1_Jawbone_Placeholder_Runtime_Result_Codex_v1"
current_review_path: "reviews/P2C_M47A1_Jawbone_Placeholder_Runtime_Audit_Claude_v1.md"

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
  - "Stop if M47-A1 requires selecting D3-D5 or implementing Reveal."
  - "Stop if revealed-Desecrated Fracture runtime or PD-013 closure enters scope."
  - "Stop if any row beyond the three authorized Jawbones is admitted."
  - "Stop if planner/optimizer behavior, public numeric output, automation, or boundary closure enters scope."
---

# P2C Active Task

M47 Mechanics Decision Closure is accepted. D1-A and D2-A are accepted project-base policies for the Jawbone clean core. Codex implemented the proposed M47-A1 runtime for exactly Gnawed, Preserved, and Ancient Jawbone, including canonical hidden placeholders, atomic D1/D2 transitions, exact/seeded execution, resolver and bounded-sequence parity, and the hidden-placeholder Fracture minimum-count/non-target rule.

Claude audited M47-A1 with verdict **GO** (`reviews/P2C_M47A1_Jawbone_Placeholder_Runtime_Audit_Claude_v1.md`): exactly the three authorized Jawbones admitted, D1-A/D2-A match the decided policy, single-Desecrated limit and fractured immutability enforced, no Reveal, the hidden-placeholder Fracture rule is the authorized one, atomic and fail-closed, additive-only integration, all tests pass.

Next: ChatGPT/User acceptance gate. M47-A1 is proposed, not accepted. Reveal, D3-D5, Echoes, Omen of Light, multiple placeholders, revealed-Desecrated Fracture runtime, and PD-013 remain closed.
