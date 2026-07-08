# Working-Tree Comparison Correction

Status: documentation-only correction after Claude `GO WITH CHANGES`

## Plain-language summary

The first Codex source-bundle result compared GitHub Layer A against the wrong source: document-only rollup ZIPs. That comparison was honest, but it could not prove runtime import fidelity because those ZIPs did not contain the runtime tree.

Claude identified the actual origin: the local working tree at `Documents/GitHub/PoECraft`.

## Corrected evidence

Claude audit result:

- origin: `Documents/GitHub/PoECraft`
- compared scope: GitHub Layer A source surfaces
- result: 79 of 79 source files byte-identical
- differ: 0
- missing: 0

Codex package-surface recalculation included in this package:

- artifact: `WORKING_TREE_BYTE_COMPARISON.csv`
- result: 75 of 75 package-surface files byte-identical
- differ: 0
- missing: 0

The count differs because Codex's recalculation uses the package's imported-baseline surface list, while Claude's audit used a broader Layer A source-file count. Both support the same conclusion: the GitHub import is a faithful byte-level copy of the actual local origin working tree.

## What this proves

Import fidelity is proven. The imported GitHub Layer A files were not corrupted or silently changed during migration from the local working tree.

## What this does not prove

The prior formal runtime package still did not exist. Therefore this correction does not by itself accept Layer A as project truth.

Layer A acceptance still requires ChatGPT/User gate approval.

## Boundary

- No M33.
- No mechanics changes.
- No accepted-ledger update.
- No source/provenance, MML, or PD-013 closure.
