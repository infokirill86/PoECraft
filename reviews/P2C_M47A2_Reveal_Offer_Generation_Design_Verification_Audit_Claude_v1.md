# P2C M47-A2 Reveal Offer-Generation Design/Mechanics Verification — Claude Audit

- Verdict: **GO** (design/mechanics verification only; no runtime accepted or authorized)
- Auditor: Claude (external auditor-designer, advisory only; acceptance remains ChatGPT/User)
- observed_repo_head: `10597e4008964650ce2b71f43c41ff3b0874e073`
- observed_active_task_sha256 (`work/active/ACTIVE_TASK.md` git-index bytes): `decaf2ae070263945262b9a9d88e5d32b9614a71b4ba3b1f17a73522fef14320`
- Package: `packages/proposed/P2C_M47A2_Reveal_Offer_Generation_Design_Verification_Codex_v1/`

## Scope audited

A design/mechanics verification for base Reveal offer generation (D3/D4/D5): it
proposes an exact auditable offer-generation contract and D3-A/D4-A/D5-A candidate
models **without accepting them**, and recommends splitting Echoes runtime out because
constraint persistence on reroll is source-conflicted. No Reveal/Echoes runtime is
authorized.

## Design-only confirmed

The only non-package change since M47-A1 acceptance is a **one-line documentary status
flip** in `mechanics_evidence.yaml`: `jawbone_clean_core_m47a1.runtime_status`
`USER_AUTHORIZED_PROPOSED_RUNTIME_PENDING_AUDIT` → `USER_ACCEPTED_RUNTIME`, correctly
recording the M47-A1 User acceptance. No `src/`, `tests/`, `operations.yaml`, or
sampling-behavior change. Foundation validation PASS; semantic fingerprint unchanged
(`6e7bc414…`), consistent with the documentary evidence file not feeding the fingerprint.

## Verified (framing + contradiction check)

1. **Nothing is presented as accepted mechanics or server truth.** Every D3/D4/D5 row
   is marked "explicit User decision required" and "remain PROPOSED until an explicit
   ChatGPT/User gate names them." The exact contract (`04`) is labelled "candidate
   contract … not accepted runtime behavior."
2. **No source conflict is silently resolved.** `02` lists each source with its
   limitation, and explicitly flags the Ancient + Echoes MML observation (rerolled
   offers reported below the Ancient minimum) as conflicting with the repository's
   `stored_desecration_constraints_persist: true` assumption — routed to the User, not
   decided. Package states this outright.
3. **Echoes is correctly split out.** `06` recommends designing the seam now but
   deferring runtime to a separate `M47-A2E` constraint-persistence verification plus
   its own gate, precisely because MML/named-Lich persistence on reroll is unresolved
   and materially changes the pool/probabilities.
4. **The candidate contract reuses accepted kernels, invents nothing.** `04` applies
   the stored Jawbone MML through the existing accepted family-internal MML interface,
   states "no fallback rule may be invented here beyond the existing accepted project
   model," fixes the placeholder side, blocks family/groups, and is fail-closed.
5. **D5 fail-closed is conservative.** Insufficient set → structured
   `NO_TRANSITION_NO_CONSUMPTION`; no reduced set, no MML/compatibility relaxation, item
   and placeholder unchanged.
6. **Fracture/PD-013 boundary preserved, not widened** (`07`): hidden placeholder still
   counts toward Fracture minimum and is never a target; revealed-Desecrated Fracture
   and PD-013 remain future/gated, not implemented or closed.
7. **Optimizer/economics drift blocked.** `09` hard-stops "the implementation tries to
   rank or automatically choose offers" and quarantines all numeric probability output.
8. **Evidence honestly qualified:** the strongest empirical support (563-window player
   dataset showing every window contained an exclusive → supports D3-A) is noted as
   rings, not quarterstaves, and as not identifying the exact sampling algorithm.

## Checks

- `validate_active_task.py`: PASS. `check_sha256sums.py`: PASS.
- `validate_foundation.py`: PASS; fingerprint `6e7bc414…` (unchanged vs M47-A1).
- Full regression: 324 total tests (package reports 324 passed; matches this repo's
  total, confirming no test removal; a prior local run's 35 "errors" were a locked
  Windows pytest tmp dir, green on a fresh basetemp).

## Auditor note routed to ChatGPT/User (not resolved here)

- **D4 offer-sampling algorithm is the load-bearing open decision.** Every offer and
  offer-set probability depends on it, and the exact server unit/weights/order are
  unpublished. This remains the prime candidate for Kirill's in-game verification
  before D4-A is treated as project-base truth.
- **Ancient + Echoes MML persistence** must be verified/decided before any Echoes
  runtime; it is a genuine source conflict, not an implementation detail.

## Remains proposed / not accepted / gated

D3-D5 candidate models; the exact offer-generation contract; base `reveal_desecrated`
runtime; Echoes runtime and constraint persistence; named-Lich/Necromancy/Omen of
Light/Putrefaction; multiple placeholders; revealed-Desecrated Fracture runtime;
PD-013 closure; planner/optimizer/economics/advice; public numeric release;
source/provenance/MML closure; automation. All require separate explicit
ChatGPT/User gates.

## Findings

None blocking. GO as design/mechanics verification only.
