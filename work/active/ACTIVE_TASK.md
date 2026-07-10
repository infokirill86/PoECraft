---
schema_version: "2.0"
repo_head_at_last_update: "ce1e46abb0fcce067def9f9165e59ab2b5089e1d"
updated_at_utc: "2026-07-10T11:20:00Z"

status: "audited_pending_user_gate"
next_actor: "chatgpt_user"
active_task_id: "M39B_GREATER_PERFECT_EXALTED_CHAOS_RUNTIME"

allowed_next_action: "chatgpt_user_gate_decision_on_m39b_greater_perfect_exalted_chaos_runtime"
forbidden_next_actions:
  - "accept_m39b_without_chatgpt_user_gate"
  - "admit_base_exalted_wrapper"
  - "admit_other_greater_or_perfect_families"
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

current_result_path: "packages/proposed/P2C_M39B_GreaterPerfect_Exalted_Chaos_Runtime_Result_Codex_v1/"
current_review_path: "reviews/P2C_M39B_GreaterPerfect_Exalted_Chaos_Runtime_Audit_Claude_v1.md"

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

Current live task: ChatGPT/User gate decision on the audited M39-B Greater/Perfect Exalted + Chaos runtime batch.

Next actor: ChatGPT/User (gate decision).

Allowed next action: decide. Claude verdict: GO — four rows (greater/perfect exalted+chaos) admitted as project-model runtime via shared kernels; Exalted = accepted ordinary_add + row-declared MML; Chaos = accepted base uniform non-fractured removal + MML on the post-removal add only (verified in code); base exalted and all other families/variants/modifiers fail closed; full suite 160 passes. Two non-blocking watchpoints: confirm the base-Exalted asymmetry is intended, and log the 35/50 MML thresholds in mechanics_evidence as source-open. MML/SOURCE-PROVENANCE/PD-013 stay open (`reviews/P2C_M39B_GreaterPerfect_Exalted_Chaos_Runtime_Audit_Claude_v1.md`).
