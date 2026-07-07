# Baseline Import Inventory

Package: `P2C_M32_Seeded_MC_Harness_Result_Codex_v1`
Patch purpose: documentation-only correction before Claude audit
Status: proposed; not accepted project truth
Prepared by: Codex

## Boundary statement

This inventory documents which files entered the GitHub repository during the M32 execution pass because the GitHub repository was initially a skeleton.

This file does not claim new project truth. It does not mark any imported runtime, data, config, schema, tool, or generated artifact as accepted baseline. All imported baseline material listed here remains proposed GitHub repository material pending Claude audit and ChatGPT/User acceptance.

No feature code is added by this documentation patch. No numeric probabilities are released. Source/provenance, MML, and PD-013 remain open.

## Source description used below

Unless a row says otherwise, `source description / local baseline source` means:

`previously accepted local P2C project baseline available in the pre-GitHub local workspace during M32 execution; copied into GitHub because the online repository initially contained only the project skeleton. Exact prior package pin is not re-established by this documentation patch and should be reviewed as part of the baseline import audit.`

## 1. Files imported from the previously accepted local project baseline

Copy status for every row in this section: copied into GitHub from the local baseline support tree during M32 execution and not modified by this documentation-only patch. These files are not being claimed as newly accepted baseline by Codex.

