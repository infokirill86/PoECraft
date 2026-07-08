# P2C ACTIVE TASK

status: claude_reaudit_complete
next_actor: chatgpt_user
active_task_id: LAYER_A_SOURCE_BUNDLE_BYTE_VERIFICATION
active_task_file: work/active/LayerA_Source_Bundle_Byte_Verification_Task.md
result_path: packages/proposed/P2C_Source_Bundle_Byte_Verification_Result_Codex_v1/
expected_output_dir: packages/proposed/P2C_Source_Bundle_Byte_Verification_Result_Codex_v1/
review_path: reviews/LayerA_Source_Bundle_Byte_Verification_Audit_Claude_v1.md
review_output_hint: reviews/LayerA_Source_Bundle_Byte_Verification_Reaudit_Claude_v1.md
base_commit: b199bf6
claude_verdict: GO WITH CHANGES (advisory; acceptance stays with ChatGPT/User)
claude_verdict_detail: Codex's bundle is honest and integrity-clean but reached the wrong conclusion by comparing against the three doc-only rollup ZIPs (0 of 75 matches, real but not meaningful). Claude compared the repo's Layer A against the actual origin working tree at Documents/GitHub/PoECraft (named in BASELINE_IMPORT_INVENTORY §5): 79 of 79 source files byte-identical, 0 differ. Import FIDELITY is proven; formal PRIOR ACCEPTANCE remains open because the runtime only ever existed as a working tree, never a packaged accepted ZIP (same class as the standing open SOURCE/PROVENANCE boundary).
claude_required_change: fold the working-tree comparison (79 of 79 exact) into the package record, superseding the wrong-source "provenance gap" framing.
claude_gate_options: (1 recommended) accept-and-pin the current repo Layer A as the accepted baseline now, provenance recorded as byte-verified-to-working-tree with no prior formal packaging; (2) keep Layer A proposed under the standing provenance-open rule and decide later. Chasing a prior accepted runtime ZIP is not viable — it never existed.
builder_summary: Source-bundle byte verification result prepared for GitHub baseline Layer A. Available prior local/source package bytes were included, SHA256 values were computed, repo imported baseline files were compared where possible, and gaps were documented. Layer A remains HOLD / NOT ACCEPTED AS PROJECT TRUTH.
correction_summary: Documentation-only correction folded Claude's working-tree comparison into the package record. The earlier 0 of 75 ZIP result is now explicitly marked as a wrong-source comparison against document-only rollups. Import fidelity is recorded as proven against `Documents/GitHub/PoECraft`; prior formal runtime package acceptance remains open; Layer A still requires ChatGPT/User gate.

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

## Claude audit — DONE
Audit complete at repo HEAD `85f40cb`. Verdict: **GO WITH CHANGES** (advisory). Full audit in
`reviews/LayerA_Source_Bundle_Byte_Verification_Audit_Claude_v1.md`. Codex's bundle is honest but used the
wrong (doc-only) source; Claude byte-verified Layer A against the real origin working tree = 79 of 79 exact.
Import fidelity proven; formal prior acceptance still open. See verdict fields above.

## Claude re-audit — DONE
Re-audit complete at repo HEAD `18f6f6a`. Verdict: **GO** (advisory). Full re-audit in
`reviews/LayerA_Source_Bundle_Byte_Verification_Reaudit_Claude_v1.md`. Correction properly folded in;
Codex's 75/75 working-tree comparison independently re-verified (75 identical, 0 differ, 0 missing);
integrity clean; ledgers untouched; Layer A stays HOLD. Byte-verification work is now closed.

## What ChatGPT/User should do next (gate decision — nothing auto-accepts)
The only open item is the Layer A acceptance decision (import fidelity is proven; formal prior acceptance
never existed as a package):
1. (recommended) Accept-and-pin the current repo Layer A as the accepted baseline now, provenance recorded
   as byte-verified-to-origin-working-tree with no prior formal packaging.
2. Or keep Layer A proposed under the standing provenance-open rule and decide later.
M33 (oracle convergence) remains closed until this is decided.

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
