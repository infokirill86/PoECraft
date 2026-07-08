---
schema_version: "2.0"
repo_head_at_last_update: "a12d5819d272422ae29a071775ab15003e6cd88f"
updated_at_utc: "2026-07-09T08:20:00Z"

status: "audited_pending_user_gate"
next_actor: "chatgpt_user"
active_task_id: "REPO_INTEGRITY_SHA_FLOOR"

allowed_next_action: "chatgpt_user_gate_decision_on_repo_integrity_sha_floor"
forbidden_next_actions:
  - "implement_m36a"
  - "implement_heterogeneous_chain_runtime"
  - "implement_new_executable_operation"
  - "change_mechanics_or_data_semantics"
  - "enable_github_actions"
  - "enable_supervised_auto_run_or_watcher_automation"
  - "optimizer_advice_ranking_economics_ev"
  - "release_public_numeric_probabilities"
  - "close_source_provenance_mml_or_pd013"
  - "self_accept_repo_integrity_sha_floor"

standing_boundaries_ref: "manifest/GitHub_Workflow_Protocol.md#standing-boundaries-for-active-task-dispatcher"
standing_boundaries_apply: true

current_result_path: "packages/proposed/P2C_Repo_Integrity_SHA_Floor_Codex_v1/"
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
  - "Stop if M36-A implementation or heterogeneous-chain runtime would be started."
  - "Stop if any new executable operation, mechanics/data semantic change, public numeric release, optimizer/economics/advice, automation, SOURCE/PROVENANCE closure, MML closure, or PD-013 closure appears."
---

# P2C Active Task

Current live task: ChatGPT/User gate decision on the repo-integrity SHA floor.

Next actor: ChatGPT/User (gate decision).

Allowed next action: decide. Claude audit verdict: GO WITH CHANGES — updater tool + rule correct, but the floor was delivered with a still-drifted manifest (I regenerated it) and needs a pre-push hook for enforcement (`reviews/P2C_Repo_Integrity_SHA_Floor_Audit_Claude_v1.md`).

M36 heterogeneous-chain design is accepted as design-only. M36-A implementation remains closed pending a separate explicit ChatGPT/User gate.
