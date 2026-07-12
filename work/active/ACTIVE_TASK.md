---
schema_version: "2.0"
repo_head_at_last_update: "ac29248cfca909130f035da3df06349d4c7d7e8e"
updated_at_utc: "2026-07-12T10:10:00Z"

status: "audited_pending_user_gate"
next_actor: "chatgpt_user"
active_task_id: "M47_DESECRATED_JAWBONE_REVEAL_MECHANICS_DESIGN"

allowed_next_action: "chatgpt_user_gate_decision_on_m47_desecrated_jawbone_reveal_mechanics_design"
forbidden_next_actions:
  - "implement_or_admit_jawbone_reveal_desecrated_or_related_omen_runtime"
  - "silently_resolve_pd013_or_source_conflicts"
  - "extend_m46a_to_desecrated_states"
  - "admit_putrefaction_multi_placeholder_or_corruption_behavior"
  - "add_conditional_retry_route_generation_planner_or_optimizer_behavior"
  - "release_public_numeric_probabilities"
  - "close_source_provenance_mml_crafted_capacity_or_pd013"
  - "enable_automation_or_github_actions"
  - "agent_self_acceptance"

standing_boundaries_ref: "manifest/GitHub_Workflow_Protocol.md#standing-boundaries-for-active-task-dispatcher"
standing_boundaries_apply: true

current_result_path: "packages/proposed/P2C_M47_Desecrated_Jawbone_Reveal_Mechanics_Design_Codex_v1"
current_review_path: "reviews/P2C_M47_Desecrated_Jawbone_Reveal_Mechanics_Design_Audit_Claude_v1.md"

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
  - "Stop if M47 design is treated as runtime authorization or accepted mechanics."
  - "Stop if prepared YAML policy is promoted without source or User gate."
  - "Stop if the documentation-versus-emulator Fracture conflict is silently resolved."
  - "Stop if planner/optimizer behavior, public numeric output, automation, or boundary closure enters scope."
---

# P2C Active Task

Claude audit of M47 Desecrated/Jawbone/Reveal Mechanics Design: verdict GO (design-only; jawbone rows + reveal_desecrated stay blocked; nothing admitted). Matches Kirill's ground truth: Jawbone -> one UNREVEALED placeholder (fixed side, consumes that side's capacity) -> Reveal offers THREE, installs one canonical modifier desecrated:true on the same side; single-Desecrated limit; Ancient Jawbone MML with family-fallback; fractured immutable; desecrated != crafted; revealed cannot gain fractured until PD-013. Reroll (Echoes) and targeted removal (Omen of Light) correctly split off. Uses the existing DesecratedPlaceholder domain type (no new algebra). Surfaces 8 decisions (D1-D8) and refuses runtime until answered - candidate YAML is not truth.

Decision routing for the gate: Kirill has ALREADY answered several in chat (ratify, not re-deliberate): Reveal=1-of-3; single-desecrated/no-rune; M47-D7 Fracture<->Desecrated (unrevealed = excluded-from-target-but-counts-toward-4 = 1-of-3; revealed = valid Fracture target -> fractured+desecrated); Echoes reroll = separate currency, same mod can reappear, tier-level. STILL OPEN, need in-game verification before M47-A (probability-affecting): D4 exact Reveal sampling algorithm (the critical one), D3 exclusive-offer guarantee, D2 full-item replacement, D1 side selection, D5 insufficient pool. Recommend M47-A only after D1-D6 decided; don't build a state shell before the offer policy is pinned. Review: reviews/P2C_M47_Desecrated_Jawbone_Reveal_Mechanics_Design_Audit_Claude_v1.md.

This is mechanics verification only. It admits no Desecrated/Jawbone/Reveal runtime, decides no offer/sampling model, closes no PD-013/MML/SOURCE-PROVENANCE/crafted-capacity, and releases no public numbers.
