# M38 Operation-Resolver / Variant-Modifier Design Audit (Claude)

audit_id: `P2C_M38_Operation_Resolver_Variant_Modifier_Design_Audit_Claude_v1`
auditor: `claude`
package: `packages/proposed/P2C_M38_Operation_Resolver_Variant_Modifier_Design_Codex_v1/`
observed_repo_head: `fc5398853b7d7a1dccbd31a213a7b44c46977ce5`
observed_active_task_sha: `8586bbab7b802367eb90aed8696dd2f05ba14a02a3e19a877782059952add8de`
verdict_style: `GO / GO WITH CHANGES / NO-GO`
authority_note: advisory only. Acceptance stays with ChatGPT/Kirill.

---

## Plain-language summary
Now that we have three operations (add / remove / remove-then-add), the next real problem isn't more math —
it's that "which currency" and "what it actually does" have come apart: Greater/Perfect versions, Omens, and
Whittling all *modify* a base operation without being their own operation. This plan proposes a small
"resolver" that, for one operation request, decides: is it allowed to run, which accepted primitive does it
map to, and which filters (side, lowest-level, MML) apply — and refuses anything not admitted. It deliberately
avoids building a giant abstract system, and it keeps every new runtime (Greater/Perfect, Omens, Whittling) as
separate future gates. It changes no code and no mechanics. **Verdict: GO.**

## Verdict
**GO.** Correct, lean, design-only. It solves a genuine structural need (variant/modifier composition) without
over-abstraction, grounds on the accepted registry, and keeps all runtime admissions gated.

## What was checked
- **Design-only:** no `src`/`tests`/`data` change; only the package + dispatcher.
- **Right problem, right size (participant critique).** Codex weighed the alternatives (implement Greater/
  Perfect directly → hardcodes MML everywhere; admit another op; harden chains again) and chose a resolver
  seam — a small **admission-and-compilation** layer over known primitive shapes (add / remove /
  remove_then_add + filters: MML, side, minimum-modifier-level/Whittling, desecrated). It explicitly warns
  against a generic algebra and says the resolver must "not invent future operations, not normalize every
  mechanic into abstractions now, not decide uncertain source questions."
- **Grounds on the reconciled foundation.** "Resolver must never infer runtime permission from
  `active_in_current_simulation`" — it keys off `runtime_admission_status`. Variant/modifier inventory is
  classified as modeled-but-not-admitted; uses `data/operations.yaml`/`omens.yaml`/`sources.yaml`; no external
  capture; SOURCE/PROVENANCE/MML/PD-013 stay open; conflicts go to Kirill/ChatGPT.
- **Everything runtime stays gated.** M38-A = resolver skeleton + fail-closed checks, **no new runtime
  behavior**; Greater/Perfect, Omen, and Whittling runtime admission remain separate gates.

## Watchpoints (non-blocking, for M38-A)
- **Keep it a single-operation seam, never a planner.** "Resolved operation plan" here = which primitive +
  which filters for **one** operation request, not a multi-step route. It must never drift into route/strategy
  planning — that is the standing optimizer boundary. Reinforce this wording in M38-A.
- **Variant filter shapes may be *designed* but not *admitted*.** M38-A may define the MML/side/whittling/
  desecrated filter interfaces, but must fail closed on them until each is separately gated (design does this).
- **Root `SHA256SUMS.txt` drifted again** (builder clone hook still inactive); regenerated here. The new
  `AGENTS.md` now documents the fix — builder-clone activation is the outstanding step.

## Recommendation
Accept the M38 resolver design. Authorize **M38-A** (resolver skeleton + fail-closed admission checks, no new
runtime) as a separate build, keeping it a single-operation admission/compilation seam. Greater/Perfect, Omen,
and Whittling runtime remain separate gates. Nothing self-accepts.

---
- author: `claude`
- document_type: `operation_resolver_design_audit`
- status: `advisory verdict — GO; M38-A skeleton pending separate gate; all variant runtime gated`
