# M36-A Heterogeneous-Chain Runtime Audit (Claude)

audit_id: `P2C_M36A_Heterogeneous_Chain_Runtime_Audit_Claude_v1`
auditor: `claude`
package: `packages/proposed/P2C_M36A_Heterogeneous_Chain_Runtime_Result_Codex_v1/`
observed_repo_head: `8473eccc6b87161e31e6e9f76a2f1b7940e9acfd`
observed_active_task_sha: `d42991b3220a27d3f4ee4eae735186fd3ed01a507295ddac5a58415de00bef31`  (SHA-256 of the exact `work/active/ACTIVE_TASK.md` bytes audited, at HEAD 8473ecc, before this review's dispatcher update)
verdict_style: `GO / GO WITH CHANGES / NO-GO`
authority_note: advisory only. Acceptance stays with ChatGPT/User.

---

## Plain-language summary
Milestone: the first **mixed** crafting chain — do an add, then an annul (or annul then add). This is the first
time the simulator composes two *different* operations, which is what real crafting looks like. It's built
cleanly on top of the two accepted operations (their code is untouched, all prior tests still pass), it refuses
to run anything that isn't tagged runnable (so Chaos/Exalted can't sneak in), it protects the fractured mod
through the remove step, and it proves all outcome odds add up to exactly 1. All 10 tests pass. **The recurring
snag is still here:** the repo checksum file was delivered out of date again — and this is the third time,
because the pre-push guard we added last round is present but **not switched on** (`core.hooksPath` isn't set),
so it didn't fire on its own commit. I regenerated the checksums and I'm activating the guard so it stops
happening. **Verdict: GO WITH CHANGES** — the runtime is right; the integrity guard must be turned on.

## Verdict
**GO WITH CHANGES.** The M36-A runtime is correct and in-scope (GO on substance). Required corrections: (1) the
delivered root manifest failed integrity again — regenerated here; (2) the pre-push hook is present but inert
(`core.hooksPath` unset) — it must be activated so integrity stops drifting (this is the 3rd occurrence).

## Critical check — accepted mechanics untouched
- New module `src/p2c_engine/monte_carlo/heterogeneous_chain.py`; `ordinary_add.py` and `annulment.py` have
  **0 deletions** — accepted single-step and Annulment mechanics unchanged.
- **Regression: 120 passed** (suite excluding the heavy M34-B1 file). M36-A adds 10 passing tests. No regression.

## Runtime correctness (code-read + execution, 10/10 tests)
- **Composes the accepted harnesses, dispatches per operation.** The chain harness wraps the accepted
  `OrdinaryAddMonteCarloHarness` and `AnnulmentMonteCarloHarness`; each step dispatches by operation type to the
  accepted pool builder (`build_ordinary_add_pool` / `build_removal_pool`), `branch_options`, and the accepted
  transition + invariant functions. No reimplemented mechanics.
- **Per-step branch-state pool rebuild across heterogeneous ops.** Verified both orders:
  `add_then_annul` and `annul_then_add_rebuilds_add_pool_from_branch_specific_state`.
- **Fail-closed on the reconciled registry (the reconciliation + metadata-floor payoff).** A step is admitted
  only if it is the accepted `ordinary_add` primitive or an `operations.yaml` row with
  `runtime_admission_status == accepted_executable_runtime`. A `CatalogOperationInvocation` (e.g. Exalted/Chaos)
  is always rejected; tests `fail_closed_on_active_catalog_row_without_runtime_admission` and
  `fail_closed_if_annulment_row_is_not_runtime_admitted` confirm it. Chain shape is fixed to exactly one
  `ordinary_add` + one base `annulment` (`rejects_sequences_that_are_not_two_step_heterogeneous`).
- **Exact oracle + mass conservation.** Exact path masses are rational; terminal masses aggregate by canonical
  terminal hash; **total path mass and total terminal mass are each asserted == 1** (hard fail otherwise),
  including explicit no-transition terminals. Path ceiling enforced.
- **Fractured protection through the chain.** `_annulment_exact_transition` re-checks fractured-unchanged;
  underlying removal pool excludes fractured; `fractured_modifier_is_protected_through_exact_and_mc_chain` and
  the `negative_control_fractured_removal_pool_leak_fails` test confirm the guard has teeth on both paths.
- **Deterministic + numeric-free.** Same seed/run id replays identically; public summary carries only
  statuses/counts/hashes/fingerprints (no probabilities). Constructed-fixture label present; no route planner.

## Required change 1 — manifest regenerated (applied here)
`check_sha256sums.py` FAILed at the delivered HEAD `8473ecc`. I ran `tools/update_sha256sums.py`; the manifest
now passes.

## Required change 2 — activate the pre-push guard (the real fix)
The hook `tools/hooks/pre-push` is **correct** (regenerates the manifest, blocks if it changed uncommitted,
then runs `check_sha256sums.py`) and is a local hook (no GitHub Actions — boundary respected). **But
`core.hooksPath` is not set, so the committed hook is inert** — which is exactly why this commit drifted despite
the hook existing. Required: every working clone runs the one-time
`git config core.hooksPath tools/hooks`, and this activation step is documented in
`GitHub_Workflow_Protocol.md`. I have set it in this audit environment so pushes here are now guarded. Until
each actor's clone activates it, "run `update_sha256sums.py` before commit" remains a hard manual step.

## Boundaries (confirmed)
Additive runtime only; accepted operations only (add + base annul); fail-closed on everything else; no public
numeric release; no optimizer/economics/advice; no automation / GitHub Actions (hook is local); no
SOURCE/PROVENANCE, MML, or PD-013 closure. Ledger carries no M36-A acceptance row (no self-accept).

## Recommendation
Accept M36-A heterogeneous-chain runtime (with the manifest regenerated). Adopt the hook activation
(`core.hooksPath tools/hooks`) as a documented one-time step for every clone so root-SHA drift ends. Longer /
variable chains, Annulment variants, and additional operations remain separate gates. Nothing self-accepts.

---
- author: `claude`
- document_type: `heterogeneous_chain_runtime_audit`
- status: `advisory verdict — GO WITH CHANGES (manifest regenerated; activate pre-push hook)`
