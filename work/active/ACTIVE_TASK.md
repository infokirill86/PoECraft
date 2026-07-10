---
schema_version: "2.0"
repo_head_at_last_update: "0006f2cfb8a211f3a3a5fc25c3587094dacea93f"
updated_at_utc: "2026-07-10T10:15:00Z"

status: "awaiting_user_gate"
next_actor: "chatgpt_user"
active_task_id: "POST_SHA256_FIX_NEXT_GATE"

allowed_next_action: "chatgpt_user_decide_greater_perfect_admission_or_next_project_move"
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

current_result_path: ""
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

Current live task: ChatGPT/User next-move gate. The SHA256 Git-normalized updater/checker fix is accepted (User gate 2026-07-10 after Claude GO); the recurring CRLF/LF checksum drift is closed structurally.

Next actor: ChatGPT/User (gate decision).

Allowed next action: decide the next project move — Greater/Perfect admission in controlled slices (Exalted + Chaos first, per accepted M39/M39-A), or another next wave. No package is currently in flight; nothing is queued for Codex or Claude until this gate.

Standing boundaries hold: no Greater/Perfect / Whittling/Omen / Essence runtime, no new operation, no longer chains, no planner/optimizer/economics/advice, no public numeric release, no automation/GitHub Actions, and no SOURCE/PROVENANCE / MML / PD-013 closure without an explicit ChatGPT/User gate.
