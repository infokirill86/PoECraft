# M45 Next Project Wave Design (Independent Omen Layer) — Claude Audit

audit_id: `P2C_M45_Next_Project_Wave_Design_Audit_Claude_v1`
auditor: `claude`
package: `packages/proposed/P2C_M45_Next_Project_Wave_Design_Codex_v1/`
observed_repo_head: `0982567d3ff1f6371f32672a7257cc4a459baf21`
observed_active_task_sha: `1859df73f053d93ab427faa05bb1a97675513a270c6842b8e76d3c291690482a`
verdict_style: `GO / GO WITH CHANGES / NO-GO`
authority_note: advisory only. Design/direction; no runtime authorized. Omen effects stay project-model, not server truth. Acceptance is ChatGPT/Kirill.

---

## Plain-language summary
This picks the next wave: **Omens** — the modifiers that steer a currency you already have (e.g. "this Exalted
only adds a suffix", "this Annulment only removes a prefix", "this Chaos removes the lowest mod"). It's the right
next move for our staff, because our base is already fractured, so controlling *which side* gets added or
removed matters more to the route than modelling how to fracture a base (Fracture is sensibly deferred). Ten
Omens are proposed, but they're really just **four kinds of tweak** on operations we already run — add-count,
add-side, remove-side, and a "remove the lowest" selector — so it's a coherent batch, not a sprawling new
system. I checked the mechanics carefully and the tricky part is right: side filters go on the **removal** for
Chaos/Perfect Essence (not on the guaranteed part), and Whittling picks the lowest level then breaks ties the
way we already agreed. **Verdict: GO** on the design, with one thing to decide at build time (below).

## Anchor-by-anchor (Kirill's audit questions)
1. **Omens vs Fracture — right next move?** Yes, and deferring Fracture is sound, not avoidance. The accepted
   base is a *pre-fractured* rare staff (fracture acquisition is out of scope per `project_scope`), so
   side-directed control of the operations we run has real route leverage; Fracture would model a base we
   already assume. ✓
2. **Ten-effect batch coherent, not over-generalized?** Yes. The ten Omens collapse to **four effect
   dimensions** over accepted operations (add-count override, add-side filter, removal-side filter,
   removal-selection policy). Same-dimension effects are mutually exclusive; different dimensions compose only
   through a **pinned, validated compatibility matrix**, one operation invocation, fail-closed — explicitly not
   a meta-crafting algebra. Coherent and bounded. ✓
3. **Filter/application stages correct?** Verified against accepted mechanics — all five are right:
   - Exalted add-side → the legal weighted **add** pool (M40-A/ordinary_add). ✓
   - Annulment removal-side → the accepted fractured-protected **removable** pool (M35-A). ✓
   - Chaos (Erasure) removal-side → the **removal** pool, **add stage unchanged** (M37-A). ✓ (the key correct call)
   - Whittling → eligibility/fractured exclusion → minimum modifier-level → **uniform project-policy tie-break**
     (matches the accepted M37 mechanics). ✓
   - Perfect Essence (Crystallisation) side-filter → the accepted **terminal-feasible removal** pool, **not the
     guaranteed add** (M42-A). ✓ (correctly understood)
4. **Reuse + fail-closed?** Yes. No Omen reimplements legality/capacity/family-group/index/weighting/canonical
   state/exact-mass/replay; all filter accepted canonical pools. Unknown/non-admitted/incompatible/duplicate/
   unsupported combinations fail closed. ✓
5. **Grounding in data + source?** Byte-checked: all ten clean-core Omens exist in `data/omens.yaml`; source
   wording (side filters, Whittling lowest-level, Crystallisation prefix/suffix) is strong enough for a later
   project-model gate, with tie behaviour kept source-open. ✓
6. **Exclusions still closed?** Yes. Historical/drop-disabled **Alchemy/Coronation/Greater Annulment** Omens are
   **absent** from `omens.yaml` (confirmed) and correctly held for a version-policy gate; Greater Annulment's
   two-removal contract, `light`/Desecrated, Jawbone/Reveal/PD-013, Fracture, Essence repeat/capacity,
   longer/unbounded routes, planner/optimizer/economics/public numbers — all excluded. Project-model vs
   server-truth is cleanly separated throughout. ✓

## Strongest finding I want to reinforce (make it mandatory, not optional)
`data/omens.yaml` currently has **no runtime-admission/availability field** (verified — only `schema_version`,
`omens`, `compatibility`, `solver_representation`), yet `project_scope` has `active_omen_system: true`. The
design's rule that **catalogue presence and scope-activity are never execution authority** is exactly right and
is the load-bearing safety of this wave — M45-A **must** add explicit Omen `runtime_admission_status` +
availability/version status (the same discipline as operation admission). Treat this as a hard M45-A deliverable.

## Recommendation on Greater Exaltation (the one thing to decide)
Nine of the ten Omens are **pure filters/selectors over already-accepted pools** — trivially safe, reuse-only.
**Greater Exaltation is the exception**: it's the only one that changes execution (adds *two* modifiers), so it
carries a project-model **sequential-draw + atomic-rollback + no-partial** contract that isn't in the accepted
kernels yet (analogous to Alchemy's 4-add and Perfect Essence's removal model). My recommendation: **default to
splitting it** — ship the nine filter/selector Omens as the clean M45-A batch, and take Greater Exaltation as a
small separate ratification (its two-add contract explicitly gated, like we did for Alchemy sampling). If the
gate prefers one batch, it must **explicitly ratify** the Greater Exaltation contract; do not let it ride in on
the filter Omens' safety. The design already offers this split as a fallback — I'd make it the primary path.
This is a `GO` with a build-shape recommendation, not a blocker.

## Verdict
**GO** on the M45 independent-Omen-layer design and direction. Authorize a later **M45-A** implementing the
side-filter/selector Omens over accepted operations through the resolver seam, with a mandatory Omen
admission/availability registry, per-family pool-stage proofs, direct/resolver/M43-A one-step parity, and
fail-closed compatibility — Greater Exaltation split out or its two-add contract explicitly ratified. Nothing
self-accepts.

## Remains proposed / not accepted / gated
- No M45 runtime/admission; no Omen executes. Historical/drop-disabled Omens, Greater Annulment two-removal,
  `light`/Desecrated, Jawbone/Reveal/PD-013, Fracture, Essence repeat/capacity, longer/unbounded routes,
  planner/optimizer/economics/advice, public numbers, automation — all closed. MML/SOURCE-PROVENANCE/
  crafted-capacity/PD-013 stay open.
- Acceptance authority remains ChatGPT/Kirill; this verdict is advisory; no agent self-acceptance.

---
- author: `claude`
- document_type: `omen_layer_design_direction_audit`
- status: `advisory verdict — GO; 10 Omens = 4 filter/selector dimensions over accepted ops, stages mechanically correct; Omen admission registry mandatory; recommend splitting Greater Exaltation`
