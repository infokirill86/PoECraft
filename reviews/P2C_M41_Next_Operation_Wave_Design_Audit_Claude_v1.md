# M41 Next Operation Wave Design Audit (Claude)

audit_id: `P2C_M41_Next_Operation_Wave_Design_Audit_Claude_v1`
auditor: `claude`
package: `packages/proposed/P2C_M41_Next_Operation_Wave_Design_Codex_v1/`
observed_repo_head: `fbe7b337039af88641dcf000f59f277a1bd8c863`
observed_active_task_sha: `99738e0f6dea780d84285127ac64e8acd65b4cb5e6e91d916cdac163bd9de919`
verdict_style: `GO / GO WITH CHANGES / NO-GO`
authority_note: advisory only. Design/selection only; no runtime. Essence semantics stay project-model, not server truth; acceptance is ChatGPT/Kirill.

---

## Plain-language summary
This picks the next thing to build. The choice: **Greater Essences for the quarterstaff** — eight of them,
including Abrasion (flat physical), which is the most relevant to our physical staff. An Essence is different
from everything so far: instead of adding a *random* modifier, it adds one **specific guaranteed** modifier and
turns a blue item yellow. The plan reuses the exact same "make an isolated copy at the target rarity, then
commit rarity + mod together" pattern we just accepted in M40-A, and reads which mod each Essence gives from
data (not hand-coded). It deliberately **splits off Perfect Essence** (which also removes a mod first — an edge
the sources don't fully pin down) and defers Omens, Alchemy, Fracturing, and Desecrated crafting. I checked the
data: all eight rows exist and are fully described in the repo. **Verdict: GO** on the design, with a couple of
mechanics points to nail when it's actually built (below), none blocking.

## Verified against real bytes
- **Design/selection only.** No `src`/`data`/`config`/`tests` change since the M40-A acceptance
  (`b68ed5b..HEAD`). Nothing is admitted; the eight rows stay `data_reference_candidate`.
- **The eight rows are real and complete.** `data/operations.yaml` carries each `greater_essence_*` row with a
  `transition` holding `guaranteed_mod_id`, `guaranteed_family_id`, `guaranteed_side`, `crafted: true`,
  `remove: {kind: none}`, and `prevalidate: [family_absent, crafted_capacity_free, result_side_capacity_free]`.
  `data/essence_outputs.yaml` mirrors them (id, family, side, modifier_level, tags, group_ids, tier) — so the
  design's "compile from operation + output data, cross-file agreement" is backed by existing bytes.
- **Selection reasoning is sound.** Essence = guaranteed-modifier capability, the largest missing product
  capability and directly relevant to the fractured-Rare staff (Abrasion = physical). Alchemy (four-add +
  discard), Omens (repo catalogue lags external sources), Fracture (disputed revealed-Desecrated edge),
  Jawbone/Desecrated/Reveal (PD-013), and longer chains are each deferred with a stated reason.
- **Right architecture (reuse, not a new algebra).** One `GreaterEssencePlan` + shared executor over the
  accepted M40-A atomic target-rarity pattern; guaranteed install with **no weighted draw**; fail-closed on
  variants/Omens/Perfect/unknown fields; family/group + capacity checks reuse accepted validation.
- **Boundaries clean and honest.** Perfect Essence is split out with its unresolved removal-capacity question
  explicitly raised as a future gate question; the package also surfaces a real source-drift finding (current
  PoE2DB Omens absent from `data/omens.yaml`) and copies no external data into project truth. PD-013, broader
  MML, SOURCE/PROVENANCE, public numbers, optimizer, automation — all stay closed.

## Watchpoints (mechanics-source; for the eventual M41-A gate — non-blocking here)
1. **`crafted: true` + separate crafted-capacity is the one model to source-verify before it becomes
   load-bearing.** Essence outputs set `crafted: true`, `crafted_capacity_cost: 1`, and
   `all_essence_outputs_consume_crafted_capacity: true`, and `prevalidate` treats `crafted_capacity_free` as a
   constraint *separate* from side capacity. PoE2 removed PoE1-style bench "crafted mod slot" crafting, so
   whether Essence-added mods truly occupy a distinct crafted-capacity slot (vs a normal prefix/suffix slot)
   should be confirmed against sources. **It is not load-bearing for the Greater-only scope** (Greater needs a
   Magic input and outputs Rare, so only one Greater Essence is ever applied to a given item, on a fresh item
   with free capacity) — but it must be nailed before Perfect/multi-essence use, where it changes results.
   Recommend a source/Kirill check, analogous to the Perfect-removal question the design already flags.
2. **First guaranteed (non-random) add.** At M41-A verify the executor installs the exact declared `mod_id`
   with zero candidate draw, and that every `guaranteed_mod_id`/family/side agrees across operations.yaml and
   essence_outputs.yaml (fail-closed on any mismatch).
3. **Greater essence family = the ordinary family** (`adds_value_to_value_physical_damage`, etc.), so
   `family_absent` correctly blocks stacking on an item that already has that ordinary family. Confirm at M41-A
   that this conflict check reuses accepted family/group rules (Perfect uses distinct `crafted_*` families —
   that's a separate, deferred concern).
4. **Still open / deferred:** Perfect Essence removal-capacity semantics; Omen catalogue reconciliation; all
   Omen/Alchemy/Fracture/Desecrated/Jawbone/Reveal runtime; longer chains; PD-013; broader MML.

## Recommendation
**GO** on the M41 design/selection. Authorize a later **M41-A** implementing only the eight Greater Essence
quarterstaff rows through one shared, data-driven guaranteed-add executor over the accepted M40-A atomic
pattern, with the mechanics checks above (esp. watchpoint 1 — the crafted-capacity model — verified before
admission, and certainly before any Perfect/multi-essence extension). Perfect Essence, Omens, and everything
else remain separate gates. Nothing self-accepts.

## Remains proposed / not accepted / gated
- No M41 runtime; the eight rows stay candidates; base/other Essence tiers (Lesser/Normal/Perfect/Corrupted)
  and all Omen/Alchemy/Fracture/Desecrated/Jawbone/Reveal behavior stay closed.
- MML not closed; SOURCE/PROVENANCE not closed; PD-013 not closed; no public numbers; no optimizer; no
  automation. Acceptance authority remains ChatGPT/Kirill; this verdict is advisory.

---
- author: `claude`
- document_type: `next_operation_wave_design_audit`
- status: `advisory verdict — GO; Greater Essence quarterstaff core selected as next wave; guaranteed-add over M40-A atomic pattern; crafted-capacity model to source-verify at M41-A`
