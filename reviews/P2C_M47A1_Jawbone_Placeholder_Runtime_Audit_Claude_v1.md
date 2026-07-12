# P2C M47-A1 Jawbone + Desecrated Placeholder Clean-Core Runtime — Claude Audit

- Verdict: **GO**
- Auditor: Claude (external auditor-designer, advisory only; acceptance remains ChatGPT/User)
- observed_repo_head: `74d9fcb25e213feff706cc97682fbe9e31238c60`
- observed_active_task_sha256 (`work/active/ACTIVE_TASK.md` git-index bytes): `2dfa27af8af5bd9e2a8742a1902468cf175b69b8e6277a2bc6c05eb84d1e4b01`
- Package: `packages/proposed/P2C_M47A1_Jawbone_Placeholder_Runtime_Result_Codex_v1/`

## Scope audited

Runtime admission of exactly three Jawbones — `gnawed_jawbone`, `preserved_jawbone`,
`ancient_jawbone` — that install a **hidden (unrevealed) Desecrated placeholder**.
No Reveal. New `src/p2c_engine/monte_carlo/jawbone.py`; additive registration in
`bounded_sequence.py` and `resolver.py`; the ratified hidden-placeholder Fracture
minimum-count / non-target rule in `fracture.py`; `operations.yaml`,
`mechanics_evidence.yaml` documentary updates.

## Framing check (authorization, not just diff)

- DECISIONS records the User gate that **selected D1-A and D2-A** as project-base
  policies and authorized M47-A1 for exactly the three named Jawbones. The
  implementation is inside its authorization, not ahead of it.
- The hidden-placeholder Fracture interaction (`fracture.py`) is exactly the change
  the same gate authorized: "the hidden placeholder counts toward Fracture's minimum
  installed count but is not targetable." It is not an unauthorized reopening of
  accepted M46-A.

## Verified by reconstruction / execution

1. **Admission is exactly three rows.** Only `gnawed_jawbone`, `preserved_jawbone`,
   `ancient_jawbone` are `accepted_executable_runtime`; `reveal_desecrated` stays
   `blocked_or_out_of_scope`. `reveal_runtime_admitted: false`, `d3_d5_closed: false`.
2. **D1 (free capacity)** matches the decided policy: one free side → install there,
   no removal; both free → uniform prefix/suffix (weight 1 each); a full side is never
   chosen while the other has capacity.
3. **D2 (full-item replacement)** matches: uniform over all removable **non-fractured**
   installed instances; placeholder inherits the removed instance's side; one atomic
   transition.
4. **Single-Desecrated limit** enforced: `_precondition_failure` returns
   `desecrated_limit_reached` if an unrevealed placeholder already exists or any
   installed modifier is desecrated. No rune bypass.
5. **Fractured immutability** enforced twice: fractured instances are excluded from the
   D2 replacement pool, and `_apply_candidate` raises `M47A1JawboneInvariantViolation`
   if a fractured candidate is ever selected (defense in depth).
6. **No Reveal happens.** The placeholder is created unrevealed; `reveal_mml` /
   `lich_tag_constraint` are merely stored on the placeholder for the future (still
   closed) D4 Reveal. Nothing is generated or revealed now.
7. **Fracture interaction** is the authorized rule: the unrevealed placeholder adds to
   `installed_count` (satisfies the ≥4 minimum) but the Fracture target pool still
   iterates only `state.modifiers`, so the placeholder is never a Fracture target.
8. **Atomic / fail-closed.** Empty pool → `no_transition_no_consumption`; exact
   enumeration sums branch mass to 1; sample and exact paths share one apply/assert.
9. **Additive-only integration.** `bounded_sequence.py` / `resolver.py` register the
   Jawbone executor mirroring the Fracture pattern; no accepted executor path is
   altered or removed. Direct / resolver / M43-A parity preserved.

## Checks run

- `validate_active_task.py`: PASS. `check_sha256sums.py`: PASS.
- `validate_foundation.py`: PASS; semantic fingerprint recomputes cleanly with Jawbone
  in scope (`6e7bc414…`).
- `test_m47a1_jawbone_placeholder_runtime.py`: 9 passed.
- Numeric/public-release leak guard: 9 passed (no numeric probability output).
- Full suite: 289 passed. The 35 reported "errors" were **environmental only** — a
  locked Windows pytest temp dir (`PermissionError WinError 5` at `tmp_path` fixture
  setup, before any assertion); rerun with a fresh basetemp: 30/30 pass, including
  `test_admitted_jawbone_prevalidate_change_…` and `…_side_policy_change_…`, which
  confirm the Jawbone admission and side policy are fingerprint-sensitive.

## Remains proposed / not accepted / gated

- M47-A1 is **proposed**, not accepted. Acceptance is ChatGPT/User.
- Still closed: Reveal and D3–D5 (esp. D4 Reveal offer-sampling), Echoes, Omen of
  Light, named-Lich/Necromancy Omens, Putrefaction, revealed-Desecrated Fracture
  runtime, multiple placeholders, PD-013 closure, planner/optimizer/economics/advice,
  public numeric release, source/provenance/MML closure, automation.

## Findings

None blocking. GO.
