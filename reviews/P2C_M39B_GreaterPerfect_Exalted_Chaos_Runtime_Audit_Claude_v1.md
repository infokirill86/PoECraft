# M39-B Greater/Perfect Exalted + Chaos Runtime Audit (Claude)

audit_id: `P2C_M39B_GreaterPerfect_Exalted_Chaos_Runtime_Audit_Claude_v1`
auditor: `claude`
package: `packages/proposed/P2C_M39B_GreaterPerfect_Exalted_Chaos_Runtime_Result_Codex_v1/`
observed_repo_head: `ce1e46abb0fcce067def9f9165e59ab2b5089e1d`
observed_active_task_sha: `04222cf7831b57f4ff89eb0af5e05109b803f9a618b0dd6f407d90bf92781124`
verdict_style: `GO / GO WITH CHANGES / NO-GO`
authority_note: advisory only. Admits real runtime — acceptance is ChatGPT/Kirill; MML stays project-model, not server truth.

---

## Plain-language summary
This is the first time real "upgraded" currencies become runnable: Greater/Perfect Exalted and Greater/Perfect
Chaos — four in total. I checked the mechanics against what you set, by running the code, not by trusting the
notes. They behave exactly as agreed:
- **Greater/Perfect Exalted** = our already-accepted "add one modifier" step, just restricted to higher-level
  modifiers (Greater ≥ 35, Perfect ≥ 50). No new engine, only the accepted one with a filter.
- **Greater/Perfect Chaos** = the accepted base Chaos: remove one modifier **uniformly** (fractured stays
  protected, exactly like before), then add one — and the level filter applies **only to the add**, never to
  the removal. I verified in code that the removal step gets no filter at all.
The four numbers (which currencies, and the 35/50 levels) are read from the data file, not hand-coded, so the
mechanic is one shared engine plus data — not four copy-pasted currencies. Everything else (base Exalted,
other families, Essences, Whittling, Omens) still refuses to run. Full test suite (160) passes on my clean
copy. **Verdict: GO.** Two things to keep an eye on below, neither blocking.

## Verified by execution / byte inspection
- **Data change is exactly the four authorized rows.** `data/operations.yaml`: `greater_exalted`,
  `perfect_exalted`, `greater_chaos`, `perfect_chaos` flipped `admission_candidate` →
  `accepted_executable_runtime`. Base `exalted` stays `admission_candidate`. Nothing else changed.
- **MML is row-declared, not hardcoded.** Resolver `_declared_add_mml` reads `transition.add.mml` from the
  admitted row (Greater = 35, Perfect = 50, present in the data); caller-supplied MML for a catalog row is
  rejected ("fixed by its admitted operation row"). No per-currency MML table in code.
- **Shared kernels, composition not duplication.** Exalted → `OrdinaryAddOperation(mml=...)` through the
  accepted ordinary-add pool builder. Chaos → `ChaosLikeOperation(mml=...)` through the accepted base-Chaos
  harness. No variant-specific add/remove code was written.
- **Chaos removal is provably unchanged.** `build_removal_pool` (`chaos_like.py:216–224`) builds
  `RemovalPoolRequest(item_class, state)` with **no MML**; `operation.mml` is passed only in `build_add_pool`
  (`:226–234`). So removal stays the base uniform, non-fractured, combined eligible-instance pool; MML narrows
  only the post-removal add pool. Fractured protection and atomic remove-then-add commit are the pre-existing
  accepted path.
- **Strong fail-closed guards (verified they raise).** New `_validate_catalog_input_rarity` (must be `rare`),
  `_validate_m39b_exalted_transition` (remove `none`, one `ordinary_weighted` add, atomic), and
  `_validate_m39b_chaos_transition` (`uniform_installed_instance` removal count 1 with `fractured` excluded,
  one weighted add, atomic). `chaos_like._validate_operation` additionally enforces
  `operation.mml == row-declared mml` (caller cannot inject a different MML) and keeps "base chaos must not use
  MML". Empty post-removal add pool → atomic no-transition/no-consumption (no remove-only terminal).
- **Boundaries held.** Base `exalted` rejected (outside the Exalted allowlist *and* not admitted); other
  Greater/Perfect families (Transmutation/Augmentation/Regal), Essence, Whittling, side/desecrated Omens, any
  `active_modifier_ids`, and non-base `variant_id` all fail closed. Omen parameters present in the row data are
  **not** executed — only the base single-add/single-remove variant runs.
- **Semantic fingerprint retune is legitimate.** `validate_foundation` reproduces Codex's
  `90e4b017…` on my clone; the two fingerprint-oriented test edits only update the admitted-row list to the six
  real rows and move a mutation probe to the still-candidate `exalted` row.
- **Tests pass on my clean clone.** Full suite **160 passed**; `test_m39b_*` (9) + M37-A/M38-A/foundation
  regressions (49 together) pass; `check_public_numeric_leaks` → PASS. No public numeric probabilities emitted.

## Watchpoints (non-blocking — for the ChatGPT/User gate)
1. **Base-Exalted asymmetry (by design).** After this batch a caller can run `greater_exalted` / `perfect_exalted`
   while base `exalted` remains fail-closed. The builder critique argues this is fine (the executable kernel —
   accepted `ordinary_add` — is already accepted; the base wrapper adds no new mechanic). I agree it is
   consistent and safe, but it is a real, visible asymmetry — the gate should confirm it is intended for now.
2. **MML numbers are now runtime-active but source-open.** 35/50 drive real distributions yet live only in
   `operations.yaml`. `mechanics_evidence.yaml` records the MML *policy* as
   `supported_empirically_server_unconfirmed` (covers exalted/chaos) but not the specific thresholds.
   Recommend cross-referencing the 35/50 values there as project-model / server-unconfirmed so the source
   status of the actual numbers is explicit. This does **not** close MML.

## Recommendation
**GO.** Accept M39-B as the first Greater/Perfect Exalted + Chaos runtime batch (project-model only). The
mechanic matches the accepted M37 base-Chaos policy (uniform non-fractured removal) and the M39/M39-A MML
posture (add-pool filter), composed through shared kernels. Suggest the gate (a) confirm the base-Exalted
asymmetry is intended and (b) log the 35/50 thresholds in `mechanics_evidence.yaml` as source-open.

## Remains proposed / not accepted / gated
- Base `exalted`; Greater/Perfect Transmutation / Augmentation / Regal; Essence; Whittling; side/desecrated
  Omens; any new operation; longer chains; planner/optimizer/economics/advice — all still closed.
- MML not closed; SOURCE/PROVENANCE not closed; PD-013 not closed; no public numeric release; no automation.
- Acceptance authority remains ChatGPT/Kirill; this verdict is advisory; no agent self-acceptance.

---
- author: `claude`
- document_type: `operation_runtime_admission_audit`
- status: `advisory verdict — GO; four Greater/Perfect Exalted+Chaos rows admitted as project-model runtime via shared kernels; MML stays open`
