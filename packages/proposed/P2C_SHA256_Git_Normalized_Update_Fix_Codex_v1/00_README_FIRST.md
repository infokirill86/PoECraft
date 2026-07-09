# P2C SHA256 Git-normalized Update Fix — Codex v1

Package type: `REPO_INTEGRITY_TOOL_FIX / PROPOSED_FOR_CLAUDE_AUDIT`

This package implements the tiny repo-integrity fix authorized after M39-A acceptance.

Goal:

> Stop recurring root `SHA256SUMS.txt` drift caused by CRLF/LF working-tree differences.

## What changed

- `tools/update_sha256sums.py` now hashes tracked files from Git index bytes.
- `tools/check_sha256sums.py` now verifies tracked files against Git index bytes.
- Untracked non-ignored files still use raw working-tree bytes.
- A focused unit test covers tracked normalized bytes versus untracked raw bytes.

## What did not change

- No crafting runtime behavior.
- No data semantics.
- No operation admission.
- No Greater/Perfect runtime.
- No MML closure.
- No SOURCE/PROVENANCE or PD-013 closure.
- No automation/GitHub Actions.
