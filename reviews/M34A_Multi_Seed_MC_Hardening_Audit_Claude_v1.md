# M34-A Multi-Seed MC-Hardening Audit (Claude)

audit_id: `M34A_Multi_Seed_MC_Hardening_Audit_Claude_v1`
auditor: `claude`
package: `packages/proposed/P2C_M34A_Multi_Seed_MC_Hardening_Result_Codex_v1/`
repo_head_audited: `cd0fefc`
base_commit: `cd2f28e`
verdict_style: `GO / GO WITH CHANGES / NO-GO`
authority_note: advisory only. Claude does not accept or close. Acceptance stays with ChatGPT/User.

---

## Plain-language summary
M34-A is the first "hardening" build from the M34 plan. Instead of one seed, it now runs the convergence
check across a **fixed set of seeds and sample sizes** on the big lopsided pool, proves the run **replays
identically** for the same seed, and — the key part — includes a **negative control that deliberately breaks
the sampler and confirms the test fails with a full, reproducible error report** (seed, tier, branch, pool
digest, deviation vs tolerance). I ran it myself: **4/4 M34-A tests pass, full suite 96, no numbers leak,
hashes match, and nothing was self-accepted.** The build also matches the exact contract the gate pinned
(seeds 34001–34003, tiers 512/2048/8192, 6σ rule). **Verdict: GO.** Still single-step and test-only;
sequences (M34-B) remain a separate gate.

## Verdict
**GO.** M34-A faithfully implements the pinned contract and the design intent, verified by execution.
Recommend M34-A acceptance at ChatGPT/User discretion. M34-B / full M34 stay closed.

## What was verified by execution
- **4/4 M34-A tests pass**; full suite **96 passed**; test-only (no `src/` change).
- **Boundaries clean:** package numeric-leak scan PASS; root + package `SHA256SUMS` PASS.
- **No self-acceptance:** ledger diff since base adds only the prior **M34-design** acceptance row; no
  M34-A / M34-B / full-M34 acceptance is written in-commit.

## Findings against the pinned contract and design
- **Contract pinned & guarded.** Constants match the gate's contract exactly (seed list `34001/34002/34003`,
  tiers `512/2048/8192`, σ-multiplier `6`), and `test_m34a_execution_contract_is_pinned` asserts them, so any
  silent drift fails.
- **Multi-seed × multi-tier hardening.** Runs the full seed × tier grid over the broad 8-branch Fibonacci-
  skewed fixture (with family/group/suffix-capacity blockers), reusing the same verified 6σ binomial
  per-branch tolerance from M33-P1 (`|X−np| ≤ 6σ`, integer-exact). Support-subset and count-sum are checked.
- **Deterministic replay.** Same seed + run id reproduces identical `result_hash` and trajectories, across
  every seed in the list.
- **Negative control with teeth + actionable diagnostics.** A forced maximal breach makes `_assert_no_breaches`
  raise, and the test asserts the failure message carries every replay field (fixture, seed, run id, tier,
  branch, pool digest, scaled deviation, scaled tolerance, category). This proves both that the suite can fail
  and that a real failure would be reproducible — exactly the design's promise.
- **Scope correct.** Single-step accepted `ordinary_add` only; no multi-step/sequence (correctly deferred to
  M34-B); no new mechanics, optimizer, economics, EV, or public numeric release; SOURCE/PROVENANCE, MML,
  PD-013 remain open; no auto-run / Actions.

## Watchpoints (non-blocking)
- Small fixed seed set (3 seeds) — adequate per the pinned contract; the seed set could be widened later if
  stronger multi-seed assurance is wanted.
- The smallest-weight branch (~1/87) at the smallest tier (512) is a low-count regime where the 6σ band is
  proportionally very wide (weak sensitivity there); the larger tiers carry the real convergence signal. Fine
  as-is; note it if future tightening is considered.
- Still test-only single-step; sequence hardening is M34-B.

## Recommendation
Accept M34-A as the multi-seed single-step hardening milestone. Authorize **M34-B** (short accepted-
`ordinary_add` sequences) only as a separate later gate, with its own pinned contract. Nothing self-accepts;
full M34 stays closed.

---
- author: `claude`
- document_type: `mc_hardening_audit`
- status: `advisory verdict — GO (M34-A); M34-B/full M34 pending separate gates`
