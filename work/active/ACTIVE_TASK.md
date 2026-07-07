# P2C ACTIVE TASK

status: ready_for_claude
next_actor: claude
active_task_id: M32_A1_A2_BASELINE_HYGIENE
active_task_file: work/active/M32_A1_A2_Baseline_Hygiene_Task.md
result_path: packages/proposed/P2C_M32_A1_A2_Baseline_Hygiene_Result_Codex_v1/
expected_output_dir: packages/proposed/P2C_M32_A1_A2_Baseline_Hygiene_Result_Codex_v1/
review_output_hint: reviews/M32_A1_A2_Baseline_Hygiene_Audit_Claude_v1.md
base_commit: e981202
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

## Claude audit target

Audit the A1/A2 baseline-hygiene result at:

`packages/proposed/P2C_M32_A1_A2_Baseline_Hygiene_Result_Codex_v1/`

Claude should verify:

1. A1 dependency declaration clears clean-clone reproducibility for the imported runtime and test suite.
2. A2 restored tests cover the load-bearing imported kernel that M32 depends on.
3. The prior accepted baseline package SHA/pin is re-established for audit traceability without accepting imported baseline truth.
4. No M33, new mechanics, optimizer/advice/ranking, public numeric release, source/provenance closure, MML closure, PD-013 closure, or accepted-ledger truth update was introduced.

Return audit under:

`reviews/M32_A1_A2_Baseline_Hygiene_Audit_Claude_v1.md`

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
