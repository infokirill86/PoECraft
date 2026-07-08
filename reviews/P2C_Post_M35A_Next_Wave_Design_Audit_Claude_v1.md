# Post-M35A Next-Wave Design Audit (Claude)

audit_id: `P2C_Post_M35A_Next_Wave_Design_Audit_Claude_v1`
auditor: `claude`
package: `packages/proposed/P2C_Post_M35A_Next_Wave_Design_Codex_v1/`
audit_type: strategic + operation/source-foundation reconciliation audit (design-only; nothing to execute)
observed_repo_head: `5a85b8ac9a6d1bbd1cecbde203e967ba76209139`
observed_active_task_sha: `a239e4f051aafc41af9dececd07795c44bb6573d51635c5f1b92d10ef212b2e8`  (SHA-256 of the exact `work/active/ACTIVE_TASK.md` bytes audited, at HEAD 5a85b8a, before this review's dispatcher update)
verdict_style: `GO / GO WITH CHANGES / NO-GO`
authority_note: advisory only. Accepting authorizes only a *direction*; no implementation, no operation
admission, no data change is authorized here.

---

## Plain-language summary
Codex proposes the next step: instead of adding a third currency, first prove the two we already have
(`ordinary_add` and base `annulment`) can be **chained together** ("add then remove", etc.). That instinct is
reasonable and safe. **But it fails the check you specifically asked for:** the proposal never opens the
project's own prepared files — `data/operations.yaml`, `data/sources.yaml`, `data/mechanics_evidence.yaml` —
and so it misses a real trap sitting in the data. Our operation database already lists **37 currencies**, and
**18 of them are flagged "active_in_current_simulation: true"** (Exalted, Chaos, Perfect Essences, Jawbones,
Reveal, Install Astrid, Annulment) — even though **only two are actually executable in the engine**. That
"active" flag does **not** mean "the engine can run it," and nothing in the repo currently makes that
distinction explicit. Building the next wave without reconciling this first is exactly the drift you were
worried about. **Verdict: GO WITH CHANGES** — do the operation/source reconciliation first; the chain design
is fine *after* that, grounded on the real database.

## Verdict
**GO WITH CHANGES.** The heterogeneous-chain direction is a valid *eventual* move and the package is
design-only and boundary-clean, but it **fails the operation/source-foundation audit**: it does not consult
or reconcile against `operations.yaml` / `sources.yaml` / `mechanics_evidence.yaml`, and does not catch the
`active_in_current_simulation` vs accepted-runtime mismatch. Per your rule, that is not a GO. The required
change is to run an **Operation Inventory & Admission Reconciliation** wave first.

## What the proposal gets right
- **Project-model framing (check 1.1):** correctly calls the engine project-model, not server truth, not advice.
- **Accepted runtime stated correctly (check 1.3):** accepted executable runtime = `ordinary_add` + base
  `annulment` only (01 §1; 02 capability map). Matches the ledger.
- **Boundaries (check 5):** design-only; no implementation, new operations, heterogeneous runtime, public
  numbers, optimizer/economics, automation, or SOURCE/PROVENANCE/MML/PD-013 closure.
- **Anti-drift instinct:** it declines to jump to Chaos/Essence/Jawbone/Reveal, and declines to add a third
  operation before composition is proven. Reasonable.

## Where it fails the foundation audit (the blocking findings)
### Finding 1 — Operation database never reconciled (check 2). BLOCKING.
The proposal makes **zero reference** to `data/operations.yaml`. That file already defines **37 operations**
with `active_in_current_simulation` flags. It must be inventoried and each entry classified as
(a) accepted-executable-runtime, (b) data/reference candidate, or (c) blocked/out-of-scope — none of which the
proposal does.

### Finding 2 — `active_in_current_simulation` vs accepted-runtime MISMATCH (check 2). BLOCKING — flagged as required.
`operations.yaml` flags **18** operations `active_in_current_simulation: true` —
`exalted / greater_exalted / perfect_exalted`, `annulment`, `chaos / greater_chaos / perfect_chaos`,
`install_astrid`, `perfect_essence_*` (6), `gnawed/preserved/ancient_jawbone`, `reveal_desecrated` — while
**only `ordinary_add` (engine primitive) and base `annulment` are accepted executable runtime.** So 16 of the
18 "active" operations are **not** executable. `active_in_current_simulation` encodes *project-scope intent*,
not *engine executability*, and nothing in the repo currently makes that distinction explicit (all entries have
no runtime/admission status). This is a real latent trap: a reader could treat `chaos: active=true` as
runtime-ready. **This must be corrected before the next implementation wave** — add an explicit per-operation
runtime/admission status so scope-intent is never conflated with executable status. (Editing `operations.yaml`
is a data change → user-approved per `sources.yaml` policy; it needs its own gate.)

### Finding 3 — Engine primitive vs currency not distinguished (check 1.2). BLOCKING.
The proposal treats `ordinary_add`/`annulment` as "operations" but never separates **engine primitives** from
the **currency catalog**. In `operations.yaml`, currencies (Exalted family, Chaos family, Essences, Jawbones,
Reveal…) are the game-facing items; the engine primitives are the add/remove mechanics beneath them (e.g. the
Exalted family is what performs `ordinary_add` on a rare). Real crafting "chains" are chains of *currencies*;
the next-wave design must state the currency→primitive mapping, or "heterogeneous chain" is under-defined.

### Finding 4 — Source hierarchy never referenced (check 3). BLOCKING.
The proposal makes no reference to `sources.yaml` or `mechanics_evidence.yaml`. The reconciliation/next wave
must respect: the `model_postulate` (PoE2DB + Craft of Exile agreement = **project-model truth, not PoE2 server
truth**; RePoE is structural support only); `conflict_resolution` (automatic overwrite forbidden; conflicts go
to the user; only user-approved resolution applies); `patch_update_policy` (new external data = PROPOSED_CHANGE,
user approval required before any runtime change); and the `mechanics_evidence.yaml` runtime-status labels
(MML `USER_APPROVED_PROJECT_RULE`, whittling `PROJECT_ADOPTED_INFERENCE`, Lich `USER_APPROVED_PROJECT_RULE`,
`fracturing_revealed_desecrated` `DISPUTED_OUT_OF_ACTIVE_SCOPE`). SOURCE/PROVENANCE, MML, PD-013 remain open.

## Strategic direction (check 4)
The proposal's answer — proceed to heterogeneous chains — skips the alternative you named: **operation
inventory/admission reconciliation first.** Given Findings 1–4, reconciliation should come **first** (its own
wave), because chaining and future operations built on a database whose "active" flags don't mean "executable"
is precisely the foundation drift to avoid. This is not infrastructure-for-its-own-sake: it grounds all future
operation work on the existing prepared database instead of re-deriving scope ad hoc.

## Required changes before this direction is accepted
1. **Insert an Operation Inventory & Admission Reconciliation wave** (design/doc; the data edit is a separate
   gated change). Inventory all 37 `operations.yaml` entries; classify each accepted-executable / data-candidate
   / blocked; map engine primitives (`ordinary_add`, remove-one) to the currency catalog.
2. **Flag and resolve the `active_in_current_simulation` mismatch** by adding an explicit per-operation
   runtime/admission status (kept distinct from `active_in_current_simulation`). Data change → user-approved gate.
3. **Fold source-hierarchy awareness in** (sources.yaml model_postulate/conflict_resolution/patch policy +
   mechanics_evidence runtime_status labels); confirm PoE2DB/CoE agreement = project-model truth; keep
   SOURCE/PROVENANCE, MML, PD-013 open.
4. **Distinguish engine primitive vs currency** explicitly in the next-wave design.

## Non-blocking (the chain design itself, once foundation is reconciled)
The proposed chain shape (fixed length 2, optional 3; explicit operation list, not a planner; per-step pool
rebuild from branch-specific state; exact/oracle path products where tractable; seeded MC where bounded;
fail-closed on unaccepted operations) is well-formed and consistent with the accepted M34-B1 pattern. Reuse it
for the chain wave **after** the reconciliation, and only over operations the reconciliation confirms as
accepted-executable.

## Safety boundaries (check 5) — confirmed
Nothing here authorizes implementation, new executable operations, operation expansion, heterogeneous chain
runtime, public numeric release, optimizer/advice/ranking/economics/EV, automation/GitHub Actions, or
SOURCE/PROVENANCE/MML/PD-013 closure. Package is design-only; root/package `SHA256SUMS` PASS; no numeric leak;
ledger untouched (no self-accept).

## Recommendation
Do **not** accept "M36 heterogeneous chains" as the immediate next wave. Instead authorize the **Operation
Inventory & Admission Reconciliation** wave (Findings 1–4), with the `operations.yaml` status correction routed
as its own user-approved data gate. After reconciliation, the heterogeneous-chain design can proceed on the
real, reconciled operation foundation. Nothing self-accepts.

---
- author: `claude`
- document_type: `strategic_and_foundation_reconciliation_audit`
- status: `advisory verdict — GO WITH CHANGES; reconcile the operation/source foundation before the chain wave`
