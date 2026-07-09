# Agent Role-Packs Design Audit (Claude)

audit_id: `P2C_Agent_Role_Packs_Design_Audit_Claude_v1`
auditor: `claude`
package: `packages/proposed/P2C_Agent_Role_Packs_Design_Codex_v1/`
audit_type: workflow-configuration design audit (design-only; no files created)
observed_repo_head: `b9cca26fcd04b7727d64654d2ac0eb4323e88c73`
observed_active_task_sha: `c4d18f79dcf145ed2d1e21495e899c7e6f505cf82c54aa0ff802b394c9739edc`
verdict_style: `GO / GO WITH CHANGES / NO-GO`
authority_note: advisory only. This audits a plan; creating the role files is a separate ChatGPT/User gate.

---

## Plain-language summary
This plans small always-on instruction files so we stop re-typing the same long prompts: `AGENTS.md` for
Codex, `CLAUDE.md` for me, a shared `Agent_Role_Pack.md` for the common rules, and optional "skills" left for
later. It's the right idea and correctly set up: the files stay compact, they keep both agents as
**critics/auditors (not silent executors)**, and they explicitly keep **acceptance with you and ChatGPT** —
the files never grant an agent the power to accept anything. I confirmed from my own side that `CLAUDE.md` is
indeed the file Claude reads, and that skills are fine to defer. **Verdict: GO WITH CHANGES** — approve the
layout, with a few tweaks so the same rules don't get copied into four files (drift risk) and so the always-on
file also carries the checksum-hook step that keeps getting forgotten.

## Verdict
**GO WITH CHANGES.** Correct minimal setup; preserves participants and the gate; reduces prompt length without
hiding gate decisions. Fold in the refinements below when the files are actually written.

## Focus questions — findings
1. **Minimal setup correct?** Yes. Clean separation: UI personalization (per-account, doesn't travel) vs
   repo-level instructions (`AGENTS.md`/`CLAUDE.md`) vs shared doctrine (`manifest/Agent_Role_Pack.md`) vs
   optional skills. ✓
2. **Codex → `AGENTS.md`?** Correct — the standard repo instruction file Codex reads; proposed content is
   compact (read-order + role + execution + response format). ✓
3. **Claude → `CLAUDE.md`?** Correct, and **verified from my environment**: root `CLAUDE.md` is the persistent
   project instruction surface Claude Code loads. Proposed content (auditor-designer, "don't rubber-stamp,"
   advisory-not-acceptance, verdict + plain-language format) matches how the role actually works. ✓
4. **Skills — needed now or deferred?** Correctly **deferred** (`.claude/skills/.../SKILL.md` /
   `.agents/skills/...`) until the always-on files prove insufficient. Verified: `.claude/skills/<name>/SKILL.md`
   is the right location and skills load on demand. Deferral avoids premature bloat. (Note: a `p2c-audit-workflow`
   skill is a genuinely strong *future* candidate — my audits are highly repetitive — but not needed now.) ✓
5. **Avoids protocol bloat?** Yes, and self-aware: Risks list "protocol bloat" and "instruction drift"; stop
   triggers block files that exceed compact size or duplicate ledgers. ✓ (See refinement 1 — push this further.)
6. **Preserves participants, not silent executors?** Yes, explicitly. `Agent_Role_Pack §Participant critique
   duty` folds in the Participant Voice Charter (raise material objections on correctness/source/foundation/
   cost/safety/direction; don't object on taste). AGENTS.md = "builder-critic"; CLAUDE.md = "contradiction
   finder, don't rubber-stamp." ✓
7. **Reduces long prompts without hiding gate decisions?** Yes. Standing role/workflow moves to always-on
   files (so prompts can be "Go. Audit X."), while volatile gate decisions stay in chat/ledger — Risk #3
   ("persistent instructions do not automate handoff") and Gate discipline ("no agent self-accepts") keep gates
   explicit. ✓
8. **Keeps ChatGPT/Kirill as acceptance authority?** Yes, explicitly in all three files. ✓

## Claude-specific verification (requested)
- Root `CLAUDE.md` is the correct persistent repo instruction surface — **confirmed**.
- `.claude/skills/<name>/SKILL.md` is appropriate for an optional future audit-workflow skill — **confirmed**;
  deferral is right.
- No Claude-specific assumption in the package is wrong; no required corrections there.

## Refinements to fold in before/at implementation (non-blocking)
1. **One doctrine source, reference not restate.** The participant-duty / gate-discipline / plain-language rules
   currently appear in `AGENTS.md`, `CLAUDE.md`, *and* `Agent_Role_Pack.md` — and they already exist in the
   **accepted** `manifest/Participant_Voice_Charter.md` and `manifest/GitHub_Workflow_Protocol.md`. To avoid the
   drift the package itself warns about, keep the authoritative copy in the accepted manifests, make
   `Agent_Role_Pack.md` a thin "who does what + pointers," and let `AGENTS.md`/`CLAUDE.md` be read-order +
   the agent-specific one-liner + output format only. Minimize duplication to one place.
2. **Put the recurring hook step in `AGENTS.md` explicitly.** Root-`SHA256SUMS.txt` drift has recurred ~7×
   because the builder clone forgets it. AGENTS.md's "use repo SHA tools before commit/push" should be explicit:
   *run `python tools/update_sha256sums.py` before every push, and set `git config core.hooksPath tools/hooks`
   once per clone.* This is the best use of an always-on file — it mechanically fixes the recurring miss.
3. **Fold the read-receipt rule** (`observed_repo_head` + `observed_active_task_sha`) into both files' output
   sections, since it's a standing requirement.

## Boundaries (confirmed)
Design-only: no `AGENTS.md`/`CLAUDE.md`/skills created; no runtime/mechanics/data change; no operation
admission; no automation; no accepted-truth change; ledger not self-accepting. (Root manifest regenerated in
this commit — recurring builder-side SHA drift; builder clone still needs `core.hooksPath`.)

## Recommendation
Accept the role-packs direction and layout; authorize a separate implementation floor to create the compact
files with refinements 1–3 folded in (single doctrine source; hook activation + read receipt in AGENTS.md;
skills deferred). Nothing self-accepts; ChatGPT/Kirill remain the acceptance gate.

---
- author: `claude`
- document_type: `workflow_configuration_design_audit`
- status: `advisory verdict — GO WITH CHANGES; implementation of role files pending separate gate`
