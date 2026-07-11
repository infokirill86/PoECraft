# Repo Integrity Check Performance (Wave D) — Claude Audit

audit_id: `P2C_Repo_Integrity_Check_Performance_Wave_D_Audit_Claude_v1`
auditor: `claude`
package: `packages/proposed/P2C_Repo_Integrity_Check_Performance_Wave_D_Result_Codex_v1/`
observed_repo_head: `689254eb4afc2ffe59c059906c1aa0416d79b58a`
observed_active_task_sha: `26519ee9530cfb2029af83d7d6806bde8ac3740b039e2c3677c5b55844b4ef00`
verdict_style: `GO / GO WITH CHANGES / NO-GO`
authority_note: advisory only. Pure repo-integrity tooling performance change; no runtime, data, mechanics, or accepted truth changed.

---

## Plain-language summary
This fixes the slow ~2-minute push. The cause was exactly what I measured: the checksum tools were asking Git
for one file at a time — 629 separate Git launches. Now they ask Git for **all files in one go** (`git cat-file
--batch`). I re-ran it: the checksum file it produces is **byte-for-byte identical** to before (same result,
nothing about the repo's contents changed), but it now takes **~0.2 seconds instead of ~37** per pass. The
engine's fingerprint is unchanged, and the tests pass. It's a pure speed change. **Verdict: GO.**

## Verified by execution / byte inspection
- **Tooling only.** `git diff db83fea..HEAD -- src data config schemas` is empty. Change is confined to
  `tools/update_sha256sums.py`, `tools/check_sha256sums.py`, and their test.
- **Correct batched implementation.** New `git_index_blobs(...)` reads all tracked index blobs through a single
  `git cat-file --batch` process, with defensive parsing (header/`blob`/size validation, truncation and
  trailing-output checks, and a newline-in-path guard). Same policy preserved: tracked files hashed from
  git-normalized/index bytes, untracked from working-tree bytes.
- **Byte-identical output (pure speed change).** Regenerating on my clone reproduces the committed
  `SHA256SUMS.txt` exactly (`git diff SHA256SUMS.txt` empty). No recorded hash changed; only new Wave-D package
  rows were added by the deterministic regeneration.
- **Measured speedup matches the fix.** `update_sha256sums.py` = **0.18s**, `check_sha256sums.py` = **0.40s**
  (640 entries), versus ~37s/pass for the old per-file spawn approach I benchmarked. The pre-push hook
  (update + check) now runs in well under a second instead of ~2 minutes.
- **No truth moved.** Foundation semantic fingerprint reproduces `230dc88…` (= accepted M42-A). Tool tests
  `tests/tools/test_sha256sums_tools.py` → **3 passed** (tracked→index-bytes / untracked→worktree distinction
  preserved). `check_sha256sums.py` → PASS.

## Watchpoints (non-blocking)
- The batch reads all blobs into memory at once — fine for this ~6 MB / 640-file repo; only relevant if the repo
  ever adds very large binaries (not in scope).
- The recurring root-SHA drift is already structurally closed (index-normalized hashing); this change keeps that
  property and adds only speed.

## Recommendation
**GO.** Accept Wave D as a repo-integrity tooling performance change: identical output, ~280× faster, no
runtime/data/mechanics/truth change. It removes the ~2-minute push friction. The lightweight package lifecycle
index (Wave C) and the M43 direction decision (sequences vs Alchemy) remain independent and pending.

## Remains proposed / not accepted / gated
- Wave D is proposed until the ChatGPT/User gate. Wave C (evidence lifecycle index) remains separate/closed; no
  package moved or deleted. No runtime/mechanics/data/admission change; no optimizer/economics/public-output/
  automation; MML/SOURCE-PROVENANCE/crafted-capacity/PD-013 stay open.
- Acceptance authority remains ChatGPT/Kirill; this verdict is advisory; no agent self-acceptance.

---
- author: `claude`
- document_type: `repo_integrity_tooling_performance_audit`
- status: `advisory verdict — GO; batched git cat-file, byte-identical manifest, ~0.2s vs ~37s per pass, fingerprint unchanged`
