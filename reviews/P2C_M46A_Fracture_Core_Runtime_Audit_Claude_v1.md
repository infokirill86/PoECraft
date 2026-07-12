# M46-A Fracture Core Runtime — Claude Audit

audit_id: `P2C_M46A_Fracture_Core_Runtime_Audit_Claude_v1`
auditor: `claude`
package: `packages/proposed/P2C_M46A_Fracture_Core_Runtime_Result_Codex_v1/`
observed_repo_head: `5abc11c0b85c8b500adca99c2826f19d30d0f961`
observed_active_task_sha: `6d177af5a146b9f5e03bd400614e5d9a3697b288df79d68bb6339f2760e3785d`
verdict_style: `GO / GO WITH CHANGES / NO-GO`
authority_note: advisory only. Fracture stays project-model; Desecrated/PD-013 not closed. Acceptance is ChatGPT/Kirill.

---

## Plain-language summary
This makes the Fracturing Orb runnable. On a Rare item with at least four mods and none already fractured, it
locks one modifier chosen **evenly from all of them** (no prefix/suffix lottery, no weighting) so no currency can
ever remove or change it again. I ran it and checked the parts that matter: it correctly refuses any item that
has fewer than four mods, an already-fractured mod, or any Desecrated mod (that disputed case stays out until we
build the Desecrate wave). A **crafted mod can be fractured and stays crafted** (both flags), exactly as you
described. And once a mod is fractured, all the currencies we've already built keep skipping it — I verified
that by running Annulment/Chaos/capacity and Alchemy against fractured items. It behaves identically whether
called directly or inside a route. Full test suite (316) passes. **Verdict: GO** — this closes the Fracture
mechanic.

## Verified by execution / byte inspection
- **Only `fracturing_orb` admitted** (`disputed_or_requires_user_resolution` → `accepted_executable_runtime`);
  `project_scope` activates the fracture group; `sources.yaml` adds the Fracture sources; nothing else admitted.
- **Preconditions fail-closed exactly as designed:** `< 4 explicit → at_least_four...`; `any fractured →
  existing_fractured_modifier_forbidden`; `unrevealed_desecrated is not None → forbidden`; `any desecrated
  instance → forbidden`; plus rare/item-class/canonical checks. The clean floor rejects every Desecrated state,
  so the disputed 25%/33% edge is not modelled (PD-013 stays open).
- **Uniform combined-pool selection.** `build_fracture_pool` enumerates all installed instances as
  `Candidate(key, 1)` — **uniform, weight-independent, no side-first**; per-instance identity keeps duplicates
  distinct. Test `..._combined_pool_is_uniform_and_includes_crafted_instances` + a negative control
  (`..._negative_control_proves_nonuniform_pool_fails_hard`) prove uniformity; exact mass via `Fraction`.
- **One-bit atomic mutation; crafted preserved.** `..._crafted_selection_preserves_crafted_and_changes_one_flag`
  confirms exactly one flag (`fractured`) flips on the selected instance, the `crafted` flag is preserved
  (fractured+crafted), everything else byte-equivalent; failure → no-transition/no-consumption unchanged.
- **Fractured immutability across accepted operations (the load-bearing safety).**
  `..._fractured_immutability_across_accepted_removal_and_capacity` and `..._alchemy_remains_fail_closed_on_
  fractured_input` pass: accepted Annulment/Chaos removal pools and capacity logic keep excluding/counting the
  fractured instance, and Alchemy stays fail-closed on fractured input.
- **Composition-safe.** `bounded_sequence.py` change is additive fracture executor registration;
  `..._direct_resolver_and_m43a_exact_and_seeded_parity` proves direct = resolver = one-step M43-A;
  `..._seeded_replay_and_internal_mc_match_exact_envelope` confirms MC↔exact convergence + deterministic replay;
  `..._resolver_fails_closed_on_variant_omen_and_wrong_rarity` keeps unsupported variants/Omens fail-closed;
  `..._public_summary_remains_numeric_probability_free` — no public numbers.
- **Project-model, source-open.** `mechanics_evidence.yaml` `fracture_core_m46a`: `project_model_source_open`,
  `server_truth_claimed: false`, `selection: uniform_without_generation_weights`, `existing_fractured_modifier_
  count: 0`, with the 0.2.0e Divine-on-fractured bug-fix cited for numeric immutability.
- **Suites green.** `test_m46a_*` = **16 passed**; full `pytest` = **316 passed** on a clean clone; foundation
  fingerprint `2e5e4454…` is self-consistent (the pinned-fingerprint regression tests pass); ACTIVE_TASK
  validator + public-numeric-leak guard PASS. (The `8066ec77` in the read receipt is the observed
  `active_task_sha`, not a fingerprint.)

## Watchpoints (non-blocking)
- Our pinned accepted base is already fractured, so it fails the no-existing-fracture precondition — M46-A
  Fracture applies to *other* Rare states in a route, not the base staff. (Expected.)
- Desecrated↔Fracture (unrevealed excluded-but-counts → 1-of-3; revealed → fractured+desecrated) is deferred to
  the Desecrate wave, where Desecrated states can first exist. Kirill's project-authority rules are recorded for
  that wave; Fracture admission does not close PD-013.

## Recommendation
**GO.** Accept M46-A as base clean Fracture: uniform combined-pool 1-of-N (≥4, no existing fracture,
non-Desecrated) one-bit atomic mutation with crafted preserved, full fractured-immutability across accepted
operations, and direct/resolver/M43-A parity — project-model/source-open. This closes the Fracture mechanic.
Desecrated/Revealed/Jawbone/PD-013, multi-fracture, side-directed Fracture, and other item classes stay gates.

## Remains proposed / not accepted / gated
- M46-A is proposed until the ChatGPT/User gate. Desecrated/Fracture interaction, Revealed/Jawbone/Reveal/
  PD-013, multiple fracture, side-directed Fracture, non-quarterstaff/unique/corrupted classes,
  planner/optimizer/economics, public numbers, automation — all closed. Crafted-capacity/MML/SOURCE-PROVENANCE/
  PD-013 stay open.
- Acceptance authority remains ChatGPT/Kirill; this verdict is advisory; no agent self-acceptance.

---
- author: `claude`
- document_type: `fracture_core_runtime_audit`
- status: `advisory verdict — GO; base Fracture = uniform combined-pool 1-of-N one-bit atomic; crafted-can-be-fractured; immutability across accepted ops verified; Desecrated/PD-013 deferred`
