# Byte Comparison Report

See `REPO_IMPORT_BYTE_COMPARISON.csv` for the full machine-readable comparison.

## Summary

| Status | Count |
|---|---:|
| exact SHA match | 0 |
| name/path candidate SHA mismatch | 0 |
| no source entry candidate found | 75 |

## Interpretation

An exact SHA match means the imported repo file bytes match a file entry inside an included source ZIP.

A name/path candidate mismatch means a source ZIP entry with the same path or filename was found, but the bytes differ.

No source entry candidate means the included source packages do not contain an obvious matching entry for the repo file. This is a verification gap, not proof that the repo file is wrong.

## Boundary

This report does not update accepted truth. GitHub baseline Layer A remains HOLD / NOT ACCEPTED AS PROJECT TRUTH.
