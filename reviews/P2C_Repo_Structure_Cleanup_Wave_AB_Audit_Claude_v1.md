# Repository Structure Cleanup Wave A+B — Claude Audit

audit_id: `P2C_Repo_Structure_Cleanup_Wave_AB_Audit_Claude_v1`
auditor: `claude`
package: `packages/proposed/P2C_Repo_Structure_Cleanup_Wave_AB_Result_Codex_v1/`
observed_repo_head: `10ea24515380542c28ea52cddbc71037eeaacac7`
observed_active_task_sha: `727fe7e2845cb892f3af44445ae54a718d7c49f01ba08159438f9c0c9c1a2328`
verdict_style: `GO / GO WITH CHANGES / NO-GO`
authority_note: advisory only. Documentation/tooling/routing cleanup; no runtime, data, mechanics, or accepted truth changed.

---

## Plain-language summary
This is the actual clean-up we planned, and it's done well. Three things happened, all safe: (1) the three old
finished task files were removed from `work/active/` so that folder now holds only the one live dispatcher —
and the validator now enforces "exactly one file" so it can't get polluted again; (2) the first-read files
(README, AGENTS, CLAUDE, START_HERE) now send an agent to the **live task first**, then orientation — and the
stale "only ordinary_add is executable" line is gone, replaced by "look it up in the ledger, don't hardcode a
list that keeps changing"; (3) the workflow protocol had a long block of old history removed so it holds only
current binding rules. I checked the important safety points by running the tools: **no code, data, or game
mechanic was touched** (the engine's fingerprint is byte-identical to before), every boundary rule is still
there, and the deleted files are fully recoverable from Git history. **Verdict: GO.**

## Verified by execution / byte inspection
- **No runtime/data/mechanics change — proven.** `git diff 5d56acc..HEAD -- src data config schemas` is empty,
  and `validate_foundation` reproduces the **same** semantic fingerprint `230dc88…` as accepted M42-A. So this
  is purely documentation/tooling/routing; no accepted truth moved.
- **Only the three authorized files removed.** `git diff --diff-filter=DR` = exactly
  `LayerA_Source_Bundle_Byte_Verification_Task.md`, `M32_A1_A2_Baseline_Hygiene_Task.md`,
  `M32_Seeded_MC_Harness_Task.md`. `git ls-files work/active/` now returns only `ACTIVE_TASK.md`. History
  retrievable via Git; no `packages/` or `reviews/` path edited, moved, or deleted (evidence preservation
  report confirmed against the diff).
- **Stale claims replaced with ledger references, not new hardcoded lists (the anti-restale pattern).**
  `START_HERE.md` now says executable scope "is intentionally not enumerated here because it changes… Only
  operations and mechanics accepted in `ledger/ACCEPTED_ARTIFACTS.md` and `DECISIONS.md` may execute. Do not
  hardcode that changing inventory." The Workflow Protocol and `OPEN_BLOCKERS.md` likewise reference "the
  accepted ledgers/runtime registry" instead of "ordinary_add + Annulment." This is the structural fix — it
  cannot go stale the same way.
- **Read order fixed (TS-01).** `CLAUDE.md`/`AGENTS.md`/`README.md` now route: verify HEAD → read
  `ACTIVE_TASK.md` → run validator → target package → then `CURRENT_STATUS`/ledger/`START_HERE`/doctrine.
  `ACTIVE_TASK.md` is declared the sole live routing source; "if routing and accepted truth conflict, return to
  ChatGPT/User." Clean truth-precedence separation (routing / snapshot / acceptance / doctrine).
- **All boundaries intact.** `OPEN_BLOCKERS.md` and `Operating_Manifest_v4.md` still forbid optimizer/advice/
  ranking/EV, public numeric/server-truth, SOURCE-PROVENANCE/MML/PD-013 closure, automation/self-acceptance,
  and changes to accepted fractured behavior. The dispatcher's `standing_boundaries_ref` anchor
  (`GitHub_Workflow_Protocol.md#standing-boundaries-for-active-task-dispatcher`) **survived the trim** (§ still
  present at line 119) with its full boundary list (lines 132–135). The 378-line protocol change is the removal
  of the non-binding historical convergence appendix, not any binding rule.
- **Validator guard added (structural fix for the recurrence).** `validate_active_task.py` now requires exactly
  one tracked file under `work/active/` (`ACTIVE_TASK.md`); an untracked local note does not trip it. Tests:
  `tests/tools/test_active_task_validator.py` → **10 passed**, including the tracked-sibling-fails negative
  control. Validator PASS on the live dispatcher.

## Watchpoints (non-blocking)
- The change is large in line count (START_HERE 179, Workflow Protocol 378) but concentrated in stale-history
  removal and reference re-pointing; I confirmed the semantic content (boundaries, anchors, runtime-truth
  ownership) is preserved. Future waves (C: evidence lifecycle links; D: checker scoping) remain separately
  gated.
- Repo growth is making the pre-push SHA hook slow (~2 min over 600+ files); Wave D's checker scoping could
  address this later, but it is not in this delta.

## Recommendation
**GO.** Accept Wave A+B as documentation/tooling/routing cleanup with no runtime/data/mechanics/truth change,
evidence preserved, boundaries intact, and a new structural guard against dispatcher pollution. Waves C/D and
the M43 direction decision (sequences vs Alchemy) remain independent and pending.

## Remains proposed / not accepted / gated
- Wave A+B is proposed until the ChatGPT/User gate. Waves C (evidence lifecycle index/links) and D (checker
  scoping) remain closed. No accepted package moved; no evidence rewritten. No runtime/mechanics/data/admission
  change; no optimizer/economics/public-output/automation; MML/SOURCE-PROVENANCE/crafted-capacity/PD-013 open.
- Acceptance authority remains ChatGPT/Kirill; this verdict is advisory; no agent self-acceptance.

---
- author: `claude`
- document_type: `repo_structure_cleanup_audit`
- status: `advisory verdict — GO; docs/tooling/routing cleanup only (fingerprint unchanged); stale claims re-pointed to ledger; evidence + boundaries intact; dispatcher-pollution guard added`
