# M41-A Greater Essence Quarterstaff Runtime Audit (Claude)

audit_id: `P2C_M41A_Greater_Essence_Quarterstaff_Runtime_Audit_Claude_v1`
auditor: `claude`
package: `packages/proposed/P2C_M41A_Greater_Essence_Quarterstaff_Runtime_Result_Codex_v1/`
observed_repo_head: `587e07839b3a695dfde6a2bfa7bcf9368fd0b584`
observed_active_task_sha: `3d403e584821691fd2b674aa35edb6aba3b906a2f771d8653c2232ab36b63675`
verdict_style: `GO / GO WITH CHANGES / NO-GO`
authority_note: advisory only. Admits guaranteed-add runtime; Essence semantics and crafted-capacity stay project-model/source-open; acceptance is ChatGPT/Kirill.

---

## Plain-language summary
This turns on the eight Greater Essences for the staff. An Essence is the first "guaranteed" currency: instead
of a random modifier it installs one **specific** modifier and turns a blue item yellow. I checked by running
the code: the executor installs exactly the modifier the data declares — **no random roll at all** (I confirmed
this both in the code and with a test that the exact, seeded, and replayed results are identical). It reuses
the same atomic "isolated copy → commit rarity+mod together" pattern from M40-A, keeps existing and fractured
mods untouched, and refuses (no-transition, nothing consumed) on wrong rarity, a family clash, or no room. All
four fixes we asked GPT to add are present and correct, and the "crafted-capacity" question we weren't sure
about is deliberately left **open and unverified**, not silently decided. Full test suite (220) passes on my
clean copy. **Verdict: GO.**

## Verified by execution / byte inspection
- **Exactly eight rows admitted.** `operations.yaml`: the eight `greater_essence_*` rows flip to
  `accepted_executable_runtime` + `active_in_current_simulation: true`; nothing else. Total accepted rows now
  24 (16 prior + 8). Perfect/Lesser/Corrupted Essence stay non-admitted.
- **Guaranteed install, no random draw (the central risk).** `greater_essence.py` builds the terminal with
  `replace(...)` appending `ModifierInstance(mod_id=operation.guaranteed_mod_id, crafted=True)` — the exact
  declared mod. No pool builder, no `random`, no weighted `branch_options` anywhere in the module. Test
  `test_m41a_exact_and_seeded_paths_have_no_random_candidate_draw` asserts exact == seeded == replay.
- **Canonical modifier index resolution (my prompt fix #3).** The guaranteed mod
  (`crafted_greater_abrasion_flat_physical`, …) resolves in `StaticGameData.modifier_index` at runtime
  (verified live), so the **shared** capacity/family/fractured validators handle it; no parallel validator was
  added. The resolver cross-checks operation row ↔ `essence_outputs.yaml` ↔ `modifier_index` for
  id/family/side/crafted/groups/class/tier and fails closed on any mismatch
  (`test_m41a_missing_or_inconsistent_canonical_output_fails_closed`, `..._tampered_operation_contract_fails_hard`).
- **project_scope activation (my fix #2).** `greater_essence` moved from `reference_only_operation_groups` to
  `active_operation_groups`; `greater_essences` added to `active_mechanics`; `greater_essence_magic_to_rare_route`
  removed from `excluded_from_active_solver`. Exactly the eight-row activation.
- **crafted-capacity held source-open (my fix #1 + refinement).** Labeled `source_open_unverified_greater_only`
  in code and docs; it uses the existing shared validator and is **not** removed, **not** closed, and
  explicitly must not be used as evidence for stacking/replacement/multi-Essence/Perfect. Tested
  (`test_m41a_crafted_capacity_stays_explicit_source_open_shared_validation`). Not outcome-bearing for
  Greater-only (fresh magic item has free crafted capacity), so it correctly did not block the wave.
- **Fingerprint delta (my fix #4).** Documented old→new (`cc39128…` → `251bf977…`); reproduces exactly on my
  clean clone; pinned by the foundation regression test; only the two expected semantic components changed
  (operations admission + project_scope); any unrelated change is a hard-fail.
- **Atomic + fail-closed.** Immutable `ItemState`, isolated replacement, rarity+mod commit together; existing
  and fractured mods preserved (`..._preserves_existing_and_fractured_instances_atomically`); ordinary-family
  conflict, wrong rarity, Perfect Essence, and capacity failure all return `no_transition_no_consumption` with
  the original state hash.
- **Repo-mandated steps actually happened (enforcement-layer check).** Codex performed the AGENTS.md
  architecture/participant critique (doc 02, substantive) and correctly **did not** silently encode
  crafted-capacity as truth — it verified against the source posture and labeled it open. This is the layered
  minimal-prompt working as intended.
- **Suite green.** Full `pytest` = **220 passed** on a clean clone; validator PASS; public-numeric-leak guard PASS.

## Watchpoints (non-blocking)
- **Crafted-capacity + Essence mod values stay project-model / source-open.** The 8 guaranteed mods and their
  values come from PoE2DB (project-model, server-unconfirmed); crafted-capacity is explicitly unverified. This
  is consistent with our posture and is documented — must be resolved before Perfect/multi-Essence, and must
  not be read as SOURCE/PROVENANCE or crafted-capacity closure.

## Recommendation
**GO.** Accept M41-A as the first guaranteed-add runtime (eight Greater Essence quarterstaff rows,
project-model only), built through one shared deterministic executor over the accepted M40-A atomic pattern.
Keep crafted-capacity source-open. Perfect Essence, Omens, Alchemy, and everything else remain separate gates.
Nothing self-accepts.

## Remains proposed / not accepted / gated
- M41-A is proposed until the ChatGPT/User gate. Perfect/Lesser/Corrupted Essence, multi-Essence capacity,
  Omens, Whittling, Alchemy, Fracture/Desecrate/Jawbone/Reveal, longer chains, planner/optimizer/economics,
  public numeric release, automation — all still closed.
- MML not closed; SOURCE/PROVENANCE not closed; PD-013 not closed; crafted-capacity source-open.
- Acceptance authority remains ChatGPT/Kirill; this verdict is advisory; no agent self-acceptance.

---
- author: `claude`
- document_type: `greater_essence_runtime_audit`
- status: `advisory verdict — GO; eight Greater Essences run as one deterministic guaranteed-add over M40-A atomic pattern; no random draw; crafted-capacity source-open`
