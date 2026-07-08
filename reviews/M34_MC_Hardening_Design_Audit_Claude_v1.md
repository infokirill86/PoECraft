# M34 MC-Hardening Design/Definition Audit (Claude)

audit_id: `M34_MC_Hardening_Design_Audit_Claude_v1`
auditor: `claude`
package: `packages/proposed/P2C_M34_MC_Hardening_Design_Definition_Codex_v1/`
repo_head_audited: `58f12c7`
base_commit: `ca4adda`
audit_type: design/definition audit (no implementation to execute)
verdict_style: `GO / GO WITH CHANGES / NO-GO`
authority_note: advisory only. This audits a **plan**, not code. Accepting it authorizes the M34 design as
the plan; it does not authorize implementation — that is a separate ChatGPT/User gate.

---

## Plain-language summary
This is a **plan for M34**, not code yet. It says how the Monte Carlo engine should be "hardened" beyond
M33: run the convergence checks across many seeds (not just one), test short chains of the accepted
operation, and make any failure print enough detail to reproduce it. **The plan is well-scoped and honest:**
it explicitly forbids new mechanics, optimizer/economics, and public numbers, and it recommends splitting
the work into a smaller M34-A (many-seed, single-step) then M34-B (short sequences) to keep each step
auditable. It even plans a "negative-control" test — deliberately breaking the sampler to prove the tests
can actually fail. **Verdict: GO** — accept the design and let M34-A be built first (still one separate
`Go`). Nothing here starts implementation. One thing to pin before building is noted below.

## Verdict
**GO.** Sound, correctly bounded design/definition. Recommend accepting it as the M34 plan and authorizing
**M34-A** implementation first (separate gate), with one build-time decision to pin (below). It directly
resolves the M33 watchpoints I carried forward (multi-seed, multi-step).

## What was checked
- **Design-only — confirmed.** No `src/` or `tests/` change since `ca4adda`; the diff is the M34 package +
  `CURRENT_STATUS` + `ACTIVE_TASK` + `SHA256SUMS`. Package + root `SHA256SUMS` PASS; package numeric-leak
  scan PASS.
- **Scope/boundaries — correct.** `02` and `06` forbid new mechanics, operation expansion beyond accepted
  `ordinary_add`, optimizer/advice/ranking, economics/EV/cost/expected-attempts, public numeric release,
  server-truth claims, and closure of SOURCE/PROVENANCE, MML, PD-013; no auto-run / GitHub Actions. Matches
  the accepted doctrine.
- **Addresses my carried-forward watchpoints.** Multi-seed convergence (M34-A) and multi-step/sequence
  validation (M34-B) are exactly the two I flagged at M33.
- **Design quality is good.** Concrete numeric-free pass/fail criteria; required replay/diagnostic fields
  (seed, run id, tier, step, pool digest, selected key, pre/post hash, failed rule); a **negative-control
  test** that proves a biased sampler would fail (the suite has teeth); honest risk register including
  "scope creep into implementation" and "constructed sequences must be labeled project-model."
- **Split A/B is the right call.** Matches the project's step-size rule (smaller auditable gates), keeps
  failure causes unmixed, and lowers accidental-operation-expansion risk. M34-A first is well justified.

## One decision to pin at M34-A build time (non-blocking for the design)
The multi-seed rule "no branch may exceed the envelope for any seed/tier" interacts with the seed-set size:
across a large seed × tier × branch grid, an envelope that is too tight would make a *correct* sampler fail
by chance (flaky), while one too loose is toothless. The design already lists this as a predeclared choice
("any breach is hard failure vs aggregate seed-level criteria"). Pin it before running M34-A: either keep a
wide per-branch envelope (≈6σ, as M33 uses, so family-wise false-failure stays negligible) with the hard
"no breach" rule, **or** adopt an explicit aggregate/expected-breach-rate rule. State the chosen rule and
seed list up front. This is a build-time parameter, not a design defect.

## Watchpoints (unchanged, non-blocking)
- Multi-step sequences of repeated `ordinary_add` are a **constructed** hardening fixture, not a claimed real
  crafting route — the design correctly requires this be labeled; keep that label explicit in M34-B.
- Governance: `ACTIVE_TASK.md` remains heavy — keep trimming toward a thin dispatcher.

## Recommendation
Accept the M34 design as the plan. Authorize **M34-A** (multi-seed single-step hardening + negative control +
leak-safety) as the next build, pinning the multi-seed breach rule/seed list first; then M34-B (short
sequences) as a separate gate. Implementation is not authorized by accepting this design. Nothing self-accepts.

---
- author: `claude`
- document_type: `design_definition_audit`
- status: `advisory verdict — GO; M34 implementation pending separate ChatGPT/User gate`
