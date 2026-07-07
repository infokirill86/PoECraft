# A2 Kernel Test Restoration Report

Status: implemented as proposed test restoration; not accepted truth.

## Restored test files

| Test path | Kernel area covered |
|---|---|
| `tests/legality/test_m5_pool_builders.py` | pool builders, pool digests, MML filtering, legality blockers, capacity interactions |
| `tests/legality/test_m5_audit_additions_claude.py` | audit-gap tests for pool builder edge cases and fail-loud request validation |
| `tests/sampling/test_sampling_contract.py` | weighted draw, exact branch options, pool digest, sampling contract failures |
| `tests/decisions/test_decision_sources.py` | seeded, exact, replay, and recording decision sources used by M32 |
| `tests/domain/test_canonical_state.py` | canonical item state hashing and modifier-instance shape |
| `tests/static_data/test_static_game_data.py` | static game data index, manifest, aliases, essence tier handling |
| `tests/static_data/test_foundation_revision_v8_1.py` | frozen static data, schema invalidation, semantic fingerprint behavior |
| `tests/static_data/test_foundation_revision_v8_2.py` | active/reference-only semantic fingerprint boundaries and cross-file defects |
| `tests/static_data/test_initial_state.py` | fixed fractured Critical Hit Chance initial state materialization |
| `tests/static_data/test_m7h1_governance_fingerprint.py` | pinned semantic fingerprint continuity |

## Why this is A2-only

The restored files test the imported kernel that M32 relies on:

- `p2c_engine.legality.pool_builders`
- `p2c_engine.legality.predicates` through pool-builder behavior
- `p2c_engine.sampling.weighted`
- `p2c_engine.sampling.exact`
- `p2c_engine.decisions`
- `p2c_engine.domain`
- `p2c_engine.static_data`

No new runtime files were added for new mechanics. No operation expansion was implemented.

## Scope boundary

Some restored baseline tests exercise functions present in the imported `pool_builders` module beyond the single M32 ordinary-add lane. This does not open those mechanics for new work and does not accept them as project truth. It only restores execution coverage for imported code that already exists in the proposed GitHub baseline import.
