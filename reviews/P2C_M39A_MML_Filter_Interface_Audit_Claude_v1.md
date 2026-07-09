# M39-A MML Filter Interface Implementation Audit (Claude)

audit_id: `P2C_M39A_MML_Filter_Interface_Audit_Claude_v1`
auditor: `claude`
package: `packages/proposed/P2C_M39A_MML_Filter_Interface_Result_Codex_v1/`
observed_repo_head: `195856327ac57f242e2552125849b2de8423ab54`
observed_active_task_sha: `335f6a30ef29b47f803d5e2b0336a35999a24a6f92bad262ea88518593a27e75`
verdict_style: `GO / GO WITH CHANGES / NO-GO`
authority_note: advisory only. MML stays project-model policy, not server truth; acceptance is ChatGPT/Kirill.

---

## Plain-language summary
This is the first build step after the M39 plan. It adds **one thing**: the resolver can now accept an
optional "minimum modifier level" (MML) number and pass it into the already-accepted add operation. Nothing
new is turned on. Only plain `ordinary_add` (which we already run) can carry the number; if you try to send an
MML to base Chaos, or to any Greater/Perfect currency, the resolver **refuses**. Bad numbers (zero, negative,
non-integer, true/false) are refused too. I re-ran the tests myself and inspected the wiring: the number really
does reach the shared add-pool and narrow it — it is not silently ignored. **Verdict: GO.**

One repo-hygiene note, not about this code: the whole-repo checksum file drifted again on delivery (same
recurring line-ending issue). I regenerated it; it now verifies clean. I also found *why* it keeps coming back
and propose a one-time fix below so we stop chasing it.

## Verified by execution / byte inspection
- **Scope is exactly one interface field.** Diff since accepted M38-A (`be84534..195856`) touches only
  `src/p2c_engine/operations/resolver.py`, its `__init__.py` export, and the resolver test file. No
  `data/operations.yaml` change; no `ordinary_add.py` / `pool_builders.py` change — the MML add-pool behavior
  is pre-existing accepted kernel, only newly *reachable* through the resolver.
- **MML plumbing is real, not cosmetic.** resolver `mml` → `OrdinaryAddOperation(mml=...)`
  (`ordinary_add.py:53`) → `OrdinaryAddPoolRequest.mml` (`pool_builders.py:33`) → `apply_family_mml`
  (`pool_builders.py:154,497`). `apply_family_mml` keeps, per family, rows with `modifier_level >= mml`, else
  falls back to that family's strongest tier. The new test asserts exact narrowed candidate keys
  (`prefix_high_t1` + `suffix_mid_t2`) and the recorded fallback family — a genuine behavioral assertion.
- **Fail-closed everywhere required.** MML only compiles for `currency_id == ordinary_add`; for accepted
  catalog ops (base Chaos, Annulment) an explicit MML raises `M38AResolverAdmissionError`; non-admitted rows
  (e.g. `greater_chaos`) are rejected by `runtime_admission_status` *before* any MML path, with or without an
  MML supplied; variants (`variant_id`) and modifier layers (`active_modifier_ids`) still reject. Invalid MML
  (`0`, negative, non-int, `bool`) rejects. Confirmed in code and by the tests.
- **Tests pass on my clean clone.** `pytest tests/monte_carlo/test_m38a_operation_resolver.py
  tests/legality/test_m5_pool_builders.py` → **22 passed**. Builder also reports full suite 151 passed.
- **Boundaries held.** No Greater/Perfect / Essence / Whittling / Omen / side-desecrated runtime admitted; no
  operation row changed; no MML / SOURCE-PROVENANCE / PD-013 closure; no public numbers; no
  optimizer/economics; no automation. Answers to all 8 audit questions in the request: yes.

## Finding — Repo integrity (MEDIUM, non-blocking; auto-corrected here)
The delivered root `SHA256SUMS.txt` **fails verification on a clean clone**: 3 recorded hashes
(`data/operations.yaml` and the nested `SHA256SUMS.txt` of the M36 design and Metadata-Floor packages) do not
match those files' committed bytes. Content did not change — this is a **line-ending discrepancy**:
`.gitattributes` normalizes committed bytes to LF, but `tools/update_sha256sums.py` hashes the raw *working
tree* (`path.open("rb")`), so when the builder's checkout holds any file with CRLF the manifest records a
CRLF-based hash that no correctly-normalized clone reproduces. Regenerating on my clean (LF) clone corrects
exactly those 3 entries and verification PASSes. I regenerated and committed the corrected manifest.

**Why the existing guard did not catch it:** the accepted fix was a local `pre-push` hook, but Codex works in a
**linked git worktree** where `git config core.hooksPath tools/hooks` is permission-denied (the config lives in
the main worktree). The hook structurally cannot fire in the builder's environment — so discipline/hook is not
a durable fix here.

## Recommendation
Accept M39-A as a fail-closed MML interface floor (project-model only; MML stays open/server-unconfirmed;
Greater/Perfect/Essence/Whittling/Omen runtime remain separate gates).

**Also authorize one tiny structural fix** so the checksum drift stops recurring regardless of who builds or
what their line endings are: make `tools/update_sha256sums.py` hash **git-normalized (index) bytes** for
tracked files (e.g. `git cat-file blob :path` / `git show :path`) instead of raw working-tree bytes; keep
working-tree hashing only for untracked files. This makes the manifest identical on every clone and does not
depend on a hook that cannot run in a linked worktree. (Alternatively, builder runs `git add --renormalize .`
before regenerating — weaker, still discipline-dependent.)

## Remains proposed / not accepted / gated
- Greater/Perfect Exalted & Chaos runtime; Essence; Whittling; Omen; side/desecrated filters — not admitted.
- MML mechanics not closed; SOURCE/PROVENANCE not closed; PD-013 not closed.
- No public numeric release; no optimizer/economics/advice; no automation.
- Acceptance authority remains ChatGPT/Kirill; this verdict is advisory.

---
- author: `claude`
- document_type: `implementation_audit`
- status: `advisory verdict — GO; MML interface floor only; root SHA regenerated; structural tool fix recommended`
