# M40 Rarity Progression Family Design-Verification Audit (Claude)

audit_id: `P2C_M40_Rarity_Progression_Family_Design_Verification_Audit_Claude_v1`
auditor: `claude`
package: `packages/proposed/P2C_M40_Rarity_Progression_Family_Design_Verification_Codex_v1/`
observed_repo_head: `0c494f931234fd5623b389890472ba90feee19f4`
observed_active_task_sha: `ed2b56dd87e019d668ca5d96c2f3876f3cc817322c91f518663f6e15650eb962`
verdict_style: `GO / GO WITH CHANGES / NO-GO`
authority_note: advisory only. Design/mechanics verification; thresholds stay project-model, not server truth; acceptance is ChatGPT/Kirill.

---

## Plain-language summary
This checks the "rarity ladder" currencies before we build them: Transmutation (normal→magic), Augmentation
(magic→magic), Regal (magic→rare), each in base/Greater/Perfect, plus base Exalted (rare→rare) — ten rows.
Answer: they're all the **same one action** we already run — "add one modifier" — differing only by the
minimum-level filter (Greater/Perfect) and by whether the item's rarity goes up. The plan is one shared,
data-driven "single-add" executor, not ten hand-coded currencies. The one genuinely new idea is correct and
important: when a currency raises rarity (Transmutation, Regal), the add pool must be built at the **target**
rarity (a normal item has no room for a modifier until it becomes magic), and the rarity change plus the added
modifier must commit **together or not at all**. I checked all ten rows against the actual data and the numbers
match. Nothing is built or turned on here. **Verdict: GO.** A few things to watch when we actually build it,
none blocking.

## Verified against real bytes
- **Design-only, no scope leak.** Diff since the M39-B acceptance (`c609632..HEAD`) touches only this package's
  docs, the dispatcher, and the regenerated manifest — no `src`, `data`, `tests`, or `config`. Nothing is
  admitted; project-scope/handler/source-registry changes are explicitly deferred to a future M40-A gate.
- **Inventory is byte-accurate.** Confirmed each of the ten `operations.yaml` rows: Transmutation/Augmentation
  base→Greater(44)→Perfect(70), Regal base→Greater(35)→Perfect(50), all `add.count = 1`, all `remove: none`;
  input→output rarities normal→magic / magic→magic / magic→rare / rare→rare as stated; base rows carry no MML;
  the nine T/A/R rows are `data_reference_candidate` and base `exalted` is `admission_candidate`. Matches the
  design's table exactly.
- **Thresholds match the design's sources.** 44/70 and 35/50 agree between the repo data and the cited PoE2DB
  wording; `mechanics_evidence.yaml` already lists Transmutation/Augmentation/Regal/Exalted as consumers of the
  shared family-internal MML policy (`supported_empirically_server_unconfirmed`). No contradictory source found.
- **Target-rarity pool build is correct and correctly labeled.** Building the add pool at the target rarity for
  Transmutation/Regal is mechanically necessary (input rarity has no capacity for the added modifier) and is
  recorded as a project-model execution inference, not server truth. The "isolated working state → build/sample
  → validate → atomic commit" order is the right way to keep failure atomic (no rarity-only leftover).
- **Augmentation needs no separate side lottery.** Correct: the accepted combined legal pool plus magic
  one-prefix/one-suffix capacity naturally removes the occupied side; this reuses the accepted pool builder's
  capacity filtering rather than inventing a side randomizer.
- **Base Exalted characterization is right.** Rare→rare, one add, no MML, Omen parameters remain unsupported /
  fail-closed. This is the plain accepted-`ordinary_add` wrapper and cleanly resolves the M39-B
  base-vs-Greater/Perfect Exalted asymmetry I flagged.
- **Failure semantics are complete.** No-transition/no-consumption on wrong rarity, full capacity, empty pool,
  or schema drift; input state unchanged on no-transition; exact terminal mass (incl. no-transition) sums to 1;
  fail-closed on unsupported variant/modifier/Omen. Lean plan (`CatalogSingleAddPlan`) stays a narrow compiler
  seam, not a generalized operation algebra.

## Watchpoints (non-blocking — for the eventual M40-A gate)
1. **Rarity-transition is the genuinely new mechanic; slice accordingly.** Everything accepted so far
   (`ordinary_add`, Annulment, Chaos, M39-B) keeps rarity fixed. Augmentation and Exalted are effectively
   in-place `ordinary_add` wrappers (low risk); **Transmutation and Regal introduce the first atomic
   rarity-transition + target-rarity pool build**. One 10-row M40-A batch is defensible, but the load-bearing
   evidence must be the Transmutation/Regal atomicity and target-rarity-pool proofs (and their negative
   controls). If the gate wants extra caution, admit the two in-place wrappers and the two rarity-transition
   families as separate slices.
2. **Thresholds go runtime-active and stay source-open.** 44/70/35/50 rest on PoE2DB + official-notes
   agreement (project-model, server-unconfirmed, since PoE2 is not datamineable). At M40-A they should be
   recorded in `mechanics_evidence.yaml` with the official 0.3.0 + PoE2DB references, without reading as MML
   or SOURCE/PROVENANCE closure. (The design already plans this.)
3. **Source-registry completeness gap (self-disclosed).** `data/sources.yaml` references a later patch, not the
   0.3.0 introduction wording that is actually load-bearing here. Add the 0.3.0 reference during the M40-A
   evidence update. Not a mechanics conflict.

## Recommendation
**GO** on the M40 design/mechanics verification. Authorize a later **M40-A** implementation gate for a shared,
data-driven single-add executor with an isolated target-rarity working state and atomic rarity+modifier
commit, admitting only the ten named rows, with the rarity-transition proofs (watchpoint 1) as first-class
evidence and thresholds logged as source-open (watchpoint 2). Nothing self-accepts.

## Remains proposed / not accepted / gated
- No M40 runtime; no operation admission; the ten rows stay candidates. Base Exalted stays gated until M40-A.
- Alchemy/multi-add, Essences, Whittling/Omens/side/desecrated, Fracture/Jawbone/Reveal, longer chains,
  planner/optimizer/economics/advice, public numeric release — all still closed.
- MML not closed; SOURCE/PROVENANCE not closed; PD-013 not closed; no automation. Acceptance authority remains
  ChatGPT/Kirill; this verdict is advisory.

---
- author: `claude`
- document_type: `rarity_progression_family_design_verification_audit`
- status: `advisory verdict — GO; ten-row single-add family verified as design; rarity-transition executor is the new mechanic; thresholds stay project-model/source-open`
