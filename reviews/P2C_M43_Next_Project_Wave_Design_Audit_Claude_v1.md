# M43 Next Project Wave Design Audit (Claude)

audit_id: `P2C_M43_Next_Project_Wave_Design_Audit_Claude_v1`
auditor: `claude`
package: `packages/proposed/P2C_M43_Next_Project_Wave_Design_Codex_v1/`
observed_repo_head: `6f9f97f9804db4900fedf76cb07e883bc41ab53c`
observed_active_task_sha: `40acc3c03f4e2b5fcc81d29b288a384f9cbf71d5395d5f85e26b3ba1bd78c31f`
verdict_style: `GO / GO WITH CHANGES / NO-GO`
authority_note: advisory only. Design/selection; the direction choice (sequences vs Alchemy) is genuinely Kirill's/ChatGPT's to make.

---

## Plain-language summary
This picks the next wave — and it's a genuine turn in the road, so I want it in front of you clearly. Instead of
adding another currency, it proposes the ability to **run a user-written sequence of the currencies we already
have** (1–8 steps): apply step 1, then rebuild the item state and apply step 2 on the real result, and so on.
That is the bridge from "a box of separate currency simulators" to "a crafting-route simulator" — which is what
your crafting videos actually are. Importantly, it is **not** the optimizer: it runs the route *you* supply, it
does not search for, rank, or recommend routes, and it has no "repeat until"/"if this then that" logic. The
design is clean and stays firmly on the safe side of that line. **Verdict: GO on the design** — with one thing
that's your call: this **defers Alchemy**, which you'd earlier wanted next.

## The direction decision (yours to make — the main point)
- **What changed:** back at M41 we deferred chains because we had too few operations. After M41-A/M42-A the
  surface is mature, so the design argues composition is now the highest-value move and Alchemy can wait
  (rationale: the primary route starts from a *Rare fractured* base, so Alchemy's Normal→Rare start isn't used
  by that route). That reasoning is sound.
- **The tension:** you told me Alchemy was next (finish the basic currencies), and asked me to hold my Alchemy
  mechanics check as a diligence test. This wave sets that aside. So it's a conscious pivot, not a detail.
- **My participant view:** I lean **for** M43. A bounded route-evaluator is the real product (evaluate a
  crafting plan), it's the natural precursor to the far-future gated optimizer, and it reuses everything we've
  built. If your goal is a route simulator, this is the right next step. If your priority is "cover every basic
  currency first," then Alchemy comes first and M43 waits. Both are legitimate — pick deliberately. (If you go
  M43, my Alchemy diligence-test simply stays on hold.)

## Verified (design quality)
- **Design/selection only.** No `src`/`data`/`config`/`tests` change since M42-A acceptance
  (`ee9ca03..HEAD`); nothing admitted; M42-A acceptance is reused as input, not duplicated.
- **Correctly a bounded evaluator, not a planner (the load-bearing boundary).** Input is a user-supplied fixed
  sequence of accepted operation ids; `stop_on_no_transition` pinned true; explicit exclusions of route
  planner, conditional/policy language, retry loop, ranking/recommendation, economics/EV, admission bypass,
  Omens, new operations, and public numbers (docs 02/05/09). This evaluates the supplied route; it does not
  choose one. The optimizer/advice boundary is respected.
- **Sound architecture (composition, not re-implementation).** Generalizes the accepted **M36-A** chain seam:
  per step, resolve against the *current branch* `ItemState` via `OperationResolver`, dispatch to the accepted
  exact/MC executor, apply that operation's own atomic contract, then rebuild from the new state. No pool or
  resolved-operation reuse across differing branches. Admitted row without a registered accepted executor →
  fail closed. Not globally atomic (each step keeps its own contract) — correct and explicit.
- **Honest exact/scale handling.** Exact enumeration only within pinned path/terminal ceilings; ceiling
  overflow → structured stop with no truncation, renormalization, or hidden MC substitution; MC available
  throughout. Three distinct identities (path / item-state / execution-terminal) with early-failure diagnostics
  preserved. No new game rule, so no new source/mechanics claim — it inherits accepted mechanics.
- **Boundaries + deferrals correct.** Omens, Fracture, Alchemy, Essence replacement/rune capacity,
  Desecrate/Jawbone/Reveal/PD-013, sequences beyond the first bound, and all planner/optimizer/economics stay
  separately gated.

## Watchpoints (for a later M43-A, non-blocking)
- **One-step parity is the safety anchor.** M43-A must prove a one-step sequence is byte-identical to calling
  that operation directly (the design lists this) — that's what guarantees the sequence layer adds no drift.
- **Exact blow-up honesty.** With up to 8 steps over all families the exact tree can explode; the "structured
  stop, no hidden approximation" rule must be enforced and tested, not just stated.
- **Executor-registry completeness.** The admitted-row → accepted-executor mapping must be exact and
  fail-closed, so a future admitted row can't silently run through a generic handler.

## Recommendation
**GO on the M43 design.** Before authorizing M43-A, make the **direction call** explicitly: bounded
sequence-composition now (my lean), or Alchemy first. If M43 proceeds, authorize an M43-A that generalizes the
M36-A seam to 1–8-step user-supplied sequences over accepted executors, with one-step parity, exact-under-
ceilings + MC, replay, early no-transition, and negative controls — and nothing that turns it into a
planner/optimizer. Nothing self-accepts.

## Remains proposed / not accepted / gated
- No M43 runtime; M43-A closed pending the gate. Omens, Fracture, Alchemy, Essence replacement/rune capacity,
  Desecrate/Jawbone/Reveal, longer sequences, conditional/retry/planner/optimizer/economics/advice, public
  numbers, automation — all closed. MML/SOURCE-PROVENANCE/crafted-capacity/PD-013 open.
- Acceptance authority remains ChatGPT/Kirill; this verdict is advisory; no agent self-acceptance.

---
- author: `claude`
- document_type: `next_project_wave_design_audit`
- status: `advisory verdict — GO on design; bounded fixed-sequence evaluator selected (bridge to route simulator, not a planner); direction pivot from Alchemy is Kirill's call`
