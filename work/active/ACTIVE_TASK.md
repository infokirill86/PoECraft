---
schema_version: "2.0"
repo_head_at_last_update: "f009c1e5a7bbad9434e7c233e0acdbd24e064d5e"
updated_at_utc: "2026-07-09T17:20:21Z"

status: "ready_for_claude"
next_actor: "claude"
active_task_id: "M38A_OPERATION_RESOLVER_SKELETON"

allowed_next_action: "claude_audit_m38a_operation_resolver_skeleton"
forbidden_next_actions:
  - "accept_m38a_without_chatgpt_user_gate"
  - "accept_greater_or_perfect_runtime"
  - "accept_whittling_or_omen_runtime"
  - "accept_side_or_desecrated_modifier_runtime"
  - "accept_new_operation_runtime"
  - "implement_longer_chains"
  - "implement_route_planner"
  - "optimizer_economics_advice"
  - "release_public_numeric_probabilities"
  - "close_source_provenance_mml_or_pd013"
  - "enable_automation_or_github_actions"
  - "agent_self_acceptance"

standing_boundaries_ref: "manifest/GitHub_Workflow_Protocol.md#standing-boundaries-for-active-task-dispatcher"
standing_boundaries_apply: true

current_result_path: "packages/proposed/P2C_M38A_Operation_Resolver_Skeleton_Result_Codex_v1/"
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
  - "Stop if audit would require implementation changes without a new Codex gate."
  - "Stop if runtime code beyond the M38-A resolver skeleton, crafting mechanics, data semantics, new operation admission, automation, accepted-truth update, SOURCE/PROVENANCE closure, MML closure, or PD-013 closure enters scope."
---

# P2C Active Task

Current live task: Claude audit of the proposed M38-A operation resolver skeleton.

Next actor: Claude.

Allowed next action: audit `packages/proposed/P2C_M38A_Operation_Resolver_Skeleton_Result_Codex_v1/`.

M38 design is accepted. M38-A implementation is proposed only and not accepted. M38-A adds a single-operation resolver skeleton and fail-closed admission checks for already accepted `ordinary_add`, base Annulment, and base Chaos-like runtime. It does not admit Greater/Perfect variants, Whittling/Omen layers, side/desecrated modifier runtime, new operations, longer chains, planner behavior, public numeric output, automation, or SOURCE/PROVENANCE/MML/PD-013 closure.
