# M42-A Perfect Essence Quarterstaff Runtime Audit (Claude)

audit_id: `P2C_M42A_Perfect_Essence_Quarterstaff_Runtime_Audit_Claude_v1`
auditor: `claude`
package: `packages/proposed/P2C_M42A_Perfect_Essence_Quarterstaff_Runtime_Result_Codex_v1/`
observed_repo_head: `daa42dcf664c96f8a28fa8d900d1a3c2a3e86759`
observed_active_task_sha: `c34ced83be22f3e11e66a50a23c508e109f6072a5e2d261cdbac83b90a4afb0c`
verdict_style: `GO / GO WITH CHANGES / NO-GO`
authority_note: advisory only. Removal model & crafted floor are project-model/source-open, not server truth; acceptance is ChatGPT/Kirill.

---

## Plain-language summary
This builds the six Perfect Essences for the staff. A Perfect Essence works on a yellow item: **removes one
modifier, then installs a specific guaranteed one**. The tricky part was *which* mod gets removed — and it's
built exactly as you decided and verified in-game: it only removes mods that leave room for the guaranteed one.
I confirmed both cases by running the code: when the guaranteed side has space, any (non-fractured) mod can be
removed with equal chance; when that side is full, only that side's mods are eligible (so the guaranteed mod
fits). No random roll for the guaranteed mod itself — it's the exact declared one. For now, Perfect Essence
only runs on an item with **no** crafted mods (the safe rule) — and, as I promised to check, that limit is
written down as a deliberate "for now / open question," not as a permanent truth, so the rune (+1 crafted slot)
path stays open for later. Full test suite (239) passes on my clean copy. **Verdict: GO.**

## Verified by execution / byte inspection
- **Exactly six rows admitted.** `operations.yaml`: the six `perfect_essence_*` rows flip to
  `accepted_executable_runtime` (30 total accepted). No Perfect Seeking/Infinite invented; nothing else added.
- **Removal model = your decision, verified both sub-cases.** `build_feasible_pool` starts from the accepted
  shared non-fractured `build_removal_pool`, then for each candidate simulates the removal + guaranteed install
  and keeps it **only if the complete terminal validates** (`_terminal_for_candidate`), adding it as
  `Candidate(key, 1)` — **uniform, weight-independent**. This cleanly yields: free target side → all
  non-fractured removals feasible; full target side → only same-side (capacity-creating) removals survive;
  empty feasible pool → `no_transition_no_consumption` **before any draw**. Tests
  `..._free_target_side_keeps_all...`, `..._full_target_side_keeps_only_removals_that_create_capacity`,
  `..._empty_feasible_pool_fails_unchanged_before_draw`, `..._uniform_exact_mass...` all pass. The
  `operations.yaml` wording was updated (`uniform_feasible_installed_instance` +
  `feasible_if: guaranteed_modifier_installable_after_removal`) — the old unconditioned wording is not treated
  as evidence, so exact probabilities now reflect the accepted model.
- **Guaranteed install, no draw.** `_terminal_for_candidate` installs the exact row-declared canonical mod via
  `with_modifiers` — no pool, no `random`, no weighted draw. Test
  `..._seeded_replay_uses_one_removal_decision_and_no_add_draw` confirms only the removal is a decision.
- **Crafted floor honestly framed (my promised catch — resolved).** Precondition is `crafted_count == 0`,
  computed from the real `capacity_snapshot` (not a hardcoded "1"); `mechanics_evidence.yaml` records it as
  `USER_APPROVED_PROJECT_RULE` / `project_model_source_open`, `crafted_capacity.broader_contract_closed:
  false`, `replacement_stacking_repeat_admitted: false`. So it is a conservative fail-closed floor, **not** a
  baked "capacity = 1 forever" truth, and the augment-socket/Astrid machinery is untouched. Test
  `..._existing_crafted_modifier_fails_closed_unchanged` passes.
- **Atomic + fail-closed + canonical.** Immutable isolated terminal; commits removal+add together; unselected
  and fractured mods preserved (`..._atomic_terminal_preserves...`); item-class / rarity / family-group /
  missing-canonical / unprepared-row / tampered-contract all fail unchanged. Guaranteed mods resolve in the
  canonical `modifier_index`.
- **Fingerprint + suite.** Foundation fingerprint reproduces `230dc88…` (doc pins it, prev `251bf97…`); full
  `pytest` = **239 passed** on a clean clone; ACTIVE_TASK validator + public-numeric-leak guard PASS. Codex
  performed the AGENTS.md participant critique (doc 02).

## Watchpoints (non-blocking)
- **Crafted precondition is stricter than the eventual mechanic** (`crafted_count == 0` vs the real
  `crafted_count < crafted_capacity` with the Astrid +1 rune). This is a deliberate, honestly-labeled floor
  that also sidesteps the still-open "is a crafted mod itself removable/replaceable" question — fine for now.
  When the rune / multi-crafted gate opens, this precondition should generalize to `crafted_count <
  crafted_capacity` (using the existing capacity fields) and `crafted_count` should count fractured-crafted
  mods.
- **Removal model + guaranteed values stay project-model / source-open.** The full-side removal rule is
  player-observed (Kirill 10/10) + community-supported, not primary-sourced; guaranteed mod values are PoE2DB.
  Consistent with our posture; not SOURCE/PROVENANCE or crafted-capacity closure.

## Recommendation
**GO.** Accept M42-A as the six Perfect Essence quarterstaff rows: one shared remove-then-guaranteed-add
executor with feasible-pool uniform removal (both sub-cases correct) and the conservative `crafted_count == 0`
floor, all project-model/source-open. Replacement/repeat, the rune capacity path, Omens/side filters, and
everything else remain separate gates.

## Remains proposed / not accepted / gated
- M42-A is proposed until the ChatGPT/User gate. Perfect Essence replacement/stacking/repeat, the
  Astrid/rune multi-crafted path, Omens/Whittling/side, Lesser/Corrupted Essences, non-inventory rows,
  Alchemy/Fracture/Jawbone/Reveal, longer chains, planner/optimizer/economics, public numbers, automation —
  all closed. Broader crafted-capacity, MML, SOURCE/PROVENANCE, PD-013 stay open.
- Acceptance authority remains ChatGPT/Kirill; this verdict is advisory; no agent self-acceptance.

---
- author: `claude`
- document_type: `perfect_essence_runtime_audit`
- status: `advisory verdict — GO; six Perfect Essences via shared feasible-pool remove-then-guaranteed-add executor; crafted_count==0 is an honest source-open floor`
