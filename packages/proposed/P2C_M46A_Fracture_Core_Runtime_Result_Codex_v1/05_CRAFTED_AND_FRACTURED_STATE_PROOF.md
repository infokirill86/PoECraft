# Crafted and Fractured State Proof

The selected installed instance is located by canonical instance identity plus duplicate ordinal. The executor replaces that one immutable dataclass instance with a copy whose `fractured` flag is true.

Load-bearing assertions verify:

- modifier count is unchanged;
- exactly one instance changes;
- the selected instance keeps its `crafted` flag;
- every unselected instance remains byte-equivalent at the domain-object level;
- rarity, item class, level, quality, corruption, unrevealed placeholder, and all other item fields remain unchanged;
- the terminal contains exactly one fractured modifier.

Duplicate installed identities remain separately selectable because candidate identity includes an occurrence ordinal.
