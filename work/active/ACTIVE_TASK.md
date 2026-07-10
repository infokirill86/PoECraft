---
schema_version: "2.0"
repo_head_at_last_update: "253297846f8870ca72ce25915b2cccf7b14b6be6"
updated_at_utc: "2026-07-10T19:30:00Z"

status: "audited_pending_user_gate"
next_actor: "chatgpt_user"
active_task_id: "M40A_RARITY_PROGRESSION_RUNTIME"

allowed_next_action: "chatgpt_user_gate_decision_on_m40a_rarity_progression_runtime"
forbidden_next_actions:
  - "accept_m40a_without_chatgpt_user_gate"
  - "expand_m40a_beyond_authorized_ten_rows"
  - "implement_alchemy_or_multi_add"
  - "enable_essence_runtime"
  - "accept_whittling_or_omen_runtime"
  - "accept_new_operation_runtime"
  - "accept_mml_closure"
  - "implement_longer_chains"
  - "implement_planner"
  - "optimizer_economics_advice"
  - "release_public_numeric_probabilities"
  - "close_source_provenance_mml_or_pd013"
  - "enable_automation_or_github_actions"
  - "agent_self_acceptance"

standing_boundaries_ref: "manifest/GitHub_Workflow_Protocol.md#standing-boundaries-for-active-task-dispatcher"
standing_boundaries_apply: true

current_result_path: "packages/proposed/P2C_M40A_Rarity_Progression_Runtime_Result_Codex_v1"
current_review_path: "reviews/P2C_M40A_Rarity_Progression_Runtime_Audit_Claude_v1.md"

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
  - "Stop if runtime code, crafting mechanics, data semantics, operation admission, automation, accepted-truth update, SOURCE/PROVENANCE closure, MML closure, or PD-013 closure enters scope without explicit ChatGPT/User gate authorization."
---

# P2C Active Task

Current live task: ChatGPT/User gate decision on the audited M40-A rarity-progression runtime.

Next actor: ChatGPT/User (gate decision).

Allowed next action: decide. Claude verdict: GO — ten rarity-ladder rows run through one shared, data-driven single-add executor; the pool is built on an isolated copy at the TARGET rarity and the rarity change + added modifier commit atomically (verified in code + 204 tests); MML 44/70 & 35/50 read from data, no per-currency branches; fractured mods stay immutable/removal-protected (only the over-strict "must be suffix" assertion relaxed); mechanics_evidence/sources/project_scope updated as source-open project-model. Also adds the validate_active_task.py dispatcher guard (wired to pre-push). Non-blocking watchpoints for the gate: acknowledge (1) the deliberate scope widening to normal/magic starts, and (2) the accepted fractured-assertion relaxation. MML/SOURCE-PROVENANCE/PD-013 stay open (`reviews/P2C_M40A_Rarity_Progression_Runtime_Audit_Claude_v1.md`).

This is a proposed runtime delta only. It is not accepted until a ChatGPT/User gate. It does not admit Alchemy/Essence/Whittling/Omen/side/desecrated runtime, longer chains, planner/optimizer/economics/advice, public numeric output, or automation, and does not close MML, SOURCE/PROVENANCE, or PD-013.
