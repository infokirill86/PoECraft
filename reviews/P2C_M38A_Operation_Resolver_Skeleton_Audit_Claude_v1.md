# M38-A Operation-Resolver Skeleton Audit (Claude)

audit_id: `P2C_M38A_Operation_Resolver_Skeleton_Audit_Claude_v1`
auditor: `claude`
package: `packages/proposed/P2C_M38A_Operation_Resolver_Skeleton_Result_Codex_v1/`
observed_repo_head: `0cb6b6e315d5b66719d5fd57940bfb8fa9c19486`
observed_active_task_sha: `1068c0f724bab8c94b6f58df8d56eef1adc2bb0e56ae65a7b87219ecec0a5249`
verdict_style: `GO / GO WITH CHANGES / NO-GO`
authority_note: advisory only. Acceptance stays with ChatGPT/Kirill.

---

## Plain-language summary
This is the small "resolver" skeleton — the piece that, for one currency request, decides *is it allowed* and
*which accepted action does it run*. It only routes to the three things we already accept (add, annul, base
Chaos), and it refuses everything else — Greater/Perfect, Whittling, Omens, side-locks — cleanly. It does not
choose strategies for you (not a planner), adds no new mechanics, and touches no data. All 8 resolver tests
pass and nothing else broke (140). **Verdict: GO.**

## Verified (by execution + code)
- **Additive / in scope:** new `src/p2c_engine/operations/resolver.py` (+`__init__.py`); accepted operation
  modules (`ordinary_add`, `annulment`, `chaos_like`, `heterogeneous_chain`) have **0 deletions**; no `data`
  change. 8/8 resolver tests pass; regression **140 passed**.
- **Single-operation seam, not a planner:** resolver docstring states it "is intentionally not a route
  planner. It compiles one currency…"; no sequence/route logic.
- **Dispatches only accepted runtime:** `ordinary_add`, base `annulment`, base `chaos` (remove_then_add).
- **Keys off `runtime_admission_status`, never the active flag:** admits only rows with
  `accepted_executable_runtime`; a non-admitted currency raises `M38AResolverAdmissionError`.
- **Variant/modifier layers fail closed:** side/whittling/Greater/Perfect/Omen/desecrated inputs default to
  none and "every non-base/non-empty value fails closed in M38-A."
- **No boundary breach:** no new operation/variant/modifier/chain runtime, no optimizer/economics/advice, no
  public numbers, no SOURCE/PROVENANCE/MML/PD-013 closure. Ledger has **no M38-A acceptance row** (no self-accept).

## Note
Root `SHA256SUMS.txt` drifted again (builder clone hook still inactive); regenerated here.

## Recommendation
Accept the M38-A resolver skeleton. It is a correct, fail-closed, single-operation admission/compilation seam
over the already-accepted operations. Greater/Perfect, Whittling, Omen, and side/desecrated modifier runtime
remain separate gates; the resolver must stay single-operation (never a route planner). Nothing self-accepts.

---
- author: `claude`
- document_type: `operation_resolver_skeleton_audit`
- status: `advisory verdict — GO; variant/modifier runtime remains gated`
