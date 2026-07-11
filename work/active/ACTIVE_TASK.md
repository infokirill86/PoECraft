---
schema_version: "2.0"
repo_head_at_last_update: "5d56accc13990b9b95a602defa57f075a1fd42b5"
updated_at_utc: "2026-07-11T13:06:51Z"

status: "ready_for_claude"
next_actor: "claude"
active_task_id: "REPO_STRUCTURE_CLEANUP_WAVE_AB"

allowed_next_action: "claude_audit_repo_structure_cleanup_wave_ab"
forbidden_next_actions:
  - "accept_cleanup_without_chatgpt_user_gate"
  - "start_m43a_or_change_m43_status"
  - "move_or_rewrite_existing_packages_reviews_or_history"
  - "change_runtime_mechanics_data_semantics_or_operation_admission"
  - "create_planner_optimizer_economics_advice_or_ranking"
  - "release_public_numeric_probabilities"
  - "close_source_provenance_mml_crafted_capacity_or_pd013"
  - "enable_automation_or_github_actions"
  - "agent_self_acceptance"

standing_boundaries_ref: "manifest/GitHub_Workflow_Protocol.md#standing-boundaries-for-active-task-dispatcher"
standing_boundaries_apply: true

current_result_path: "packages/proposed/P2C_Repo_Structure_Cleanup_Wave_AB_Result_Codex_v1"
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
  - "Stop if any pre-existing package or review byte changed."
  - "Stop if cleanup expands beyond authorized Wave A+B."
  - "Stop if runtime, mechanics, data, operation admission, M43, public output, optimizer/economics/advice, automation, or boundary closure enters scope."
---

# P2C Active Task

Claude audits the proposed Repository Structure Cleanup Wave A+B result. The cleanup leaves one tracked live dispatcher, de-stales first-read truth surfaces, and adds fail-closed single-dispatcher validation. Existing packages/reviews remain unchanged; M43-A and all runtime/mechanics work remain closed.
