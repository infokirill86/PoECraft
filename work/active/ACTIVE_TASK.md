---
schema_version: "2.0"
repo_head_at_last_update: "5122428d2e963a430a54bfd2878754dbfbee187a"
updated_at_utc: "2026-07-12T14:51:46Z"

status: "ready_for_claude"
next_actor: "claude"
active_task_id: "M47A2V_REVEAL_SAMPLING_VERIFICATION"

allowed_next_action: "claude_audit_m47a2v_reveal_sampling_verification"
forbidden_next_actions:
  - "accept_or_promote_d3_d5_from_observations_without_explicit_chatgpt_user_gate"
  - "implement_or_admit_reveal_or_echoes_runtime"
  - "implement_omen_of_light_necromancy_lich_or_putrefaction"
  - "admit_multiple_placeholders_or_revealed_desecrated_fracture_runtime"
  - "publish_captured_probability_results_or_crafting_advice"
  - "add_conditional_retry_route_generation_planner_or_optimizer_behavior"
  - "release_public_numeric_probabilities"
  - "close_source_provenance_mml_crafted_capacity_or_pd013"
  - "enable_automation_or_github_actions"
  - "agent_self_acceptance"

standing_boundaries_ref: "manifest/GitHub_Workflow_Protocol.md#standing-boundaries-for-active-task-dispatcher"
standing_boundaries_apply: true

current_result_path: "packages/proposed/P2C_M47A2V_Reveal_Sampling_Verification_Codex_v1"
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
  - "Stop if a D3-D5 candidate or limited observation set is represented as accepted mechanics."
  - "Stop if evidence tooling turns into Reveal or Echoes implementation/admission."
  - "Stop if D4 is inferred without reproducible setups and eligible-pool evidence."
  - "Stop if an external-source conflict is silently resolved."
  - "Stop if revealed-Desecrated Fracture runtime or PD-013 closure enters scope."
  - "Stop if planner/optimizer behavior, public numeric output, automation, or boundary closure enters scope."
---

# P2C Active Task

M47-A2 Reveal Offer Generation Design Verification is accepted as design-only after Claude GO audit. D3-A, D4-A, and D5-A remain proposed candidate models; no Reveal or Echoes runtime is authorized.

Codex created the proposed M47-A2V offline evidence-support layer: an in-game capture protocol, canonical observation schema, fail-closed validator/analyzer, decision criteria, and focused tests. The analyzer reports contradictions and uncertainty but cannot update runtime or accepted truth. D4 remains inconclusive without homogeneous reproducible setups and eligible-pool/weight snapshots. Ancient+Echoes MML persistence remains a separate unresolved conflict.

Next: Claude audits `packages/proposed/P2C_M47A2V_Reveal_Sampling_Verification_Codex_v1/`. D3-D5 acceptance, Reveal/Echoes runtime, named-Lich/Necromancy, Omen of Light, Putrefaction, revealed-Desecrated Fracture runtime, public numeric release, and PD-013 closure remain gated.
