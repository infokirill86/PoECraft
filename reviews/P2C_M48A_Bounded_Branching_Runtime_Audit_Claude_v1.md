# P2C M48-A Bounded Caller-Authored Branching Runtime — Claude Audit

- Verdict: **GO**
- Auditor: Claude (external auditor-designer, advisory only; acceptance remains ChatGPT/User)
- observed_repo_head: `fcdb2e1be3302f934bdda27d4c9573c75ade2212`
- observed_active_task_sha256 (`work/active/ACTIVE_TASK.md` git-index bytes): `4e95ebd44e8d43048ed30280fb55cea528c349406f16e8e98c19951dee02946f`
- Package: `packages/proposed/P2C_M48A_Bounded_Branching_Runtime_Result_Codex_v1/`

## Scope audited

Runtime for a bounded, caller-authored **branching** route evaluator: the caller supplies
a finite acyclic DAG of operation / predicate-branch / terminal nodes; P2C evaluates it
through the accepted M43-A resolver/executor seam with exact rational mass, seeded MC,
replay, and one deterministic state predicate. This is the wave whose design I audited GO
(M48), and the one whose evaluator↔optimizer firewall I elevated as the load-bearing
invariant. New `bounded_branching.py` (1239 lines); an additive/refactored composition
seam in `bounded_sequence.py`; `__init__` exports; 21 tests.

## The evaluator↔optimizer firewall — verified in code, not just claimed

This was the decisive check. Confirmed by reading the source:

1. **Closed predicate registry.** Only `success_class.v1`; the registry is documented and
   built as "closed deterministic state-predicate registry; no callback/plugin seam."
   No `eval`/`exec`/`lambda`/callback/plugin/expression path exists.
2. **`PredicateDecision` carries nothing rankable.** Its only fields are
   `predicate_id`, `result` (categorical `TOP`/`ACCEPTABLE`/`NOT_SUCCESS`), and
   `state_hash`. No score/probability/cost/EV/utility/desirability/ranking anywhere in the
   type or its public payload.
3. **No optimizer surface.** There is no generate/search/compare/rank/recommend/improve/
   best/score method on the evaluator (verified by absence).
4. **The classifier interprets, never invents.** It reads only `static.success_criteria`
   and hard-validates the exact accepted shape (`schema_version==2`, `status=="READY"`,
   exact tier convention, `evaluation_order==(TOP,ACCEPTABLE,NOT_SUCCESS)`, origin-flag
   behavior not admitted, TOP/ACCEPTABLE suffix contracts require exactly three rules).
   Any deviation raises `M48APredicateError` — it does not write, extend, or reinterpret
   the config.

## Other verified controls

5. **Caller owns the whole graph.** Operation/predicate/terminal nodes, edges, and
   terminal labels are all caller-supplied; the evaluator proposes nothing.
6. **Finite acyclic DAG, fail-closed.** Pinned maxima (64 nodes, 128 edges, 8 operation
   nodes per root-to-leaf path); cycles, missing targets, duplicate nodes/labels,
   unreachable nodes, incomplete predicate cases, and ceilings above the maxima return
   structured failure codes.
7. **Exact mass is honest.** Completed results require path mass **and** terminal mass to
   each equal `Fraction(1,1)` (else `M48ABranchingInvariantViolation`). Overflow returns
   `status="ceiling_exceeded"` with `path_count=0`, `terminal_count=0`,
   `mass_sum_exactly_one=False`, and empty paths/terminals — **no truncation,
   renormalization, or hidden MC fallback**. Deterministic predicate edges split by state,
   not probability.
8. **Branch correctness.** Each operation resolves from the actual current branch state; a
   post-mutation branch never reuses the root plan/legality/pool/state digest (predicate
   uses the post-operation state hash — test-confirmed).
9. **Reuse, not duplication.** M48-A contains no currency/pool/removal/add/rarity/Essence/
   Omen/Fracture/Jawbone/Alchemy logic; it calls the accepted M43-A seam
   (`AcceptedStepTransition`, `enumerate_accepted_step`, `sample_accepted_step`,
   `validate_composition_step`). The `bounded_sequence.py` change is a behavior-preserving
   refactor (private `_StepTransition` promoted to public `AcceptedStepTransition` + the
   new seam), verified by M43-A parity below.
10. **Quarantine intact.** Public summaries carry `public_numeric_release: false` /
    `probability_values_printed: false`; no numeric probabilities, advice, or economics.

## Checks

- `validate_active_task.py`: PASS. `check_sha256sums.py`: PASS.
- `validate_foundation.py`: PASS; semantic fingerprint unchanged (`6e7bc414…`); no
  `data/` or `config/` change (no operation/omen/criteria/mechanics/fingerprint input
  touched).
- `test_m48a_bounded_branching_runtime.py`: **21 passed** (contract, parity, exact,
  seeded, replay, firewall negative controls incl. probability-threshold predicate
  rejected, absent optimizer methods, forbidden-vocabulary absence, config-shape mutation
  fails closed, post-op-state branching).
- M43-A / sequence regression after the seam refactor: **48 passed** — behavior preserved.
- Full regression: green (run clean-basetemp; the recurring 35 Windows `tmp_path`
  "errors" are an environmental locked-temp-dir issue, not logic).

## Findings

None blocking. GO.

Minor, non-blocking (carry forward, do not fix here): the seam refactor made
`AcceptedStepTransition` public API — worth a one-line note in the M43-A/M48 contract that
this type is now a shared, stable seam so future changes treat it as public.

## Remains proposed / not accepted / gated

M48-A is **proposed**, not accepted. Still gated: any route generation / search /
comparison / ranking / recommendation / optimizer / economics / advice; any predicate
returning a score/probability/cost/EV/utility/ranking; new operations/omens/predicates/
mechanics/success-criteria; Reveal / Echoes / Omen of Light / Putrefaction / Astrid;
D3–D5, revealed-Desecrated Fracture, PD-013, crafted-capacity; public numeric release;
automation. All require separate explicit ChatGPT/User gates.
