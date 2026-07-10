---
schema_version: "2.0"
repo_head_at_last_update: "0c494f931234fd5623b389890472ba90feee19f4"
updated_at_utc: "2026-07-10T16:30:00Z"

status: "audited_pending_user_gate"
next_actor: "chatgpt_user"
active_task_id: "M40_RARITY_PROGRESSION_FAMILY_DESIGN_VERIFICATION"

allowed_next_action: "chatgpt_user_gate_decision_on_m40_rarity_progression_family_design"
forbidden_next_actions:
  - "implement_m40_runtime"
  - "admit_transmutation_augmentation_regal_or_base_exalted"
  - "change_runtime_mechanics_or_data_semantics"
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

current_result_path: "packages/proposed/P2C_M40_Rarity_Progression_Family_Design_Verification_Codex_v1"
current_review_path: "reviews/P2C_M40_Rarity_Progression_Family_Design_Verification_Audit_Claude_v1.md"

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

Current live task: ChatGPT/User gate decision on the audited M40 Rarity Progression Family design verification.

Next actor: ChatGPT/User (gate decision).

Allowed next action: decide. Claude verdict: GO — ten rarity-ladder rows (Transmutation/Augmentation/Regal base+Greater/Perfect + base Exalted) verified as one shared data-driven single-add family; inventory and 44/70 & 35/50 thresholds match repo data; target-rarity pool build + atomic rarity+modifier commit is the correct new mechanic; base Exalted is the plain accepted ordinary_add wrapper (resolves the M39-B asymmetry). Design-only, nothing admitted. Non-blocking watchpoints for M40-A: rarity-transition (Transmutation/Regal) is the genuinely new mechanic and its atomicity/target-rarity proofs are load-bearing (slice if extra caution wanted); log 44/70 & 35/50 in mechanics_evidence as source-open with 0.3.0+PoE2DB refs; add the 0.3.0 source to sources.yaml. MML/SOURCE-PROVENANCE/PD-013 stay open (`reviews/P2C_M40_Rarity_Progression_Family_Design_Verification_Audit_Claude_v1.md`).

This is design/mechanics verification only. It does not implement M40 runtime, admit any rarity-progression row, admit base Exalted, close MML, close SOURCE/PROVENANCE, close PD-013, release public numeric output, or authorize automation.
