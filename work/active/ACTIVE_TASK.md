# P2C ACTIVE TASK

status: claude_audit_complete
next_actor: chatgpt_user
active_task_id: M33_P1_STATISTICAL_CONVERGENCE
claude_verdict: GO — all four M33-P0 blocking items resolved; recommend full M33 acceptance (advisory; acceptance stays with ChatGPT/User)
claude_verdict_detail: Verified by execution (6/6 M33 tests, full suite 92, test-only, no leak, SHA clean, ledger only records legitimate P0 acceptance — no self-accept). Tolerance is now a true 6-sigma binomial band (den cancels: |X-np|<=6*sigma), integer-exact; sample tiers 1024/4096/16384 assert ~1/sqrt(n) shrinkage (independently reproduced: band 0.081->0.041->0.020; biased p'=0.28 breaches n=16384); breaches hard-fail; broad 8-branch skewed fixture exercises family/group/capacity filtering. Shared kernel still code-enforced.
claude_watchpoints_m34: sqrt-n check is single-seed/directional (not multi-seed rate estimate); k=6 conservative to tiny biases; still single-step ordinary_add (multi-step is M34+); keep ACTIVE_TASK a thin dispatcher.
active_task_file: packages/proposed/P2C_M33_P1_Statistical_Convergence_Result_Codex_v1/00_README_FIRST.md
result_path: packages/proposed/P2C_M33_P1_Statistical_Convergence_Result_Codex_v1/
review_output_hint: reviews/M33_P1_Statistical_Convergence_Audit_Claude_v1.md
base_commit: f8b8f13
gate_decision: M33-P0 accepted as foundation partial only; M33-P1 authorized by ChatGPT/User on 2026-07-08.
builder_summary: M33-P1 replaced the P0 loose count tolerance with a statistically derived per-branch tolerance, added increasing sample-count tiers, fixed deterministic seed/divergence policy, and a broader skewed ordinary-add fixture with family/group/capacity filtering. Changes are test-only. Full M33 is not accepted. M34 remains closed.

## Prior P0 audit

- Claude audit file: `reviews/M33_Oracle_Convergence_Audit_Claude_v1.md`
- Verdict: GO WITH CHANGES.
- ChatGPT/User gate decision: accept M33-P0 as a foundation partial only, not full M33.
- Blocking items for full M33 are addressed by this M33-P1 delta for Claude audit.

## Current project checkpoint

- Operating Manifest v4: accepted baseline.
- Participant Voice Charter: accepted and active.
- GitHub workflow: active manual loop, no mailbox automation yet.
- GitHub baseline import Layer A: accepted and pinned as project-model GitHub baseline.
- M31 Monte Carlo policy: accepted after folded C-1 correction.
- M32 seeded MC harness: accepted.
- M33-P0 oracle-convergence foundation: accepted partial only.
- M33-P1 statistical convergence delta: ready for Claude audit.
- Full M33: not accepted.
- SOURCE/PROVENANCE, MML, and PD-013 remain open.
- M34: not open.

## M33-P1 result summary

Modified:

- `tests/monte_carlo/test_m33_oracle_convergence.py`

Added:

- `packages/proposed/P2C_M33_P1_Statistical_Convergence_Result_Codex_v1/`

M33-P1 covers:

- statistically derived per-branch tolerance;
- fixed deterministic seed policy;
- fixed divergence stop rule;
- increasing sample-count tiers;
- square-root shrinkage direction check;
- broader skewed accepted-ordinary-add fixture;
- family, group, and capacity filtering without new mechanics.

## Validation summary

Executed checks:

- `python -m pytest tests/monte_carlo/test_m33_oracle_convergence.py -q`
- `python -m pytest tests/monte_carlo -q`
- `python tools/validate_foundation.py`
- `python tools/validate_m4.py`
- `python -m pytest -q`
- `python tools/check_public_numeric_leaks.py packages/proposed/P2C_M33_P1_Statistical_Convergence_Result_Codex_v1`
- `python tools/check_sha256sums.py packages/proposed/P2C_M33_P1_Statistical_Convergence_Result_Codex_v1/SHA256SUMS.txt`
- `python tools/check_sha256sums.py SHA256SUMS.txt`
- `git diff --check`

All checks passed before rebase onto `f8b8f13`; conflict resolution was documentation/SHA only.

## Claude audit — DONE
Audit complete at HEAD `fcde807`. Verdict: **GO — recommend full M33 acceptance** (advisory). Full audit:
`reviews/M33_P1_Statistical_Convergence_Audit_Claude_v1.md`. All four M33-P0 blocking items resolved and
verified by execution; statistics now sound (true 6σ band, real 1/√n shrinkage, hard-fail divergence, broad
legality-filtered fixture). See verdict fields above.

## What ChatGPT/User should do next (gate decision — nothing auto-accepts)
1. Accept full M33 on this M33-P1 delta if desired.
2. Watchpoints are non-blocking (M34-era): multi-seed convergence-rate check; multi-step convergence.
3. M34 remains closed until a separate gate.

## Optional automation control (inactive)

This block is metadata only. It does not enable automation by itself.

```yaml
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
```

Manual mode means Kirill still sends each `Go`.

Future `supervised_auto_run` mode, if explicitly enabled later, means agents may pass the turn for a limited number of handoffs. It still cannot accept project truth, start a new milestone, update accepted ledgers, or bypass ChatGPT/User authority. Any listed stop trigger must set `status: blocked_for_human` and `next_actor: chatgpt_user`.

## Stop conditions still active

STOP_OR_ESCALATION if:

- the task starts M34;
- the task changes executable mechanics beyond test-only statistical validation;
- operation expansion beyond accepted `ordinary_add` appears;
- public output leaks probability values;
- optimizer/advice/ranking, economics, EV, or expected-attempts work appears;
- source/provenance, MML, or PD-013 closure is claimed;
- supervised auto-run or GitHub Actions are enabled.
