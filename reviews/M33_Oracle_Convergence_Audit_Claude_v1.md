# M33 Oracle-Convergence Audit (Claude)

audit_id: `M33_Oracle_Convergence_Audit_Claude_v1`
auditor: `claude`
package: `packages/proposed/P2C_M33_Oracle_Convergence_Result_Codex_v1/`
repo_head_audited: `9aae867`
base_commit: `a27d09a`
verdict_style: `GO / GO WITH CHANGES / NO-GO`
external_input: incorporates the external Gemini sanity-audit concerns (shared-kernel enforcement, statistical contract, sample adequacy, false-confidence/fixture breadth, governance).
authority_note: advisory only. Claude does not accept or close. Acceptance stays with ChatGPT/User.

---

## Plain-language summary
M33 adds one test file that checks the random (Monte Carlo) engine lands near what the exact engine says,
on a few tiny made-up pools. **On my own run all 4 tests pass, the full suite (90) passes, no numbers leak,
and nothing new was accepted.** The work is honest — Codex itself labels the fixtures "narrow by design."
But it is **not yet a real convergence proof**: the "close enough" rule is a fixed loose band (about nine
standard deviations wide at the tested sizes), so a biased sampler could still slip through, and the pools
are very small. So it is a solid **foundation (P0) step**, not full M33. **Verdict: GO WITH CHANGES —
accept as M33-P0 now; hold the "full M33" label until a real statistical rule and a bigger, more varied
fixture are added.** No new mechanics, still `ordinary_add` only, boundaries still open, M34 not started.

## Verdict
**GO WITH CHANGES.** Accept as **M33-P0 / oracle-convergence foundation partial**. The four blocking items
below must land before **full** M33 acceptance; the watchpoints can wait until M34.

## What was verified by execution (not trusted from claims)
- **Tests pass on a clean run:** all 4 M33 tests; full suite **90 passed** (86 prior + 4).
- **Boundaries clean:** `check_public_numeric_leaks` on the package → PASS; the test file is integer-only
  (no decimal/percent/probability renderings); root + package `SHA256SUMS` → PASS.
- **Test-only:** no runtime `src/` change since `a27d09a` — mechanics untouched.

## Focus-area findings (folds in the Gemini concerns)

### 1. Scope — clean
`ordinary_add` only (operation id fixed); no new executable mechanics; no M34; no optimizer/advice/ranking/
economics/EV; no public numeric probability release (verified); SOURCE/PROVENANCE, MML, PD-013 remain open
in ledger/status. ✓

### 2. Shared-kernel enforcement — sufficient (GO)
Enforced by **code/injection, not only docs**: both the oracle path (`enumerate_outcomes` → exact
`branch_options`) and the MC path (`run` → `sample_once`) call the harness's single `build_pool()`, which
delegates to the injected `build_ordinary_add_pool`. The spy-builder test asserts
`call_count == 1 (enumerate) + 1 per sample`, proving both routes use the same injected builder. The oracle
carries exact rational per-branch probabilities (numerator/denominator), so the comparison is genuinely
MC-empirical vs exact — not circular. Adequate for a foundation gate. ✓

### 3. Statistical contract — DEFINED but not JUSTIFIED (blocking for full M33)
The tolerance is explicit, integer, and deterministic (cross-multiplication of observed counts vs exact
weights; band = `sample_count // 16`). That is good for reproducibility. But it is **not a statistically
motivated convergence criterion**: at n=4096 the band is ~256 counts while one standard deviation is ~28, so
the band is **roughly nine standard deviations** — a loose sanity envelope a biased sampler could pass. There
is no confidence/epsilon derivation, no sample-count tiers showing error shrinks with n, and no
statistically-defined divergence rule. → **enough for P0, not for full M33.**

### 4. False-confidence risk — fixtures too narrow (blocking for full M33)
Fixtures are 2-branch, 3-branch, empty, single-step, PREFIX-only. No larger/higher-variance pool; no
family/group/capacity interaction under sampling. Real false-confidence risk. → at least one larger, varied
mock pool required before full M33.

### 5. Governance/process — mostly fine; one watchpoint
Human summary (`01_HUMAN_SUMMARY.md`) is readable and meets the plain-language rule; numeric-quarantine
report is honest. The package is doc-heavy (8 docs for a one-file test delta) but each doc maps to a real
purpose — acceptable, not process-for-its-own-sake. **Watchpoint:** `ACTIVE_TASK.md` is drifting from a thin
dispatcher toward a history dump (checkpoint + result summary + validation summary + gate record + automation
block + stop conditions). Narrative belongs in `ledger/`/package; keep ACTIVE_TASK lean.

## Blocking changes — required before FULL M33 acceptance
1. **Statistically-derived tolerance.** Replace the fixed `//16` band with a per-branch band derived from the
   sampling distribution — e.g. `k · sqrt(n·p·(1−p))` for a stated `k`/confidence, or an explicit epsilon on
   the empirical proportion at a stated confidence level.
2. **Sample-count tiers showing convergence.** Run growing n and demonstrate empirical deviation shrinks about
   as `1/sqrt(n)` — evidence of convergence, not just "inside a fixed band."
3. **Confidence/epsilon + divergence stop rule.** State the significance/confidence explicitly (e.g. a
   chi-square/G-test at fixed α with a fixed seed) and make a breach a **hard defect failure**, not silent.
4. **Broader fixture.** Add ≥1 larger, higher-variance pool (e.g. 6–10 skewed-weight branches, ideally
   exercising a family/group/capacity interaction) to cut false confidence.
   (Deterministic seed-pinned replay is already in place from M32 — keep it.)

## Follow-up watchpoints — may wait until M34
- Multi-step / operation-sequence convergence (M33 is single `ordinary_add` step).
- Family/group/capacity behavior under sampling at scale.
- ACTIVE_TASK dispatcher hygiene (governance watchpoint above).

## Recommendation
- **Accept M33-P0 (foundation partial)** at ChatGPT/User discretion: the sampler draws only oracle-known
  outcomes, shares the kernel by construction, is deterministic, and lands in a loose but explicit band —
  a legitimate first rung, honestly labeled.
- **Do not label it full M33 / oracle convergence** until blocking items 1–4 land. Then a short M33-P1 delta
  (still test-only, still `ordinary_add`) can be built and re-audited.
- Nothing here self-accepts. M34 stays closed.

---
- author: `claude`
- document_type: `oracle_convergence_audit`
- status: `advisory verdict — GO WITH CHANGES (accept as M33-P0); full M33 pending statistical contract`
