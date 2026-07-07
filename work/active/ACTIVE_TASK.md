# P2C ACTIVE TASK

status: claude_audit_complete
next_actor: chatgpt_user
active_task_id: M32_A1_A2_BASELINE_HYGIENE
active_task_file: work/active/M32_A1_A2_Baseline_Hygiene_Task.md
result_path: packages/proposed/P2C_M32_A1_A2_Baseline_Hygiene_Result_Codex_v1/
expected_output_dir: packages/proposed/P2C_M32_A1_A2_Baseline_Hygiene_Result_Codex_v1/
review_path: reviews/M32_A1_A2_Baseline_Hygiene_Audit_Claude_v1.md
base_commit: e981202
claude_verdict: GO (advisory; acceptance stays with ChatGPT/User)
claude_verdict_detail: A (A1/A2 baseline hygiene) = GO, verified by execution — deps declared, restored kernel tests cover the M32 load-bearing imports, 86/86 tests pass on a clean run, ledgers untouched, baseline pin re-established as honest traceability. B (supervised auto-run protocol metadata) = GO — documentation only; mode manual / enabled false / max_handoffs 0 / human_gate_required true; no GitHub Actions/watcher/automation; cannot accept truth, update ledgers, or start M33; plain-language summary requirement present.
claude_forward_notes: (1) Layer A is now traceable but not byte-verified in-repo against the prior accepted package; a separate SOURCE_BUNDLE / byte comparison is the remaining step before accepting Layer A as truth. (2) Minor: a bare pytest hit a Windows temp-dir permission error; passes with a writable --basetemp — worth a one-line run-doc note.
builder_summary: A1/A2 baseline-hygiene result prepared only for the proposed GitHub baseline import. Dependencies are declared in repo config; restored kernel tests cover the imported load-bearing layers used by M32; prior accepted baseline package SHA/pin is documented for audit traceability. Layer A remains proposed and is not accepted truth.

## Gate decision recorded (2026-07-07, User)

- M32 seeded MC harness (Layer B): ACCEPTED as a passing milestone, on Claude's GO audit
  (`reviews/M32_Audit_Claude_v1.md`).
- GitHub baseline import / repo consolidation (Layer A): NOT accepted; remains PROPOSED, not
  accepted project truth, until required changes A1 and A2 are cleared.

## Current project checkpoint

- Operating Manifest v4: accepted baseline.
- Participant Voice Charter: accepted and active.
- GitHub workflow: active manual loop, no mailbox automation yet.
- M31 Monte Carlo policy: accepted after folded C-1 correction.
- M32 seeded MC harness: accepted (Layer B).
- GitHub baseline import: PROPOSED (Layer A), pending Claude audit of this A1/A2 hygiene result.
- M33: not open.
- M26-M30 operation mechanics blueprint: open/context only, not accepted.

## Claude audit — DONE
Audit complete at repo HEAD `85b0236`. Verdict: **GO** (advisory). Full audit in
`reviews/M32_A1_A2_Baseline_Hygiene_Audit_Claude_v1.md`. A1/A2 verified by execution (86/86 tests pass,
integrity clean, ledgers untouched); auto-run protocol metadata is safe docs-only. See forward notes above.

## What ChatGPT/User should do next (gate decision — nothing auto-accepts)
1. Decide whether the GitHub baseline import (Layer A) is now accepted as project truth, or held pending
   the byte-level SOURCE_BUNDLE (forward note 1).
2. If byte-level assurance is wanted first, route a SOURCE_BUNDLE / FULL_REPRODUCIBILITY_BUNDLE task to Codex.
3. M33 (oracle convergence) remains closed until Layer A acceptance is decided.

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

- the delta starts M33;
- the delta introduces new executable mechanics;
- restored tests require importing broad operation/runtime layers outside the A1/A2 hygiene target;
- imported baseline/support files are treated as accepted project truth without Claude audit and ChatGPT/User acceptance;
- public output leaks probability values;
- optimizer/advice/ranking or public numeric release appears;
- source/provenance, MML, or PD-013 closure is claimed.
