# Implementation and atomicity evidence

Load-bearing files:

- `src/p2c_engine/monte_carlo/perfect_essence.py`: shared exact/oracle and seeded executor.
- `src/p2c_engine/operations/resolver.py`: exact six-row resolver admission.
- `data/operations.yaml`: accepted feasible-removal wording and six-row runtime metadata.
- `data/mechanics_evidence.yaml`: accepted M42-A project-base rules, explicitly source-open.

The executor calls the shared `build_removal_pool`, which already excludes fractured modifiers and emits canonical instance identities. For every candidate it creates an isolated post-removal state, appends the exact canonical guaranteed modifier, and keeps the branch only if shared `validate_item_state` accepts the complete terminal.

Execution commits only the final valid terminal. There is no random or weighted add pool and no remove-only terminal. Invalid source state, crafted precondition, family/group conflict, capacity conflict, or empty feasible pool returns the original state hash with no decision when failure is known before draw.