| Repo path | Source description / local baseline source | Copied unchanged or modified | Why needed for M32 | Acceptance claim |
|---|---|---|---|---|
| `config/failure_consumption_matrix.yaml` | local P2C baseline config snapshot | copied unchanged at import time | validator/runtime support | proposed repo material pending audit |
| `config/initial_states.yaml` | local P2C baseline config snapshot | copied unchanged at import time | real-data smoke and static initial state support | proposed repo material pending audit |
| `config/project_scope.yaml` | local P2C baseline config snapshot | copied unchanged at import time | scope guard support for validators | proposed repo material pending audit |
| `config/success_criteria.yaml` | local P2C baseline config snapshot | copied unchanged at import time | validation support | proposed repo material pending audit |
| `data/essence_outputs.yaml` | local P2C baseline data snapshot | copied unchanged at import time | static data loader completeness | proposed repo material pending audit |
| `data/family_registry.yaml` | local P2C baseline data snapshot | copied unchanged at import time | family legality checks for ordinary-add pools | proposed repo material pending audit |
| `data/mechanics_evidence.yaml` | local P2C baseline data snapshot | copied unchanged at import time | foundation validator evidence support | proposed repo material pending audit |
| `data/mods_desecrated_quarterstaff.yaml` | local P2C baseline data snapshot | copied unchanged at import time | static data index completeness and validator scope checks | proposed repo material pending audit |
| `data/mods_ordinary_quarterstaff.yaml` | local P2C baseline data snapshot | copied unchanged at import time | load-bearing ordinary-add pool candidates and weights | proposed repo material pending audit |
| `data/omens.yaml` | local P2C baseline data snapshot | copied unchanged at import time | static data loader completeness; not used to expand M32 mechanics | proposed repo material pending audit |
| `data/operations.yaml` | local P2C baseline data snapshot | copied unchanged at import time | operation metadata support for validators | proposed repo material pending audit |
| `data/reveal_sampling_contract.yaml` | local P2C baseline data snapshot | copied unchanged at import time | validator completeness; Reveal remains out of M32 scope | proposed repo material pending audit |
| `data/sources.yaml` | local P2C baseline data snapshot | copied unchanged at import time | source registry support for validators and fingerprints | proposed repo material pending audit |
| `schemas/item_state.schema.yaml` | local P2C baseline schema snapshot | copied unchanged at import time | foundation/state validation support | proposed repo material pending audit |
| `schemas/static_modifier.schema.yaml` | local P2C baseline schema snapshot | copied unchanged at import time | static modifier validation support | proposed repo material pending audit |
| `src/p2c_engine/__init__.py` | local P2C baseline runtime snapshot | copied unchanged at import time | package import support | proposed repo material pending audit |
| `src/p2c_engine/canonical/__init__.py` | local P2C baseline runtime snapshot | copied unchanged at import time | canonical package import support | proposed repo material pending audit |
| `src/p2c_engine/canonical/hashes.py` | local P2C baseline runtime snapshot | copied unchanged at import time | deterministic hash support | proposed repo material pending audit |
| `src/p2c_engine/canonical/json.py` | local P2C baseline runtime snapshot | copied unchanged at import time | canonical JSON support | proposed repo material pending audit |
| `src/p2c_engine/canonical/normalize.py` | local P2C baseline runtime snapshot | copied unchanged at import time | canonical normalization support | proposed repo material pending audit |
| `src/p2c_engine/decisions/__init__.py` | local P2C baseline runtime snapshot | copied unchanged at import time | decision package import support | proposed repo material pending audit |
| `src/p2c_engine/decisions/_guard.py` | local P2C baseline runtime snapshot | copied unchanged at import time | fail-closed decision-source guard support | proposed repo material pending audit |
| `src/p2c_engine/decisions/exact_branching.py` | local P2C baseline runtime snapshot | copied unchanged at import time | shared exact/branching decision support | proposed repo material pending audit |
| `src/p2c_engine/decisions/ids.py` | local P2C baseline runtime snapshot | copied unchanged at import time | decision identity support | proposed repo material pending audit |
| `src/p2c_engine/decisions/protocol.py` | local P2C baseline runtime snapshot | copied unchanged at import time | decision-source protocol used by MC harness | proposed repo material pending audit |
| `src/p2c_engine/decisions/recording.py` | local P2C baseline runtime snapshot | copied unchanged at import time | MC replay/trace recording support | proposed repo material pending audit |
| `src/p2c_engine/decisions/replay.py` | local P2C baseline runtime snapshot | copied unchanged at import time | deterministic replay support | proposed repo material pending audit |
| `src/p2c_engine/decisions/seeded.py` | local P2C baseline runtime snapshot | copied unchanged at import time | seeded deterministic sampling support | proposed repo material pending audit |
| `src/p2c_engine/domain/__init__.py` | local P2C baseline runtime snapshot | copied unchanged at import time | domain package import support | proposed repo material pending audit |
| `src/p2c_engine/domain/action.py` | local P2C baseline runtime snapshot | copied unchanged at import time | M4 validator support | proposed repo material pending audit |
| `src/p2c_engine/domain/action_fingerprint.py` | local P2C baseline runtime snapshot | copied unchanged at import time | M4 validator support | proposed repo material pending audit |
| `src/p2c_engine/domain/candidate.py` | local P2C baseline runtime snapshot | copied unchanged at import time | candidate representation for pool builder | proposed repo material pending audit |
| `src/p2c_engine/domain/candidate_pool.py` | local P2C baseline runtime snapshot | copied unchanged at import time | candidate pool representation for ordinary-add pool builder | proposed repo material pending audit |
| `src/p2c_engine/domain/decision.py` | local P2C baseline runtime snapshot | copied unchanged at import time | decision record support | proposed repo material pending audit |
| `src/p2c_engine/domain/defects.py` | local P2C baseline runtime snapshot | copied unchanged at import time | fail-closed defect reporting | proposed repo material pending audit |
| `src/p2c_engine/domain/enums.py` | local P2C baseline runtime snapshot | copied unchanged at import time | side/mode/static category support | proposed repo material pending audit |
| `src/p2c_engine/domain/evidence.py` | local P2C baseline runtime snapshot | copied unchanged at import time | evidence structure support for validators | proposed repo material pending audit |
| `src/p2c_engine/domain/failure.py` | local P2C baseline runtime snapshot | copied unchanged at import time | failure semantics support | proposed repo material pending audit |
| `src/p2c_engine/domain/item_state.py` | local P2C baseline runtime snapshot | copied unchanged at import time | ItemState and installed mod-id state support | proposed repo material pending audit |
| `src/p2c_engine/domain/pool_building.py` | local P2C baseline runtime snapshot | copied unchanged at import time | pool request/result structures | proposed repo material pending audit |
| `src/p2c_engine/domain/static_modifier.py` | local P2C baseline runtime snapshot | copied unchanged at import time | StaticModifier model support | proposed repo material pending audit |
| `src/p2c_engine/domain/versions.py` | local P2C baseline runtime snapshot | copied unchanged at import time | schema/version constants | proposed repo material pending audit |
| `src/p2c_engine/legality/__init__.py` | local P2C baseline runtime snapshot | copied unchanged at import time | legality package import support | proposed repo material pending audit |
| `src/p2c_engine/legality/blockers.py` | local P2C baseline runtime snapshot | copied unchanged at import time | family/group/capacity legality blockers | proposed repo material pending audit |
| `src/p2c_engine/legality/capacity.py` | local P2C baseline runtime snapshot | copied unchanged at import time | prefix/suffix/total capacity checks | proposed repo material pending audit |
| `src/p2c_engine/legality/pool_builders.py` | local P2C baseline runtime snapshot | copied unchanged at import time | load-bearing ordinary-add pool builder used by M32 | proposed repo material pending audit |
| `src/p2c_engine/legality/predicates.py` | local P2C baseline runtime snapshot | copied unchanged at import time | legality predicates used by pool builder | proposed repo material pending audit |
| `src/p2c_engine/legality/prevalidation.py` | local P2C baseline runtime snapshot | copied unchanged at import time | fail-closed prevalidation support | proposed repo material pending audit |
| `src/p2c_engine/legality/state_validation.py` | local P2C baseline runtime snapshot | copied unchanged at import time | state invariant support | proposed repo material pending audit |
| `src/p2c_engine/sampling/__init__.py` | local P2C baseline runtime snapshot | copied unchanged at import time | sampling package import support | proposed repo material pending audit |
| `src/p2c_engine/sampling/digest.py` | local P2C baseline runtime snapshot | copied unchanged at import time | deterministic digest support | proposed repo material pending audit |
| `src/p2c_engine/sampling/exact.py` | local P2C baseline runtime snapshot | copied unchanged at import time | exact sampling support reused by seeded decision source | proposed repo material pending audit |
| `src/p2c_engine/sampling/order.py` | local P2C baseline runtime snapshot | copied unchanged at import time | deterministic ordering support | proposed repo material pending audit |
| `src/p2c_engine/sampling/ppswor.py` | local P2C baseline runtime snapshot | copied unchanged at import time | existing sampling support; not used to expand M32 scope | proposed repo material pending audit |
| `src/p2c_engine/sampling/weighted.py` | local P2C baseline runtime snapshot | copied unchanged at import time | weighted sampling support for seeded MC draws | proposed repo material pending audit |
| `src/p2c_engine/static_data/__init__.py` | local P2C baseline runtime snapshot | copied unchanged at import time | static-data package import support | proposed repo material pending audit |
| `src/p2c_engine/static_data/admission.py` | local P2C baseline runtime snapshot | copied unchanged at import time | static data admission checks | proposed repo material pending audit |
| `src/p2c_engine/static_data/checks.py` | local P2C baseline runtime snapshot | copied unchanged at import time | static data validation checks | proposed repo material pending audit |
| `src/p2c_engine/static_data/fingerprints.py` | local P2C baseline runtime snapshot | copied unchanged at import time | source/semantic fingerprint support | proposed repo material pending audit |
| `src/p2c_engine/static_data/game_data.py` | local P2C baseline runtime snapshot | copied unchanged at import time | StaticGameData construction support | proposed repo material pending audit |
| `src/p2c_engine/static_data/immutable.py` | local P2C baseline runtime snapshot | copied unchanged at import time | immutable static data support | proposed repo material pending audit |
| `src/p2c_engine/static_data/initial_state.py` | local P2C baseline runtime snapshot | copied unchanged at import time | initial state loader support | proposed repo material pending audit |
| `src/p2c_engine/static_data/loaders.py` | local P2C baseline runtime snapshot | copied unchanged at import time | YAML data loading for controlled real-data smoke | proposed repo material pending audit |
| `src/p2c_engine/static_data/manifest.py` | local P2C baseline runtime snapshot | copied unchanged at import time | static data manifest support | proposed repo material pending audit |
| `src/p2c_engine/static_data/modifier_index.py` | local P2C baseline runtime snapshot | copied unchanged at import time | static modifier index support | proposed repo material pending audit |
| `src/p2c_engine/static_data/normalize.py` | local P2C baseline runtime snapshot | copied unchanged at import time | static data normalization support | proposed repo material pending audit |
| `src/p2c_engine/static_data/semantic.py` | local P2C baseline runtime snapshot | copied unchanged at import time | semantic fingerprint support | proposed repo material pending audit |
| `src/p2c_engine/trace/__init__.py` | local P2C baseline runtime snapshot | copied unchanged at import time | trace package import support | proposed repo material pending audit |
| `src/p2c_engine/trace/events.py` | local P2C baseline runtime snapshot | copied unchanged at import time | trace event support | proposed repo material pending audit |
| `src/p2c_engine/trace/ledger.py` | local P2C baseline runtime snapshot | copied unchanged at import time | ledger hash support | proposed repo material pending audit |
| `src/p2c_engine/trace/replay_context.py` | local P2C baseline runtime snapshot | copied unchanged at import time | replay context support | proposed repo material pending audit |
| `src/p2c_engine/trace/schema.py` | local P2C baseline runtime snapshot | copied unchanged at import time | trace schema support | proposed repo material pending audit |
| `src/p2c_engine/trace/v2.py` | local P2C baseline runtime snapshot | copied unchanged at import time | M4 validator support | proposed repo material pending audit |
| `src/p2c_engine/trace/verify.py` | local P2C baseline runtime snapshot | copied unchanged at import time | trace verification support | proposed repo material pending audit |
| `tools/validate_foundation.py` | local P2C baseline validation tool | copied unchanged at import time | required validation command | proposed repo material pending audit |
| `tools/validate_m4.py` | local P2C baseline validation tool | copied unchanged at import time | required validation command | proposed repo material pending audit |

