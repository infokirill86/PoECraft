---
schema_version: "2.0"
repo_head_at_last_update: "420f337506d258ca6ceed3a653044947f73c6a69"
updated_at_utc: "2026-07-11T12:30:00Z"

status: "audited_pending_user_gate"
next_actor: "chatgpt_user"
active_task_id: "REPO_STRUCTURE_TRUTH_SURFACE_AUDIT"

allowed_next_action: "chatgpt_user_gate_decision_on_repo_structure_truth_surface_audit"
forbidden_next_actions:
  - "implement_cleanup_move_delete_or_archive_actions"
  - "accept_m43_or_start_m43a"
  - "change_runtime_mechanics_data_semantics_or_operation_admission"
  - "rewrite_or_delete_historical_evidence"
  - "create_planner_optimizer_economics_advice_or_ranking"
  - "release_public_numeric_probabilities"
  - "close_source_provenance_mml_crafted_capacity_or_pd013"
  - "enable_automation_or_github_actions"
  - "agent_self_acceptance"

standing_boundaries_ref: "manifest/GitHub_Workflow_Protocol.md#standing-boundaries-for-active-task-dispatcher"
standing_boundaries_apply: true

current_result_path: "packages/proposed/P2C_Repo_Structure_Truth_Surface_Audit_Codex_v1"
current_review_path: "reviews/P2C_Repo_Structure_Truth_Surface_Audit_Audit_Claude_v1.md"

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
  - "Stop if audit turns into cleanup, evidence deletion, accepted-truth change, or M43-A implementation."
  - "Stop if public numeric output, optimizer/economics/advice, automation, or boundary closure enters scope."
---

# P2C Active Task

Claude audits the repository structure/truth-surface findings: verdict GO. Findings independently verified by scanning the repo: TS-02 (four tracked files in work/active/, three historical), TS-03/04/05 (START_HERE.md:58 + Workflow_Protocol:179 + OPEN_BLOCKERS say "only ordinary_add executable" - stale vs 24 accepted rows), TS-01 (CLAUDE.md reads START_HERE/CURRENT_STATUS before ACTIVE_TASK - reads stalest files first), TS-09 (39 dirs in packages/proposed, accepted/ has only README). Posture is safe: evidence immutable, no blind deletion, cleanup staged (Waves A-D) and separately gated. repo_head_at_last_update clarification is correct.

Next: ChatGPT/User gate. Recommended follow-up = a separately gated cleanup task (Wave A+B first: destale the "only ordinary_add" first-read files by replacing volatile runtime lists with accepted-ledger references; remove the three historical work/active files from the current tree with git preserving history; require exactly one tracked file under work/active). Keep every accepted package/review byte-immutable. This is report-only; no cleanup applied. M43 direction decision (sequences vs Alchemy) stays independent and pending. Review: reviews/P2C_Repo_Structure_Truth_Surface_Audit_Audit_Claude_v1.md.

No cleanup, move, deletion, evidence rewrite, runtime/mechanics/data/admission change, optimizer, public output, or automation is authorized by this audit.
