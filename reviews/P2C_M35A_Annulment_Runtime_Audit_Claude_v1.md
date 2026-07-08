# M35-A Annulment Runtime Audit (Claude)

audit_id: `P2C_M35A_Annulment_Runtime_Audit_Claude_v1`
auditor: `claude`
package: `packages/proposed/P2C_M35A_Annulment_Runtime_Result_Codex_v1/`
observed_repo_head: `2a2d55be76b798b5c5aa738c1c2c2c920f2eac27`
observed_active_task_sha: `eb191302fd7ce43f1187c116b69c88782fbf78488562c51bea5bacc20d205fde`  (SHA-256 of the exact `work/active/ACTIVE_TASK.md` bytes audited, at HEAD 2a2d55b, before this review's dispatcher update)
verdict_style: `GO / GO WITH CHANGES / NO-GO`
authority_note: advisory only. Claude does not accept or close. Acceptance stays with ChatGPT/User.

---

## Plain-language summary
This is a milestone: **the first crafting operation beyond `ordinary_add`** — Annulment ("remove a random
modifier"). It's real engine code, so I first checked it didn't disturb the accepted one — it didn't
(`ordinary_add.py` untouched, Annulment lives in its own new file, and every prior test still passes: 96).
The sacred rule — never remove the fractured mod — is protected in **three independent places** and tested on
both the exact and the random path, with a deliberate-leak test proving the guard actually fires. It removes
exactly one of the k eligible mods with equal odds (1/k), handles the "two identical mods → same result, add
the odds" case, refuses to touch normal-rarity items, does nothing (cleanly) when there's nothing removable,
and never prints probabilities. All 10 tests pass, hashes match, and nothing was self-accepted. **Verdict:
GO.** Still just base Annulment; omens/Chaos/heterogeneous chains are later gates.

## Verdict
**GO.** Correct, careful, in-scope first new-operation implementation, verified by execution. Recommend
accepting Annulment runtime (M35-A) at ChatGPT/User discretion.

## Critical check — accepted mechanics untouched
- Annulment is a **new module** (`src/p2c_engine/monte_carlo/annulment.py`); `ordinary_add.py` is **not
  changed at all**; `monte_carlo/__init__.py` only gains an export (0 deletions).
- **Regression confirmed:** the suite excluding the two heavy sequence/annulment files = **96 passed**,
  identical to before. M35-A adds 10 passing tests. Accepted `ordinary_add` behavior is unchanged.

## What was verified by execution (10/10 M35-A tests)
`contract pinned`; `exact paths uniform over non-fractured installed instances`; `fractured modifier never
removed by exact OR MC path`; `empty pool → no-transition, no mutation, exact mass one`; `duplicate-instance
terminal aggregation sums paths`; `exact and MC use the same shared removal-pool path`; `same seed/run id
replays exactly`; `negative control fails on a fractured-candidate leak`; `fail-closed on unsupported
operation and rarity`; `public summary is numeric-probability-free`.

## Correctness (code-read + execution)
- **Reuses the accepted kernel.** Both exact enumeration and MC sampling call the injected accepted
  `build_removal_pool` (which excludes fractured) and `branch_options` / `SeededDecisionSource` — no
  reimplemented removal mechanics.
- **Fractured protection is defence-in-depth and tested.** Rejected at pool validation
  (`_validate_annulment_pool` — any fractured candidate is a hard failure), at removal
  (`_remove_modifier_instance` refuses a fractured instance), and at post-assertion
  (`_assert_annulment_runtime_invariants` + `_assert_fractured_modifiers_unchanged`). The negative-control test
  proves the guard fires on a deliberate leak. Both exact and MC paths are covered.
- **Uniform 1/k exact oracle.** Pool candidates are asserted uniform (weight 1), so `branch_options` gives each
  removal exact rational `1/k`; terminal masses aggregate by canonical terminal-state hash with `Fraction`.
- **Duplicate-instance aggregation.** Removal targets a specific `duplicate_ordinal`; two removals of
  indistinguishable duplicates that reach the same canonical terminal sum their exact masses (tested).
- **Exactly one removed / no-transition.** Applied path asserts `len(post) == len(pre) - 1`; empty pool yields
  `no_transition_no_consumption` with a byte-identical state (`_assert_no_transition_unchanged`) and exact mass
  one — no fabricated removal.
- **Fail-closed.** Non-`annulment` operation id, semantics-version mismatch, item-class mismatch, and
  normal-rarity states all raise. Base Annulment only; omen/desecrated/Chaos variants explicitly out of scope.

## Boundaries & governance
Package numeric-leak scan PASS; root + package `SHA256SUMS` PASS; public outputs carry only statuses/counts/
hashes/fingerprints (`M32_VALUE_POLICY` reused). Annulment semantics are labelled project-model, not server
truth; SOURCE/PROVENANCE, MML, PD-013 remain open. **No self-acceptance:** the ledger diff carries only the
prior M35 **design** acceptance; no Annulment-runtime acceptance is written in-commit.

## Watchpoints (non-blocking)
- Single-operation only; heterogeneous plans (e.g. `ordinary_add` then Annulment) and Annulment variants
  (omens, desecrated-only, Chaos composition) are future, separately-gated work.
- Overall test-suite runtime remains heavy due to the M34-B1 sequence file (M35-A itself is fast); consider a
  fast/slow split later.

## Recommendation
Accept M35-A Annulment runtime as the first admitted operation beyond `ordinary_add`, under the M35 admission
framework. Further operations and Annulment variants remain separate gates. Nothing self-accepts.

---
- author: `claude`
- document_type: `operation_runtime_implementation_audit`
- status: `advisory verdict — GO (M35-A Annulment); acceptance pending ChatGPT/User`