## 2. Files newly created or modified specifically for M32

| Repo path | Status | Why created or modified for M32 | Acceptance claim |
|---|---|---|---|
| `src/p2c_engine/monte_carlo/__init__.py` | new | M32 Monte Carlo package marker | proposed pending audit |
| `src/p2c_engine/monte_carlo/ordinary_add.py` | new | M32 seeded MC harness over accepted ordinary-add only | proposed pending audit |
| `tests/monte_carlo/test_m32_seeded_mc_harness.py` | new | M32 replay/shared-kernel/invariant/micro-fixture tests | proposed pending audit |
| `examples/m32_seeded_mc_smoke.py` | new | metadata-only smoke runner for M32 | proposed pending audit |
| `packages/proposed/P2C_M32_Seeded_MC_Harness_Result_Codex_v1/00_README_FIRST.md` | new | M32 result package orientation | proposed pending audit |
| `packages/proposed/P2C_M32_Seeded_MC_Harness_Result_Codex_v1/01_IMPLEMENTATION_SUMMARY.md` | new | implementation summary | proposed pending audit |
| `packages/proposed/P2C_M32_Seeded_MC_Harness_Result_Codex_v1/02_SHARED_KERNEL_REPORT.md` | new | shared-kernel evidence summary | proposed pending audit |
| `packages/proposed/P2C_M32_Seeded_MC_Harness_Result_Codex_v1/03_SEED_REPLAY_AND_PRNG_REPORT.md` | new | seed replay and PRNG evidence summary | proposed pending audit |
| `packages/proposed/P2C_M32_Seeded_MC_Harness_Result_Codex_v1/04_RUNTIME_INVARIANTS_REPORT.md` | new | invariant evidence summary | proposed pending audit |
| `packages/proposed/P2C_M32_Seeded_MC_Harness_Result_Codex_v1/05_TEST_AND_SMOKE_REPORT.md` | new | validation evidence summary | proposed pending audit |
| `packages/proposed/P2C_M32_Seeded_MC_Harness_Result_Codex_v1/06_M33_ORACLE_CONVERGENCE_NEXT.md` | new | next-floor boundary note | proposed pending audit |
| `packages/proposed/P2C_M32_Seeded_MC_Harness_Result_Codex_v1/07_CLAUDE_AUDIT_REQUEST.md` | new | Claude audit request for M32 | proposed pending audit |
| `packages/proposed/P2C_M32_Seeded_MC_Harness_Result_Codex_v1/BASELINE_IMPORT_INVENTORY.md` | new in documentation-only patch | baseline import transparency for Claude audit | proposed pending audit |
| `packages/proposed/P2C_M32_Seeded_MC_Harness_Result_Codex_v1/PACKAGE_MANIFEST.md` | new, then updated | package manifest; updated to include this inventory | proposed pending audit |
| `packages/proposed/P2C_M32_Seeded_MC_Harness_Result_Codex_v1/SHA256SUMS.txt` | generated, then updated | package integrity after adding this inventory | proposed pending audit |
| `work/active/ACTIVE_TASK.md` | modified | task state and Claude audit instructions | operational status only; not accepted project truth |
| `pyproject.toml` | new | test path/pythonpath support for the GitHub skeleton | proposed pending audit |
| `.gitattributes` | modified | line-ending hygiene for repo reproducibility | proposed pending audit |
| `SHA256SUMS.txt` | modified | root repository integrity after M32 and this patch | proposed pending audit |

