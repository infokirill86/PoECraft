---
schema_version: "2.0"
repo_head_at_last_update: "473958483ead92624d2a303266f844dbc978a79a"
updated_at_utc: "2026-07-08T20:55:00Z"

status: "audited_pending_user_gate"
next_actor: "chatgpt_user"
active_task_id: "M36_HETEROGENEOUS_CHAIN_DESIGN"

allowed_next_action: "chatgpt_user_gate_decision_on_m36_heterogeneous_chain_design"
forbidden_next_actions:
  - "implement_m36"
  - "implement_heterogeneous_operation_chains"
  - "implement_new_executable_operation"
  - "implement_annulment_variants_or_omens"
  - "implement_chaos_essence_fracture_desecrate_jawbone_or_reveal"
  - "expand_operation_scope"
  - "optimizer_advice_ranking_economics_ev"
  - "release_public_numeric_probabilities"
  - "close_source_provenance_mml_or_pd013"
  - "enable_supervised_auto_run"
  - "enable_github_actions"
  - "self_accept_m36"

standing_boundaries_ref: "manifest/GitHub_Workflow_Protocol.md#standing-boundaries-for-active-task-dispatcher"
standing_boundaries_apply: true

current_result_path: "packages/proposed/P2C_M36_Heterogeneous_Chain_Design_Codex_v1/"
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
  - "Stop if M36 implementation or heterogeneous-chain runtime would be started without explicit later gate."
  - "Stop if any additional operation would be marked accepted executable runtime without explicit later gate."
  - "Stop if full M35 or full M36 would be marked accepted."
  - "Stop if public numeric release, optimizer/economics/advice, automation, SOURCE/PROVENANCE closure, MML closure, or PD-013 closure appears."
---

# P2C Active Task

Current live task: ChatGPT/User gate decision on the M36 heterogeneous-chain design.

Next actor: ChatGPT/User (gate decision).

Allowed next action: decide. Claude audit verdict: GO WITH CHANGES — design correct and grounded on the reconciled registry; root SHA256SUMS drifted again (prior fix reverted) and was re-corrected; recommend enforcing the SHA check pre-push (`reviews/P2C_M36_Heterogeneous_Chain_Design_Audit_Claude_v1.md`).

No M36 implementation, heterogeneous-chain runtime, new executable operation, public numeric release, optimizer/economics/advice, automation, or boundary closure is authorized by this dispatcher.
