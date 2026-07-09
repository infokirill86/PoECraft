# M37 Chaos-like Remove-then-Add Design Audit (Claude)

audit_id: `P2C_M37_ChaosLike_RemoveThenAdd_Design_Audit_Claude_v1`
auditor: `claude`
package: `packages/proposed/P2C_M37_ChaosLike_RemoveThenAdd_Design_Codex_v1/`
audit_type: design/definition audit (no implementation to execute)
observed_repo_head: `86f5410ab9610504666089558147dd1b1e9f861b`
observed_active_task_sha: `5813c0d62b8ae0d592cffdd4261844cd2c1e1c8dbd26a71d2964e99122161610`  (SHA-256 of the exact `work/active/ACTIVE_TASK.md` bytes audited, before this review's dispatcher update)
verdict_style: `GO / GO WITH CHANGES / NO-GO`
authority_note: advisory only. Accepting authorizes the design; M37-A implementation is a separate gate.

---

## Plain-language summary
This is the plan for the next currency: **Chaos-like — remove one mod, then add one mod** (the first
"remove-then-add" operation). The structure is good: it removes on a scratch copy, protects the fractured mod,
rebuilds the add pool from the *new* item, is all-or-nothing, and requires the odds of all outcomes to add up
to 1. It correctly keeps Chaos tagged "candidate, not runnable" and defers the harder Greater/Perfect variants.
**But there's one real mechanics question it side-steps:** *how* does Chaos pick which mod to remove? Our own
notes say Chaos-like removal follows "whittling" (remove the **lowest-level** mod), yet this plan quietly
removes a **random** mod (like Annulment) and just files whittling under "later." Those are different Chaos.
Our source rules say a conflict like this must go to **you** to decide, not be settled silently. **Verdict:
GO WITH CHANGES** — sound plan, but pin the Chaos removal rule (random vs lowest-level) with a user decision
before it's built. (Also: the repo checksum drifted again — I regenerated it; the builder's clone still hasn't
switched the guard on.)

## Verdict
**GO WITH CHANGES.** The remove-then-add design is structurally correct and well-bounded, but it makes a
material, unresolved mechanics choice (uniform Chaos removal) that conflicts with the project's own
`mechanics_evidence.yaml`. That must be resolved by a user decision before M37-A, per `sources.yaml`.

## Design strengths
- **Grounded on the reconciled registry.** Chaos-like rows (`chaos`/`greater_chaos`/`perfect_chaos`) are
  correctly reported as `admission_candidate`, not `accepted_executable_runtime`; the design explicitly does
  not grant runtime admission, and step 1 requires executable-admission before any execution.
- **Primitive vs currency separated.** The `remove_then_add` engine primitive is distinguished from the
  game-facing Chaos-like currency rows (`03`).
- **Correct composite semantics.** Remove one non-fractured installed instance on a branch copy → **rebuild the
  add pool from the post-removal branch state** → add one legal ordinary modifier; **atomic** (precondition
  failure ⇒ no consumption, no mutation); a removal-succeeds-but-empty-add-pool branch yields explicit
  no-transition/no-consumption to the original state (no partial remove-only terminal).
- **Fractured protection** (removal excludes fractured) and **path-vs-canonical-terminal identity** with
  duplicate aggregation.
- **Exact oracle + mass conservation.** Path mass = removal mass × add mass (rationals); terminal marginal by
  canonical state; total committed + no-transition/failure mass **== 1**, missing mass = hard failure; exact
  ceilings pinned; no probability values released.
- **Scope discipline.** Greater/Perfect Chaos (MML) and Omens deferred to separate gates; MML/SOURCE/PROVENANCE/
  PD-013 kept open; no optimizer/economics/public numbers.

## Blocking change — resolve the Chaos removal rule (user decision)
The design defers "Whittling" and, by omission, models base Chaos removal as **uniform over all removable
non-fractured instances** (the Annulment removal pool). But `data/mechanics_evidence.yaml` states whittling —
`official_rule: remove the lowest modifier-level removable modifier` (`PROJECT_ADOPTED_INFERENCE`, tie behavior
unpublished) — and the accepted reconciliation records that whittling **"affects Chaos-like remove filtering."**
So the project's own adopted model applies lowest-modifier-level filtering to Chaos-like removal, which
**contradicts** a uniform-removal base Chaos. This is a source/mechanics conflict, and `sources.yaml`
(`conflict_resolution`: automatic overwrite forbidden; present the conflict to the user; apply only the
user-approved resolution) requires it be **decided by the user before runtime**, not settled by fiat in the
design. Required before M37-A:
- Present the two candidate models explicitly and get a user decision: **(a)** base Chaos removes a *uniformly
  random* non-fractured mod and "Orb of Whittling" is a *separate* lowest-level mechanic (then uniform base
  Chaos is correct); or **(b)** Chaos-like removal *is* lowest-modifier-level (whittling), in which case M37-A
  base Chaos must use whittling removal (lowest level, uniform tie-break), not uniform.
- Whichever is chosen, label it project-model (not server truth) and keep tie behavior/SOURCE-PROVENANCE open.
Until this is pinned, "base Chaos-like" is under-defined and could model an operation that does not match the
project's own evidence.

## Recurring integrity issue (applied + still open on builder side)
Root `SHA256SUMS.txt` FAILed again at the delivered HEAD (4th consecutive floor). I regenerated it via
`tools/update_sha256sums.py` (now PASS). The pre-push hook is accepted and required, but `core.hooksPath` is
evidently still not set in the builder's clone, so its pushes keep drifting. Builder must run the one-time
`git config core.hooksPath tools/hooks`; I have it active in this environment.

## Boundaries (confirmed)
Design-only (no `src/`/`tests/`/`data` change); no operation admitted; no public numbers; no optimizer/
economics/advice; no automation/GitHub Actions; no SOURCE/PROVENANCE, MML, or PD-013 closure. Package
numeric-leak scan PASS; package internal `SHA256SUMS` PASS; ledger carries only the M37 design *authorization*,
no runtime acceptance.

## Recommendation
Accept the M37 design structure, but **do not authorize M37-A** until the Chaos removal-rule decision (uniform
vs whittling/lowest-level) is made by the user and folded into the design. Then M37-A base Chaos runtime can be
built on the M35 admission framework, fail-closed on `runtime_admission_status`, with the M36-A-style exact/MC
+ mass-conservation harness. Greater/Perfect (MML) and Omens/Whittling variants remain later gates. Nothing
self-accepts.

---
- author: `claude`
- document_type: `operation_design_audit`
- status: `advisory verdict — GO WITH CHANGES; resolve Chaos removal rule (user decision) before M37-A`
