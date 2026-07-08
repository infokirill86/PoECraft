# P2C ACTIVE TASK

status: claude_audit_complete
next_actor: chatgpt_user
active_task_id: M34A_MULTI_SEED_MC_HARDENING
claude_verdict: GO — recommend M34-A acceptance (advisory; acceptance stays with ChatGPT/User)
claude_verdict_detail: Verified by execution — 4/4 M34-A tests pass, full suite 96, test-only, leak+SHA clean, ledger only carries prior M34-design acceptance (no self-accept). Matches the pinned contract exactly (seeds 34001/34002/34003, tiers 512/2048/8192, sigma 6) with a guard test. Multi-seed x multi-tier grid over the broad skewed fixture reuses the verified 6-sigma binomial tolerance; deterministic replay holds; negative-control forces a breach and asserts the diagnostic carries every replay field. Scope clean (single-step ordinary_add only; no M34-B/sequences).
claude_watchpoints: small fixed 3-seed set (fine per contract, could widen later); smallest-weight branch at tier 512 is a low-count regime where 6-sigma is weakly sensitive (larger tiers carry the signal); still single-step (M34-B is sequences).
active_task_file: packages/proposed/P2C_M34A_Multi_Seed_MC_Hardening_Result_Codex_v1/00_README_FIRST.md
result_path: packages/proposed/P2C_M34A_Multi_Seed_MC_Hardening_Result_Codex_v1/
review_output_hint: reviews/M34A_Multi_Seed_MC_Hardening_Audit_Claude_v1.md
base_commit: cd2f28e
gate_decision: M34 design accepted as plan; M34-A implementation authorized by ChatGPT/User on 2026-07-08.
builder_summary: M34-A implemented test-only multi-seed single-step MC hardening for accepted `ordinary_add`. It pins a fixed seed list, fixed sample tiers, and a 6-sigma-style per-branch binomial tolerance rule; hard-fails any non-negative-control breach; proves deterministic replay for fixed seed/run id; and includes a negative-control breach-reporting test. M34-B and full M34 remain closed.

## Gate decision recorded (2026-07-08, User)

- Accept the M34 MC-hardening design as the plan.
- Authorize M34-A implementation only.
- Do not start M34-B.
- Do not implement full M34 in one step.
- Scope: multi-seed single-step convergence hardening over accepted `ordinary_add` only.
- Pin execution contract before running.

## Pinned M34-A execution contract

- Fixed seed identifiers: `34001`, `34002`, `34003`.
- Fixed sample tiers: `512`, `2048`, `8192`.
- Tolerance policy: M33-P1-shaped wide per-branch binomial envelope with fixed multiplier `6`.
- Breach rule: any non-negative-control branch/tier/seed breach is a hard failure.
- Negative-control rule: explicitly marked negative-control must prove the suite can fail.
- Replay rule: same seed plus same run id must replay exactly.

## Current project checkpoint

- Operating Manifest v4: accepted baseline.
- Participant Voice Charter: accepted and active.
- GitHub workflow: active manual loop, no mailbox automation yet.
- GitHub baseline import Layer A: accepted and pinned as project-model GitHub baseline.
- M31 Monte Carlo policy: accepted after folded C-1 correction.
- M32 seeded MC harness: accepted.
- M33 oracle-convergence validation: accepted as completed for accepted `ordinary_add` only.
- M34 design: accepted as the plan.
- M34-A: ready for Claude audit.
- M34-B: not open.
- Full M34: not accepted.
- SOURCE/PROVENANCE, MML, and PD-013 remain open.

## M34-A result summary

Added:

- `tests/monte_carlo/test_m34a_multi_seed_hardening.py`
- `packages/proposed/P2C_M34A_Multi_Seed_MC_Hardening_Result_Codex_v1/`

M34-A covers:

- contract pinning;
- multi-seed single-step convergence hardening;
- deterministic replay across the fixed seed set;
- tolerance breach diagnostics;
- negative-control failure reporting;
- package/report leak safety.

## Validation summary

Executed checks:

- `python -m pytest tests/monte_carlo/test_m34a_multi_seed_hardening.py -q`
- `python -m pytest tests/monte_carlo -q`
- `python tools/validate_foundation.py`
- `python tools/validate_m4.py`
- `python -m pytest -q`
- `python tools/check_public_numeric_leaks.py packages/proposed/P2C_M34A_Multi_Seed_MC_Hardening_Result_Codex_v1`
- `python tools/check_sha256sums.py packages/proposed/P2C_M34A_Multi_Seed_MC_Hardening_Result_Codex_v1/SHA256SUMS.txt`
- `python tools/check_sha256sums.py SHA256SUMS.txt`
- `git diff --check`

All checks passed.

## Claude audit — DONE
Audit complete at HEAD `cd0fefc`. Verdict: **GO** (advisory). Full audit:
`reviews/M34A_Multi_Seed_MC_Hardening_Audit_Claude_v1.md`. Verified by execution; matches the pinned
contract; negative-control has teeth; scope clean. See verdict fields above.

## What ChatGPT/User should do next (gate decision — nothing auto-accepts)
1. Accept M34-A (multi-seed single-step hardening) if desired.
2. Authorize **M34-B** (short accepted-`ordinary_add` sequences) only as a separate later gate, with its own
   pinned contract.
3. M34-B / full M34 remain closed until then.

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

- the task starts M34-B without explicit ChatGPT/User authorization;
- the task implements multi-step or sequence validation;
- the task changes executable mechanics beyond test-only M34-A diagnostics;
- operation expansion beyond accepted `ordinary_add` appears;
- public output leaks probability values;
- optimizer/advice/ranking, economics, EV, or expected-attempts work appears;
- source/provenance, MML, or PD-013 closure is claimed;
- supervised auto-run or GitHub Actions are enabled.
