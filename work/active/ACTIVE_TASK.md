---
schema_version: "2.0"
repo_head_at_last_update: "596fcdb7f69a8c285ff5a51698eddd10e167bf3f"
updated_at_utc: "2026-07-10T09:40:00Z"

status: "audited_pending_user_gate"
next_actor: "chatgpt_user"
active_task_id: "SHA256_GIT_NORMALIZED_UPDATE_FIX"

allowed_next_action: "chatgpt_user_gate_decision_on_sha256_git_normalized_update_fix"
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
current_review_path: "reviews/P2C_SHA256_Git_Normalized_Update_Fix_Audit_Claude_v1.md"

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

Current live task: ChatGPT/User gate decision on the audited SHA256 git-normalized updater/checker fix.

Next actor: ChatGPT/User (gate decision).

Allowed next action: decide. Claude verdict: GO — both updater and checker now hash git-normalized (index) bytes for tracked files; recurring CRLF checksum drift closed by construction (proven by execution: forced-CRLF worktree still verifies PASS; regeneration is a no-op). No scope creep, no self-acceptance (`reviews/P2C_SHA256_Git_Normalized_Update_Fix_Audit_Claude_v1.md`).

M39-A MML Filter Interface is accepted after Claude GO and ChatGPT/User gate. The current proposed change is repo-integrity tooling only: tracked files are hashed and checked from Git index bytes to avoid CRLF/LF checksum drift. It does not change crafting runtime, mechanics, data semantics, operation admission, public output, optimizer/economics/advice, automation, or SOURCE/PROVENANCE/MML/PD-013 boundaries.
