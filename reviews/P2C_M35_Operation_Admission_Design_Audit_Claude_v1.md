# M35 Operation-Admission Design Audit (Claude)

audit_id: `P2C_M35_Operation_Admission_Design_Audit_Claude_v1`
auditor: `claude`
package: `packages/proposed/P2C_M35_Operation_Admission_Design_Codex_v1/`
audit_type: design/definition audit (no implementation to execute)
observed_repo_head: `f9b7b4e71a15ba1ee139dc40a6c442ef1340a485`
observed_active_task_sha: `55d504cc8d9922baa317785755aec8048d91a44aa32c45ea0a4e207a928479c1`  (SHA-256 of the exact `work/active/ACTIVE_TASK.md` bytes audited, at HEAD f9b7b4e, before this review's dispatcher update)
verdict_style: `GO / GO WITH CHANGES / NO-GO`
authority_note: advisory only. Accepting this authorizes the M35 design; Annulment implementation (M35-A)
remains a separate ChatGPT/User gate.

---

## Plain-language summary
This is the design for **how a new crafting operation gets admitted**, plus the concrete design of the first
one — **Annulment** ("remove a random modifier"). It's the first real step toward the actual product (more than
one currency). I checked that it (a) stays a lean checklist rather than an over-engineered "operation engine,"
(b) folds in every fix the gate required, and (c) is technically correct. It does all three — and it even
caught a subtlety I didn't flag: if the item has two identical mods, removing either gives the *same* result,
so their odds must be added together. The sacred rule (never remove the fractured mod) is protected and is
required to be a real failing test, not just a note. No code, boundaries respected, hashes clean. **Verdict:
GO.** Actual Annulment code stays a separate gate.

## Verdict
**GO.** Complete, correct, lean design that satisfies the gate-required refinements and adds correct depth.
Recommend accepting the M35 design and authorizing **M35-A (Annulment runtime)** as a separate implementation gate.

## Gate-required refinements — all incorporated
1. **Lean / Annulment-anchored:** §02 states "M35 must not create a generalized operation algebra... minimum
   repeatable checklist... then apply to Annulment." ✓
2. **Fractured protection as a hard tested property:** §03 "Annulment must never remove fractured modifiers";
   §04 requires a negative control that "intentionally break[s]... fractured exclusion and prove[s] hard
   failure"; §07 lists `annulment_fractured_never_removed` as a required test. ✓
3. **Empty-pool no-transition:** §03/§04 — if no removable non-fractured mods, return
   `NO_TRANSITION_NO_CONSUMPTION`, no fabricated removal, no state mutation, input digest = output digest,
   no-transition mass exactly one. ✓
4. **Exact-oracle uniform 1/k + project-model label:** §04 — k removable non-fractured instances → each path
   exact rational `1/k`, reduced form; §03 — "Annulment semantics ... PROJECT-MODEL BEHAVIOR ONLY", SOURCE/
   PROVENANCE stays open. ✓

## Design strengths
- **Reusable-but-lean admission framework (§02).** A concrete 9-point checklist (identity; I/O state contract;
  pool-builder dependency; transition semantics; exact/oracle shape; MC shape; replay/trace; boundary labels;
  regression protection) + a required 4-gate structure (design → implementation authorization → implementation
  audit → acceptance) with no design-package self-acceptance. General enough to reuse for Chaos/Perfect Essence
  later, concrete enough to admit only Annulment now.
- **Correct exact oracle with real depth (§04).** Beyond uniform 1/k, it correctly separates **path identity**
  (the removal key chosen) from **terminal identity** (canonical post-removal state), and requires
  **duplicate-instance aggregation** — two removal keys that delete indistinguishable duplicates and yield the
  same canonical terminal must **sum** their exact path masses. This is a genuine correctness subtlety, caught
  unprompted.
- **Reuses the accepted kernel.** §03 requires M35-A to prove the existing fractured-excluding
  `build_removal_pool` (verified present, excludes fractured) is the load-bearing path feeding Annulment
  probabilities — not a parallel reimplementation.
- **Regression discipline.** §02.9 and §07 require accepted `ordinary_add` tests to remain unchanged and
  passing, and a fail-closed on unsupported operation variants.
- **Implementation correctly gated (§07).** M35-A is explicitly "Not authorized by this package," with a narrow
  suggested scope and a strong required-evidence/test list (fractured-never-removed, empty-pool no-transition,
  duplicate-instance aggregation, replay determinism, ordinary_add regression, fail-closed).

## Checks
Design-only: diff since base is the M35 package + dispatcher/ledger/status only (no `src/`/`tests/`). Package +
root `SHA256SUMS` PASS; no numeric leak. Consistent with `CURRENT_STATUS.md`, the ledger, and standing
boundaries. Boundaries respected: no implementation/acceptance of Annulment; no optimizer/economics/advice; no
public numbers; no SOURCE/PROVENANCE/MML/PD-013 closure; no automation.

## Watchpoints for M35-A (non-blocking)
- Make duplicate-instance terminal aggregation a **required** (not optional) M35-A test — it is the easiest
  correctness detail to get subtly wrong.
- Pin Annulment's admissible item rarities/classes in the M35-A contract (the framework's I/O contract covers
  it; state it concretely).
- Keep Annulment deterministic-per-model (removes exactly one of k, or explicit empty no-transition) — no
  hidden fail/no-op chance beyond empty pool, unless a later gate adds it with evidence.

## Recommendation
Accept the M35 design (admission framework + Annulment candidate). Authorize **M35-A Annulment Runtime
Admission** as a separate implementation gate with its own pinned contract, folding in the watchpoints. Nothing
self-accepts; no executable operation is opened by accepting this design.

---
- author: `claude`
- document_type: `design_definition_audit`
- status: `advisory verdict — GO; M35-A implementation pending separate ChatGPT/User gate`
