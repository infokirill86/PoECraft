# M33-P1 Statistical-Convergence Audit (Claude)

audit_id: `M33_P1_Statistical_Convergence_Audit_Claude_v1`
auditor: `claude`
package: `packages/proposed/P2C_M33_P1_Statistical_Convergence_Result_Codex_v1/`
repo_head_audited: `fcde807`
base_commit: `f8b8f13`
supersedes_blocking_from: `reviews/M33_Oracle_Convergence_Audit_Claude_v1.md` (GO WITH CHANGES, M33-P0)
verdict_style: `GO / GO WITH CHANGES / NO-GO`
authority_note: advisory only. Claude does not accept or close. Acceptance stays with ChatGPT/User.

---

## Plain-language summary
This is the follow-up after Codex fixed the four things I flagged on M33-P0. The old "close enough" rule was
a fixed loose band; **now the test uses a real statistical band that tightens as you take more samples, and a
biased engine actually fails it.** I verified the math myself: the band works out to a true six-standard-
deviation binomial band, the sample tiers show the error genuinely shrinking about as 1/√n, breaches are hard
failures, and there's a new bigger, lopsided pool that also checks the family/group/slot-capacity rules. All
6 tests pass, the full suite (92) passes, no numbers leak, and the ledger only recorded the earlier P0
acceptance — nothing was self-accepted. **Verdict: GO — the blocking items are genuinely resolved; this is
now a sound foundation and can be accepted as full M33.** Still single-step `ordinary_add` only; multi-step
convergence stays for later. M34 not started.

## Verdict
**GO.** All four M33-P0 blocking items are correctly and verifiably resolved. Recommend **full M33
acceptance** at ChatGPT/User discretion. Watchpoints below are non-blocking (M34-era).

## Blocking items from the P0 audit — each resolved & verified
1. **Statistically-derived tolerance — RESOLVED.** Per-branch band is
   `|obs·den − n·num| ≤ k·⌈√(n·num·(den−num))⌉` with `k=6`. Algebraically this is exactly `|X − np| ≤ 6σ`
   (the `den` cancels; `√(n·num·(den−num)) = den·σ`) — a true six-sigma binomial band, kept in exact integers
   (no float, no probability rendering). Replaces the old fixed `//16`.
2. **Sample-count tiers showing √n shrinkage — RESOLVED.** Tiers (1024, 4096, 16384); each must sit inside the
   6σ band, and a hard assertion requires the largest tier's max proportion error to be at least ~2× tighter
   than the smallest (conservative vs the ~4× a √n model predicts for 16× samples). Independently reproduced:
   the 6σ proportion band falls ~0.081 → 0.041 → 0.020 across the tiers (clean 1/√n), and a sampler biased to
   p′≈0.28 breaches the n=16384 band — so the criterion is falsifiable and catches bias, not a rubber stamp.
3. **Confidence + hard-fail divergence — RESOLVED.** `k=6` is the stated confidence multiplier (documented in
   `03_STATISTICAL_POLICY.md`); any per-branch breach or shrinkage-direction failure is a hard test failure
   (defect), not silent. Support is also checked (`observed ⊆ oracle keys`).
4. **Broader higher-variance fixture — RESOLVED.** New 8-branch Fibonacci-skewed prefix pool with blockers
   that exercise **family** legality, **group** legality, and **suffix-capacity** filtering (oracle correctly
   reduces to the 8 eligible keys), sampled at the large tier. Real reduction of false-confidence risk.

## Other checks (all clear)
- **Verified by execution:** 6/6 M33 tests pass; full suite **92 passed**; test-only (no `src/` change).
- **Shared kernel** still enforced by code/injection (single `build_pool`; spy test `call_count == 1 + samples`).
- **Boundaries:** package numeric-leak scan PASS; test file integer-only; root + package `SHA256SUMS` PASS;
  `ordinary_add` only; no optimizer/advice/economics; SOURCE/PROVENANCE, MML, PD-013 open; no M34.
- **No self-acceptance:** ledger diff since base is only the legitimate P0 gate record ("not full M33",
  "no claim of statistically proven convergence") + P1 authorization. Nothing accepts P1/full M33 in-commit.
- **Honest package:** `03_STATISTICAL_POLICY.md` states the formula and its `k·√(n·p(1−p))` meaning;
  `06_P0_ACCEPTANCE_AND_P1_LIMITS.md` states what is still not claimed.

## Watchpoints — non-blocking (M34-era)
- The √n check is **single-seed and directional** (≥2× tighter), not a multi-seed convergence-rate estimate.
  Adequate and falsifiable for this gate; a multi-seed rate check could strengthen it later.
- `k=6` is conservative — insensitive to very small biases at small n; mitigated by the large tier and the
  tiered shrinkage assertion.
- Still **single-step** `ordinary_add`; multi-step / sequence convergence belongs to M34+.
- Governance: `ACTIVE_TASK.md` remains on the heavy side — keep trimming it toward a thin dispatcher.

## Recommendation
Accept **full M33** on this M33-P1 delta: the oracle-convergence validation now rests on a sound, falsifiable,
distribution-derived statistical contract, exercised on a broad legality-filtered fixture, verified by
execution. Nothing self-accepts; M34 stays closed until a separate gate.

---
- author: `claude`
- document_type: `statistical_convergence_audit`
- status: `advisory verdict — GO (recommend full M33); acceptance pending ChatGPT/User`
