# M44-A Alchemy Runtime — Claude Audit

audit_id: `P2C_M44A_Alchemy_Runtime_Audit_Claude_v1`
auditor: `claude`
package: `packages/proposed/P2C_M44A_Alchemy_Runtime_Result_Codex_v1/`
observed_repo_head: `79c48129a3e0b90a5682148cde9701e485b5e7da`
observed_active_task_sha: `77bd086b79384ba960acbe235e6a256d13221aead2cdf9bdcdd2173ed7429b9b`
verdict_style: `GO / GO WITH CHANGES / NO-GO`
authority_note: advisory only. The four-modifier sampling is project-model (server-unverified). Acceptance is ChatGPT/Kirill.

---

## Plain-language summary
This makes Alchemy runnable — the last of the basic currencies you wanted. It turns a white or blue quarterstaff
into a yellow one with **four** new random modifiers, atomically: the engine builds the result on a private
copy, adds four modifiers one at a time (rechecking room each time), and only swaps your item in if all four
succeed — otherwise your item is untouched and the orb isn't spent. I ran it: your "2-2 or 3-1?" question is
handled correctly — a test proves the four modifiers land as **3-1, 2-2, or 1-3 by weight, never 4-0**. It
refuses a fractured item (that case is still unverified), reuses our accepted "add a modifier" engine (no new
random logic), and behaves identically whether called directly or as a one-step route. The four-modifier
rolling model is recorded as **our model, not confirmed server behaviour** — matching your gate decision. Full
test suite (282) passes. **Verdict: GO.**

## Verified by execution / byte inspection
- **Only `alchemy` admitted.** `operations.yaml`: the single `alchemy` row flips to `accepted_executable_runtime`
  + `active_in_current_simulation: true`; nothing else. `project_scope.yaml` activates the alchemy group;
  `sources.yaml` adds the 0.3.1 alchemy patch reference.
- **Atomic four-add over the accepted kernel.** `AlchemyHarness` builds from an isolated empty-Rare
  `_working_state`, loops `range(add_count)` = 4 sequential adds via the accepted `build_ordinary_add_pool`
  (rebuilding the legal pool from the branch state each time), and commits the caller-visible item **once**
  after the fourth success. No new sampling kernel. `_validate_operation_contract` pins the exact sequence
  (`discard_all_explicit → create_empty_rare_shell → add_ordinary_x4 → commit`) and fails closed on drift.
- **Distribution is correct (your 2-2/3-1 question).** `test_m44a_weight_driven_side_distributions_cover_three_
  one_two_two_one_three` proves the four modifiers distribute by weight across sides, capped at 3/side —
  covering 3-1, 2-2, and 1-3, never 4-0. Matches my independent source check.
- **Atomic rollback + fractured floor.** `test_m44a_intermediate_pool_failure_rolls_back_magic_item_atomically`
  and `..._fractured_input_fails_closed_and_original_is_unchanged` pass: fewer than four legal selections, or a
  fractured/unrevealed-desecrated input, returns no-transition/no-consumption with the original item unchanged
  (no partial-Rare, no <4-mod result). Magic input's original explicits are discarded on the working copy only.
- **Composition-safe (the M43-A anchors hold).** `bounded_sequence.py` change is **additive** — it registers the
  alchemy executor in the accepted fail-closed registry so sequences can include it.
  `test_m44a_resolver_direct_and_m43a_one_step_parity` proves a direct call, a resolver call, and a one-step
  M43-A sequence all produce the identical result. `test_m44a_exact_terminal_aggregation_and_seeded_mc_
  convergence_replay` confirms seeded MC converges to the exact distribution and replays deterministically;
  exact ceilings return a structured stop (no truncation/approximation).
- **Sampling model recorded as project-model/source-open.** `mechanics_evidence.yaml` `alchemy_m44a`:
  `project_model_source_open`, `server_truth_claimed: false`, `selection:
  sequential_accepted_ordinary_weighted_add` — exactly the model ChatGPT/User ratified; not claimed as server
  truth.
- **Suites green.** `test_m44a_*` = **11 passed**; full `pytest` = **282 passed** on a clean clone; foundation
  fingerprint reproduces the package-pinned `fcc79311…` (changed only for the alchemy admission);
  ACTIVE_TASK validator + public-numeric-leak guard PASS.

## Watchpoints (non-blocking)
- The four-modifier sampling stays project-model / server-unverified (the exact internal server algorithm is not
  public). Recorded correctly as source-open; do not read admission as closing that question.
- Fractured-input Alchemy remains a deferred separate gate (correct — our accepted base is fractured, so Alchemy
  is exercised on the normal/magic starting route, not the base staff).

## Recommendation
**GO.** Accept M44-A as base non-fractured quarterstaff Alchemy: one atomic four-modifier multi-add over the
accepted ordinary-weighted-add kernel, isolated Rare working copy, all-or-nothing commit, weight-driven
capped distribution, resolver + M43-A one-step parity, MC↔exact convergence — sampling model project-model/
source-open. This closes the basic-currency set. Fractured-input Alchemy, variants, Omens, non-equipment
classes remain separate gates.

## Remains proposed / not accepted / gated
- M44-A is proposed until the ChatGPT/User gate. Fractured-input Alchemy, Alchemy variants,
  Omens/Whittling/Fracture/Desecrate/Jawbone/Reveal, maps/jewels/other item classes, conditional/retry/route
  generation, planner/optimizer/economics, public numbers, automation — all closed. MML/SOURCE-PROVENANCE/
  crafted-capacity/PD-013 stay open.
- Acceptance authority remains ChatGPT/Kirill; this verdict is advisory; no agent self-acceptance.

---
- author: `claude`
- document_type: `alchemy_runtime_audit`
- status: `advisory verdict — GO; base Alchemy = atomic 4x sequential weighted-add over accepted kernel; weight-driven 3-1/2-2/1-3; fractured rejected; parity + convergence verified; sampling project-model/source-open`
