# Gaps and Limits

## Missing local source bytes

The following expected source artifact bytes were not found locally:

- `P2C_Baseline_Rollup_Delta_ChatGPT_accepted_v1_1.zip`

## Superseded wrong-source gap

The available source packages do not provide direct byte-level matches for most imported runtime/data/config/schema/tool files. This likely means one of the following:

- the actual source package that contained the imported runtime tree is not among the available local bytes;
- the imported repo baseline was assembled from an unpacked local working tree rather than directly from one accepted ZIP;
- paths or generated/normalized files differ from the archived source package structure.

Claude audit supersedes this as the main Layer A import-fidelity conclusion. The available ZIPs were real, but they were document-only rollups and therefore the wrong source for runtime/data/config/schema/tool byte verification.

The actual local origin working tree was:

`Documents/GitHub/PoECraft`

Claude reports 79 of 79 source files byte-identical, 0 differ, 0 missing. This package also includes `WORKING_TREE_BYTE_COMPARISON.csv`, which records Codex's package-surface recalculation as 75 of 75 byte-identical, 0 differ, 0 missing.

## Remaining real gap

Import fidelity is proven. Formal prior runtime-package acceptance is still open because the runtime appears to have lived as a working tree rather than as a prior accepted runtime ZIP. Layer A acceptance still requires a ChatGPT/User gate.

## Explicit non-claims

- No new mechanics are implemented.
- M33 is not started.
- Imported baseline truth is not accepted.
- Accepted ledgers are not updated as accepted.
- Source/provenance, MML, and PD-013 are not closed.