## 3. Runtime/data/config/schema/tool support needed because GitHub was initially a skeleton

These files overlap with Section 1. They were imported so that the M32 harness could run validators, tests, and a controlled metadata-only smoke check in GitHub without relying on unstaged local files.

| Support group | Repo paths | Why needed for M32 | Acceptance claim |
|---|---|---|---|
| Static project data | `data/*.yaml` | load ordinary quarterstaff modifiers, family registry, source registry, and related static-data support | proposed repo material pending audit |
| Project config | `config/*.yaml` | initial state, scope, failure/validation support | proposed repo material pending audit |
| Schemas | `schemas/*.yaml` | state/static modifier validation support | proposed repo material pending audit |
| Runtime model and legality kernel | `src/p2c_engine/domain/*`, `src/p2c_engine/legality/*`, `src/p2c_engine/static_data/*` | provide ItemState, StaticGameData, and load-bearing `build_ordinary_add_pool` | proposed repo material pending audit |
| Deterministic decision and sampling support | `src/p2c_engine/decisions/*`, `src/p2c_engine/sampling/*` | seeded deterministic draw and replay support | proposed repo material pending audit |
| Canonical and trace support | `src/p2c_engine/canonical/*`, `src/p2c_engine/trace/*` | hashes, ledger, M4 validation, and replay checks | proposed repo material pending audit |
| Validators | `tools/validate_foundation.py`, `tools/validate_m4.py` | required validation commands | proposed repo material pending audit |
| Test configuration | `pyproject.toml` | allows GitHub skeleton to run scoped M32 pytest suite | proposed pending audit |

