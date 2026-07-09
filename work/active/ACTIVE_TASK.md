---
schema_version: "2.0"
repo_head_at_last_update: "592bc4696c6321e2365c5fa8781d61386131e1aa"
updated_at_utc: "2026-07-09T21:20:33Z"

status: "ready_for_claude"
next_actor: "claude"
active_task_id: "SHA256_GIT_NORMALIZED_UPDATE_FIX"

allowed_next_action: "claude_audit_sha256_git_normalized_update_fix"
forbidden_next_actions:
  - "start_greater_or_perfect_runtime"
  - "enable_greater_or_perfect_exalted_or_chaos"
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

current_result_path: "packages/proposed/P2C_SHA256_Git_Normalized_Update_Fix_Codex_v1/"
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

Current live task: Claude audit of the proposed SHA256 Git-normalized updater/checker fix.

Next actor: Claude.

Allowed next action: audit `packages/proposed/P2C_SHA256_Git_Normalized_Update_Fix_Codex_v1/`.

M39-A MML Filter Interface is accepted after Claude GO and ChatGPT/User gate. The current proposed change is repo-integrity tooling only: tracked files are hashed and checked from Git index bytes to avoid CRLF/LF checksum drift. It does not change crafting runtime, mechanics, data semantics, operation admission, public output, optimizer/economics/advice, automation, or SOURCE/PROVENANCE/MML/PD-013 boundaries.
