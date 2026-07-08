# P2C ACTIVE TASK

status: awaiting_user_go_for_m33
next_actor: chatgpt_user
active_task_id: LAYER_A_ACCEPT_AND_PIN
active_task_file: work/active/LayerA_Source_Bundle_Byte_Verification_Task.md
result_path: packages/proposed/P2C_Source_Bundle_Byte_Verification_Result_Codex_v1/
review_path: reviews/LayerA_Source_Bundle_Byte_Verification_Reaudit_Claude_v1.md
base_commit: c8722c3
gate_decision: Layer A GitHub baseline import ACCEPTED AND PINNED by User on 2026-07-08.
builder_summary: CURRENT_STATUS and ledgers updated to accept/pin GitHub Layer A as the project-model runtime/data/config/schema/tool baseline. Provenance recorded as imported from local origin working tree `Documents/GitHub/PoECraft`, byte-verified exact; no prior formal runtime package existed. M33 remains closed pending explicit ChatGPT/User authorization.

## Gate decision recorded (2026-07-08, User)

- Layer A GitHub baseline import: ACCEPT AND PIN.
- Import fidelity is proven against actual origin working tree `Documents/GitHub/PoECraft`.
- Claude verified 79 of 79 source files byte-identical, 0 differ, 0 missing.
- Codex correction folded the working-tree comparison into the package record.
- A1/A2 baseline hygiene is accepted.
- Prior formal runtime ZIP did not exist; runtime lived as a working tree.
- Do not claim server truth.
- Do not close SOURCE/PROVENANCE, MML, or PD-013.
- Do not start M33 in this commit.
- Do not change mechanics.

## Current project checkpoint

- Operating Manifest v4: accepted baseline.
- Participant Voice Charter: accepted and active.
- GitHub workflow: active manual loop, no mailbox automation yet.
- M31 Monte Carlo policy: accepted after folded C-1 correction.
- M32 seeded MC harness: accepted (Layer B).
- A1/A2 baseline hygiene: accepted.
- Supervised auto-run protocol metadata: accepted documentation-only metadata.
- GitHub baseline import Layer A: accepted and pinned as project-model GitHub baseline.
- SOURCE/PROVENANCE, MML, and PD-013 remain open.
- M33: not open.

## What ChatGPT/User should do next

Explicitly authorize M33 if the next milestone should start.

No agent may start M33 from this status alone.

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

- the task starts M33 without explicit ChatGPT/User authorization;
- the task changes executable mechanics;
- public output leaks probability values;
- optimizer/advice/ranking or public numeric release appears;
- source/provenance, MML, or PD-013 closure is claimed.
