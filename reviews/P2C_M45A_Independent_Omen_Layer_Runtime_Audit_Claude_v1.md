# M45-A Independent Omen Layer Runtime — Claude Audit

audit_id: `P2C_M45A_Independent_Omen_Layer_Runtime_Audit_Claude_v1`
auditor: `claude`
package: `packages/proposed/P2C_M45A_Independent_Omen_Layer_Runtime_Result_Codex_v1/`
observed_repo_head: `4420a40b07038139922d706117bde550c43ce27e`
observed_active_task_sha: `b99365920ed0cbbf08b2ab0cc3008ee9f897caaea595dfa972c9611e5d728982`
verdict_style: `GO / GO WITH CHANGES / NO-GO`
authority_note: advisory only. Omen effects are project-model, not server truth. Acceptance is ChatGPT/Kirill.

---

## Plain-language summary
This turns on the ten Omens — the modifiers that steer a currency you already have. I checked the two things I
asked for at the design stage and both are done: (1) Omens now carry an explicit "is this executable?" flag, so
just being listed in the data never means an Omen runs; (2) Greater Exaltation (the only one that adds *two*
modifiers) had its rules explicitly locked in at your gate, not slipped through with the simple filters. By
running the code I confirmed the tricky mechanics are right: side filters go on the **removal** for
Chaos/Whittling/Perfect Essence (the add is untouched), Whittling removes the lowest-level mod then breaks ties
the way we agreed, and Greater Exaltation's two adds either both succeed or the item is untouched. Nothing about
the existing currencies changed — the filters are optional and default to "no filter", and the whole test suite
(300) passes. **Verdict: GO.**

## Verified by execution / byte inspection
- **Exactly ten Omens admitted.** `omens.yaml` now carries `runtime_admission_status` + `availability_status`
  per Omen; only the ten clean-core Omens are `accepted_executable_modifier`
  (Greater/Sinistral/Dextral Exaltation, Sinistral/Dextral Annulment, Sinistral/Dextral Erasure, Whittling,
  Sinistral/Dextral Crystallisation). The other seven present rows (light, necromancy×2, liege, blackblooded,
  sovereign, abyssal_echoes) are `blocked_or_out_of_scope`; historical Alchemy/Coronation/Greater Annulment
  remain absent. This is the admission-registry deliverable I required — catalogue presence ≠ execution.
- **Accepted operations unchanged (additive filters).** The hooks added to `ordinary_add`, `annulment`,
  `chaos_like`, `perfect_essence`, `rarity_progression` are optional params defaulting to `None`/`False` (=
  accepted behaviour); the Omen path engages only with admitted Omen metadata and validates the effect plan
  fail-closed. Base-op behaviour is proven unchanged by one-step parity + full regression.
- **Filter/application stages are correct (verified against accepted mechanics):**
  - Exalted add-side → the add pool (`rarity_progression`/`ordinary_add`).
  - Annulment removal-side → the fractured-protected removable pool.
  - Chaos (Erasure) + Whittling → the **removal** pool, **add stage unchanged**
    (`test_m45a_chaos_erasure_and_whittling_filter_removal_before_unchanged_add`).
  - Whittling → eligibility/fractured exclusion → `lowest_modifier_level` → uniform project-policy tie.
  - Perfect Essence Crystallisation → the **terminal-feasible removal** pool, **not the guaranteed add**
    (`test_m45a_crystallisation_filters_feasible_removal_not_guaranteed_add`).
- **Greater Exaltation matches the User-ratified contract.** `greater_exaltation.py`: two sequential accepted
  ordinary-weighted adds over an isolated workspace with branch-state rebuild, exact product mass (`Fraction`),
  canonical terminal aggregation, and atomic rollback/no-consumption if either add fails
  (`..._is_atomic_exact_and_replayable`, `..._insufficient_side_capacity_rolls_back_before_draw`). No partial
  one-add state.
- **Fail-closed compatibility.** `omen.py` `compile_omen_effects` rejects unknown, non-admitted, unavailable,
  duplicate, out-of-allowlist, wrong-group, and same-dimension-collision requests via a pinned
  (group, dimension, effect) matrix — validated, never inferred from order
  (`..._fails_closed_on_duplicate_incompatible_unavailable_and_wrong_group`).
- **Composition-safe.** `test_m45a_direct_resolver_and_m43a_one_step_exact_parity` proves a direct call, a
  resolver call, and a one-step M43-A sequence give the identical result; seeded MC replays with diagnostics.
- **Project-model, source-open.** `mechanics_evidence.yaml` `omen_layer_m45a`: `project_model_source_open`,
  `server_truth_claimed: false`, admitted-omen list + availability requirement.
- **Suites green.** `test_m45a_*` = **18 passed**; full `pytest` = **300 passed** on a clean clone; foundation
  fingerprint reproduces the package-pinned `3b20a622…` (changed only for the Omen admission data);
  ACTIVE_TASK validator + public-numeric-leak guard PASS.

## Watchpoints (non-blocking)
- Omen effects (side filters, Whittling tie, Greater Exaltation two-add) stay project-model / server-unverified,
  correctly recorded as source-open. Admission does not close that.
- Historical/drop-disabled Omens, Greater Annulment two-removal, light/Desecrated, Jawbone/Reveal/PD-013,
  Fracture, and any planner/optimizer remain separate gates — none entered this delta.

## Recommendation
**GO.** Accept M45-A as the independent Omen layer: ten side-filter/selector + double-add Omen effects over
accepted operations, applied at the correct pool stages through the resolver seam, additive and fail-closed,
with Greater Exaltation's ratified atomic two-add contract, an explicit Omen admission/availability registry,
and direct/resolver/M43-A parity. Both design-audit conditions (admission registry; Greater Exaltation
ratification) are satisfied. Nothing self-accepts.

## Remains proposed / not accepted / gated
- M45-A is proposed until the ChatGPT/User gate. The seven blocked Omens, historical/drop-disabled Omens,
  Greater Annulment two-removal, light/Desecrated, Jawbone/Reveal/PD-013, Fracture, Essence repeat/capacity,
  longer/unbounded routes, planner/optimizer/economics, public numbers, automation — all closed.
  MML/SOURCE-PROVENANCE/crafted-capacity/PD-013 stay open.
- Acceptance authority remains ChatGPT/Kirill; this verdict is advisory; no agent self-acceptance.

---
- author: `claude`
- document_type: `omen_layer_runtime_audit`
- status: `advisory verdict — GO; ten Omens over accepted operations, correct pool stages, additive + fail-closed, Greater Exaltation ratified two-add atomic; admission registry added; 300 tests pass`
