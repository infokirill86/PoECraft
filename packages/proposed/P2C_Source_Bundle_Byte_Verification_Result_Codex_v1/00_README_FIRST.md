# Source Bundle Byte Verification Result

Package: `P2C_Source_Bundle_Byte_Verification_Result_Codex_v1`
Package type: `SOURCE_BUNDLE_BYTE_VERIFICATION_RESULT_PROPOSED`
Status: ready for Claude audit

## Plain-language summary

This package checks whether the imported GitHub baseline can be proven byte-for-byte against prior local accepted/source package bytes.

## Correction after Claude audit

Claude returned `GO WITH CHANGES` and found that the original `0 matches / provenance gap` conclusion was a wrong-source comparison: the included rollup ZIPs were document-only bundles, not the runtime origin.

The actual origin for the imported GitHub Layer A runtime/data/config/schema/tool files was the local working tree:

`Documents/GitHub/PoECraft`

Claude's comparison result:

- 79 of 79 source files byte-identical;
- 0 differ;
- 0 missing.

Codex's package-surface recalculation in `WORKING_TREE_BYTE_COMPARISON.csv` covers the imported baseline surfaces represented in this package and reports:

- 75 of 75 files byte-identical;
- 0 differ;
- 0 missing.

The practical conclusion is the same: import fidelity is proven against the actual local origin working tree. The prior formal runtime package still did not exist, so Layer A acceptance still requires a ChatGPT/User gate.

What happened:

- Found and included available local source package bytes under `SOURCE_BYTES/`.
- Computed SHA256 for each included source file and each ZIP entry.
- Compared imported GitHub baseline support files against ZIP entries where a path or filename candidate existed.
- Documented exact matches, mismatches, missing source bytes, and unresolved gaps.

Why it matters:

GitHub baseline Layer A is currently traceable and tested, but not accepted as project truth. This byte-level check is the next evidence step before any future acceptance decision.

Original wrong-source ZIP comparison result:

- Source files found and included: 3
- Source files missing locally: 1
- ZIP entries indexed: 29
- Imported repo baseline files compared: 75
- Exact SHA matches found: 0
- Candidate filename/path mismatches: 0
- No source entry candidate found: 75

Important: this package does not accept Layer A. It gives evidence and gaps for Claude/ChatGPT/User review.
