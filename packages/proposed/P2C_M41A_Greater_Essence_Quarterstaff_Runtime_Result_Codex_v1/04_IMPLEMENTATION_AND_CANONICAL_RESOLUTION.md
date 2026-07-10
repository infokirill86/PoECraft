# Implementation and canonical modifier resolution

Load-bearing files:

- `src/p2c_engine/monte_carlo/greater_essence.py`: one shared deterministic Greater Essence executor and exact/replay evidence surface.
- `src/p2c_engine/operations/resolver.py`: compiles only the eight admitted rows into the shared executor contract.
- `src/p2c_engine/static_data/game_data.py`: exposes immutable `essence_outputs` through `StaticGameData`.
- `data/operations.yaml` and `config/project_scope.yaml`: exact eight-row activation.

For every execution, the resolver cross-checks the operation row, `data/essence_outputs.yaml`, and `StaticGameData.modifier_index`. Modifier id, family, side, crafted flag, group ids, item class, category, and tier must agree. The installed `ModifierInstance` uses the canonical id and normal shared state validation; no parallel modifier or capacity validator was added.

Missing or inconsistent canonical data raises a fail-closed admission error before state mutation.
