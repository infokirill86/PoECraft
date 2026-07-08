# P2C ACTIVE TASK

status: claude_audit_complete
next_actor: chatgpt_user
active_task_id: M34_MC_HARDENING_DESIGN_DEFINITION
claude_verdict: GO — accept the M34 design as the plan; authorize M34-A build first (advisory; implementation is a separate gate)
claude_verdict_detail: Design-only confirmed (no src/tests change; SHA + leak scan clean). Scope/boundaries correct (ordinary_add only; no new mechanics/optimizer/economics/public numbers; SOURCE/PROVENANCE, MML, PD-013 stay open; no auto-run/Actions). Addresses my carried M33 watchpoints (multi-seed, multi-step). Good design: concrete numeric-free pass/fail, required replay/diagnostic fields, a negative-control test that proves the suite can fail, honest risk register, sensible M34-A/M34-B split. Accepting the design does NOT authorize implementation.
claude_build_note: pin the multi-seed breach rule + seed list before M34-A runs — keep a wide (~6 sigma) per-branch envelope with the hard no-breach rule OR an explicit aggregate/expected-breach-rate rule, to avoid flaky failures on a large seed grid. Build-time parameter, not a design defect.
active_task_file: packages/proposed/P2C_M34_MC_Hardening_Design_Definition_Codex_v1/00_README_FIRST.md
result_path: packages/proposed/P2C_M34_MC_Hardening_Design_Definition_Codex_v1/
review_output_hint: reviews/M34_MC_Hardening_Design_Audit_Claude_v1.md
base_commit: ca4adda
gate_decision: M33 accepted and pinned; M34 design/definition package authorized by ChatGPT/User on 2026-07-08.
builder_summary: Created a design-only M34 package defining MC hardening beyond M33 over accepted `ordinary_add` only. No M34 runtime/test implementation was started. Package proposes multi-seed convergence hardening, multi-step/sequence validation, replay/debug diagnostics, failure reporting, pass/fail criteria, and a recommended split into M34-A and M34-B.

## Gate decision recorded (2026-07-08, User)

- M33 is accepted and pinned.
- Do not start implementation of M34 yet.
- Create a small M34 design/definition package.
- Define M34 as MC hardening beyond M33, still over accepted `ordinary_add` only.
- Include Claude audit request.
- Update ACTIVE_TASK to `ready_for_claude`.

## Current project checkpoint

- Operating Manifest v4: accepted baseline.
- Participant Voice Charter: accepted and active.
- GitHub workflow: active manual loop, no mailbox automation yet.
- GitHub baseline import Layer A: accepted and pinned as project-model GitHub baseline.
- M31 Monte Carlo policy: accepted after folded C-1 correction.
- M32 seeded MC harness: accepted.
- M33 oracle-convergence validation: accepted as completed for accepted `ordinary_add` only.
- M34 design package: ready for Claude audit.
- M34 implementation: not open.
- SOURCE/PROVENANCE, MML, and PD-013 remain open.

## M34 design result summary

Added:

- `packages/proposed/P2C_M34_MC_Hardening_Design_Definition_Codex_v1/`

The design package covers:

- what M34 should validate beyond M33;
- what M34 must not do;
- proposed pass/fail criteria;
- proposed tests/checks;
- split recommendation: M34-A and M34-B;
- human-readable explanation;
- Claude audit request.

## Claude audit — DONE
Audit complete at HEAD `58f12c7`. Verdict: **GO** (advisory). Full audit:
`reviews/M34_MC_Hardening_Design_Audit_Claude_v1.md`. Design-only, correctly bounded, addresses the M33
multi-seed/multi-step watchpoints; sensible M34-A/M34-B split. See verdict fields above.

## What ChatGPT/User should do next (gate decision — nothing auto-accepts, nothing implements)
1. Accept the M34 design as the plan if desired.
2. If accepted, authorize **M34-A** implementation as the next build (separate gate) — pin the multi-seed
   breach rule + seed list first (see claude_build_note). Then M34-B as a later separate gate.
3. M34 implementation is NOT authorized by accepting this design.

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

- the task starts M34 implementation without explicit ChatGPT/User authorization;
- the task changes executable mechanics;
- operation expansion beyond accepted `ordinary_add` appears;
- public output leaks probability values;
- optimizer/advice/ranking, economics, EV, or expected-attempts work appears;
- source/provenance, MML, or PD-013 closure is claimed;
- supervised auto-run or GitHub Actions are enabled.
