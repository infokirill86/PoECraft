# Repository Structure & Truth-Surface Audit — Claude Audit

audit_id: `P2C_Repo_Structure_Truth_Surface_Audit_Audit_Claude_v1`
auditor: `claude`
package: `packages/proposed/P2C_Repo_Structure_Truth_Surface_Audit_Codex_v1/`
observed_repo_head: `420f337506d258ca6ceed3a653044947f73c6a69`
observed_active_task_sha: `7a6ed852435df9e72f98e4b35d2799f9e63f6dae1bd8547a2abd7fbca81c801a`
verdict_style: `GO / GO WITH CHANGES / NO-GO`
authority_note: advisory only. This audits an inventory/report. No cleanup is authorized; any cleanup is a separate gated task.

---

## Plain-language summary
This is the repo "spring-cleaning survey" — a report, nothing was moved or deleted. I re-checked its main claims
by scanning the repo myself, and they hold up. The important ones: (1) three old finished task files still sit in
`work/active/` next to the live one, so the folder falsely looks like four active tasks; (2) our first-read
orientation files (`START_HERE.md`, the workflow protocol, the blockers list) still say **"only ordinary_add is
executable"** — that's badly out of date now that ~24 operations are accepted, and our role files tell agents to
read those *before* the live task; (3) accepted packages still live in `packages/proposed/` while
`packages/accepted/` has only a README. The report proposes fixing routing and stale text and adding lifecycle
links — while **keeping all the evidence (packages/reviews) untouched** and doing any actual cleanup as a
separate, audited step. That's the right, safe approach. **Verdict: GO** on the audit.

## Verified by my own scan (not trusting the report)
- **Report-only, nothing destructive.** Diff since M43 audit (`0cc9f14..HEAD`) is the package docs + dispatcher
  + status/ledger lines. `git diff --diff-filter=DR` = empty: no file moved, renamed, or deleted.
- **TS-02 confirmed (dispatcher pollution).** `git ls-files work/active/` returns four tracked files:
  `ACTIVE_TASK.md` plus `LayerA_Source_Bundle_Byte_Verification_Task.md`, `M32_A1_A2_Baseline_Hygiene_Task.md`,
  `M32_Seeded_MC_Harness_Task.md`. The folder's contract is "live routing only," so the three historical files
  are real noise (and are the ones a linter kept re-touching this session).
- **TS-03/04/05 confirmed — the highest-risk finding.** `START_HERE.md:58` literally reads
  "no new executable mechanics (only `ordinary_add` is executable)"; `manifest/GitHub_Workflow_Protocol.md:179`
  says "current accepted executable runtime is accepted `ordinary_add` … and base `annulment`";
  `ledger/OPEN_BLOCKERS.md:9` echoes the same. All three are **stale** against accepted M35-A…M42-A (rarity
  progression, Exalted, Annulment, Chaos, Greater/Perfect Essence — 24 accepted runtime rows + `ordinary_add`).
- **TS-01 confirmed and, combined with TS-03, effectively Critical.** `CLAUDE.md` boot order reads `START_HERE`
  (1) and `CURRENT_STATUS` (2) *before* `ACTIVE_TASK` (5). So the very files that are stalest are read first. A
  naive agent could conclude "only ordinary_add is executable" and mis-audit or wrongly reject accepted
  operations. (I was not misled only because I lean on `CURRENT_STATUS`/ledger, which are kept current — but
  the hazard is real for a cold boot.) I'd raise TS-03 from High to effectively Critical *because of* the
  read-order.
- **TS-09 confirmed.** 39 package dirs in `packages/proposed/`; `packages/accepted/` holds only `README.md`.
  Accepted milestones live in `proposed/`, so the folder name is not acceptance authority.
- **`repo_head_at_last_update` clarification is correct.** The field is the *input* HEAD observed when the
  dispatcher was written, not the containing commit (which cannot self-reference). Freshness = read at verified
  remote HEAD + check the read receipt, not field-equals-containing-commit. This is right and worth adopting
  explicitly (it also refines my own "definition of done").

## Why the posture is right (and safe)
- **Evidence is treated as immutable.** Accepted packages and reviews are kept in place; the report explicitly
  rejects mass deletion, bulk package moves, and rewriting historical prose. Lifecycle is fixed with *links and
  an index*, not by moving 33+ directories (which would break immutable references). Correct.
- **Cleanup is staged and gated.** Waves A (routing repair) → B (canonical-truth destaling) → C (evidence
  lifecycle links) → D (checker scoping), each as a later gated delta with Claude audit and a single-commit
  rollback plan. No runtime/mechanics/data/admission/optimizer/public-output in any wave.
- **One structural point I want to reinforce:** when destaling `START_HERE`/`Operating_Manifest`/`Workflow
  Protocol`, replace the volatile runtime lists with **references to the accepted ledger**, not a fresh
  hardcoded list — otherwise the same staleness returns in a month. The report already says this (doc 10); it
  is the right pattern and should be treated as mandatory, not optional. Same spirit as our "fix recurring
  errors structurally" rule.

## Recommendation
**GO** on the audit. The findings are accurate and the plan is safe. Suggested for the follow-up cleanup gate:
prioritize **Wave A + B first** (the stale "only ordinary_add" claims in first-read files are the real hazard),
keep every accepted package/review byte-immutable, replace stale runtime prose with ledger references, and
extend `validate_active_task.py` to require exactly one tracked file under `work/active/`. This audit itself
changes no truth and requires no rollback beyond reverting its own package/status commit. The M43 direction
decision (sequences vs Alchemy) is independent and still pending — hygiene should not consume it.

## Remains proposed / not accepted / gated
- No cleanup applied; no file moved/deleted; no accepted truth changed. Cleanup Waves A–D remain closed pending
  a separate ChatGPT/User gate + Claude audit. M43 stays Claude-GO/proposed; M43-A closed. No runtime/mechanics/
  data/admission change; no optimizer/economics/public-output/automation; MML/SOURCE-PROVENANCE/crafted-capacity/
  PD-013 stay open.
- Acceptance authority remains ChatGPT/Kirill; this verdict is advisory; no agent self-acceptance.

---
- author: `claude`
- document_type: `repo_structure_truth_surface_audit_audit`
- status: `advisory verdict — GO; findings verified accurate by independent scan; stale "only ordinary_add" first-read claims are the priority fix; evidence stays immutable; cleanup separately gated`
