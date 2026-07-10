# M40-A Rarity Progression Runtime Audit (Claude)

audit_id: `P2C_M40A_Rarity_Progression_Runtime_Audit_Claude_v1`
auditor: `claude`
package: `packages/proposed/P2C_M40A_Rarity_Progression_Runtime_Result_Codex_v1/`
observed_repo_head: `253297846f8870ca72ce25915b2cccf7b14b6be6`
observed_active_task_sha: `52c552162f9e4691379f70c693b97de70432babb76d7281665d1f56c2c11b386`
verdict_style: `GO / GO WITH CHANGES / NO-GO`
authority_note: advisory only. Admits real rarity-changing runtime; thresholds stay project-model/source-open; acceptance is ChatGPT/Kirill.

---

## Plain-language summary
This builds the "rarity ladder" for real: Transmutation (white→blue), Augmentation (blue→blue), Regal
(blue→yellow), each in base/Greater/Perfect, plus base Exalted — ten currencies. I checked the mechanics by
running the code, and they match exactly what we agreed with you: it's one shared "add one modifier" engine;
the level filter (Greater/Perfect) and whether rarity goes up are read from data, not hand-coded per currency.
The one genuinely new and correct part: when a currency raises rarity, the engine first makes an **isolated
copy at the target rarity**, builds the add pool there (so the right capacity applies), and commits the rarity
change and the new modifier **together or not at all** — a failed roll leaves the item exactly as it was.
Augmentation's "forced opposite side" falls out of magic capacity (1+1), no separate coin-flip — as you said.
Fractured mods stay locked and unremovable. The full test suite (204) passes on my clean copy. It also folds
in the little dispatcher-file guard I asked for after my own slip. **Verdict: GO**, with a few things the gate
should acknowledge (below), none blocking.

## Verified by execution / byte inspection
- **Exactly ten rows admitted.** `operations.yaml`: the ten M40 rows flip to `accepted_executable_runtime`
  (nine T/A/R also `active_in_current_simulation: true`; base `exalted` from `admission_candidate`). Total
  accepted rows = 16 (the 6 prior + these 10); no stray admission (no Alchemy/Essence).
- **Target-rarity pool build is real (the core mechanic).** `CatalogSingleAddHarness.build_pool` constructs
  `_working_state = replace(state, rarity=pool_build_rarity)` and builds `build_ordinary_add_pool` on that
  isolated state (`rarity_progression.py:225`). Transmutation builds at magic, Regal at rare — so capacity and
  legality reflect the post-transition rarity, not the input.
- **Atomic and non-mutating.** `ItemState` is immutable; the original is never touched. `_assert_applied_
  transition` checks terminal rarity == `output_rarity`, capacity, family/group conflicts, and fractured
  immutability together. Empty pool or failed precondition → one exact `no_transition_no_consumption` path with
  the original state hash; exact mass asserted to sum to 1. Verified in code and tests.
- **Data-driven, no per-currency branches.** Resolver `_compile_m40a_single_add` validates the row shape
  (`remove.kind=none`, one `ordinary_weighted` add, `count=1`, no `side_filter`, atomic) and reads
  input/output/pool-build rarity and MML from the row; fail-closes on shape/rarity drift and on unsupported
  variants/modifier layers. Row MML = 44/70 (Transmutation/Augmentation), 35/50 (Regal); base rows no MML.
- **Fractured protection preserved; only an over-strict assertion relaxed.** The global "fractured must be a
  suffix" check was removed (renamed to `_assert_fractured_modifiers_unchanged`) consistently across
  ordinary_add/chaos/annulment. Immutability (`pre_fractured != post_fractured → raise`) and removal-exclusion
  remain intact. The accepted fractured-crit-suffix staff still validates; no accepted computation changes.
- **Evidence recorded as source-open, exactly as authorized.** `mechanics_evidence.yaml` gains the capacity
  table (normal 0/0, magic 1/1, rare 3/3), mutable modifier count incl. `magic_zero_after_removal_supported`,
  fractured-consumes-its-side + "current fractured-suffix staff is a supported scenario, not a global
  invariant", augmentation opposite-side = capacity-derived (no side lottery), and the rarity-transition
  atomic-commit rule — all `USER_AUTHORIZED_M40A_PROJECT_MODEL` / `project_model_source_open`,
  `server_truth_claimed: false`. `sources.yaml` adds official 0.3.0 as project-model context, not server truth.
- **Dispatcher guard added (the structural fix for my prior slip).** `tools/validate_active_task.py` rejects
  missing/invalid/duplicate frontmatter and inconsistent status/actor/paths; it is wired into `tools/hooks/
  pre-push` *before* SHA regen and has positive+negative tests. Confirmed it hard-fails a truncated
  frontmatter — it would have blocked the bad push I made earlier.
- **Suite green.** `pytest` full run = **204 passed** on a clean clone; foundation fingerprint reproduces
  (`cc39128…`); resolver/harness/mechanics-evidence tests included.

## Watchpoints (non-blocking — for the ChatGPT/User gate)
1. **Deliberate scope widening.** `project_scope.yaml` moves Transmutation/Augmentation/Regal into
   `active_operation_groups` and removes `normal_or_magic_start` from `excluded_from_active_solver` — the
   simulator now models the full normal→magic→rare ladder, not only the fractured rare base. This is the
   intended point of M40 and was flagged in the M40 design, but the gate should acknowledge it explicitly.
   `starting_item_has_required_fractured_crit: true` is unchanged.
2. **Accepted-invariant relaxation.** Dropping the "fractured must be suffix" assertion is a change to already
   accepted annulment/chaos/ordinary_add code. It is safe (protection intact) and necessary for a general
   rarity engine, but it is an accepted-runtime change and should be acknowledged, not slipped in silently.
3. **Thresholds now runtime-active, still source-open.** 44/70/35/50 drive real distributions; recorded as
   project-model/server-unconfirmed with PoE2DB + 0.3.0 refs. No MML/SOURCE-PROVENANCE closure. Keep it open.
4. **Leak-guard false positive (minor tooling).** `check_public_numeric_leaks.py` flags `0.3` from the
   "official 0.3.0" patch string in a doc — not a probability. No real numeric leak exists in the package.
   The guard could ignore `X.Y.0` version strings.

## Recommendation
**GO.** Accept M40-A as the first rarity-changing runtime batch (ten rows, project-model only), and accept the
`validate_active_task.py` dispatcher guard as truth-neutral tooling. At the gate, explicitly acknowledge the
scope widening (watchpoint 1) and the fractured-assertion relaxation (watchpoint 2). Nothing self-accepts.

## Remains proposed / not accepted / gated
- M40-A is proposed until the ChatGPT/User gate. Alchemy/multi-add, Essences, Whittling/Omens/side/desecrated,
  Fracture/Desecrate/Jawbone/Reveal, longer/mixed chains, planner/optimizer/economics/advice, public numeric
  release, automation — all still closed. MML/SOURCE-PROVENANCE/PD-013 not closed.
- Acceptance authority remains ChatGPT/Kirill; this verdict is advisory; no agent self-acceptance.

---
- author: `claude`
- document_type: `rarity_progression_runtime_audit`
- status: `advisory verdict — GO; ten-row rarity ladder runs through one shared target-rarity atomic single-add executor; fractured protected; thresholds source-open`
