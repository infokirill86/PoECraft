# P2C ACTIVE TASK

status: ready_for_claude
next_actor: claude
active_task_id: M34_MC_HARDENING_DESIGN_DEFINITION
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

## What Claude should do next

Audit:

- `packages/proposed/P2C_M34_MC_Hardening_Design_Definition_Codex_v1/`
- this `ACTIVE_TASK.md`
- `CURRENT_STATUS.md`

Return GO, GO WITH CHANGES, or NO-GO.

## What ChatGPT/User should do after Claude

Make an explicit gate decision.

No artifact in this commit starts M34 implementation.

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
