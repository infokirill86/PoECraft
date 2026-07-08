# M34-B Design Audit (Claude)

audit_id: `P2C_M34B_Design_Audit_Claude_v1`
auditor: `claude`
package: `packages/proposed/P2C_M34B_Design_Codex_v1/`
audit_type: design/definition audit (no implementation to execute)
observed_repo_head: `307ee3ae7d90dca2ae48af5f62a3e13b259de575`
observed_active_task_sha: `1b95fe697f1b2466e150e6d213540fe7bdec43243767a85f73e052b217bf5a61`  (SHA-256 of the exact `work/active/ACTIVE_TASK.md` bytes audited, at HEAD 307ee3a, before this review's dispatcher update)
verdict_style: `GO / GO WITH CHANGES / NO-GO`
authority_note: advisory only. This audits a **plan**. Accepting it authorizes the M34-B1 design; it does
not authorize implementation — that is a separate ChatGPT/User gate.

---

## Plain-language summary
This is the **plan for M34-B** — testing short chains of the accepted operation (two steps: do it, then do
it again from the new item). The plan is good and, importantly, **deliberately narrow:** Codex pushed back on
the risky reading and scoped it to exactly two steps ("M34-B1"), so it validates the chaining seam without
turning into a route-planner. It correctly nails the hard part — the exact answer for a two-step chain has to
be computed by walking the whole branch tree and rebuilding the pool after step 1 from the *new* state, then
grouping by the final item — and it lists the exact ways a fake "sequence" test could cheat and forbids them.
Design-only (no code), nothing touched, boundaries open. **Verdict: GO.** A few things to pin before building
are noted; none block accepting the plan.

## Verdict
**GO.** Sound, correctly-bounded M34-B1 design. Recommend accepting it as the plan and authorizing **M34-B1**
implementation as a separate build (with a pinned contract). Build-time watchpoints below.

## What was checked
- **Design-only:** no `src/`/`tests/` change; diff is the M34-B package + `ACTIVE_TASK` + `SHA256SUMS`.
  Package + root `SHA256SUMS` PASS; package numeric-leak scan PASS.
- **Full-participant critique (01):** Codex correctly flagged that a broad generic sequence layer would blur
  MC-hardening into a planner/strategy engine (a doctrine risk — optimizer is last and separately gated) and
  narrowed to a two-step floor. Good scope discipline.

## Design strengths
- **Exact sequence oracle is correct (07).** Build step-0 pool from S0 → enumerate → apply transition → S1 →
  **rebuild step-1 pool from that branch-specific S1** → enumerate → aggregate terminal probability by
  **canonical terminal-state identity across paths**. This targets the real new risk (branch-state pool
  rebuild) and compares by canonical state, not path text. Correct.
- **Sequence model (03)** pins step-identity/replay fields, the pool-rebuild rule (step-1 pool must not reuse
  step-0's or be built from S0), terminal canonical identity, and explicit no-transition handling (record,
  don't fabricate).
- **Anti-cheat acceptance list (08).** Explicitly rejects the ways a "sequence" test could be faked: single-
  step repeated under a new name; a display pool while MC masses use a stale pool; terminal hashes without
  step linkage; single-seed replay; missing negative control; silently skipping the oracle. This is mature.
- **Tractability/ceiling safeguards (05, 07).** Explicit pre-execution ceilings; if exact enumeration exceeds
  them, stop and report — must **not** silently drop the oracle for approximate-only validation.
- **Boundaries/read-receipt (08).** Non-goals correct (no planner/optimizer/economics/operation-expansion/
  public numbers/server-truth/boundary closure); requires read receipts; human gate still required after GO.

## Build-time watchpoints to pin before M34-B1 runs (non-blocking for the design)
1. **Rare-terminal sensitivity.** Applying the inherited M34-A 6σ per-branch envelope to *terminal* counts:
   rare terminals (tiny mass) at modest sample tiers land in the low-count regime where 6σ is very wide (weak
   sensitivity) — the M34-A caveat, amplified by the tree. Keep fixtures small/balanced enough that terminal
   masses aren't negligibly tiny, or add a per-step marginal check alongside the terminal check.
2. **Exact terminal mass as rationals.** Keep terminal probabilities as exact rationals (sum of path products;
   common denominator = product of per-step totals) to preserve the integer-exact comparison style used in
   M33/M34-A. The design implies aggregation but should pin the rational arithmetic.
3. **Explicit constructed-fixture labels.** The "project-model fixture when labeled" requirement is present
   but light (04) — make each two-step fixture explicitly labeled a constructed hardening sequence, not a real
   crafting route, in the result package.
4. **Pin the execution contract** (seeds, tiers, ceilings, tolerance) up front, as M34-A did.

## Recommendation
Accept the M34-B1 design as the plan. Authorize **M34-B1** implementation (two accepted `ordinary_add` steps,
exact-oracle terminal comparison, deterministic replay, negative control, leak safety) as a separate build,
pinning the contract and folding in the four watchpoints. Later ≥3-step / variable-length sequences require
their own gate. Nothing self-accepts; implementation is not authorized by accepting this design.

---
- author: `claude`
- document_type: `design_definition_audit`
- status: `advisory verdict — GO; M34-B1 implementation pending separate ChatGPT/User gate`