## 4. Files that should remain proposed and not accepted until audit

The following categories must remain proposed until Claude audit and ChatGPT/User acceptance:

- The M32 MC harness: `src/p2c_engine/monte_carlo/*`.
- The M32 test and smoke runner: `tests/monte_carlo/test_m32_seeded_mc_harness.py`, `examples/m32_seeded_mc_smoke.py`.
- The full M32 result package under `packages/proposed/P2C_M32_Seeded_MC_Harness_Result_Codex_v1/`.
- The GitHub baseline import itself: `config/*`, `data/*`, `schemas/*`, and imported `src/p2c_engine/*` support files.
- The imported validators: `tools/validate_foundation.py`, `tools/validate_m4.py`.
- Repo hygiene additions made to support reproducibility: `.gitattributes`, `pyproject.toml`, and generated `SHA256SUMS.txt`.

No ledger file was updated to claim acceptance of the imported baseline or M32 result.

## 5. Untracked legacy-copy leftovers not committed or pushed

The original local checkout at `C:\Users\infok\Documents\GitHub\PoECraft` contains untracked files from the first local import attempt. They were intentionally not committed and not pushed. They should not be treated as GitHub project truth.

Grouped untracked leftovers:

- `src/p2c_core/*`
- `src/p2c_engine/domain/execution.py`
- `src/p2c_engine/domain/jawbone.py`
- `src/p2c_engine/domain/outcome.py`
- `src/p2c_engine/domain/reveal.py`
- `src/p2c_engine/engine/*`
- `src/p2c_engine/operations/*`
- `src/p2c_engine/planning/*`
- `src/p2c_engine/probability/*`
- `tests/architecture/*`
- `tests/contract/*`
- `tests/decisions/*`
- `tests/domain/*`
- `tests/engine/*`
- `tests/legality/*`
- `tests/p2c_core/*`
- `tests/planning/*`
- `tests/probability/*`
- `tests/regression_v7_1/*`
- `tests/sampling/*`
- `tests/state_validation/*`
- `tests/static_data/*`
- `tests/trace/*`

These leftovers should either be removed from the local checkout with explicit cleanup approval or imported later only through a separate audited baseline/delta process.

## Claude audit request for this inventory

Claude should audit both:

- whether the M32 seeded MC harness stays within M32 scope and uses the accepted ordinary-add kernel rather than duplicating legality logic;
- whether the GitHub baseline import is sufficiently transparent, scoped, and not silently accepted as project truth.
