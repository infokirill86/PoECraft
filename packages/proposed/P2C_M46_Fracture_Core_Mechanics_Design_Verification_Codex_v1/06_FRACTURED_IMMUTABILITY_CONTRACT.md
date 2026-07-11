# Fractured Immutability Contract

A successful Fracture changes exactly one state bit: the selected installed modifier instance becomes fractured.

Required invariants:

- the selected modifier remains installed;
- all unselected modifiers remain identical;
- rarity, item level, item class, side occupancy, family/group state, crafted flags, and every unrelated flag remain unchanged;
- accepted Annulment and Chaos removal pools continue to exclude the fractured instance;
- accepted Perfect Essence feasible-removal construction continues to exclude it;
- accepted Alchemy remains fail-closed on fractured input under its existing boundary;
- ordinary add and accepted rarity/capacity logic continue to count the fractured modifier on its canonical side;
- deterministic replay reproduces the same selected path and terminal state;
- no operation may clear or modify the fractured flag without a separate explicit mechanics gate.

The official 0.2.0e fix is supporting evidence that even numerical reroll behavior must not affect a fractured modifier. Numeric-value mutation is not implemented or expanded in M46.
