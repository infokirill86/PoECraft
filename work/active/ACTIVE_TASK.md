---
schema_version: "2.0"
repo_head_at_last_update: "092c627274e475d567a9b18ff87eb0ae5c4feaf3"
updated_at_utc: "2026-07-10T19:56:12Z"

status: "awaiting_user_gate"
next_actor: "chatgpt_user"
active_task_id: "POST_M40A_NEXT_GATE"

allowed_next_action: "chatgpt_user_decide_next_operation_or_modifier_wave"
forbidden_next_actions:
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

Current live task: ChatGPT/User decides the next operation or modifier wave after accepted M40-A.

Next actor: ChatGPT/User (gate decision).

Allowed next action: choose the next separately gated operation or modifier wave. No new runtime/mechanics work is authorized by this acceptance record.

M40-A and the ACTIVE_TASK validator/pre-push guard are accepted. Alchemy/Essence/Whittling/Omen/side/desecrated runtime, longer chains, planner/optimizer/economics/advice, public numeric output, automation, and MML/SOURCE-PROVENANCE/PD-013 closure remain closed.
