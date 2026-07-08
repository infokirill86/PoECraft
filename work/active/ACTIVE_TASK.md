# P2C ACTIVE TASK

status: ready_for_claude
next_actor: claude
active_task_id: LAYER_A_SOURCE_BUNDLE_BYTE_VERIFICATION
active_task_file: work/active/LayerA_Source_Bundle_Byte_Verification_Task.md
result_path: packages/proposed/P2C_Source_Bundle_Byte_Verification_Result_Codex_v1/
expected_output_dir: packages/proposed/P2C_Source_Bundle_Byte_Verification_Result_Codex_v1/
review_output_hint: reviews/LayerA_Source_Bundle_Byte_Verification_Audit_Claude_v1.md
base_commit: b199bf6
builder_summary: Source-bundle byte verification result prepared for GitHub baseline Layer A. Available prior local/source package bytes were included, SHA256 values were computed, repo imported baseline files were compared where possible, and gaps were documented. Layer A remains HOLD / NOT ACCEPTED AS PROJECT TRUTH.

## Gate decision recorded (2026-07-08, User)

- A1/A2 baseline hygiene: ACCEPTED as completed.
- Supervised auto-run protocol metadata: ACCEPTED as safe documentation-only metadata.
- GitHub baseline import Layer A: HOLD / NOT ACCEPTED AS PROJECT TRUTH until byte-level SOURCE_BUNDLE / FULL_REPRODUCIBILITY_BUNDLE verification is completed.
- M33: not open.

## Current project checkpoint

- Operating Manifest v4: accepted baseline.
- Participant Voice Charter: accepted and active.
- GitHub workflow: active manual loop, no mailbox automation yet.
- M31 Monte Carlo policy: accepted after folded C-1 correction.
- M32 seeded MC harness: accepted (Layer B).
- A1/A2 baseline hygiene: accepted as completed.
- Supervised auto-run protocol metadata: accepted documentation-only metadata.
- GitHub baseline import Layer A: HOLD / NOT ACCEPTED AS PROJECT TRUTH.
- M33: not open.

## Claude audit target

Audit the source-bundle byte verification result at:

`packages/proposed/P2C_Source_Bundle_Byte_Verification_Result_Codex_v1/`

Claude should verify:

1. Source bytes included under `SOURCE_BYTES/` are appropriate and their SHA256 values are correct.
2. ZIP entry SHA values and repo import comparison rows are accurate.
3. Missing source bytes and unresolved gaps are honestly documented.
4. GitHub baseline Layer A remains HOLD / NOT ACCEPTED AS PROJECT TRUTH.
5. No M33, mechanics changes, optimizer/advice/ranking, public numeric release, source/provenance closure, MML closure, PD-013 closure, or accepted-ledger truth update was introduced.

Return audit under:

`reviews/LayerA_Source_Bundle_Byte_Verification_Audit_Claude_v1.md`

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

- the task starts M33;
- the task changes executable mechanics;
- imported baseline/support files are treated as accepted project truth without Claude audit and ChatGPT/User acceptance;
- public output leaks probability values;
- optimizer/advice/ranking or public numeric release appears;
- source/provenance, MML, or PD-013 closure is claimed.
