# M36-A Implementation Summary

## Added runtime

- `src/p2c_engine/monte_carlo/heterogeneous_chain.py`

## Added tests

- `tests/monte_carlo/test_m36a_heterogeneous_chain_runtime.py`

## Implemented scope

M36-A implements fixed two-step heterogeneous chains over already accepted executable behavior only:

- accepted engine primitive `ordinary_add`;
- accepted operation row `annulment` with `runtime_admission_status: accepted_executable_runtime`.

## Core behavior

- Exactly two steps.
- Exactly one `ordinary_add` and one base Annulment step.
- Supports add -> annul and annul -> add.
- Rebuilds each operation pool from the branch-specific current item state.
- Multiplies exact rational path masses across steps.
- Aggregates terminals by canonical terminal-state identity.
- Treats path identity and terminal identity separately.
- Requires exact mass conservation.
- Terminates explicitly on no-transition/failure branch.
- Preserves fractured modifiers through Annulment steps.
- Provides deterministic seeded replay.
- Fails closed on catalog rows that are active but not executable-admitted.

## Not implemented

- Chains longer than two.
- Route planner.
- Variable-length route search.
- Chaos runtime.
- Essence runtime.
- Fracture runtime.
- Desecrate/Jawbone/Reveal runtime.
- Annulment variants or omens.
- Optimizer, advice, ranking, economics, EV.
- Public numeric probability release.
