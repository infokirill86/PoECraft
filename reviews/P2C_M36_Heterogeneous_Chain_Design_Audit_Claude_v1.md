# M36 Heterogeneous-Chain Design Audit (Claude)

audit_id: `P2C_M36_Heterogeneous_Chain_Design_Audit_Claude_v1`
auditor: `claude`
package: `packages/proposed/P2C_M36_Heterogeneous_Chain_Design_Codex_v1/`
audit_type: design/definition audit (no implementation to execute)
observed_repo_head: `473958483ead92624d2a303266f844dbc978a79a`
observed_active_task_sha: `2623ddf6f0914ab9ca7fba895ac2c6ae03699ac0abdd437e36d3bfdecd1eddf3`  (SHA-256 of the exact `work/active/ACTIVE_TASK.md` bytes audited, at HEAD 4739584, before this review's dispatcher update)
verdict_style: `GO / GO WITH CHANGES / NO-GO`
authority_note: advisory only. Accepting authorizes the design; M36-A implementation is a separate gate.

---

## Plain-language summary
Now that the operation database is reconciled, this is the plan for **chaining two *different* operations**
("add, then annul", etc.) — the real crafting behaviour. The design is solid and, importantly, it plugs
straight into the fix we just did: a chain may only use operations tagged runnable (`accepted_executable_
runtime`), so it can't accidentally pull in Chaos/Essence/etc. It rebuilds the pool from the new item after
each step, keeps everything in exact fractions, protects the fractured mod through the remove step, and
requires all outcomes' odds to add up to exactly 1 (any missing mass = hard fail). **One recurring problem,
not in the design itself:** the repo's integrity checksum file is out of date again — and worse, it dropped
the fix I applied last time. I've re-fixed it and I'm flagging the pattern firmly: this keeps happening, so
the checksum check should become a required pre-push step. **Verdict: GO WITH CHANGES** — the design is right;
the repo integrity needs to stop drifting.

## Verdict
**GO WITH CHANGES.** The heterogeneous-chain design is correct, well-scoped, and correctly grounded on the
reconciled registry. The required correction is repo integrity: root `SHA256SUMS.txt` is inconsistent again
(and a prior fix of mine was reverted). I re-applied the fix in this commit and flag the recurrence.

## Design assessment — strong (GO on substance)
- **Grounds on the reconciled registry (the reconciliation payoff).** A chain step is admitted only if the
  operation is an accepted engine primitive or an `operations.yaml` row with
  `runtime_admission_status: accepted_executable_runtime` (02, 03, 07). `01_PARTICIPANT_CRITIQUE` explicitly
  notes the metadata floor "makes runtime admission explicit, so the chain layer can fail closed instead of
  accidentally pulling in active catalog rows." Exactly the point of the reconciliation.
- **Correct heterogeneous step model (04).** Per step: validate accepted-executable → build pool for the exact
  branch state → enumerate/sample → apply → rebuild pool from `S(i+1)`. Different operations dispatch to their
  own pool builder (ordinary_add → weighted add pool; annulment → removal pool). "No step may use a pool built
  from the root state." Path identity vs canonical terminal identity separated; same-terminal paths aggregate.
- **Correct exact oracle (05).** `path_mass = product of per-step exact masses` (rationals); per-operation mass
  is each operation's real distribution (ordinary_add weighted; annulment uniform over non-fractured
  removables); `terminal_mass(T) = sum over paths to canonical T`; and **total terminal mass + explicit
  failure/no-transition mass must sum to exactly 1, missing mass = hard failure.** This mass-conservation
  invariant is the key correctness property for a mixed chain, and it is specified rigorously.
- **Fractured protection preserved** through the annulment step (remove non-fractured only).
- **Conservative no-transition policy (04):** M36-A default = a no-transition at any step becomes a terminal
  chain failure/no-transition, no later step runs, mass conserved — "must be audited before implementation."
- **Scope discipline:** constructed-fixture label (`PROJECT-MODEL HARDENING FIXTURE`); explicit operation list,
  not a route planner; tractability ceilings (max length 2, max branch/path/terminal counts, stop if exceeded);
  M36-A implementation floor (09) gated separately.
- Design-only: no `src/`/`tests/`/`data` change; package numeric-leak scan PASS; package internal `SHA256SUMS`
  PASS. Boundaries held (no new operation admitted, no public numbers, no optimizer/economics, no automation,
  no SOURCE/PROVENANCE/MML/PD-013 closure).

## Required change — repo integrity (recurring)
`check_sha256sums.py` FAILs at the delivered HEAD. Failing entries:
`data/operations.yaml` (expected `5729ebd…`, got `e0763a9…`), the metadata-floor package `SHA256SUMS.txt`
(expected `eefe2d48…`, got `1dca42b…`), and the M36 package `SHA256SUMS.txt` (expected `d02105db…`, got
`86a987a…`). The first two are the **exact entries I corrected in the previous audit commit (`51179b0`)** — a
later commit reverted that correction, so the stale pre-metadata hashes are back. This is now a **recurring**
integrity-manifest drift across builder/gate commits, not a one-off.
- **Applied here:** I recomputed the mismatched entries so root integrity passes again.
- **Process recommendation (observed-failure-driven, per governance rule 9):** make
  `python tools/check_sha256sums.py SHA256SUMS.txt` a **mandatory pre-push check** (add it to
  `GitHub_Workflow_Protocol.md` required checks, and/or wire the deferred `ACTIVE_TASK`/repo validator to
  include it). Manual root-SHA upkeep has now failed twice and lost a correction; it needs enforcement, not
  more discipline. This is a workflow change — flagged for a gate, not self-adopted here.

## Recommendation
Accept the M36 heterogeneous-chain design (with the root-SHA correction applied) and authorize **M36-A**
implementation as a separate gate — two-step accepted-operation chains (add↔annul), exact-oracle mass
conservation to 1, fractured protection, deterministic replay, negative controls, fail-closed on non-admitted
operations. Adopt the pre-push SHA check before or alongside M36-A so integrity stops drifting. Longer chains
remain a later gate. Nothing self-accepts.

---
- author: `claude`
- document_type: `heterogeneous_chain_design_audit`
- status: `advisory verdict — GO WITH CHANGES (root SHA corrected + enforce SHA check); M36-A implementation pending gate`
