# P2C — Independent Project Architecture & Reality Audit (Claude)

- Auditor: Claude, acting as project architect and co-author (independent reconstruction from repo; no other model's audit was read).
- observed_repo_head: `1ffa193babda26e0467f59e1c9af07392085695f`
- ACTIVE_TASK.md SHA-256 (git-index bytes examined): `a58c2f469349cb48fad0fe1c6590789b3c5f9423f10a5272a26a78539125c8bf`
- Scope: whole-project reality/architecture audit. Implements nothing, changes no accepted ledger, accepts/closes no gate.

---

## 1. Executive summary for Kirill (plain language)

**The project is on the right track and the foundation is real, not faked.** We genuinely have a working crafting engine: 35 executable currency operations, an omen layer, fracture, the jawbone placeholder, and the ability to run a fixed 1–8 step recipe with both exact math and Monte-Carlo on one shared kernel — 329 automated tests pass. This is a real simulator core, not a demo.

**What's still only on paper:** Reveal (opening a desecrated mod), Astrid (+1 crafted slot), the branching "if-good-stop-else-continue" evaluator, and the optimizer/economics layers. Those are correctly *not* pretended to work.

**The one genuinely hard truth we confirmed:** the Desecrated modifiers have no real weight data — in the repo they are all "1". So the exact probability of a Reveal cannot be computed from data. This is not a bug in our work; the data doesn't exist. Our conversation's plan (treat the desecrated slot as a *guaranteed target* with a symbolic attempt-cost, and let the market/economics bound it) is the correct way around this, and it means Reveal is **not** a blocker for building the optimizer.

**My main criticism is not technical, it's about pace and shape of work:** we have spent ~54 proposed packages and ~56 reviews to reach 35 operations. The engineering is clean, but the milestones are cut very small and a large share of effort went into scaffolding (checksums, validators, evidence tooling, repo-structure cleanups). That was each individually justified, but cumulatively it's process-heavy. The next wave should be **broad and product-facing**: the branching evaluator plus a success classifier — the last big pieces before an optimizer.

---

## 2. Current reality — technical current-state map

Source tree: `src/p2c_engine` (75 py files) across `domain`, `legality`, `operations`, `sampling`, `canonical`, `decisions`, `trace`, `static_data`, `monte_carlo`. (`src/p2c_core` exists but is empty — vestigial.)

Layered architecture actually present:

1. **Static game data** (`data/`): `mods_ordinary_quarterstaff.yaml` (158 mods, **real differentiated generation_weights** 25–200, 70 prefix / 88 suffix, with family_id, group_ids, modifier_level, tier), `mods_desecrated_quarterstaff.yaml` (16 mods), `family_registry.yaml`, `essence_outputs.yaml`, `operations.yaml`, `omens.yaml`, `sources.yaml`, `reveal_sampling_contract.yaml`. Static modifier index = 188.
2. **Domain item-state model** (`domain/item_state.py`): `ItemState(rarity, modifiers[], unrevealed_desecrated, augment_socket_capacity/used, astrid_installed)`; `ModifierInstance(mod_id, crafted, desecrated, fractured)`; `DesecratedPlaceholder`. Canonical `state_hash`.
3. **Engine primitives** (`monte_carlo/`): `ordinary_add`, `annulment` (remove), `chaos_like` (remove-then-add), `rarity_progression` (transmutation/augmentation/regal/exalted transitions + add), `greater_essence` / `perfect_essence` (guaranteed add), `alchemy` (4× sequential add), `fracture` (flag mutation), `jawbone` (placeholder insertion), `greater_exaltation` (omen 2× add).
4. **Currency/variant composition**: MML filter layer + `OperationResolver` compose Greater/Perfect variants over the base kernels rather than duplicating logic.
5. **Omen modifier layer**: 10 accepted omens compiled over canonical pools; fail-closed on unsupported combinations.
6. **Sequence evaluator**: `bounded_sequence.py` (M43-A) evaluates a caller-supplied fixed 1–8 step route with exact rational mass + seeded MC + replay + parity. (`heterogeneous_chain.py` (M36-A) is the older fixed-2-step chain, now superseded in capability but retained and still exporting shared constants used by `chaos_like.py`.)
7. **Evidence/verification tooling**: `tools/analyze_reveal_observations.py` + schema (M47-A2V), foundation/fingerprint/SHA validators, dispatcher validator.

Dual-engine design is genuine: exact `Fraction` oracle enumerates branches to mass 1; seeded MC validated against it; both run the same kernel.

## 3. Executable capability map

**Genuinely executable today** (test-verified, 329 tests): all 35 accepted operations; the 10-omen layer incl. atomic Greater Exaltation; base `fracturing_orb`; the three jawbones creating a hidden placeholder (D1/D2, no reveal); linear 1–8 step sequences (exact + MC + replay + one-step direct parity); foundation fingerprint + repo-integrity tooling; the Reveal-observation analyzer (report-only, quarantined).

**Not executable (correctly):** `reveal_desecrated` (blocked); `install_astrid` (admission_candidate); branching/conditional routes; any route generation/search/ranking/optimizer/economics; public numeric output.

## 4. Operation / currency classification matrix

Engine primitives (executors): `ordinary_add`, `annulment`, `chaos_like`, `rarity_progression`(→catalog_single_add/rarity), `greater_essence`, `perfect_essence`, `alchemy`, `fracture`, `jawbone`. Every accepted operation resolves to one of these (fail-closed on admitted-without-executor; test-verified).

| Operation(s) | Class | Runtime status |
|---|---|---|
| `transmutation`, `augmentation`, `regal` (+ greater/perfect each) | currency mapping over rarity-transition + add primitive (MML variant) | accepted (9) |
| `exalted`, `greater_exalted`, `perfect_exalted` | currency mapping over add primitive (MML variant) | accepted (3) |
| `annulment` | engine primitive (remove) | accepted (1) |
| `chaos`, `greater_chaos`, `perfect_chaos` | currency mapping over remove-then-add primitive | accepted (3) |
| `alchemy` | currency mapping (4× sequential add) | accepted (1) |
| `fracturing_orb` | engine primitive (flag mutation) | accepted (1) |
| 8× `greater_essence_*` | currency mapping over guaranteed-add primitive | accepted (8) |
| 6× `perfect_essence_*` | currency mapping over guaranteed-add primitive | accepted (6) |
| 3× `*_jawbone` | engine primitive (placeholder insertion) | accepted (3) |
| `reveal_desecrated` | proposed candidate; blocked by unresolved D3–D5 sampling | blocked_or_out_of_scope |
| `install_astrid` | proposed candidate; needs capacity/persistence mechanics verification | admission_candidate |
| 10 omens (Exaltation/Annulment/Erasure/Whittling/Crystallisation ± side) | modifier layer over canonical pools | accepted_executable_modifier |
| 7 omens (Light, 2× Necromancy, 3× Lich, Abyssal Echoes) | data/reference only; blocked by mechanics/source | blocked_or_out_of_scope |

No obsolete/duplicate *operations* in the data. Code-level: `heterogeneous_chain` is a redundant-capability module (superseded by `bounded_sequence`) worth consolidating.

## 5. Source & evidence foundation

`sources.yaml` (checked 2026-06-25) defines a clear hierarchy: **poe2db** (quarterstaves/currency/desecrated — primary), **craft_of_exile** (independent pool/weights, *notes weights are extrapolated*), **repoe_poe2** (structural IDs only — explicitly not the weight source), plus official patches and user/in-game verification. `mechanics_evidence.yaml` records each mechanic's status and `server_truth_claimed: false` throughout. Doctrine — trusted-site data as project-model truth, not server truth — is applied consistently. This foundation is honest and above the norm.

**Discrepancy / evidence register:**

| # | Finding | Severity | Evidence | Recommended handling (not resolved here) |
|---|---|---|---|---|
| D1 | **Desecrated weights are effectively flat** (15× `1`, 1× `2`) → Reveal probability/EV cannot be computed from data | High (foundational) | `mods_desecrated_quarterstaff.yaml` | Adopt the guaranteed-acquire abstraction + symbolic attempt-cost; Reveal RNG becomes optional, not a blocker. User/GPT gate. |
| D2 | `reveal_sampling_contract.yaml` says `status: PROJECT_VERIFIED` and `weight: generation_weight` (PPSWOR), implying a real weighted sampler, while D3–D5 are explicitly unaccepted and `reveal_desecrated` is blocked; and its weight basis is the flat "1"s of D1 | Medium (misleading certainty) | contract file vs `mechanics_evidence.yaml` (`d3_d5_closed: false`), dispatcher | Re-label to a proposed/candidate status; note the sampler reduces to uniform under current weights. Do not silently resolve. |
| D3 | `project_scope.yaml` lists `reveal` and (via Astrid) prepared groups as *active*, while runtime blocks them | Low (readability trap) | `project_scope.yaml` vs `operations.yaml` | Consistent with the documented scope≠runtime rule, but a first-time reader can misread "active scope" as "executable." A one-line note would remove the trap. |
| D4 | Item-state carries `astrid_installed` / `augment_socket_*` while `install_astrid` is not accepted | Low (state ahead of runtime) | `item_state.py` vs `operations.yaml` | Acceptable (prepared state), flag so it isn't mistaken for live capacity. |
| D5 | Even accepted **ordinary** weights are Craft-of-Exile *extrapolations*, not server truth | Low (documented) | `sources.yaml` note | Already disclosed; keep the project-model framing. |

Places needing **in-game/user verification**: whether Reveal offers are truly uniform vs low-tier-weighted (D1 — the M47-A2V tool is built to test this); Ancient-MML persistence through Echoes; Astrid replacement/persistence and its effect on Essence preconditions.

## 6. Architecture & project-direction critique

**Strengths (real):** primitives are cleanly separated from currency variants — Greater/Perfect compose through an MML filter + resolver over shared add/remove/rarity kernels, so there is **no duplicated operation logic**. Fail-closed admission (catalogue presence ≠ execution authority) is enforced and test-covered. The exact-oracle + seeded-MC dual engine on one kernel is the correct and distinctive backbone for a future *trustworthy* optimizer.

**Where I push back:**
- **Milestone boundaries are cut too small.** ~54 proposed packages / ~56 reviews for 35 operations. The M47 line alone (M47 → M47-A1 → M47-A2 → M47-A2V) is four waves to reach "placeholder created, reveal still not built." Each was auditable, but the cadence is process-dominant.
- **Drift into scaffolding/evidence work.** A substantial fraction of waves were checksum tooling, validators, repo-structure cleanups, and evidence tooling. Valuable, but the balance tilted away from product capability.
- **Redundant capability retained.** `heterogeneous_chain` (M36-A) is functionally inside `bounded_sequence` (M43-A); it lingers and leaks shared constants into `chaos_like`. Empty `p2c_core` dir. Minor, but they are the kind of residue small waves leave.
- **Missing foundational capability (the real gap):** a **branching** evaluator and an executable **success classifier** (the criteria data exists in `success_criteria.yaml`, but nothing interprets it yet). These are prerequisites for any optimizer and are the highest-value missing pieces.
- **Consistency:** accepted statuses, active flags, and runtime largely reconcile; the exceptions are D2–D4 above.

## 7. Strategic options comparison

| Option | Value now | Dependencies | Verdict |
|---|---|---|---|
| Complete engine primitive layer | Low — primitives already cover the accepted surface | none | Not needed as a wave |
| Map remaining prepared currencies (Astrid, Reveal) | Medium | Astrid=capacity mechanics; Reveal=D1 unknown | Astrid = small separate mechanics wave; Reveal = deferrable (abstraction removes it as blocker) |
| Operation-admission reconciliation | Low | none | Fold the D2–D4 fixes into any wave; not a wave itself |
| **Branching heterogeneous chains + success classifier** | **High** | none beyond accepted surface | **Strongest next wave** |
| Additional source verification | Medium | in-game data | Ongoing via M47-A2V; not a standalone wave |
| Probability/MC hardening | Low | none | Mature already |
| Optimizer/strategy prerequisites | High but premature | needs branching + classifier first | Immediately after the branching wave |

## 8. Recommended roadmap & immediate next wave

**Broad roadmap:** (1) **M48-A branching evaluator + success classifier** (widest safe product wave) → (2) optimizer prerequisites: cost/attempt accounting scaffold with the desecrated **guaranteed-acquire** abstraction + symbolic attempt-cost (design-first) → (3) optimizer/search over the evaluator → (4) economics (market-bounded cost, cheapest-acquisition incl. "buy") — gated last.

**Immediate next wave (recommended): `M48-A Bounded Caller-Authored Branching Sequence Runtime + Accepted Success Classifier`**, batched because all parts share one evaluator contract and are reconstructible/testable/truth-neutral:
1. success classifier interpreting `success_criteria.yaml` → `TOP`/`ACCEPTABLE`/`NOT_SUCCESS`, fail-closed on unsupported shapes;
2. finite acyclic route-DAG schema + validator (unique IDs, complete cases, ≤8 op nodes/path, no cycles/expressions);
3. exact evaluator reusing the M43-A resolver/executor registry with rational mass conservation + honest ceilings;
4. seeded MC + replay through the same executors/predicates;
5. parity + negative controls (one-node = direct op; linear DAG = M43-A; planner/cost/probability fields hard-fail);
6. fold in the D2–D4 documentation fixes; internal-only reporting.

Keep out (genuine gates): route generation/search/ranking, costs/EV/economics/advice, cycles/unbounded retry, public numeric release, and any predicate that returns a score/probability/cost (the evaluator↔optimizer firewall).

## 9. Explicit user decisions / in-game checks required

1. **Desecrated cost model** (design decision): ratify the guaranteed-acquire abstraction + symbolic attempt-cost (`N`/`p`, never silently 0/1); confirm Reveal RNG is deferred, not blocking. (Kirill + GPT gate.)
2. **In-game:** are Reveal offers uniform or low-tier-weighted? (Decides whether attempt-count is combinatorially computable or stays symbolic. M47-A2V tool tests it.)
3. **In-game:** Ancient-MML persistence through Echoes.
4. **Astrid:** replacement/removal persistence and its effect on accepted Essence preconditions, before `install_astrid`.
5. **Governance:** re-label `reveal_sampling_contract.yaml` PROJECT_VERIFIED (D2).

## 10. Governance execution check (Participant Voice Charter)

The existing charter/role rules are **materially sufficient** — I do **not** propose a new charter. Assessment of adherence:

- **Claude (me):** has audited *direction and framing*, not only correctness — e.g. the M48 evaluator-vs-optimizer boundary critique, co-designing the desecrated cost model, and verifying Whittling in-game rather than rubber-stamping. Adequate participation.
- **Codex:** has behaved mostly as an **executor**. I find little evidence of Codex challenging a task boundary *before* building (no builder-authored "this scope is too narrow / wrong" packages). Its packages are clean and self-critical in prose, but pushback is retrospective, not pre-build.
- **ChatGPT:** has been the **dominant planner** — it sizes and sequences every wave. The steady pattern (GPT plans → Codex builds → Claude audits → gate) has reduced Codex, in practice, to execution.
- **Why inconsistent:** the workflow *mechanics* reward it. A thin dispatcher + one small package per wave optimizes for auditable compliance, which structurally nudges toward narrow execution over architectural pushback. The charter says "be a participant," but nothing in the normal loop *requires* the builder to contest scope.
- **Smallest non-bloat fix:** add one required field to every task package and to the dispatcher — a **builder boundary-challenge line**: before building, Codex must state "scope is right" or "scope is too narrow/wrong because …", and Claude's audit must check that field. This makes the participant duty a visible, mandatory part of normal work (one line), without adding a new document or process. Milestone sizing should also default to the **widest safe batch** (as in §8) rather than the smallest auditable step.

---

### Verdict

The project is progressing correctly and its foundation is sound and honest. No accepted-truth or mechanics change is warranted by this audit. The recommended correction is one of **cadence and breadth**, not direction: take a wide, product-facing branching-evaluator + classifier wave next, fold in the small discrepancy fixes (D2–D4), and carry the desecrated guaranteed-acquire cost model to a design gate. Advisory only; ChatGPT/Kirill remain the acceptance gate.
