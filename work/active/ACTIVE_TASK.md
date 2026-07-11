---
schema_version: "2.0"
repo_head_at_last_update: "db83fea423071545c34fe7ad88b5ac7896e0fab6"
updated_at_utc: "2026-07-11T13:57:53Z"

status: "ready_for_claude"
next_actor: "claude"
active_task_id: "REPO_INTEGRITY_CHECK_PERFORMANCE_WAVE_D"

allowed_next_action: "claude_audit_repo_integrity_check_performance_wave_d"
forbidden_next_actions:
  - "accept_wave_d_without_chatgpt_user_gate"
  - "start_wave_c_or_m43a"
  - "move_delete_or_rewrite_existing_packages_reviews_or_history"
  - "change_runtime_mechanics_data_semantics_or_operation_admission"
  - "reduce_checksum_verification_to_changed_files"
  - "create_planner_optimizer_economics_advice_or_ranking"
  - "release_public_numeric_probabilities"
  - "close_source_provenance_mml_crafted_capacity_or_pd013"
  - "enable_automation_or_github_actions"
  - "agent_self_acceptance"

standing_boundaries_ref: "manifest/GitHub_Workflow_Protocol.md#standing-boundaries-for-active-task-dispatcher"
standing_boundaries_apply: true

current_result_path: "packages/proposed/P2C_Repo_Integrity_Check_Performance_Wave_D_Result_Codex_v1"
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
  - "Stop if SHA256SUMS behavior or bytes differ beyond the expected Wave D source-file hashes after staging."
  - "Stop if full-file checksum verification is weakened."
  - "Stop if any existing package or review byte changes."
  - "Stop if runtime, mechanics, data, admission, M43, optimizer/public output, automation, or boundary closure enters scope."
---

# P2C Active Task

Claude audits the proposed repo-integrity performance Wave D. Both checksum tools retain full Git-normalized index-byte verification while replacing per-file Git launches with one `git cat-file --batch` stream per tool. Wave A+B is accepted; Wave D remains proposed. Wave C, M43-A, runtime/mechanics, evidence movement, optimizer/public output, and automation remain closed.
