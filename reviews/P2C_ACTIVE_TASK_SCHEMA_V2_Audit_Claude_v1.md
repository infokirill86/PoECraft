# ACTIVE_TASK_SCHEMA_V2 Result Audit (Claude)

audit_id: `P2C_ACTIVE_TASK_SCHEMA_V2_Audit_Claude_v1`
auditor: `claude`
package: `packages/proposed/P2C_ACTIVE_TASK_SCHEMA_V2_Result_Codex_v1/`
observed_repo_head: `9e1019ddd0a03745e07db8b38ada10288fe5caf3`
observed_active_task_sha: `5212d5a6e1a04df66250ab2e2396f3aa4a9d03d21d4253f06552596d576b06b5`  (SHA-256 of the exact `work/active/ACTIVE_TASK.md` bytes audited, at HEAD 9e1019d, before this review's own dispatcher update)
verdict_style: `GO / GO WITH CHANGES / NO-GO`
authority_note: advisory only. Claude does not accept or close. Acceptance stays with ChatGPT/User.

---

## Plain-language summary
Codex turned `ACTIVE_TASK.md` into the strict thin dispatcher we asked for, and all five of my earlier
changes (C1–C5) are in. I checked the actual file bytes, not just the look of it. **The scare about "the
whole thing is one long line" is a false alarm — a raw-viewer artifact: the real file is 79 normal lines and
parses as valid YAML.** Standing rules now live once in the manifest and the dispatcher just points to them;
read-receipts live in packages/reviews (not logged into this file); the validator is only proposed, not
built. Nothing touched code, tests, mechanics, or the ledger, and M34-B was not started. **Verdict: GO.**

## Verdict
**GO.** Faithful, minimal implementation of `ACTIVE_TASK_SCHEMA_V2`; C1–C5 incorporated and independently
verified from bytes. Recommend acceptance of the workflow-hygiene schema at ChatGPT/User discretion.

## Required-check results (all confirmed from exact bytes)
- **HEAD verified:** `observed_repo_head = 9e1019d…`. `observed_active_task_sha = 5212d5a6…` (above).
- **Valid parseable YAML frontmatter, not just visually YAML:** `yaml.safe_load` on the frontmatter returns a
  dict with all 14 mandatory fields.
- **"One long physical line" = FALSE (viewer artifact, not a defect).** The file is 2537 bytes, **79 newline-
  separated lines**, no CRLF, longest line 110 chars; first lines are properly separate (`---`,
  `schema_version: "2.0"`, …). The single-line appearance is a raw/cache rendering artifact, not the bytes.
- **No prose before frontmatter:** file starts with `---`. ✓
- **Exactly one live state:** one `status` (`ready_for_claude`), one `next_actor` (`claude`), one
  `allowed_next_action`. ✓
- **No history/task log** remains; the old narrative blocks are gone. ✓
- **Human summary (4 lines) introduces no new state** — it restates task/actor/action and the "routing only,
  not truth" principle. ✓
- **Standing boundaries referenced, defined once:** `standing_boundaries_ref` →
  `manifest/GitHub_Workflow_Protocol.md#standing-boundaries-for-active-task-dispatcher` (section present);
  the inline `forbidden_next_actions` are task-specific only. ✓ (my C3)
- **Read-receipt rule documented, no read-log churn:** protocol §"ACTIVE_TASK read receipt rule" requires
  `observed_repo_head` + `observed_active_task_sha`, and states the latter must be the SHA-256 of the exact
  `ACTIVE_TASK.md` file bytes acted on (my C4 refinement). The package's own `00_README_FIRST.md` carries a
  receipt — and it is **honest**: its `observed_active_task_sha b6b6ce2…` exactly equals ACTIVE_TASK.md at the
  pre-Codex commit `514a81b`. The mechanism works on its first use. ✓
- **C1–C5 incorporated & verified:** C1 six-status enum only (no `*_working_or_pending_push`); C2 pruned to
  the mandatory set (no `phase`/`milestone`/`builder`/`auditor`/`required_*_paths`); C3 standing boundaries in
  manifest + pointer; C4 read receipts in packages/reviews; C5 validator proposed in a "Deferred validator"
  section, **no `tools/` code or tests added**. ✓
- **Status/actor consistency rules added to the protocol** (`ready_for_codex⇒codex`, `ready_for_claude⇒claude`,
  etc.). ✓
- **Automation manual/disabled:** `mode: manual`, `enabled: false`, `max_handoffs: 0`. ✓
- **No code/tests/mechanics/data change:** diff since `514a81b` touches only `ACTIVE_TASK.md`, the protocol,
  the package, and `SHA256SUMS.txt`. ✓
- **M34-B not started/designed:** the only M34-B/sequence mentions in the diff are inside forbidden lists. ✓
- **Boundaries open:** ledger untouched; SOURCE/PROVENANCE, MML, PD-013 not closed. ✓
- **Integrity:** package `SHA256SUMS` PASS; root `SHA256SUMS` PASS. ✓

## Watchpoints (non-blocking)
- The status/actor consistency + single-live-state rules are documented but not yet mechanically enforced —
  by design (C5 validator deferred). Fine for now; build the small `check_active_task.py` when a real drift is
  observed, per the process-change-on-failure rule.
- Keep the post-block human summary permanently short; do not let evidence/history creep back in.

## Recommendation
Accept `ACTIVE_TASK_SCHEMA_V2` as the workflow-hygiene dispatcher standard, at ChatGPT/User discretion. Then
future tasks should populate this schema (and each Codex package / Claude review carries its read receipt).
Nothing here self-accepts; M34-B remains a separate gate.

---
- author: `claude`
- document_type: `workflow_hygiene_audit`
- status: `advisory verdict — GO; acceptance pending ChatGPT/User`
