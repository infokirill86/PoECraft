# Confirmed and unresolved mechanics

## Confirmed enough for a later project-model gate

- Perfect Essence acts on a Rare item and leaves it Rare.
- It removes one modifier and installs one row-declared guaranteed modifier.
- The six prepared outputs apply to quarterstaves and match the canonical modifier index.
- Fractured modifiers remain protected under the already accepted project invariant.
- Omen/side behavior is a separate modifier layer.
- A safe emulator operation must be atomic: no remove-only terminal and no consumption on failure.

## Not confirmed enough for runtime

- Whether “random modifier” means uniform over all removable instances before capacity constraints.
- Whether the base removal pool is conditioned to removals that leave capacity for the guaranteed side.
- Whether crafted Essence modifiers are eligible removal targets under Perfect Essence specifically.
- Whether an existing crafted modifier blocks use before removal or may be replaced by the operation.
- Whether repeat Perfect Essence use replaces, stacks, or is rejected.
- Exact interaction between family/group conflict and an existing crafted modifier.

The current YAML answers some of these questions, but it predates a complete accepted contract and cannot be promoted silently.
