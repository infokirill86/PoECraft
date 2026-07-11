# M44 Alchemy Mechanics Design Verification — Claude Audit

audit_id: `P2C_M44_Alchemy_Mechanics_Design_Verification_Audit_Claude_v1`
auditor: `claude`
package: `packages/proposed/P2C_M44_Alchemy_Mechanics_Design_Verification_Codex_v1/`
observed_repo_head: `cff00323ad7923f0fcc9c79314e942ffa301eb55`
observed_active_task_sha: `4fe73b6ea73a7bd957237c20a4b9d4aa8c27e7dd5db828e14574d383be506dfe`
verdict_style: `GO / GO WITH CHANGES / NO-GO`
authority_note: advisory only. Design/mechanics verification; the four-modifier sampling model is project-model, not server truth; acceptance is ChatGPT/Kirill.

---

## Plain-language summary
This checks Alchemy before we build it. Alchemy turns a white or blue item into a yellow one with **four** new
random modifiers (the old blue mods are thrown away). I did my own source check independently of Codex, and the
facts line up: exactly 4 modifiers (PoE2-specific — PoE1 gave 4–6), works on Normal or Magic, originals not
kept, capped at 3 per side. On your earlier "is it 2-2 or 3-1?" question — the honest answer is **neither is
fixed**: the four land randomly across prefix/suffix by weight, capped at 3 a side, so you can get 3-1, 2-2, or
1-3, but never 4-0. Codex modelled it as "add four modifiers one at a time, rechecking room each time," which
reproduces exactly that, and — importantly — it **did not pretend to know the server's exact internal roll**;
it flagged that as an open project-model decision for you. It also correctly refuses Alchemy on a **fractured**
item for now (our base is fractured, so Alchemy is really for the white/blue starting route). **Verdict: GO** on
the design; one decision is yours to ratify.

## Diligence-test result (you asked me to hold my check and see if Codex caught the questions)
Codex substantially **passed**. Independently of me it confirmed the count (4), the Normal/Magic input, and the
replacement rule — all of which my own source pass agrees with. Crucially, it did **not** silently invent a
fixed distribution or a server sampling algorithm: it explicitly labelled the exact four-modifier roll as
**unresolved / project-model** and asked for your gate, and it flagged the fractured-input interaction as
unverified and fenced it off. That is exactly the behaviour we want — it surfaced the uncertainty instead of
guessing. The only thing I'd add over its wording is the plain-language answer to your 2-2/3-1 question above
(weight-driven, capped at 3/side, never 4-0), which its sequential model already realises.

## Verified against real bytes + independent sources
- **Design-only.** No `src`/`data`/`config`/`tests` change since M43-A acceptance (`39039ae..HEAD`); the
  `alchemy` row stays `data_reference_candidate` (not admitted).
- **Repo comparison is byte-accurate.** `operations.yaml` `alchemy`: input `[normal, magic]`, atomic, output
  `rare`, `remove: all_explicit`, `add: ordinary_weighted_sequential count 4`, sequence
  `[discard_all_explicit, create_empty_rare_shell, add_ordinary_x4, commit]` — matches doc 03 exactly.
- **Independent source check agrees** (my own, held back from Codex per the test): 4 modifiers exactly
  (PoE2-specific), Normal/Magic input, original Magic mods not retained, Rare, max 3 prefix / 3 suffix; the 4
  distribute by weight across both sides capped at 3/side. No source I checked exposes the server's exact
  internal sampling algorithm — matching Codex's "unresolved" flag.
- **Sound atomic architecture.** One consumption boundary, one atomic result: isolated empty-Rare working copy →
  four sequential accepted ordinary-weighted adds with legality/capacity rebuild after each → commit only if all
  four succeed; any empty intermediate pool / precondition failure → whole-operation no-transition/no-consumption
  (no partial-Rare, no <4-mod result). Reuses accepted kernels; correctly **not** compiled as four
  caller-visible M43-A steps.
- **Unresolved items correctly surfaced, not decided:** (a) fractured-input behaviour → M44-A floor rejects
  fractured input unchanged (defensible: "originals not retained" vs "fractured immutable" is an undocumented
  joint case); (b) exact 4-modifier sampling algorithm → adopt sequential accepted-pool sampling only as
  labelled project-model, pending an explicit user gate. Non-equipment item classes excluded.
- **Boundaries intact.** Base non-fractured quarterstaff Alchemy only; no Alchemy variants/Omens/modifier
  layers, maps/jewels, conditional/retry/route generation, optimizer/economics/advice, public numbers, or
  SOURCE-PROVENANCE/MML/crafted-capacity/PD-013 closure.

## The one decision for the gate (advisory lean)
Ratify **"four modifiers via sequential accepted ordinary-weighted add with capacity rebuild"** as the
project-model implementation of Alchemy's 4-mod roll (server-unverified, recorded in `mechanics_evidence` as
source-open). I lean **for** it: it's the standard crafting-sim model, reproduces the correct
weight-driven/capped distribution, and reuses accepted kernels — but it is a project-model probability choice,
so it needs your explicit acceptance, exactly like the Perfect-Essence removal model. Keep the fractured-input
rejection as the floor.

## Recommendation
**GO** on the M44 Alchemy mechanics verification. Authorize a later **M44-A** implementing base non-fractured
quarterstaff Alchemy as one atomic multi-add (four sequential accepted weighted adds, isolated Rare working
copy, all-or-nothing commit) through the resolver/executor-registry, with one-step direct/resolver parity and
M43-A one-step parity, exact/oracle + MC + replay + negative controls — only after you ratify the sequential
sampling model. Fractured input, variants, Omens, and other item classes stay separate gates.

## Remains proposed / not accepted / gated
- No M44 runtime/admission; the `alchemy` row stays a candidate. Fractured-input Alchemy, variants,
  Omens/Whittling/Fracture/Desecrate, non-equipment classes, conditional/retry/route generation,
  planner/optimizer/economics, public numbers, automation — all closed. MML/SOURCE-PROVENANCE/crafted-capacity/
  PD-013 stay open.
- Acceptance authority remains ChatGPT/Kirill; this verdict is advisory; no agent self-acceptance.

---
- author: `claude`
- document_type: `alchemy_mechanics_design_verification_audit`
- status: `advisory verdict — GO; base non-fractured Alchemy = atomic 4x sequential weighted add (project-model, server-unverified); Codex passed the diligence test; sampling model needs a user gate`
