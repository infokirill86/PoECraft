# M39 Greater/Perfect + MML Design-Verification Audit (Claude)

audit_id: `P2C_M39_GreaterPerfect_MML_Design_Verification_Audit_Claude_v1`
auditor: `claude`
package: `packages/proposed/P2C_M39_GreaterPerfect_MML_Design_Verification_Codex_v1/`
observed_repo_head: `b948dcbbb0e21b604291a18fdd08a55933e66991`
observed_active_task_sha: `e5923818a40ab8f4c1eb7540b3d25267f651afd6a4c690e67252bbf8f3f1e1a5`
verdict_style: `GO / GO WITH CHANGES / NO-GO`
authority_note: advisory only. MML stays project-model policy, not server truth; acceptance is ChatGPT/Kirill.

---

## Plain-language summary
This checks the Greater/Perfect currencies before we build them. Answer: for the normal families they're the
**same action plus a "minimum modifier level" filter** — Greater/Perfect just narrow which mods can be added
(higher-level only). For Greater/Perfect Chaos, the removal stays base Chaos and the filter applies to the mod
it adds afterward. The plan is to build **one shared MML filter** (through the resolver) instead of coding 24
currencies by hand, and to turn them on in small slices — Exalted and Chaos first, since their base actions
already exist. It correctly flags that **Essences are not just MML** (they force a specific crafted mod) and
need their own gate. Nothing is built or turned on, and MML stays "our model," not confirmed game truth.
**Verdict: GO.**

## Verified
- **Design + source-verification only:** no `src`/`tests`/`data` change; admits nothing; does not close MML,
  SOURCE/PROVENANCE, or PD-013.
- **Matches the accepted mechanics posture:** MML = an add-pool filter (candidates restricted by
  `modifier_level` threshold); labeled `USER_APPROVED_PROJECT_RULE`, server-unconfirmed → stays project-model.
- **Right architecture (composition, not hardcoding):** one shared fail-closed MML filter layer via the M38-A
  resolver, not one function per Greater/Perfect row. Matches the resolver seam.
- **Correct scoping:** 24 Greater/Perfect rows inventoried; ~10 are MML add / remove-then-add variants;
  **Essences excluded** (guaranteed-crafted / Perfect-Essence remove-plus-install → separate operation gate).
  Recommends admitting only Greater/Perfect Exalted + Chaos first (base primitives already accepted).
  Whittling/Omen deferred (removal-selection change + unresolved tie behavior — harder).
- **Everything gated:** no Greater/Perfect runtime, no Whittling/Omen, no new operation, no public numbers, no
  optimizer/economics, no automation, no boundary closure. Grounded on `operations.yaml` + `mechanics_evidence`.

## Watchpoints (non-blocking, for M39-A)
- Keep MML source-open (server-unconfirmed); do not let admission read as MML closure.
- Admit in controlled slices (Exalted/Chaos first), not all 24 rows at once; Essences via a separate operation
  gate, not the MML layer.
- Root `SHA256SUMS.txt` drifted again (builder clone hook inactive); regenerated here.

## Recommendation
Accept the M39 verification/design. Authorize an **M39-A** that adds only a fail-closed MML filter interface to
the resolver (no runtime admission), then admit Greater/Perfect Exalted + Chaos in a later separate slice.
Essences, Whittling/Omens, and other variants remain separate gates. Nothing self-accepts.

---
- author: `claude`
- document_type: `variant_layer_design_verification_audit`
- status: `advisory verdict — GO; MML stays project-model, Greater/Perfect runtime gated in slices`
