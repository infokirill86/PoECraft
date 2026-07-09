# M37-A Chaos-like Remove-then-Add Runtime Audit (Claude)

audit_id: `P2C_M37A_ChaosLike_RemoveThenAdd_Runtime_Audit_Claude_v1`
auditor: `claude`
package: `packages/proposed/P2C_M37A_ChaosLike_RemoveThenAdd_Runtime_Result_Codex_v1/`
observed_repo_head: `0bdc5dba64f9b5c6105eabf18b6e286b7b9aabaf`
observed_active_task_sha: `bde9a1a28565e096dbbdeeceadefe29c22b1c1388e931358fd3258be0ac79a8d`
verdict_style: `GO / GO WITH CHANGES / NO-GO`
authority_note: advisory only. Accepting this **admits base Chaos as executable truth** (a data change) — a conscious ChatGPT/User gate decision, not a rubber stamp.

---

## Plain-language summary
This is the real Chaos runtime — the first operation that both **removes and adds** in one shot, and the
second new currency after Annulment. It's built correctly on our verified rules: it removes a mod uniformly,
rebuilds the add pool from the new item, adds by weight, is all-or-nothing (if it can't add, it doesn't leave
you with just a removal), never touches the fractured mod, and its outcome odds sum to 1. All 12 tests pass
and nothing else broke (132). **One thing you must decide consciously:** accepting this doesn't just add code
— it marks base Chaos as "runnable" in the data (only base Chaos; the Greater/Perfect versions stay locked).
It's correctly presented as *proposed*, not self-accepted. **Verdict: GO WITH CHANGES** — the work is right;
the change to confirm is "base Chaos is now executable," plus the checksum drifted again (I regenerated it).

## Verdict
**GO WITH CHANGES.** The runtime is correct, in-scope, and verified. Required: (1) the gate must consciously
accept the truth change (base `chaos` → `accepted_executable_runtime`); (2) manifest regenerated (recurring).

## Verified by execution
- **12/12 M37-A tests pass:** contract pinned; base-Chaos exact mass + **combined add weights**; **uniform
  removal** over eligible non-fractured instances; no-removable → no-transition/no-consumption; **fractured
  never removed (exact + MC)** with a leak negative-control; **add pool rebuilt from the branch-specific
  post-removal state**; empty post-removal add pool → **does not commit a partial remove** (atomic); duplicate
  terminal aggregation; deterministic replay; **fail-closed on non-admitted operations and variants**;
  numeric-free public summary.
- **Regression: 132 passed** (suite excl. the heavy M34-B1 file). Accepted modules unchanged:
  `ordinary_add.py` / `annulment.py` / `heterogeneous_chain.py` have **0 deletions**.
- **Reuses accepted kernels.** `chaos_like.py` composes `build_removal_pool` + `build_ordinary_add_pool` +
  the accepted `_remove_modifier_instance` / `_append_ordinary_modifier` / fractured assertions — no
  reimplemented mechanics. Exact path mass = removal(uniform) × add(weighted) as `Fraction`; no-transition
  handled; atomic.
- **Matches the accepted M37 mechanics policy:** removal uniform-combined, add combined-`generation_weight`,
  Whittling/side/desecrated Omens NOT in base Chaos (variants fail-closed).
- **Validators pass;** semantic fingerprint changed (chaos now on the runtime-admitted surface) — intentional,
  with fingerprint tests re-pinned; `validate_foundation` PASS implies chaos has its required handler
  declaration.

## The truth change to confirm (flag)
M37-A flips base `chaos` in `data/operations.yaml` from `admission_candidate` → `accepted_executable_runtime`
(Greater/Perfect chaos stay `admission_candidate`; variants fail-closed). This is the actual **admission of a
new executable operation into accepted data**, and it moves the semantic fingerprint. It is correctly
**proposed, not self-accepted** — the ledger carries no M37-A runtime acceptance row. Accepting M37-A means
the gate consciously accepts "base Chaos is now executable project-model runtime" (not server truth;
SOURCE/PROVENANCE/MML/PD-013 stay open). Please gate it as such.

## Recurring integrity
Root `SHA256SUMS.txt` FAILed again at the delivered HEAD (builder clone still lacks
`git config core.hooksPath tools/hooks`). Regenerated here via `tools/update_sha256sums.py`. Builder-clone
hook activation remains the outstanding process fix.

## Recommendation
Accept M37-A base Chaos runtime and the base-`chaos` executable admission, as a conscious project-model gate
decision, with the manifest regenerated. Greater/Perfect Chaos (MML), Whittling, side/desecrated Omens, and
all other operations remain separate gates. Nothing self-accepts.

---
- author: `claude`
- document_type: `operation_runtime_implementation_audit`
- status: `advisory verdict — GO WITH CHANGES; base-Chaos executable admission is a conscious gate decision`
