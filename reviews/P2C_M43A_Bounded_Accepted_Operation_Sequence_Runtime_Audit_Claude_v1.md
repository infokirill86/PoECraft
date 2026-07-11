# M43-A Bounded Accepted-Operation Sequence Runtime — Claude Audit

audit_id: `P2C_M43A_Bounded_Accepted_Operation_Sequence_Runtime_Audit_Claude_v1`
auditor: `claude`
package: `packages/proposed/P2C_M43A_Bounded_Accepted_Operation_Sequence_Runtime_Result_Codex_v1/`
observed_repo_head: `0e87c636b7e752041300829d51691fc99cc5efe3`
observed_active_task_sha: `25894425ba3854482bb91e3a7054242684fc7226f56936e3c5bd6d40c80e0bab`
verdict_style: `GO / GO WITH CHANGES / NO-GO`
authority_note: advisory only. Composition of already-accepted operations; no new mechanic, admission, or accepted truth. Acceptance is ChatGPT/Kirill.

---

## Plain-language summary
This is the big bridge: the engine can now run a **user-written sequence** of currencies we already have (up
to 8 steps) — e.g. Greater Essence → Chaos → Annulment → Exalted — applying each step to the real, current
state of the item and rebuilding legality every step. I checked the four things that matter most, by running
the code: (1) a one-step "sequence" gives the **exact same result** as calling that currency directly (so the
new layer adds no drift); (2) each later step sees the truly-updated item, not the starting one; (3) when the
exact math would blow up it **stops cleanly and says so** — it never quietly approximates; (4) an operation
with no registered runner is **refused**, not guessed. It's still an evaluator, not an optimizer: it runs the
route you give it, with no searching, ranking, retries, or "if/then". The full test suite (271) passes and the
engine's fingerprint is unchanged. **Verdict: GO.**

## Verified by execution / byte inspection
- **Composition only — no new mechanic or admission.** `data/operations.yaml` admission is unchanged; the
  foundation semantic fingerprint reproduces `230dc88…` (= accepted M42-A). New `bounded_sequence.py` dispatches
  each step through the accepted `OperationResolver` to accepted executors.
- **The 3 accepted-file edits are safe type-widenings, not mechanic changes.** `chaos_like.py`,
  `heterogeneous_chain.py`, `rarity_progression.py` change `isinstance(x, dict)` → `Mapping` and
  `isinstance(x, list)` → `(list, tuple)`. This is required so the executors accept the deep-frozen static data
  (`MappingProxyType`/tuples) when reached through the sequence path; `dict` is a `Mapping` and `list` is in
  `(list, tuple)`, so every previously-passing/failing case is unchanged and all fail-closed shape checks
  (`kind`, `count`, `exclude_flags`, atomic) remain identical. Behavior-preserving — and exactly what makes
  one-step parity hold through the frozen path.
- **Anchor 1 — one-step parity (the anti-drift guarantee).** `test_one_step_exact_parity_for_every_accepted_
  executor_family` and `..._seeded_parity_...` pass: a single-step sequence is identical (exact and seeded) to
  invoking that accepted operation directly, for every family.
- **Anchor 2 — branch-state correctness.** `test_branch_state_is_load_bearing_and_add_annul_aggregates_
  terminals` passes; each later step re-resolves and rebuilds from the actual current branch `ItemState`; no
  root-state pool/plan reuse.
- **Anchor 3 — exact-ceiling honesty.** `ExactCeilingStop` / `_ExactCeilingExceeded` produce a structured stop
  (`candidate_branch`/`exact_path`/`exact_terminal` ceilings); `test_exact_ceiling_returns_structured_stop_
  without_partial_or_mc_output` proves no truncation, renormalization, or hidden MC substitution on overflow.
- **Anchor 4 — executor-registry completeness.** `AcceptedOperationExecutorRegistry` raises
  `M43ASequenceAdmissionError` for an admitted row without a registered accepted executor and for non-admitted
  operations (`test_missing_executor_and_nonadmitted_operation_fail_closed`, `..._registry_is_complete_...`).
- **Evaluator, not planner.** `test_request_schema_blocks_modifiers_unbounded_steps_and_continue_policy` passes:
  `active_modifier_ids`, sequences beyond 8 steps, and any non-`stop`/continue policy are rejected. No route
  generation, ranking, conditional/retry logic. `stop_on_no_transition: true`; early no-transition preserves
  prior committed state and skips later steps (`test_early_no_transition_preserves_prior_success...`).
- **Cross-engine convergence (the watchpoint I flagged).** `test_seeded_mc_matches_tractable_mixed_exact_
  projection` and `test_eight_step_seeded_sequence_replays_exactly` pass — seeded MC uses the same accepted
  executors, replays deterministically, and matches the exact projection where tractable (continuing the
  M33/M34 discipline).
- **Suites green.** `test_m43a_*` = **28 passed**; full `pytest` = **271 passed** on a clean clone; ACTIVE_TASK
  validator + public-numeric-leak guard PASS.

## Watchpoints (non-blocking)
- Exact enumeration of 8 mixed steps is inherently combinatorial; correctness depends on the pinned ceilings
  actually firing the structured stop before blow-up. This is tested, and MC remains the path beyond exact —
  keep the ceilings conservative when longer/wider sequences are later requested.
- This is the natural precursor to the (far-future, separately gated) optimizer. The evaluator/planner line is
  clean here; it must stay clean — any future "choose/rank/repeat" is a new gate, not an extension of M43-A.

## Recommendation
**GO.** Accept M43-A as the bounded fixed-sequence evaluator (1–8 user-supplied steps over accepted operations),
composed via the accepted resolver/executors with proven one-step parity, branch-state correctness, honest
exact ceilings, and a fail-closed executor registry. No new mechanic/admission/truth. Alchemy remains deferred;
Omens/Fracture/Desecrate, longer/conditional sequences, and any planner/optimizer stay separate gates.

## Remains proposed / not accepted / gated
- M43-A is proposed until the ChatGPT/User gate. No new operation/modifier admission; Alchemy runtime,
  Omens/Whittling/Fracture/Desecrate/Jawbone/Reveal, conditional/retry/route-generation/ranking/optimizer/
  economics/EV/advice, public numeric release, and automation all remain closed. MML/SOURCE-PROVENANCE/
  crafted-capacity/PD-013 stay open.
- Acceptance authority remains ChatGPT/Kirill; this verdict is advisory; no agent self-acceptance.

---
- author: `claude`
- document_type: `bounded_sequence_runtime_audit`
- status: `advisory verdict — GO; 1-8 step evaluator over accepted operations; one-step parity + branch-state + honest ceilings + fail-closed registry verified; evaluator not planner; fingerprint unchanged`
