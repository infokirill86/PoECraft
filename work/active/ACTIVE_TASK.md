---
schema_version: "2.0"
repo_head_at_last_update: "b948dcbbb0e21b604291a18fdd08a55933e66991"
updated_at_utc: "2026-07-09T18:10:00Z"

status: "audited_pending_user_gate"
next_actor: "chatgpt_user"
active_task_id: "M39_GREATER_PERFECT_MML_DESIGN_VERIFICATION"

allowed_next_action: "chatgpt_user_gate_decision_on_m39_greater_perfect_mml_verification"
forbidden_next_actions:
  - "implement_runtime_code"
  - "accept_greater_or_perfect_runtime"
  - "accept_mml_closure"
  - "accept_whittling_or_omen_runtime"
  - "accept_new_operation_runtime"
  - "implement_longer_chains"
  - "implement_planner"
  - "optimizer_economics_advice"
  - "release_public_numeric_probabilities"
  - "close_source_provenance_mml_or_pd013"
  - "enable_automation_or_github_actions"
  - "agent_self_acceptance"

standing_boundaries_ref: "manifest/GitHub_Workflow_Protocol.md#standing-boundaries-for-active-task-dispatcher"
standing_boundaries_apply: true

current_result_path: "packages/proposed/P2C_M39_GreaterPerfect_MML_Design_Verification_Codex_v1/"
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
  - "Stop if runtime code, crafting mechanics, data semantics, operation admission, automation, accepted-truth update, SOURCE/PROVENANCE closure, MML closure, or PD-013 closure enters scope without explicit ChatGPT/User gate authorization."
---

# P2C Active Task

Current live task: ChatGPT/User gate decision on the M39 Greater/Perfect + MML design verification.

Next actor: ChatGPT/User (gate decision).

Allowed next action: decide. Claude verdict: GO — Greater/Perfect = op + shared MML add-pool filter (project-model, not server truth); Essences excluded (separate gate); admit Exalted/Chaos first; nothing admitted, all runtime gated (`reviews/P2C_M39_GreaterPerfect_MML_Design_Verification_Audit_Claude_v1.md`).

This is design/mechanics verification only. It does not implement runtime behavior, admit Greater/Perfect variants, close MML, close SOURCE/PROVENANCE, close PD-013, release public numeric output, or authorize automation.
