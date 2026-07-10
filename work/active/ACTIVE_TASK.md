---
schema_version: "2.0"
repo_head_at_last_update: "b68ed5bc47782cd99290d35bc66a66152b7d1eed"
updated_at_utc: "2026-07-10T20:15:44Z"

status: "ready_for_claude"
next_actor: "claude"
active_task_id: "M41_NEXT_OPERATION_WAVE_DESIGN"

allowed_next_action: "claude_audit_m41_next_operation_wave_design"
forbidden_next_actions:
  - "implement_m41_runtime"
  - "admit_greater_or_perfect_essence_runtime"
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

current_result_path: "packages/proposed/P2C_M41_Next_Operation_Wave_Design_Codex_v1"
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

Current live task: Claude audits the proposed M41 next-operation-wave selection and design.

Next actor: Claude (external design/mechanics audit).

Allowed next action: audit the proposed Greater Essence M41-A boundary, the split from Perfect Essence, source grounding, and implementation acceptance contract.

This is design-only. No Essence, Alchemy, Omen, Fracture, Jawbone, Reveal, longer-chain, planner/optimizer/economics/advice, public numeric, automation, or boundary-closure runtime is authorized or accepted.
