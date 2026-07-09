---
schema_version: "2.0"
repo_head_at_last_update: "d383e9339c245c436198c5cdb6abbd4d7c910672"
updated_at_utc: "2026-07-09T14:12:25Z"

status: "ready_for_claude"
next_actor: "claude"
active_task_id: "M38_OPERATION_RESOLVER_VARIANT_MODIFIER_DESIGN"

allowed_next_action: "claude_audit_m38_operation_resolver_variant_modifier_design"
forbidden_next_actions:
  - "implement_m38_runtime"
  - "accept_greater_or_perfect_runtime"
  - "accept_whittling_or_omen_runtime"
  - "accept_additional_operation_runtime"
  - "implement_chains_longer_than_accepted_m36a_scope"
  - "implement_route_planner"
  - "optimizer_advice_ranking_economics_ev"
  - "release_public_numeric_probabilities"
  - "claim_server_truth"
  - "close_source_provenance_mml_or_pd013"
  - "enable_github_actions"
  - "enable_supervised_auto_run_or_watcher_automation"

standing_boundaries_ref: "manifest/GitHub_Workflow_Protocol.md#standing-boundaries-for-active-task-dispatcher"
standing_boundaries_apply: true

current_result_path: "packages/proposed/P2C_M38_Operation_Resolver_Variant_Modifier_Design_Codex_v1/"
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
  - "Stop if M38 audit would require implementation without a new Codex gate."
  - "Stop if a new runtime operation, variant, Omen layer, public numeric output, optimizer/economics/advice, automation, SOURCE/PROVENANCE closure, MML closure, or PD-013 closure enters scope."
---

# P2C Active Task

Current live task: Claude audit of the proposed M38 Operation Resolver / Variant & Modifier Layer design package.

Next actor: Claude.

Allowed next action: audit `packages/proposed/P2C_M38_Operation_Resolver_Variant_Modifier_Design_Codex_v1/`.

M38 is design-only and proposed. It does not implement a resolver, does not admit Greater/Perfect runtime, does not admit Whittling/Omen runtime, and does not accept additional operation runtime. Accepted runtime remains `ordinary_add`, base Annulment, and base Chaos-like remove-then-add.
