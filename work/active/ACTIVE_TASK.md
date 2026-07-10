---
schema_version: "2.0"
repo_head_at_last_update: "587e07839b3a695dfde6a2bfa7bcf9368fd0b584"
updated_at_utc: "2026-07-10T22:45:00Z"

status: "audited_pending_user_gate"
next_actor: "chatgpt_user"
active_task_id: "M41A_GREATER_ESSENCE_QUARTERSTAFF_RUNTIME"

allowed_next_action: "chatgpt_user_gate_decision_on_m41a_greater_essence_quarterstaff_runtime"
forbidden_next_actions:
  - "accept_m41a_without_chatgpt_user_gate"
  - "admit_perfect_lesser_or_corrupted_essence_runtime"
  - "decide_multiple_essence_stacking_replacement_or_capacity_semantics"
  - "accept_whittling_or_omen_runtime"
  - "implement_alchemy_fracture_desecrate_jawbone_or_reveal"
  - "implement_longer_chains_or_planner"
  - "optimizer_economics_advice"
  - "release_public_numeric_probabilities"
  - "close_source_provenance_mml_or_pd013"
  - "enable_automation_or_github_actions"
  - "agent_self_acceptance"

standing_boundaries_ref: "manifest/GitHub_Workflow_Protocol.md#standing-boundaries-for-active-task-dispatcher"
standing_boundaries_apply: true

current_result_path: "packages/proposed/P2C_M41A_Greater_Essence_Quarterstaff_Runtime_Result_Codex_v1"
current_review_path: "reviews/P2C_M41A_Greater_Essence_Quarterstaff_Runtime_Audit_Claude_v1.md"

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
  - "Stop if operation, essence-output, canonical modifier, scope, resolver, or fingerprint data disagree."
  - "Stop if crafted-capacity semantics become load-bearing beyond the existing shared Greater-only validation."
  - "Stop if any unauthorized Essence tier, operation, modifier layer, chain, public numeric output, optimizer/economics/advice, automation, or boundary closure enters scope."
---

# P2C Active Task

Current live task: ChatGPT/User gate decision on the audited M41-A Greater Essence quarterstaff runtime.

Next actor: ChatGPT/User (gate decision).

Allowed next action: decide. Claude verdict: GO — eight Greater Essence rows run through one shared deterministic guaranteed-add executor over the accepted M40-A atomic pattern: magic->rare, install exactly the row-declared mod with NO random draw (verified in code + exact==seeded==replay test), existing/fractured mods preserved, cross-file (operations/essence_outputs/modifier_index) consistency, fail-closed on wrong rarity/family-conflict/capacity/Perfect. All four prompt fixes present (project_scope activation, canonical index resolution, fingerprint delta pinned, crafted-capacity source-open-not-blocking). Codex did the AGENTS.md critique and did NOT silently encode crafted-capacity. Full suite 220 passed. Crafted-capacity + essence values stay project-model/source-open; MML/SOURCE-PROVENANCE/PD-013 stay open (`reviews/P2C_M41A_Greater_Essence_Quarterstaff_Runtime_Audit_Claude_v1.md`).

This is a proposed runtime delta only, not accepted until a ChatGPT/User gate. It does not admit Perfect/Lesser/Corrupted Essence, multi-Essence capacity, Omens, Whittling, Alchemy, Fracture/Desecrate/Jawbone/Reveal, longer chains, planner/optimizer/economics, public numeric output, or automation, and does not close crafted-capacity, MML, SOURCE/PROVENANCE, or PD-013.
