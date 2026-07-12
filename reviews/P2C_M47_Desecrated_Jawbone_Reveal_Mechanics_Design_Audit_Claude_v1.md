# M47 Desecrated / Jawbone / Reveal Mechanics Design — Claude Audit

audit_id: `P2C_M47_Desecrated_Jawbone_Reveal_Mechanics_Design_Audit_Claude_v1`
auditor: `claude`
package: `packages/proposed/P2C_M47_Desecrated_Jawbone_Reveal_Mechanics_Design_Codex_v1/`
observed_repo_head: `ac29248cfca909130f035da3df06349d4c7d7e8e`
observed_active_task_sha: `1f4dac86b0ea71aa9f5a8438c85c9a85d96ba60583423ce5861fd959e6e4651b`
verdict_style: `GO / GO WITH CHANGES / NO-GO`
authority_note: advisory only. Design/mechanics verification; multiple probability-affecting decisions are ChatGPT/Kirill's. PD-013 not closed. Acceptance is ChatGPT/Kirill.

---

## Plain-language summary
This maps out Desecrated crafting before we build it — the biggest remaining mechanic. Flow: a **Jawbone** adds
one **hidden** ("unrevealed") slot of a fixed side; later a **Reveal** turns it into one real modifier chosen
from **three offered options**; an item can hold only **one** Desecrated thing at a time. This matches exactly
what you told me. The design is honest: it lays out the confirmed core, and it **refuses to turn anything on
until you decide the parts that change the odds** — mainly the exact Reveal offer/sampling rules. Two nice
things: it correctly splits **reroll (Echoes)** and **targeted removal (Omen of Light)** off as their own
future pieces, and it keeps the Fracture↔Desecrated question open (PD-013) rather than guessing. Good news for
you: **you've already answered several of these decisions in our chat** — so the gate can just ratify those,
and only a couple genuinely still need your in-game check. **Verdict: GO** on the verification.

## Verified against ground truth + real bytes
- **Design-only.** No `src`/`data`/`config`/`tests` change; the 3 Jawbone rows and `reveal_desecrated` stay
  `blocked_or_out_of_scope`. The `DesecratedPlaceholder` domain type already exists (fields
  `side`/`jawbone_id`/`reveal_mml`/`lich_tag_constraint`), so no new state algebra is needed — the design uses
  it, not a fake modifier id.
- **Confirmed core matches Kirill's ground truth:** Jawbone → one **unrevealed** placeholder of fixed side that
  consumes that side's capacity; **single-Desecrated limit**; Reveal offers **three**, installs one canonical
  modifier with `desecrated: true` on the same side (consumes ordinary capacity, blocks family/groups,
  participates in canonical state/replay); Ancient Jawbone carries **MML** with the accepted family-fallback;
  fractured mods stay immutable and can't be removed by Jawbone; failure → no-transition/no-consumption. Also
  correctly: **Desecrated ≠ crafted**, and a revealed mod **cannot gain `fractured`** until PD-013 is decided.
- **Reroll and targeted removal correctly split off:** Echoes reroll (M47-D8) and Omen of Light targeted removal
  (M47-D6) are identified as separate gated pieces — matching that they are their own currencies. The base
  M47-A is just Jawbone + Reveal.
- **It surfaces the probability-affecting decisions instead of encoding YAML as truth** (D1–D8), and explicitly
  says a candidate answer "does not become accepted merely because it is already in YAML or tested as a
  prototype." Correct posture (same discipline as M42/M44/M46).

## Decision routing (the useful part) — what you've already answered vs what's still open
You gave me project-authority answers in chat that resolve several of these — the gate can **ratify**, not
re-deliberate:
- **Reveal = choose 1 of 3** — confirmed (matches the design).
- **Single Desecrated per item, no rune bypass** — confirmed (design says single-limit; note the "no rune"
  explicitly at M47-A).
- **M47-D7 (Fracture ↔ Desecrated) — you resolved this:** an **unrevealed** placeholder is **excluded from the
  Fracture target pool but counts toward the ≥4 minimum** (the 1-of-3 odds trick); a **revealed** Desecrated
  mod **is** a valid Fracture target → if hit it becomes **fractured + desecrated** (both flags, like
  crafted+fractured). This resolves the PD-013 Fracture sub-question by project authority; the design's "no
  default" was correct-by-design, but it can now be ratified rather than left open.
- **Reroll (Echoes):** separate currency; the **same mod can reappear** (no exclusion); **tier-level** (we don't
  model values) — record this for the D8 gate.

Genuinely still open — need your in-game verification before M47-A (these change exact probabilities):
- **M47-D4 — the exact Reveal offer/sampling algorithm** (weighting unit, without-replacement, family/group
  order, whether displayed order matters). This is the probability-critical one.
- **M47-D3** exclusive-offer guarantee, **M47-D2** full-item replacement, **M47-D1** side selection when both
  sides have room, **M47-D5** insufficient-pool behaviour.

## Recommendation
**GO** on the M47 verification. Before authorizing **M47-A** (Jawbone + Reveal batch over the existing
`DesecratedPlaceholder`, atomic, fail-closed, with direct/resolver/M43-A parity), the gate should: (a) **ratify**
the already-answered rules (Reveal-1-of-3, single-limit/no-rune, D7 Fracture interaction, Echoes reroll rule) —
recorded in `mechanics_evidence` as project-model/source-open; and (b) **decide/verify** the still-open ones,
above all **D4 the Reveal sampling algorithm**. Do not build a state shell before the offer/sampling policy is
pinned (the design says this too). Omen of Light, Echoes, Lich exactness, and the Fracture combined-state
runtime stay separate gates.

## Remains proposed / not accepted / gated
- No M47 runtime/admission; Jawbone/Reveal rows stay blocked. Reveal sampling/offer policy, full-item
  replacement, side selection, Omen of Light, Echoes reroll, Lich exactness, Fracture combined-state, PD-013 —
  all open/gated. MML/SOURCE-PROVENANCE/crafted-capacity/PD-013 stay open.
- Acceptance authority remains ChatGPT/Kirill; this verdict is advisory; no agent self-acceptance.

---
- author: `claude`
- document_type: `desecrated_jawbone_reveal_mechanics_design_audit`
- status: `advisory verdict — GO; Jawbone→unrevealed→Reveal(1-of-3)→install desecrated matches ground truth; 8 decisions surfaced; several already answered by Kirill (ratify), D4 sampling still needs verification`
