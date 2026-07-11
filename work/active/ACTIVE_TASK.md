---
schema_version: "2.0"
repo_head_at_last_update: "10ea24515380542c28ea52cddbc71037eeaacac7"
updated_at_utc: "2026-07-11T13:40:00Z"

status: "audited_pending_user_gate"
next_actor: "chatgpt_user"
active_task_id: "REPO_STRUCTURE_CLEANUP_WAVE_AB"

allowed_next_action: "chatgpt_user_gate_decision_on_repo_structure_cleanup_wave_ab"
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
current_review_path: "reviews/P2C_Repo_Structure_Cleanup_Wave_AB_Audit_Claude_v1.md"

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

Claude audit of Repo Structure Cleanup Wave A+B: verdict GO. Docs/tooling/routing cleanup only - PROVEN no runtime/data/mechanics change (empty src/data diff; foundation fingerprint unchanged at 230dc88). Verified: only the 3 authorized historical files removed from work/active (git history + packages/reviews untouched); work/active now has exactly one tracked file and the validator enforces it (10 tests pass); stale "only ordinary_add" claims in START_HERE/Workflow_Protocol/OPEN_BLOCKERS replaced with accepted-ledger references + "do not hardcode the changing inventory" (anti-restale); read order fixed (ACTIVE_TASK before orientation); all standing boundaries intact and the dispatcher's standing_boundaries_ref anchor survived the protocol trim (only the non-binding historical appendix removed).

Next: ChatGPT/User gate. Waves C (evidence lifecycle links) and D (checker scoping) remain separate/closed. M43 direction decision (sequences vs Alchemy) stays independent and pending. Review: reviews/P2C_Repo_Structure_Cleanup_Wave_AB_Audit_Claude_v1.md.

No runtime/mechanics/data/admission change, no accepted-package move, no evidence rewrite, no optimizer/public-output/automation is authorized by this cleanup.
