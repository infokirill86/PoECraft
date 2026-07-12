# M47 Mechanics Decision Closure — Claude Audit

audit_id: `P2C_M47_Mechanics_Decision_Closure_Audit_Claude_v1`
auditor: `claude`
package: `packages/proposed/P2C_M47_Mechanics_Decision_Closure_Codex_v1/`
observed_repo_head: `988d006da2812c594a2026fcfae25ea2ec92e21d`
observed_active_task_sha: `21f2701be7dee1481fbedb92e49ab81be935b0219ff86f8b94b6deb5aecc21fc`
verdict_style: `GO / GO WITH CHANGES / NO-GO`
authority_note: advisory only. Documentary decision-recording; no runtime admitted; PD-013 not closed. Acceptance is ChatGPT/Kirill.

---

## Plain-language summary
This writes down the Desecrated decisions you already made, so they're on record before we build anything.
Everything you ratified is captured exactly — Reveal shows three and you pick one; only one Desecrated per item,
no rune; the Fracture rules (a hidden slot counts toward the four but can't be hit → your 1-in-3; a revealed
one can be hit and becomes fractured+desecrated); Echoes reroll is its own currency where the same mod can come
back, at tier level; Omen of Light is its own later piece. All of it is marked "our model, not confirmed server
behaviour, and not turned on yet." Importantly, it **did not** quietly decide the parts you still need to check
in-game — above all the exact Reveal offer/sampling maths (D4) — those stay open. Nothing runs; only text was
added. Full test suite (316) passes. **Verdict: GO.**

## Verified by execution / byte inspection
- **Documentary only — no runtime.** The only change since M47 acceptance is `data/mechanics_evidence.yaml`
  (+29/-3); no `src`/`config`/`tests`. Foundation fingerprint unchanged (`2e5e4454…` — mechanics_evidence is
  documentary, not a fingerprint input); static-data tests + full `pytest` = **316 passed**; validator PASS.
- **Ratified rules recorded exactly as decided** (`m47_ratified_rules` + updated `fracturing_revealed_
  desecrated`), all `USER_RATIFIED_PROJECT_RULE...RUNTIME_NOT_ADMITTED`, `server_truth_claimed: false`:
  - Reveal: `offer_count: 3`, `installed_choice_count: 1`.
  - `desecrated_limit`: max 1 hidden-or-revealed, `rune_bypass: false`.
  - Unrevealed placeholder + Fracture: `counts_toward_fracture_minimum: true`,
    `eligible_fracture_target: false` (= the 1-of-3 rule).
  - Revealed + Fracture: `eligible_fracture_target: true`, `combined_fractured_and_desecrated_flags_valid:
    true` (→ fractured+desecrated).
  - Echoes: `separate_currency: true`, `same_modifier_may_reappear: true`, `model_granularity:
    tier_not_value`, `runtime_admitted: false`.
  - Omen of Light: `separate_later_gate: true`, `runtime_admitted: false`.
  These match Kirill's ground truth and my prior decision-routing precisely.
- **PD-013 correctly stays open.** `pd013_blocker_closed: false`, `runtime_extension_admitted: false`. The
  Fracture-Desecrated *project policy* is recorded but is **not** a runtime extension of M46-A and does not
  close PD-013.
- **The genuinely-open decisions are NOT force-closed.** Doc 06 lists D1–D5 as `pending` with source-aligned
  *recommendations* only, and states explicitly: "No recommendation is accepted merely because it is the
  recommended option; a later gate must name the selected model for every row." Critically,
  `reveal.sampling_algorithm_closed: false` — **D4 (the exact offer sampling algorithm) stays open**, which is
  exactly the probability-critical decision I flagged as still needing your in-game verification.
- **No re-interpretation of the ratified set.** Doc 06 fences the ratified rules from being reopened during
  D1–D5 closure. Correct separation.

## Watchpoints (non-blocking)
- Before M47-A: the gate must still explicitly select **D1–D5**, above all **D4 the Reveal sampling algorithm**
  (weighting unit, without-replacement, family/group order, display-order meaning). The package's D-A
  recommendations are candidates, not accepted. Consider Kirill's in-game check for D4 (the offer composition)
  since it drives Reveal probabilities.

## Recommendation
**GO.** Accept the M47 mechanics decision closure as a documentary record of the User-ratified Desecrated rules
(project-model/source-open, runtime not admitted, PD-013 open). Do not authorize M47-A until D1–D5 are
explicitly selected (especially D4). Omen of Light, Echoes, Lich exactness, and the Fracture combined-state
runtime remain separate gates. Nothing self-accepts.

## Remains proposed / not accepted / gated
- No runtime admitted; Jawbone/Reveal rows stay blocked. D1–D5 (incl. D4 sampling), Omen of Light, Echoes
  reroll runtime, Lich exactness, Fracture combined-state runtime, and PD-013 remain open/gated.
  MML/SOURCE-PROVENANCE/crafted-capacity/PD-013 stay open.
- Acceptance authority remains ChatGPT/Kirill; this verdict is advisory; no agent self-acceptance.

---
- author: `claude`
- document_type: `mechanics_decision_closure_audit`
- status: `advisory verdict — GO; ratified Desecrated rules recorded (project-model, not admitted, PD-013 open); D1-D5 incl. D4 sampling correctly left pending; fingerprint unchanged, 316 tests pass`
