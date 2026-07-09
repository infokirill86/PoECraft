# M37 Mechanics-Verification Audit (Claude)

audit_id: `P2C_M37_Mechanics_Verification_Audit_Claude_v1`
auditor: `claude`
package: `packages/proposed/P2C_M37_Mechanics_Verification_Codex_v1/`
observed_repo_head: `1947c735b453b0fadcd3088bdda95479a03c98b7`
observed_active_task_sha: `3000b5c5e43a34d1dd655d3c14124628a6fcf2ee2d6e62c47abc065106af7a0d`
verdict_style: `GO / GO WITH CHANGES / NO-GO`
authority_note: advisory only. The base-selection rules are **project-model policy** and require a ChatGPT/User gate; they are not server truth.

---

## Plain-language summary
This package re-checks, against sources and our own data, how the base currencies actually pick what to
remove/add. It lands the right answers: base **Chaos/Annulment removes a random mod uniformly among all
eligible mods** (no side-picked-first); **Exalted-style adding uses one weighted pool** of all legal mods;
and **"remove the weakest" (Whittling) and side-locking are Omens layered on top, not base behavior.** It's
honest that public sources don't *prove* the exact server odds, so it labels these as our project-model rule
needing your gate, with a real in-game test as the only path to server-truth certainty. I cross-checked the
claims against our actual engine code and they match. **Verdict: GO.**

## Verdict
**GO.** The verification is accurate, correctly scoped to project-model policy (not server truth), and
resolves the earlier M37 removal-rule ambiguity (Whittling = Omen layer). Requires a ChatGPT/User gate to
adopt the rules as project-model policy.

## The three required base-selection checks (verified against OUR code, not just the package's claims)
- **Annulment removal = all eligible removable instances, uniform (NOT side-first).** Our
  `build_removal_pool` sets `Candidate(row.key, 1)` — every non-fractured removable instance gets equal
  weight over one combined pool (1/k). Matches the package and the verified PoE1 model. ✓
- **ordinary_add / Exalted-like add = one combined legal weighted pool (NOT prefix/suffix-side-first).** Our
  `build_ordinary_add_pool` sets `Candidate(mod.mod_id, mod.generation_weight)` over all legal mods of both
  sides, with side only a **capacity filter** (`free_by_side[...] > 0`). Note: a *weight-proportional*
  side-first is mathematically identical to a combined weighted pool (P(mod)=weight/total either way); the
  only wrong model would be a **fixed 50/50 side split**, which our code does **not** do. ✓
- **Omens / currency modifiers = separate behavior layers, not base mechanics.** `data/omens.yaml` carries
  `whittling` (`selection: minimum_modifier_level`) and side Omens as metadata; our pools apply `side_filter`
  as an optional layer (base = `None` → combined). The package correctly treats Whittling and side/desecrated
  Omens as overrides on top of base Chaos/Annulment/Exalted. ✓

## Source honesty (as required)
The package's `02_SOURCE_TABLE` documents that **no accessible public source proves the base remove/add server
distribution** (Craft of Exile PoE2 is experimental/disclaimed; patch notes don't specify; wikis say only
"random"). It therefore classifies base removal-uniformity and add-weighting as **project-model policy
(`PROJECT_ADOPTED_INFERENCE`), not server truth**, and states server-truth confidence needs later
user-approved in-game/emulator testing. This is exactly the required treatment. It also correctly keeps
Chaos rows `admission_candidate` and reiterates `active_in_current_simulation` ≠ executable.

## Resolves the earlier M37 design flag
My M37 design audit flagged the base-Chaos removal rule as unresolved (uniform vs whittling). This package
resolves it: **base Chaos removal is uniform; Whittling is an Omen override** (poe2db Omen of Whittling +
`data/omens.yaml`). So the M37 design's "uniform base, defer whittling" is correct — with the fix that
Whittling must be documented as Omen-only (the package proposes this correction).

## Recurring integrity issue
Root `SHA256SUMS.txt` FAILed again at the delivered HEAD (still drifting on the builder side because its clone
has not run `git config core.hooksPath tools/hooks`). Regenerated here via `tools/update_sha256sums.py`.
Builder-clone hook activation remains the outstanding fix.

## Recommendation
Accept the verification and adopt, via ChatGPT/User gate, the project-model rules: (1) base removal = uniform
over eligible non-fractured installed instances; (2) base add = one combined `generation_weight`-weighted
legal pool with side as capacity constraint; (3) Whittling / side / desecrated behaviors are Omen layers, not
base mechanics — all labeled project-model, not server truth, SOURCE/PROVENANCE open. Fold the M37 design
correction (Whittling = Omen-only) before M37-A. Then the open follow-up (verify `ordinary_add` side handling)
is effectively answered: our add pool is combined-weighted, not fixed-50/50. Nothing self-accepts.

---
- author: `claude`
- document_type: `mechanics_verification_audit`
- status: `advisory verdict — GO; base-selection rules are project-model policy pending ChatGPT/User gate`
