# ACTIVE_TASK_SCHEMA_V2 Proposal Audit (Claude)

audit_id: `ACTIVE_TASK_SCHEMA_V2_Proposal_Audit_Claude_v1`
auditor: `claude`
audit_type: **proposal / design audit** (pre-build; requested by Kirill). Not an audit of a built package.
proposal_audited: `P2C_ACTIVE_TASK_SCHEMA_V2_Proposal_ChatGPT_draft_v1.md` (ChatGPT, proposal-only)
observed_repo_head: `c34d056`
observed_active_task_sha: (ACTIVE_TASK.md at `c34d056`)
verdict_style: `GO / GO WITH CHANGES / NO-GO`
authority_note: advisory only. This audits a **proposal**; it does not implement or accept it. Building the
schema is Codex's step; acceptance is ChatGPT/User. I did not modify the live dispatcher.

---

## Plain-language summary
ChatGPT proposed turning `ACTIVE_TASK.md` into a strict "thin dispatcher" so agents stop confusing live
state with history/proposals/accepted truth. **The idea is right and fixes a real problem we actually hit
(this file kept bloating — I flagged it three times).** The proposal's core rules are sound. My main pushback
is to make it *smaller*, not bigger: a schema that lists every standing rule in every task is the same bloat
in a new costume. **Verdict: GO WITH CHANGES.** Adopt the tighter version your own prompt already implies
(6 statuses, read-receipts in packages/reviews not in this file), keep only task-specific forbidden items
here, and point to the manifest for the standing ones. Then Codex builds the minimal version and I re-audit.

## Verdict
**GO WITH CHANGES.** The proposal correctly targets a real, observed failure (so it satisfies the
"process-change only on observed failure" rule) and its fail-closed principles are correct. Five required
changes below make it minimal and prevent re-bloat; then it is safe for Codex to implement.

## Answers to the proposal's own audit questions (§8)
1. **Removes the failure or just longer?** Removes it *only if kept minimal*. As drafted (8 statuses, ~20
   fields, full standing-forbidden list inline) it risks re-creating the bloat it fixes. With the changes
   below, it genuinely removes it.
2. **Redundant/dangerous fields?** Yes — `phase`, `milestone`, `last_completed_gate`, `current_gate_required`,
   and `required_input_paths`/`required_output_paths` overlap with `current_result_path`/`current_review_path`
   and `allowed_next_action`. Prune.
3. **Missing fields?** Your prompt's `forbidden_next_actions` should be **task-specific only**, plus one field
   pointing at the manifest for standing boundaries (see C3). Otherwise the mandatory set is complete.
4. **Enums sufficient/unambiguous?** The tighter 6-status set (your prompt) is better than draft_v1's 8 — see C1.
5. **Is `repo_head_at_last_update` enough, or a read receipt too?** A read receipt is needed, but **not** in
   this file — see C4. Endorsed exactly as your prompt states.
6. **Overfit to one failure?** No, if minimal; the fail-closed + single-live-state rules are general.
7. **Cockpit-not-museum preserved?** Yes, and strengthened — provided C2/C3 keep it thin.
8. **New write-location ambiguity?** No new mailbox; good. Keep it that way (do not add `handoff/`).
9. **Separates proposed/accepted/active/historical?** Yes — R5 + pointing to ledger/reviews/packages is the
   right split.
10. **Automation stays disabled?** Yes (R6, `enabled:false`, `max_handoffs:0`). Correct.
11. **Builder/auditor/gate independence preserved?** Yes (`acceptance_authority: chatgpt_user`, separate
    builder/auditor). Keep.

## Required changes before Codex implements (blocking, most-important first)
- **C1 — Adopt the tighter 6-status enum** (`awaiting_user_gate, ready_for_codex, ready_for_claude,
  audited_pending_user_gate, blocked_for_human, accepted_closed`). Drop draft_v1's
  `codex_working_or_pending_push` / `claude_working_or_pending_push`: "mid-work" states are exactly the
  ambiguous in-between that the read-receipt mechanism (C4) makes unnecessary, and they invite dispatcher
  churn. Fewer states = stronger fail-closed.
- **C2 — Prune to the mandatory field set** (the 14 in your prompt). Make `schema_name`, `phase`, `milestone`,
  `builder`, `auditor`, `updated_by` optional-or-omit; drop `required_input_paths`/`required_output_paths`
  (covered by `allowed_next_action` + `current_result_path`/`current_review_path`). Over-fielding is itself
  the bloat failure mode.
- **C3 — Keep standing boundaries in the manifest, not inline (the real anti-bloat fix).** The recurring
  13-item "not_authorized / forbidden" block (no optimizer, no PD-013 closure, no public numbers, …) is
  INVARIANT — it belongs in `manifest/` + START_HERE §6, referenced once. `ACTIVE_TASK.forbidden_next_actions`
  should list only **task-specific** forbidden actions (e.g. `start_m34b`) plus a single pointer field like
  `standing_boundaries_ref: manifest/GitHub_Workflow_Protocol.md`. This is what actually stops the file
  re-growing every gate.
- **C4 — Read receipt lives in packages/reviews, not in ACTIVE_TASK.** Endorse your rule verbatim: never
  update ACTIVE_TASK just to log a read; every Codex result package and every Claude review must carry
  `observed_repo_head` and `observed_active_task_sha`. Add this as a rule in `GitHub_Workflow_Protocol.md`.
  Note: `observed_active_task_sha` should be the **SHA-256 of the ACTIVE_TASK.md file bytes** the actor acted
  on (not HEAD) — that is what actually detects a stale raw/cache read, since HEAD can move while this file
  does not, and vice versa.
- **C5 — Propose a validator, do not build it now.** The `consistency_rules` (status↔next_actor, `enabled=false
  ⇒ max_handoffs=0`, "referenced not established") are good but are only text until enforced. Per your scope,
  propose a tiny future `tools/check_active_task.py` (single machine block, enum membership, status/actor
  consistency, one-live-state) as a deferred follow-up — not runtime work in this hygiene delta. Until then
  the schema relies on fail-closed discipline + read receipts, which is acceptable.

## Non-blocking watchpoints
- **Version-label discrepancy:** the task prompt names `..._revised_v2.md`, but only
  `..._draft_v1.md` exists locally. I audited `draft_v1` (the sole extant proposal); confirm it is the intended
  target, or supply `revised_v2`.
- Keep the post-block human summary to a few lines and forbid it from introducing any state not in the machine
  block (proposal R3 — keep it).

## Recommendation
GO WITH CHANGES. Authorize Codex to implement the **minimal** SCHEMA_V2 (C1–C4 folded in, C5 proposed-not-built),
updating `work/active/ACTIVE_TASK.md` + `manifest/GitHub_Workflow_Protocol.md` + a short proposed package, then
set `ready_for_claude` for my re-audit. Do not open M34-B; do not touch code/mechanics; keep automation disabled.
Nothing here self-accepts.

---
- author: `claude`
- document_type: `proposal_design_audit`
- status: `advisory verdict — GO WITH CHANGES; implementation by Codex, acceptance by ChatGPT/User`
