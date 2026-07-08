# Repo-Integrity SHA Floor Audit (Claude)

audit_id: `P2C_Repo_Integrity_SHA_Floor_Audit_Claude_v1`
auditor: `claude`
package: `packages/proposed/P2C_Repo_Integrity_SHA_Floor_Codex_v1/`
observed_repo_head: `a12d5819d272422ae29a071775ab15003e6cd88f`
observed_active_task_sha: `e2a0416a8e9ecc44baf7f52ec05a46fff80a16e9eacdbe145741aed92b2cb531`  (SHA-256 of the exact `work/active/ACTIVE_TASK.md` bytes audited, at HEAD a12d581, before this review's dispatcher update)
verdict_style: `GO / GO WITH CHANGES / NO-GO`
disclosure: **This floor implements a fix I recommended** in the M36 audit (the recurring root-SHA drift).
Per the Participant Voice Charter I disclose that and scrutinise it harder rather than rubber-stamp my own idea.
authority_note: advisory only. Acceptance stays with ChatGPT/User.

---

## Plain-language summary
This is the fix for the checksum file that kept drifting: a small script that **rebuilds the whole checksum
file from the real repository bytes**, plus a rule to run it before every push. The script is correct — I
tested it, and running it repaired the checksums so the integrity check passes. **The catch is almost funny but
important: the commit that adds this fix did not actually run it, so the repo was delivered still broken** (the
integrity check fails at this commit). I ran the tool to repair it as part of this review. That miss — forgetting
to run the tool on the very commit meant to end this problem — is exactly why the rule needs a real gate
(a pre-push block), not just a written instruction. **Verdict: GO WITH CHANGES** — keep the tool and rule, but
regenerate the manifest (done here) and add enforcement so the check can't be skipped.

## Verdict
**GO WITH CHANGES.** The regenerator tool and the "run it before every push" protocol rule are correct and are
the right regulation. Required corrections: (1) the delivered manifest was not regenerated and still fails —
applied here; (2) add enforcement (a committed pre-push hook), because this floor's own commit shows the
documented rule alone is not enough.

## What was verified
- **`tools/update_sha256sums.py` is correct.** It lists files via `git ls-files --cached --others
  --exclude-standard`, excludes the root manifest itself, hashes actual bytes, sorts by POSIX path, writes LF.
  Deterministic and machine-generated — this structurally eliminates hand-edit drift.
- **The tool works, by execution.** Running it changed exactly 3 stale entries and then
  `check_sha256sums.py` → **PASS**. Idempotent thereafter (a second run is a no-op). So the tool does fix the
  drift.
- **Protocol rule added** (`GitHub_Workflow_Protocol.md`): "Before every push that changes repository files,
  run `python tools/update_sha256sums.py`." This is the standing regulation requested.
- **Boundary-clean:** no `.github/`, no GitHub Actions, no watcher — respects the automation standing boundary
  (the tool is a manual command). No `src/`/`tests/`/`data` runtime change; tooling + docs only. Package
  numeric-leak scan and package internal `SHA256SUMS` are consistent. Ledger shows M36 design accepted
  (design-only) and does **not** self-accept this SHA floor.

## Required change 1 — the delivered manifest still FAILS (applied in this audit)
At the delivered HEAD `a12d581`, `check_sha256sums.py` returns **FAIL**: Codex added the updater but **did not
run it**, so 3 entries are still stale (the same recurring drift). I ran `tools/update_sha256sums.py` as part of
this review; the manifest now passes `check_sha256sums.py`. The builder must run the tool before committing —
which is precisely the rule this floor introduces.

## Required change 2 — enforce, don't just document (strongly recommended)
This floor's own commit **forgot to run its own tool**. That is direct evidence that a documented "remember to
run it" rule is insufficient. Add a **committed local pre-push hook** (e.g. `tools/hooks/pre-push` that runs
`update_sha256sums.py` then `check_sha256sums.py` and blocks the push on mismatch, enabled via
`git config core.hooksPath tools/hooks`). This stays within the automation boundary (a local git hook, not
GitHub Actions) and makes the check unskippable. Until the hook exists, treat "run the updater + `check`
before every push" as a hard, non-optional step for every actor (Codex and Claude).

## Recommendation
Accept the repo-integrity SHA floor (tool + protocol rule) with the manifest regenerated (done) and with the
pre-push hook added as the enforcement layer. This closes the recurring root-SHA drift that has now recurred
across several floors — including this one. Nothing self-accepts; M36-A implementation remains a separate gate,
and this floor is a prerequisite hygiene fix for it.

---
- author: `claude`
- document_type: `repo_integrity_tooling_audit`
- status: `advisory verdict — GO WITH CHANGES (manifest regenerated; add pre-push enforcement)`
