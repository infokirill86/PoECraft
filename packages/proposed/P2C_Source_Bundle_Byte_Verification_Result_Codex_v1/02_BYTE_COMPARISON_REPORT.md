# Byte Comparison Report

See `REPO_IMPORT_BYTE_COMPARISON.csv` for the full machine-readable comparison.

## Corrected conclusion after Claude audit

The original ZIP comparison below is preserved as evidence, but it is superseded as the main conclusion. Those ZIPs were document-only rollups and were the wrong source for runtime byte verification.

The actual origin working tree is:

`Documents/GitHub/PoECraft`

Claude's audit reports:

- 79 of 79 source files byte-identical;
- 0 differ;
- 0 missing.

This package now includes `WORKING_TREE_BYTE_COMPARISON.csv`, a Codex-generated package-surface comparison against that origin working tree:

| Status | Count |
|---|---:|
| byte-identical | 75 |
| differ | 0 |
| missing | 0 |

Therefore import fidelity is proven against the actual local origin working tree. Prior formal runtime-package acceptance remains open because no accepted runtime ZIP existed.

## Summary

| Status | Count |
|---|---:|
| exact SHA match | 0 |
| name/path candidate SHA mismatch | 0 |
| no source entry candidate found | 75 |

## Interpretation

An exact SHA match means the imported repo file bytes match a file entry inside an included source ZIP.

A name/path candidate mismatch means a source ZIP entry with the same path or filename was found, but the bytes differ.

No source entry candidate means the included source packages do not contain an obvious matching entry for the repo file. After Claude audit, this is understood as a wrong-source comparison against document-only ZIPs, not as evidence that the repo import is unverifiable.

## Boundary

This report does not update accepted truth. GitHub baseline Layer A remains HOLD / NOT ACCEPTED AS PROJECT TRUTH.
