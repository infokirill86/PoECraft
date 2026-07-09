# Edge-case Table

| Edge case | Required design behavior |
|---|---|
| No removable mod | Explicit no-transition/no-consumption; original state unchanged; exact mass assigned to no-transition terminal. |
| Fractured-only item | Same as no removable mod; fractured modifiers are never removable. |
| Removal succeeds but post-removal add pool is empty | Branch-specific no-transition/no-consumption to the original state; no partial remove-only terminal. |
| Removed prefix | Rebuilt add pool may include prefix or suffix according to accepted ordinary-add legality from the post-removal state. |
| Removed suffix | Same rule: no side is inferred from removal; accepted add legality decides from branch state. |
| Full rare item | Removal creates one explicit slot on the branch-copy; add pool must be rebuilt from that state. |
| Partially full item | Removal may increase free capacity; add legality is computed after removal. |
| Duplicate installed mod instances | Removal path identity must include duplicate ordinal or stable removal candidate key. |
| Different paths same terminal | Aggregate by canonical terminal-state identity. |
| Remove alpha then add alpha | Valid if accepted add legality allows the candidate after removal; terminal may equal original state and must aggregate with any no-transition terminal by canonical state if applicable. |
| Active catalog row without accepted runtime admission | Fail closed; do not execute because `active_in_current_simulation` is not runtime permission. |
| Chaos variants / Omens / Whittling | Out of M37-A unless separately gated. |

