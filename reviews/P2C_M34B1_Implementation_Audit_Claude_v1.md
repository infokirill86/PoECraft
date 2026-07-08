# M34-B1 Two-Step Sequence Implementation Audit (Claude)

audit_id: `P2C_M34B1_Implementation_Audit_Claude_v1`
auditor: `claude`
package: `packages/proposed/P2C_M34B1_Result_Codex_v1/`
observed_repo_head: `be9406d2b5ed9f21ec61f9f357e5af5529c547b5`
observed_active_task_sha: `4016ef9529d09b9dfbd6b2a4e7d9348ae09702152f403e3ab7ca1ed0854898de`  (SHA-256 of the exact `work/active/ACTIVE_TASK.md` bytes audited, at HEAD be9406d, before this review's dispatcher update)
verdict_style: `GO / GO WITH CHANGES / NO-GO`
authority_note: advisory only. Claude does not accept or close. Acceptance stays with ChatGPT/User.

---

## Plain-language summary
M34-B1 is the first build that runs the accepted operation **twice in a row** and checks the result. This one
adds real engine code (not just tests), so the first thing I checked is that it did **not** touch the already-
accepted single-step engine — and it didn't: zero lines removed, the whole 396-line addition is a new "two-step"
layer bolted on top, and every previously accepted test still passes unchanged (96). The hard part — computing
the exact answer for a two-step chain — is done correctly: it walks the whole branch tree, **rebuilds the pool
from the new item after step one** (the real risk), uses exact fractions, and groups by the final item. The MC
result is checked against that exact answer across several seeds and sizes, it replays identically, a deliberate
break is proven to fail, and it refuses anything that isn't the accepted operation. All 8 tests pass, no numbers
leak, hashes match, and nothing was self-accepted. **Verdict: GO.** Still exactly two steps; longer chains are a
separate gate.

## Verdict
**GO.** Correct, in-scope M34-B1 implementation, verified by execution. Recommend acceptance at ChatGPT/User
discretion. It resolves the M34-B design and all four of my design-audit build-time watchpoints.

## Critical check — accepted mechanics untouched
- The src change to `monte_carlo/ordinary_add.py` is **purely additive: 0 deletions.** The accepted single-step
  `ordinary_add` mechanics, invariants, and pool/weight kernel are unchanged.
- **Regression confirmed:** the full suite excluding the new (slow) M34-B1 file = **96 passed**, identical to
  before. M34-B1 adds 8 passing tests (104 total). No behavioral change to accepted code.

## What was verified by execution
- **8/8 M34-B1 tests pass:** contract pinned; exact terminal distribution aggregates canonical terminals;
  branch-specific pool rebuild blocks a step-0-installed family at step 1; seeded MC converges to exact
  terminals **and step marginals**; deterministic replay; negative-control terminal breach reporting fails
  with full diagnostics; fail-closed on a non-`ordinary_add` operation; exact-enumeration ceiling is a hard
  failure.
- **Boundaries:** package numeric-leak scan PASS; root + package `SHA256SUMS` PASS; still `ordinary_add` only.
- **No self-acceptance:** ledger diff carries only the prior M34-B **design** acceptance row; no M34-B1
  implementation acceptance is written in-commit.

## Correctness of the two-step layer (code-read + execution)
- **Reuses the accepted kernel, does not reimplement mechanics.** Both the exact enumeration and the MC sampler
  call the same `build_pool` (→ accepted `build_ordinary_add_pool`), `branch_options` / `SeededDecisionSource`,
  `_append_ordinary_modifier`, and `_assert_runtime_invariants` per step.
- **Correct exact two-step oracle.** Frontier tree from S0: for each branch state it **rebuilds the pool from
  that state** (step-1 pool from the branch-specific S1, not from S0), carries exact `Fraction` path mass
  (product of per-step branch probabilities), aggregates terminal mass by **canonical terminal-state hash**, and
  enforces a `max_exact_paths` ceiling with a hard `SamplingContractDefect`. This matches the accepted design.
- **Anti-cheat list (design §8) honored:** genuine two steps (not single repeated); exact and MC use the same
  pool (no stale-pool display trick); step linkage verified; multiple seeds; negative control present; oracle is
  compared, and when intractable it hard-fails rather than being silently skipped.

## Design-audit watchpoints — all addressed
1. **Rare-terminal sensitivity:** the test checks convergence to exact **step marginals** in addition to
   terminals, and uses small tractable fixtures — my suggested mitigation is in.
2. **Exact terminal mass as rationals:** implemented with `fractions.Fraction` (exact numerator/denominator).
3. **Constructed-fixture labels:** explicit constant `"project-model hardening fixture; not a real crafting route"`.
4. **Pinned contract:** seeds `34001/34002/34003`, tiers `512/2048/8192`, σ-multiplier `6`, `max_exact_paths=64`,
   sequence length `2`, all pinned and guarded by `test_..._contract_is_pinned`.

## Watchpoints (non-blocking)
- **Test runtime:** the two-step sampling across seeds × tiers is heavy — the full suite now exceeds ~2 min. Not
  a defect, but as sequence work grows consider a fast/slow test split or a reduced-tier smoke lane so routine
  runs stay quick.
- Still exactly two steps; ≥3-step / variable-length sequences remain a separate gate (correctly forbidden).

## Recommendation
Accept M34-B1 as the two-step accepted-`ordinary_add` sequence-hardening milestone. Longer sequences, any
planner/optimizer, operation expansion, and public numeric release remain closed. Nothing self-accepts.

---
- author: `claude`
- document_type: `mc_hardening_implementation_audit`
- status: `advisory verdict — GO (M34-B1); acceptance pending ChatGPT/User`
