# Rarity capacity and mutable modifier-count evidence

Accepted project-model capacities used by the shared pool/invariant paths:

| Rarity | Prefix capacity | Suffix capacity | Current count rule |
|---|---:|---:|---|
| normal | 0 | 0 | initially zero |
| magic | 1 | 1 | may be zero, one, or two after valid transitions/removals |
| rare | 3 | 3 | may be below the usual generated count after removals |

Capacity and current count are separate. Tests cover:

- zero-modifier magic Augmentation;
- one-prefix magic forcing suffix through capacity filtering;
- one-suffix magic forcing prefix through capacity filtering;
- full magic no-transition/no-consumption;
- a fractured prefix as valid protected state;
- removal-pool exclusion of that fractured prefix;
- the existing fractured critical suffix scenario through the full regression suite.

There is no hardcoded global “five available mods” rule and no global “every rare item has one fractured suffix” invariant.
