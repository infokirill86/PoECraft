---
schema_version: "2.0"
repo_head_at_last_update: "f2650b0355f1dac870be7daf6fb83a180c74ea02"
updated_at_utc: "2026-07-10T18:33:35Z"

status: "ready_for_claude"
next_actor: "claude"
active_task_id: "M40A_RARITY_PROGRESSION_RUNTIME"

allowed_next_action: "claude_audit_m40a_rarity_progression_runtime"
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

Current live task: Claude audit of the proposed M40-A Rarity Progression Runtime implementation.

Next actor: Claude (external implementation/mechanics audit).

Allowed next action: audit the proposed ten-row M40-A runtime, with target-rarity pool construction and atomicity as load-bearing evidence. M40-A is not accepted by this implementation commit.

All non-M40-A operations/modifiers, longer chains, planner/optimizer/economics/advice, public numeric output, automation, and SOURCE/PROVENANCE/broader-MML/PD-013 closure remain separately gated.
