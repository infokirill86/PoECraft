# P2C M47-A2V Reveal Sampling Verification & Decision Support — Claude Audit

- Verdict: **GO** (offline evidence tooling only; no runtime, no accepted mechanics, no D3-D5 promotion)
- Auditor: Claude (external auditor-designer, advisory only; acceptance remains ChatGPT/User)
- observed_repo_head: `8bc34b0561a9a6b545fe78eae4a5efa425d5c910`
- observed_active_task_sha256 (`work/active/ACTIVE_TASK.md` git-index bytes): `be2c66e03fd36bf9f361ea3db11d0f3b05f340125b8a3ea9ff33d974d79ab6cb`
- Package: `packages/proposed/P2C_M47A2V_Reveal_Sampling_Verification_Codex_v1/`

## Scope audited

An offline evidence-support layer to capture and validate in-game Reveal observations
so real captures can eventually inform the D4 sampling decision: an in-game capture
protocol, a canonical observation schema (`schemas/reveal_observation.schema.yaml`), a
fail-closed validator/analyzer (`tools/analyze_reveal_observations.py`), decision
criteria, and tests. No Reveal/Echoes runtime; no D3-D5 acceptance.

## Tooling-only confirmed

Changed outside the package: new `schemas/…`, new `tools/analyze_reveal_observations.py`,
new `tests/tools/test_reveal_observation_analysis.py`, plus documentary updates to
`CURRENT_STATUS.md`, `ledger/DECISIONS.md`, `ledger/ACCEPTED_ARTIFACTS.md`, and a +7
documentary block in `mechanics_evidence.yaml`. **No `src/`, no `data/operations.yaml`,
no mechanics-rule change.** Foundation validation PASS; semantic fingerprint unchanged
(`6e7bc414…`); root SHA check PASS.

## Verified (contradiction / boundary check)

1. **No accepted-truth promotion.** The `mechanics_evidence.yaml` addition records
   `reveal_offer_design_m47a2` as `USER_ACCEPTED_DESIGN_ONLY` with D3-A/D4-A/D5-A each
   `PROPOSED_CANDIDATE_NOT_ACCEPTED` and reveal/echoes runtime not admitted. The ledger
   rows record the M47-A2 design acceptance and this package's authorization as "offline
   evidence tooling only … may not accept D3-D5, promote observations automatically,
   produce crafting advice/public probabilities." Consistent with the package.
2. **Analyzer never promotes or accepts.** Every report carries
   `accepted_truth_update_performed:false`, `runtime_mechanics_update_performed:false`,
   `crafting_advice_or_ranking:false`, `public_release_allowed:false`,
   `classification:internal_quarantined_evidence_only`. Each D-assessment is a
   classification string (e.g. `inconclusive_missing_eligible_pool_snapshots`,
   `structurally_compatible_but_sampling_model_not_identified`,
   `candidate_structurally_contradicted`) — it never emits "accepted"; the docstring and
   `_decision_support()` keep "User still gates acceptance" on every decision.
3. **Contradiction-first, as an auditor tool should be.** It hunts counterexamples: D3
   (a window with a known compatible-exclusive pool but no exclusive offer → reject),
   D4 (offered rows outside the eligible-pool snapshot, within-set family/group
   conflicts, duplicate offer identities → structurally contradicted), D5 (currency
   consumed or state mutated on failure → contradicted). This mirrors the M47-A2
   accept/reject criteria.
4. **Fail-closed validation.** Draft-2020-12 JSON-schema plus contract checks
   (successful windows require display_order exactly {1,2,3}; `stored_mml` must match
   Jawbone context; compatible-exclusive IDs must appear in the pool snapshot; unique
   `observation_id`). Verified live: a malformed dataset exits 1 with
   `REVEAL_OBSERVATION_ANALYSIS: FAIL`.
5. **Hardcoded MML constant is correct.** The validator's `stored_mml == 40` for
   `ancient_jawbone` (else `None`) matches accepted `data/operations.yaml` exactly
   (`ancient_jawbone.reveal_mml: 40`; gnawed/preserved `null`), so it will not reject
   correct observations.
6. **No public numeric leak.** The one computed ratio
   (`exclusive_offer_frequency_internal`) is explicitly internal and quarantined —
   exactly the internal-provenance sample recording the accepted M47-A2 design permitted;
   probabilities/rates/advice are not released.
7. **Honest limitations stated in-report:** no observation count proves a server
   algorithm; D4 needs homogeneous setups + complete pool snapshots; display-position
   counts are screening only; the report cannot alter runtime/data/ledgers/acceptance.

## Checks

- `validate_active_task.py`: PASS. `check_sha256sums.py`: PASS. `validate_foundation.py`:
  PASS (fingerprint `6e7bc414…`, unchanged).
- `test_reveal_observation_analysis.py`: 5 passed (clean basetemp). A prior run's single
  "error" was the known locked-Windows pytest tmp dir, not a logic failure.

## Auditor note routed to ChatGPT/User (not resolved here)

- This tool **supports** the D4 decision; it does not make it. D4-A can only move from
  proposed to accepted once real homogeneous in-game captures with eligible-pool/weight
  snapshots are recorded and a User gate names the model. This is the in-game
  verification step for Kirill.
- Ancient + Echoes MML persistence remains a separate unresolved source conflict, out of
  this package's scope.

## Remains proposed / not accepted / gated

D3-D5 acceptance; base Reveal and Echoes runtime; named-Lich/Necromancy/Omen of
Light/Putrefaction; multiple placeholders; revealed-Desecrated Fracture runtime; PD-013
closure; planner/optimizer/economics/advice; public numeric release;
source/provenance/MML closure; automation. All require separate explicit ChatGPT/User
gates.

## Findings

None blocking. GO as offline evidence tooling only.
