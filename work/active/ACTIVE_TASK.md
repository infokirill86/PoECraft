# P2C ACTIVE TASK

status: awaiting_user_go_for_m34b
next_actor: chatgpt_user
active_task_id: M34A_ACCEPT_AND_PIN

current_gate_result: M34-A multi-seed MC hardening accepted as completed by ChatGPT/User on 2026-07-08.

current_paths:
- result_path: packages/proposed/P2C_M34A_Multi_Seed_MC_Hardening_Result_Codex_v1/
- review_path: reviews/M34A_Multi_Seed_MC_Hardening_Audit_Claude_v1.md

next_required_action:
- ChatGPT/User must explicitly authorize M34-B before any multi-step or sequence validation starts.
- M34-B and full M34 remain closed.

accepted_scope:
- Accepted `ordinary_add` only.
- M34-A single-step multi-seed hardening accepted.
- Pinned seeds: `34001`, `34002`, `34003`.
- Pinned sample tiers: `512`, `2048`, `8192`.
- Pinned tolerance multiplier: `6`.
- Deterministic replay accepted.
- Hard-fail breach diagnostics accepted.
- Negative-control failure proof accepted.

not_authorized:
- M34-B.
- Full M34.
- Multi-step / sequence validation.
- New executable mechanics.
- Operation expansion beyond accepted `ordinary_add`.
- Optimizer, advice, ranking, economics, EV, expected attempts.
- Public numeric probability release.
- Server-truth claims.
- SOURCE/PROVENANCE closure.
- MML closure.
- PD-013 closure.
- Supervised auto-run.
- GitHub Actions.

automation:
  mode: manual
  enabled: false
  max_handoffs: 0
  current_handoff_count: 0
  human_gate_required: true
  allowed_next_actors:
    - codex
    - claude
  stop_on:
    - NO_GO
    - GO_WITH_CHANGES_REQUIRES_DESIGN_DECISION
    - scope_expansion
    - missing_required_bytes
    - sha_mismatch
    - test_failure
    - dependency_or_provenance_uncertainty
    - builder_auditor_conflict
    - accepted_truth_update_needed
    - milestone_transition
    - max_handoffs_reached

stop_conditions:
- Stop if any agent starts M34-B without explicit ChatGPT/User authorization.
- Stop if multi-step or sequence validation is introduced without a new gate.
- Stop if executable mechanics are changed.
- Stop if operation expansion beyond accepted `ordinary_add` appears.
- Stop if public probability values are released.
- Stop if optimizer/advice/ranking/economics/EV/expected-attempts work appears.
- Stop if SOURCE/PROVENANCE, MML, or PD-013 closure is claimed.
- Stop if supervised auto-run or GitHub Actions are enabled.
