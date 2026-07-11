---
schema_version: "2.0"
repo_head_at_last_update: "22f8cc2de295bab63c857a247d3dc6ed23d37309"
updated_at_utc: "2026-07-11T18:45:53Z"

status: "ready_for_claude"
next_actor: "claude"
active_task_id: "M44A_ALCHEMY_RUNTIME"

allowed_next_action: "claude_audit_m44a_alchemy_runtime"
forbidden_next_actions:
  - "accept_m44a_without_chatgpt_user_gate"
  - "admit_alchemy_variants_omens_whittling_or_other_item_classes"
  - "admit_fractured_input_alchemy"
  - "change_accepted_ordinary_add_legality_capacity_or_weighting"
  - "expose_internal_alchemy_adds_as_caller_visible_sequence_steps"
  - "add_conditional_retry_route_generation_planner_or_optimizer_behavior"
  - "release_public_numeric_probabilities"
  - "close_source_provenance_mml_crafted_capacity_or_pd013"
  - "enable_automation_or_github_actions"
  - "agent_self_acceptance"

standing_boundaries_ref: "manifest/GitHub_Workflow_Protocol.md#standing-boundaries-for-active-task-dispatcher"
standing_boundaries_apply: true

current_result_path: "packages/proposed/P2C_M44A_Alchemy_Runtime_Result_Codex_v1"
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
  - "Stop if Alchemy does not rebuild the accepted ordinary pool after every internal add."
  - "Stop if any failed intermediate add exposes a partial Rare state or consumes the operation."
  - "Stop if direct/resolver or M43-A one-step parity fails."
  - "Stop if fractured input, variants, Omens, other item classes, planner/optimizer behavior, public numeric output, automation, or boundary closure enters scope."
---

# P2C Active Task

Claude audits the proposed M44-A base-Alchemy runtime. The implementation admits one non-fractured quarterstaff operation: Normal/Magic input, isolated empty Rare working state, four sequential internal draws through the accepted ordinary weighted-add pool with branch-state rebuild, and one atomic commit. Any failure returns the unchanged input with no consumption. The four internal adds are not caller-visible M43-A steps. M44-A remains proposed; fractured input, variants, Omens/modifiers, other item classes, planner/optimizer behavior, public numeric release, automation, and boundary closures remain closed.
