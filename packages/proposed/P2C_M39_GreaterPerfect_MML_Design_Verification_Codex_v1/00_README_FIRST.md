# P2C M39 Greater/Perfect + MML Design Verification — Codex v1

Package type: `DESIGN_MECHANICS_VERIFICATION / PROPOSED`

This package verifies and designs the Greater/Perfect variant and Minimum Modifier Level (MML) layer before any runtime admission.

It does not implement runtime code. It does not admit Greater/Perfect variants. It does not close MML, SOURCE/PROVENANCE, or PD-013.

## Result

Codex recommends treating MML as a shared add-pool filter layer, but not admitting all Greater/Perfect rows as one batch.

The nearest safe future admission candidates are Greater/Perfect Exalted and Greater/Perfect Chaos, because their base behaviors map onto already accepted runtime capabilities:

- accepted `ordinary_add` engine primitive;
- accepted base Chaos-like remove-then-add runtime.

Greater/Perfect Transmutation, Augmentation, and Regal should wait for their base currency wrappers to be admitted. Greater/Perfect Essence rows are not MML-only variants and require separate operation admission.

## Included files

- `01_PLAIN_LANGUAGE_SUMMARY_FOR_KIRILL.md`
- `02_PARTICIPANT_CRITIQUE.md`
- `03_GREATER_PERFECT_INVENTORY.md`
- `04_MML_MECHANICS_SOURCE_TABLE.md`
- `05_REPO_DATA_VS_TRUSTED_SOURCE_COMPARISON.md`
- `06_PROPOSED_MML_FILTER_MODEL.md`
- `07_BATCHING_AND_SEPARATE_GATES.md`
- `08_RECOMMENDED_M39A_IMPLEMENTATION_FLOOR.md`
- `09_CLAUDE_AUDIT_REQUEST.md`
- `10_READ_RECEIPT.md`
- `11_COMMANDS_AND_RESULTS.md`
- `PACKAGE_MANIFEST.md`

