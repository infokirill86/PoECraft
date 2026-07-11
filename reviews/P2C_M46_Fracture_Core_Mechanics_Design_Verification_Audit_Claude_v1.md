# M46 Fracture Core Mechanics Design Verification — Claude Audit

audit_id: `P2C_M46_Fracture_Core_Mechanics_Design_Verification_Audit_Claude_v1`
auditor: `claude`
package: `packages/proposed/P2C_M46_Fracture_Core_Mechanics_Design_Verification_Codex_v1/`
observed_repo_head: `77c8418e2b80480d46af77ae55598ddb9e51ca51`
observed_active_task_sha: `7af1bc4e6f10d55c900c0eeb9177db5ba116add998283d42d4dfe5fe30572fae`
verdict_style: `GO / GO WITH CHANGES / NO-GO`
authority_note: advisory only. Design/mechanics verification; Fracture stays project-model, PD-013 not closed. Acceptance is ChatGPT/Kirill.

---

## Plain-language summary
This checks the Fracturing Orb before we build it. It locks one modifier on a Rare item so it can never be
removed or changed. I checked the design against both the sources and what you told me from the game, and it's
right: it needs a Rare item with **at least four** mods and no existing fractured mod, then it locks **one
random mod chosen evenly from all of them** (no prefix/suffix lottery, no weighting). It correctly captures the
subtle bit you flagged — a **crafted mod can be fractured and stays crafted**. And it correctly **stays away
from the disputed Desecrated case** (the "make it 1-in-3 instead of 1-in-4" trick): sources disagree on whether
Desecrated mods can be fractured, so the clean version simply refuses any item with a Desecrated mod and leaves
that decision (PD-013) for later. The immutability side is thorough — once fractured, every currency we've built
must keep skipping that mod. **Verdict: GO.**

## Verified against real bytes + ground truth
- **Design-only.** No `src`/`config`/`tests` change; `data` diff is only my own accepted Whittling-evidence
  commit. The `fracturing_orb` row stays `disputed_or_requires_user_resolution` — nothing admitted.
- **Clean-core contract matches the game + accepted mechanics.** `operations.yaml` `fracturing_orb` already
  encodes: rare input; preconditions `occupied_explicit_slots >= 4` and `fractured_modifier_count == 0`;
  target `uniform_installed_instance` excluding `fractured` and `unrevealed_desecrated_placeholder`; mutation
  `set_flag fractured: true`; `preserve_flags: [crafted, desecrated]`. This is exactly Kirill's ground truth
  (≥4 mods, random one of all — a **combined uniform pool, no side-first, no generation weight**) and matches
  our accepted removal-model discipline.
- **Fractured-can-be-crafted captured.** The candidate pool includes ordinary **and** `crafted` instances and
  preserves the `crafted` flag; `ModifierInstance` already carries independent `crafted`/`fractured` flags, so a
  crafted mod can become fractured-and-crafted with no new state algebra (matches the player report + Kirill's
  in-game note). Crafted-capacity impact stays source-open.
- **Disputed Desecrated edge correctly deferred (the right conservative call).** Sources conflict — GGG wiki
  says Desecrated are ineligible but count toward the minimum; Craft of Exile/old-emulator observation says
  eligible. The clean M46-A **rejects any input with a Desecrated modifier or unrevealed placeholder**
  (fail-closed) and keeps `fracturing_revealed_desecrated`/PD-013 open (entry present in
  `mechanics_evidence.yaml`). The "1-of-3 desecrate trick" is therefore not modelled — correctly deferred.
- **Fractured-immutability contract is thorough.** One-bit atomic mutation; unselected mods unchanged;
  and explicit cross-operation invariants: accepted Annulment/Chaos removal pools and Perfect Essence
  feasible-removal continue to exclude the fractured instance, Alchemy stays fail-closed on fractured input,
  ordinary-add/capacity still count it on its side, and no operation may clear the fractured flag without a
  separate gate. Cites the 0.2.0e Divine-on-fractured bug-fix as support for numeric immutability. M46-A will
  add these as regression proofs — the load-bearing safety.
- **Honest source discipline.** Fresh external pass (0.2.0 notes, PoE2DB, GGG wiki, 0.2.0e fix, PoE1 3.20
  analogue, Craft of Exile, a supporting-only player report); project-model, not server truth; RNG modelled as
  uniform instance selection over the clean pool. No public numbers.
- **Direction sound.** With Omens done, Fracture is the coherent next operation; it reuses accepted state and
  stays a single atomic flag mutation, not new infrastructure.

## Watchpoints (non-blocking, for M46-A)
- **Our pinned accepted base is already fractured**, so it fails the `fractured_modifier_count == 0`
  precondition — M46-A Fracture applies to *other* Rare states in a route (e.g. a freshly-made rare a user
  wants to lock), not the base staff. Worth stating so no one expects to re-fracture the base.
- Selection is uniform over **all** eligible instances (1-of-N, N≥4), not literally "1-of-4" — correct and
  general; keep the min-count precondition and the all-instances pool exact.
- At M46-A, record the Fracture clean-core in `mechanics_evidence.yaml` as project-model/source-open with the
  Desecrated conflict explicitly noted; do not let admission read as PD-013 closure.

## Recommendation
**GO** on the M46 Fracture core mechanics verification. Authorize a later **M46-A** implementing one base
`fracturing_orb` executor for clean Rare quarterstaff states through the resolver/executor registry: uniform
combined-pool instance selection (≥4, no existing fracture, non-Desecrated), one-bit atomic fractured mutation
with rollback, and full fractured-immutability regression across accepted Annulment/Chaos/Perfect
Essence/Alchemy/capacity, plus direct/resolver/M43-A parity. Desecrated/Revealed/Jawbone/PD-013, multi-fracture,
side-directed Fracture, and other item classes stay separate gates.

## Remains proposed / not accepted / gated
- No M46 runtime/admission; `fracturing_orb` stays disputed/candidate. Revealed/unrevealed Desecrated,
  Jawbone/Reveal/PD-013, multiple fracture, side-directed Fracture, non-quarterstaff/unique/corrupted classes,
  planner/optimizer/economics, public numbers, automation — all closed. Crafted-capacity/MML/SOURCE-PROVENANCE/
  PD-013 stay open.
- Acceptance authority remains ChatGPT/Kirill; this verdict is advisory; no agent self-acceptance.

---
- author: `claude`
- document_type: `fracture_core_mechanics_design_verification_audit`
- status: `advisory verdict — GO; clean Fracture = uniform combined-pool 1-of-N (>=4, no existing fracture, non-Desecrated) one-bit atomic + immutability; crafted-can-be-fractured captured; Desecrated/PD-013 deferred`
