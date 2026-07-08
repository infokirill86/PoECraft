# Layer A Source Bundle Byte Verification Task

task_id: LAYER_A_SOURCE_BUNDLE_BYTE_VERIFICATION
task_type: source_bundle_byte_verification
source_agent: ChatGPT/User gate decision (2026-07-08)
target_agent: Codex
base_commit: b199bf6
expected_output: packages/proposed/P2C_Source_Bundle_Byte_Verification_Result_Codex_v1/
review_output_hint: reviews/LayerA_Source_Bundle_Byte_Verification_Audit_Claude_v1.md

## Gate decision

- A1/A2 baseline hygiene: accepted as completed.
- Supervised auto-run protocol metadata: accepted as safe documentation-only metadata.
- GitHub baseline import Layer A: HOLD / NOT ACCEPTED AS PROJECT TRUTH until byte-level SOURCE_BUNDLE / FULL_REPRODUCIBILITY_BUNDLE verification is completed.
- M33 is not open.

## Goal

Provide byte-level evidence for the imported GitHub baseline against prior accepted local/source package bytes, or clearly document any gap that prevents byte-level verification.

## Allowed actions

- Identify source bundle / prior accepted baseline bytes.
- Compute and record SHA256.
- Compare imported repo baseline files to source bytes where possible.
- Document exact matches, intentional differences, missing source bytes, and unresolved gaps.
- Prepare a Claude audit request.

## Forbidden actions

- Do not change mechanics.
- Do not implement or start M33.
- Do not update accepted ledger/truth as accepted.
- Do not accept GitHub baseline Layer A.
- Do not release public numeric probabilities.
- Do not add optimizer, advice, ranking, EV, budget, or expected-attempt logic.

## Codex completion note

Result produced at:

`packages/proposed/P2C_Source_Bundle_Byte_Verification_Result_Codex_v1/`

Status after Codex work: ready for Claude audit.

## Stop conditions

STOP_OR_ESCALATION if:

- source bytes cannot be located and no useful gap report can be produced;
- comparison requires changing runtime mechanics;
- evidence would require accepting Layer A without audit;
- M33 or milestone transition becomes necessary.
