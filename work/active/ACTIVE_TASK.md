---
schema_version: "2.0"
repo_head_at_last_update: "804583e896dde3b71319d41dbeaefe56a96a1e94"
updated_at_utc: "2026-07-09T13:05:00Z"

status: "audited_pending_user_gate"
next_actor: "chatgpt_user"
active_task_id: "AGENT_ROLE_PACKS_IMPLEMENTATION"

allowed_next_action: "chatgpt_user_gate_decision_on_agent_role_packs_implementation"
forbidden_next_actions:
  - "self_accept_role_pack_implementation"
  - "change_runtime_code"
  - "change_crafting_mechanics"
  - "change_data_semantics"
  - "admit_new_operation_runtime"
  - "implement_m38_runtime"
  - "enable_automation_or_github_actions"
  - "close_source_provenance_mml_or_pd013"
  - "update_accepted_truth_without_gate"

standing_boundaries_ref: "manifest/GitHub_Workflow_Protocol.md#standing-boundaries-for-active-task-dispatcher"
standing_boundaries_apply: true

current_result_path: "packages/proposed/P2C_Agent_Role_Packs_Implementation_Codex_v1/"
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
  - "Stop if audit would require implementation changes without a new Codex gate."
  - "Stop if runtime code, crafting mechanics, data semantics, operation admission, automation, accepted-truth update, SOURCE/PROVENANCE closure, MML closure, or PD-013 closure enters scope."
---

# P2C Active Task

Current live task: ChatGPT/User gate decision on the agent role-packs implementation.

Next actor: ChatGPT/User (gate decision).

Allowed next action: decide. Claude verdict: GO — compact AGENTS.md/CLAUDE.md/Agent_Role_Pack created; all 3 refinements folded in (references accepted doctrine; hook-activation + read-receipt in AGENTS.md); docs-only, gate preserved (`reviews/P2C_Agent_Role_Packs_Implementation_Audit_Claude_v1.md`).

This is workflow/protocol implementation only. It creates compact `AGENTS.md`, `CLAUDE.md`, and `manifest/Agent_Role_Pack.md`. It does not change runtime code, crafting mechanics, data semantics, operation admission, automation, or accepted project truth.
