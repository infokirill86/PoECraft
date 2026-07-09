# SHA256 Git-Normalized Updater/Checker Fix Audit (Claude)

audit_id: `P2C_SHA256_Git_Normalized_Update_Fix_Audit_Claude_v1`
auditor: `claude`
package: `packages/proposed/P2C_SHA256_Git_Normalized_Update_Fix_Codex_v1/`
observed_repo_head: `596fcdb7f69a8c285ff5a51698eddd10e167bf3f`
observed_active_task_sha: `47cc21d166ca835f07780e4e8f47c4b5cf5ce2e166c086a973e1e14f8b683ff3`
verdict_style: `GO / GO WITH CHANGES / NO-GO`
authority_note: advisory only. Acceptance is ChatGPT/Kirill.

---

## Plain-language summary
This is the one-time fix for the checksum file that kept "drifting" on every handoff. The cause was
line-ending differences (Windows CRLF vs the repo's normalized LF): the old tool measured files as they sat on
disk, so whoever built the package stamped in hashes tied to their machine, and they failed on anyone else's.
The fix makes both tools measure the **stored (normalized) version** of tracked files instead of the on-disk
copy. I proved it end-to-end: I deliberately rewrote a tracked file to CRLF on disk and the checker still said
PASS — the exact situation that used to break now can't. And regenerating the checksum file on my clean copy
produced **no changes** to what Codex delivered (previously it corrected 3 lines every time). The drift is
actually closed, not patched over. **Verdict: GO.**

## Verified by execution / byte inspection
- **Correct, symmetric fix.** `tools/update_sha256sums.py` now hashes tracked files from Git index bytes
  (`git cat-file blob :path`) and untracked files from the working tree; `tools/check_sha256sums.py` was
  updated the **same way** (this is the load-bearing half — a checker still reading the worktree would fail on a
  fresh CRLF clone against an index-based manifest). Both use the same `-z` NUL-safe path listing.
- **Determinism proven.** Regenerating the manifest on my clean clone yields byte-identical output to Codex's
  committed `SHA256SUMS.txt` (469 entries) and `check` → **PASS**. Under the pre-fix tool, every audit had to
  correct ~3 entries; now it corrects zero.
- **Line-ending invariance proven by execution.** For a tracked file (`data/operations.yaml`) the manifest
  records the index-bytes hash; after I forcibly rewrote that file to CRLF in the working tree, the checker
  still returned **PASS** (it reads index bytes, not the worktree). Restored clean afterward.
- **Real test, not vacuous.** `tests/tools/test_sha256sums_tools.py` writes a CRLF working file whose index
  bytes are LF, and asserts the recorded hash equals the LF hash and is *not* the CRLF hash, while an untracked
  file keeps its raw bytes — then round-trips through the checker. `pytest` → **1 passed**.
- **No scope creep / no self-acceptance.** Change is confined to the two integrity tools + their test + the
  package docs. The `CURRENT_STATUS.md` / `ledger/` edits are legitimate **User gate records** (2026-07-10:
  accept M39-A, authorize this fix); the fix itself is correctly recorded as "proposed for Claude audit, not
  accepted yet." No engine/data/mechanics/operation change; no boundary closure; no automation.

## Watchpoint (non-blocking)
- Both tools now require being run inside a Git working tree (they shell out to `git`). That is always true for
  this workflow, but a detached export (a tarball with no `.git`) can no longer be self-checked. Acceptable;
  worth a one-line note in the tool docstring if ever exporting.

## Why this supersedes the pre-push hook for this problem
The earlier guard was a local `pre-push` hook, which cannot run in Codex's linked worktree (`core.hooksPath`
write is permission-denied there). This fix removes the dependency on any hook: the manifest is now identical
on every clone by construction, so the drift cannot reappear regardless of who builds or their line endings.

## Recommendation
**GO.** Accept the SHA256 git-normalized updater/checker fix as the durable repo-integrity mechanism. No
corrections required.

## Remains proposed / not accepted / gated
- Everything gated before remains gated: no Greater/Perfect / Essence / Whittling / Omen runtime; no new
  operation; no MML / SOURCE-PROVENANCE / PD-013 closure; no public numbers; no optimizer/economics; no
  automation. Acceptance authority remains ChatGPT/Kirill; this verdict is advisory.

---
- author: `claude`
- document_type: `tooling_integrity_fix_audit`
- status: `advisory verdict — GO; recurring checksum drift closed structurally (index-normalized hashing), proven by execution`
