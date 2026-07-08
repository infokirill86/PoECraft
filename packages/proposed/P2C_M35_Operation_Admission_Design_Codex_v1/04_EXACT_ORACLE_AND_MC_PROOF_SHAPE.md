# Exact / Oracle and MC Proof Shape

## Exact/oracle shape

For a state with `k` removable non-fractured installed modifier instances:

- enumerate the `k` removal candidate keys;
- each path has exact rational probability `1/k`;
- remove the selected candidate instance from a branch copy;
- canonicalize the terminal item state;
- aggregate terminal probability by canonical terminal-state identity;
- include no-transition terminal only when the removal pool is empty.

All exact values in later implementation evidence must use canonical rational representation:

- numerator: integer;
- denominator: positive integer;
- reduced form.

## Duplicate-instance handling

If two removable candidate keys remove indistinguishable duplicate instances and yield the same canonical terminal state, the terminal probability must sum both exact path products.

The path identity and terminal identity are different concepts:

- path identity includes the selected removal candidate key;
- terminal identity is the canonical post-removal item state.

## Empty-pool oracle

If the removal pool is empty:

- no removable candidate paths exist;
- no-transition terminal mass is exactly one;
- input state digest equals output/no-transition state digest;
- no modifier flags are changed.

## MC proof shape for later M35-A

If M35-A is authorized, MC validation should use:

- fixed seed list pinned before running;
- fixed sample tiers pinned before running;
- uniform categorical sampling over removal candidate keys;
- comparison against exact terminal probabilities;
- deterministic replay for selected samples;
- negative controls that intentionally break uniformity or fractured exclusion and prove hard failure.

M35 design does not execute MC and does not release public numeric probabilities.

