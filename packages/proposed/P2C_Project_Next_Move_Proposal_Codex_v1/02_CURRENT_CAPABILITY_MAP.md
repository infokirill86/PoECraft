# Current Capability Map

## Runtime/data foundation

| Capability | Status | Evidence |
|---|---|---|
| Project-model GitHub runtime baseline | accepted | `ledger/ACCEPTED_ARTIFACTS.md` |
| Static data loading | implemented | `src/p2c_engine/static_data/` |
| Static data validation | implemented | `tools/validate_foundation.py` |
| M4 sampling/trace validation | implemented | `tools/validate_m4.py` |
| Canonical hashes/state payloads | implemented | `src/p2c_engine/canonical/`, `src/p2c_engine/domain/` |

## Pool and legality kernel

| Capability | Status | Evidence |
|---|---|---|
| Ordinary add pool builder | implemented and accepted through current gates | `src/p2c_engine/legality/pool_builders.py` |
| Removal pool builder | implemented as kernel support | `build_removal_pool` |
| Reveal base pool builder | implemented as kernel support | `build_reveal_base_pool` |
| Capacity/family/group blockers | implemented | legality tests |
| MML project-model handling | implemented but server-truth closure remains open | blockers ledger |

## Executable operation runtime

| Capability | Status | Evidence |
|---|---|---|
| Accepted `ordinary_add` execution | accepted | M32-M34-B1 packages and audits |
| Single-step seeded MC | accepted | M32/M33/M34-A |
| Two-step accepted-ordinary-add sequence | accepted | M34-B1 |
| Annulment execution | not accepted / not implemented as executable runtime | no accepted operation handler |
| Chaos execution | not accepted / not implemented as executable runtime | no accepted operation handler |
| Perfect Essence execution | not accepted / not implemented as executable runtime | no accepted operation handler |
| Jawbone/Reveal execution | not accepted / not implemented as executable runtime | source/mechanic blockers remain |

## Product-level capability

| Capability | Status |
|---|---|
| Real multi-operation crafting route simulation | missing |
| Target success probability over real operation results | missing |
| Attempt model over real operation results | missing |
| Cost/budget/economics | missing and forbidden until later gate |
| Optimizer/advice/ranking | missing and forbidden until later gate |

## Bottom line

The engine has a strong ordinary-add foundation, but it is not yet a useful crafting simulator for real routes. The missing bridge is operation admission.
