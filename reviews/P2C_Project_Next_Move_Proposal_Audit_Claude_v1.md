# Project Next-Move Proposal Audit (Claude)

audit_id: `P2C_Project_Next_Move_Proposal_Audit_Claude_v1`
auditor: `claude`
package: `packages/proposed/P2C_Project_Next_Move_Proposal_Codex_v1/`
audit_type: strategic + correctness audit of a project-direction proposal (design-only; nothing to execute)
observed_repo_head: `d8515b644b9d5611520671c93a98c306f3761f3f`
observed_active_task_sha: `500c0d7ab617142a641609420a126694e272f5cc935ddbecde4cd8cc1af87b82`  (SHA-256 of the exact `work/active/ACTIVE_TASK.md` bytes audited, at HEAD d8515b6, before this review's dispatcher update)
verdict_style: `GO / GO WITH CHANGES / NO-GO`
authority_note: advisory only. Accepting this authorizes only the *direction* (a design-only M35 wave);
implementation of any new operation stays a separate ChatGPT/User gate.

---

## Plain-language summary
Codex stepped back and asked the right question: *are we just polishing one operation forever?* And it
answered honestly — **yes, that risk is real, and we should stop.** The simulator today can only do one
currency (`ordinary_add`), plus hardening of it. Codex recommends pivoting to **admitting the first new real
operation**, doing it **design-first** (write the rules for how any new operation gets admitted, plus a
concrete design for **Annulment** — "remove a random modifier"), and keeping the actual code for a later,
separate gate. I checked its facts against the repo and the direction against the product goal. It's accurate,
it respects every standing boundary, it correctly protects the one sacred rule (Annulment must never remove
the fractured mod — and the existing removal code already enforces that), and it behaved as a real project
thinker, not an order-taker. **Verdict: GO** — this is technically clean *and* strategically right.

## Verdict
**GO.** Accept the direction: a **design-only M35 operation-admission framework + Annulment candidate design**,
with all implementation gated separately. Refinements below are for the M35 design wave, non-blocking.

## Strategic assessment (the part that matters most)
- **Drift caught — by Codex itself.** §5–6 state plainly that after M34-B1 "another pure `ordinary_add`
  hardening wave is lower value" and the project should "pivot from more confidence in ordinary add to
  controlled admission of the first additional real operation." This is exactly the infrastructure-loop risk to
  watch, and Codex flagged it unprompted. I independently agree: the MC/exact foundation over `ordinary_add` is
  now well-validated (M31–M34-B1); continuing to harden the same single operation is diminishing-returns
  runway work, not product progress.
- **Direction is right.** Moving toward operation breadth is the actual product path (the goal is a crafting
  simulator, not a one-operation test harness). Doing it **design-first** (an admission contract before any new
  mechanic) matches the standing doctrine "extend the model first; new mechanics are a separate gate," and
  turns future operations into a repeatable gate instead of ad-hoc ones.
- **Annulment is the right first candidate** — verified, not just asserted: it is removal-only and reuses the
  existing `legality/pool_builders.build_removal_pool` (confirmed present), which **already excludes fractured
  modifiers** (`lambda row: not row.instance.fractured`). So it exercises a genuinely new transition (removing
  an installed mod) with minimal new surface and no add/remove composition, crafted-mod, or reveal/Lich/PD-013
  complexity.

## Answers to the 10 audit questions
1. **Describes what the project should become?** Yes, accurately (narrow-first sim → exact+MC → optimizer last;
   "not intended to remain a test harness for one add operation").
2. **Describes what's implemented/accepted?** Yes — matches the ledger exactly (Layer A, ordinary_add runtime,
   shared kernel, MC harness, oracle, M34-A, M34-B1).
3. **What it can/can't do today?** Accurate: can load data, build ordinary_add/removal/reveal pools, run
   ordinary_add exact+MC, two-step sequences, replay; cannot execute any non-add operation, has no general
   operation interface, no heterogeneous plans, no target aggregation, no economics/optimizer.
4. **Catches hardening drift?** Yes, explicitly and correctly (§5–6).
5. **Recommended move right?** Yes — design-only admission framework + Annulment. Better than the alternatives
   it lists (continue hardening = drift; N-step infra = second-best runway; implement-now = too early without a
   contract). I concur.
6. **Project thinker, not executor?** Strongly — reality check, capability maps, options table with value/risk,
   self-caught drift, recommends leaving the comfortable path. Exemplary participant behavior.
7. **Boundary too narrow/broad/correct?** Correct. §06 explicitly is *not* a generic operation engine — just
   admission rules + one candidate. See refinement 1.
8. **Respects standing boundaries?** Yes — design-only; no new mechanics/acceptance; no optimizer/economics/
   advice; no public numbers; no automation; no SOURCE/PROVENANCE/MML/PD-013 closure.
9. **Batched parts reconstructible / auto-testable / truth-neutral?** Yes — the batched set is all design
   (framework, candidate selection, Annulment design contract, audit-package pattern): reconstructible,
   truth-neutral, testable after later implementation.
10. **Gated parts correctly split?** Yes — Annulment implementation/acceptance, Chaos/Perfect Essence/Jawbone/
    Reveal, anything on unresolved source/provenance/MML/PD-013/Lich, public numbers, target success, optimizer,
    automation, and boundary closure all stay gated.

## Consistency checks
`CURRENT_STATUS.md`, `ledger/ACCEPTED_ARTIFACTS.md`, and standing boundaries all match the proposal's claims.
Proposal-only: diff since base is the package + dispatcher only (no src/tests); package + root `SHA256SUMS`
PASS; no numeric leak.

## Refinements for the M35 design wave (non-blocking; fold in when M35 is built)
1. **Keep the admission framework lean and Annulment-anchored.** Do not let "framework" grow into an abstract
   generalized-operation-algebra — that would be a new infrastructure loop in strategy clothing. Codex already
   commits to this (§06 "not a generic operation engine"); reinforce it.
2. **Make the fractured protection a hard tested property, not just prose.** The kernel already excludes
   fractured, but the M35 Annulment design must require a negative-control test proving the removal pool never
   contains the fractured suffix, and that a state with no removable non-fractured mods yields an explicit
   no-transition (not a fabricated removal).
3. **Pin Annulment's exact-oracle shape.** State the selection rule explicitly (uniform over the k removable
   installed instances → exact 1/k each) so the exact/oracle comparison is defined in integer/rational terms,
   as M33/M34 do.
4. **Label the Annulment mechanic as accepted project-model, not server truth.** Its "remove a uniformly random
   non-fractured mod" semantics is a project-model assumption; keep SOURCE/PROVENANCE open and say so.

## Recommendation
Accept the direction and authorize a **design-only M35** (operation-admission framework + Annulment candidate
design), folding in the four refinements. Implementation (M35-A Annulment runtime) remains a separate gate
after the M35 design is audited and authorized. Nothing self-accepts; no new mechanics are opened by this.

---
- author: `claude`
- document_type: `strategic_direction_audit`
- status: `advisory verdict — GO; M35 design authorization and all implementation remain ChatGPT/User gates`
