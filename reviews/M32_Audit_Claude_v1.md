# M32 Audit — Seeded Monte Carlo Harness + GitHub Baseline Import (Claude)

audit_id: `M32_Audit_Claude_v1`
auditor: `claude`
audit_type: `result_and_baseline_import_audit`
package: `packages/proposed/P2C_M32_Seeded_MC_Harness_Result_Codex_v1/`
repo_head_audited: `fc2c5a5`
verdict_style: `GO / GO WITH CHANGES / NO-GO`
authority_note: this verdict is **advisory only**. Claude does not accept or close. Acceptance stays with ChatGPT/User.

---

## Verdict

- **Layer B — M32 seeded MC harness over accepted `ordinary_add`: GO.**
- **Layer A — GitHub baseline import / repo consolidation: GO WITH CHANGES.**
- **Overall: GO WITH CHANGES** — the M32 harness is sound and verified by execution; the required
  changes attach to the *baseline import*, which must stay **proposed, not accepted truth**, until the
  conditions below are met. The inventory already states this correctly; the conditions make it enforceable.

---

## What was executed / reconstructed (not trusted from claims)

- **Integrity.** Root `SHA256SUMS.txt` → `PASS` via `tools/check_sha256sums.py`. Package
  `SHA256SUMS.txt` recomputed independently: all rows match, none missing. `tools/check_no_nested_zips.py` → `PASS`.
- **Test suite.** `tests/monte_carlo/test_m32_seeded_mc_harness.py` executed on a clean clone: all
  cases pass, including the shared-kernel spy test, replay-determinism, different-seed divergence,
  one-outcome and empty-pool fixtures, every invariant failure path, and the numeric-free summary check.
- **Determinism, independently reproduced.** Ran the smoke runner twice; `result_hash` was byte-identical
  across runs. Confirmed the PRNG is a **named, portable, deterministic** sampler
  (`p2c.sha256_rejection.v1`): a SHA-256 rejection draw over a canonical-JSON payload of
  `{seed, decision_id, rejection_counter, block_index, rng_stream_version}` — not a language-default RNG.
- **Shared kernel, confirmed by code + execution.** Both `enumerate_outcomes` (exact, via
  `sampling.exact.branch_options`) and `sample_once` (MC, via `SeededDecisionSource` →
  `sampling.weighted.weighted_choice`) consume `pool.candidates` from **one** injected
  `legality.pool_builders.build_ordinary_add_pool`. No second ordinary-add legality/pool/weight path
  exists for MC. The spy-builder test proves a single shared builder is called for both paths.
- **Boundary check.** Smoke and `public_summary()` output carry only statuses / counts / hashes /
  fingerprints / seed / algorithm ids — **no probabilities, decimals, percentages, or rationals.**

## Layer B — M32 harness findings (GO)

- **Accepted-lane only.** `operation_id` is fail-closed to `ordinary_add`; `semantics_version` is
  pinned; unsupported operations raise `M32InvariantViolation`. No new executable mechanics.
- **Runtime invariants fail closed, not silently.** Fractured suffix unchanged, prefix/suffix/total
  capacity, duplicate family/group legality, operation identity, and mode-unchanged are each asserted
  on every trajectory (including the empty-pool `no_transition` path) and raise hard failures.
- **Micro-fixtures adequate for sampler sanity.** Two-outcome weighted, one-outcome deterministic, and
  empty/invalid-pool behaviors are covered.
- **Scope honesty.** Harness performs a single `ordinary_add` step (`m32_single_ordinary_add`); oracle
  convergence is explicitly deferred to M33. No optimizer / advice / EV / ranking / economics introduced.

## Layer A — baseline import findings (GO WITH CHANGES)

The `BASELINE_IMPORT_INVENTORY.md` is thorough and honest: every imported runtime/data/config/schema/tool
file is marked *proposed pending audit*, imported-vs-M32-created files are separated, and no ledger was
updated to claim acceptance. That is the correct posture. The following must be resolved **before the
imported baseline is accepted as project truth** — none of them block the M32 harness itself.

- **A1 — Undeclared runtime dependencies (reproducibility). REQUIRED.**
  `pyproject.toml` declares **zero dependencies**, but the runtime imports `yaml` and `jsonschema`, and
  the suite needs `pytest`. A fresh clone cannot reproduce the builder's "tests/smoke passed" claim
  without an auditor discovering and installing these by hand (I had to). Pin runtime + dev dependencies
  (a `requirements`/`[project.dependencies]` block) so the harness is reproducible from a clean checkout.

- **A2 — Imported kernel has no committed tests + prior pin not re-established. REQUIRED before acceptance.**
  The load-bearing shared kernel that M32 depends on (`legality/pool_builders`, `legality/predicates`,
  `sampling/weighted`, `sampling/exact`, `static_data/*`, `domain/*` — ~70 files) was imported **without
  its test suite**; inventory §5 confirms the local `tests/*` were intentionally left untracked. The
  inventory also states the "exact prior package pin is not re-established." Consequence: inside this
  repo, the kernel's correctness rests on prior local acceptance that cannot be re-verified by execution
  here — only M32's own thin layer is tested. Recommend importing (via a **separate audited baseline
  delta**) at least the tests covering the M32 load-bearing kernel, and pinning the prior accepted
  package SHA. Until then the imported `src/p2c_engine/*`, `data/*`, `config/*`, `schemas/*`, and
  `tools/validate_*` remain **proposed**, exactly as the inventory says.

- **A3 — Public-numeric-leak tool is unscoped (process, minor).**
  `tools/check_public_numeric_leaks.py` scans all text — internal `data/*.yaml` weights, manifest prose,
  and even the `__version__ = "0.9.0.dev0"` string — and reports them as `LEAK_CANDIDATE`. It cannot
  distinguish public output from internal data, so it cannot actually gate "no public numeric release."
  None of its current hits are in the M32 package. Consider scoping it to public-output surfaces or an
  allowlist. Low priority; per the "process changes only on observed failure" rule, note now, fix if it
  ever blocks a real release check.

- **B-minor — Run provenance placeholder.** Run artifacts record `code_version = "p2c.m32.dev"` rather
  than a real commit reference. Once the repo is stable, pin the actual commit SHA for full replay provenance.

## Material risks

- Accepting the imported baseline as truth on the strength of M32 passing would over-claim: M32's green
  suite verifies M32, not the imported kernel beneath it (A2). Keep them as two separate acceptance decisions.
- No correctness defect was found in the M32 harness by execution or reconstruction at `fc2c5a5`.

## Recommendation

- **Accept M32 (Layer B)** as a passing seeded-MC harness milestone, at ChatGPT/User discretion.
- **Do not yet accept the imported baseline (Layer A) as project truth.** Clear A1 and A2 first
  (dependency pin; import the kernel tests + re-establish the prior accepted SHA via a separate audited
  delta). A3 and B-minor are non-blocking hygiene.
- Nothing here self-accepts or self-closes; this is advisory input to the gate.

---
- author: `claude`
- document_type: `milestone_result_and_import_audit`
- status: `advisory verdict — GO WITH CHANGES; acceptance pending ChatGPT/User`
