# Candidate Pool and Selection Contract

## Pool construction order

1. Validate operation admission and exact base operation ID.
2. Validate Rare quarterstaff, at least four explicit instances, and no existing fracture.
3. Fail closed if any canonical resolution is missing.
4. Fail closed if any Desecrated modifier or unrevealed placeholder is present in the M46-A clean floor.
5. Build one combined candidate pool from installed explicit instance identities.
6. Select uniformly across that pool.

The pool must not:

- choose prefix/suffix first;
- use modifier generation weight;
- collapse duplicate installed instances by mod ID;
- create a parallel modifier-index interpretation;
- infer permission from `active_in_current_simulation`.

## Exact/oracle shape

Each eligible instance path receives the same canonical exact rational mass, expressed symbolically as numerator one over eligible-instance count. Path identity records the selected installed-instance key. Terminals aggregate by canonical terminal-state identity, so duplicate-instance paths that yield the same canonical state are summed exactly.

No actual probability values are released by this design package.

## Diagnostic identity

Every exact or sampled transition should record operation ID, input state digest, candidate-pool digest, selected instance key, canonical terminal digest, seed/run ID when sampled, and failure category when no transition occurs.
