# Exact / Oracle Design

## Exact path shape

For each removable candidate `r`:

1. compute exact removal probability from the accepted removal pool;
2. remove `r` on a branch-copy;
3. rebuild the ordinary add pool from the branch-copy;
4. for each add candidate `a`, compute exact add probability from the rebuilt pool;
5. path mass is the product of removal mass and add mass.

No concrete probability values are released in this design.

## Failure/no-transition mass

If the removal pool is empty:

- the terminal is no-transition/no-consumption;
- original state is unchanged;
- exact mass is the full operation mass.

If a removal branch has an empty add pool:

- that branch contributes failure/no-transition mass to the original state;
- the branch does not produce a partial remove-only terminal;
- resource consumption remains false for that branch.

## Terminal aggregation

Terminal distribution is a marginal over canonical terminal-state identity:

- path identity is ordered and operation-specific;
- terminal identity is canonical item state;
- all paths yielding the same canonical terminal state are summed.

## Mass conservation

The sum over all committed terminals plus explicit no-transition/failure terminals must be exactly one.

Any missing mass is a hard failure.

## Exact ceilings

M37-A implementation should pin ceilings before running:

- maximum removal candidates;
- maximum add candidates per branch;
- maximum total paths;
- maximum terminal count.

If exceeded, runtime must stop and report rather than silently switching methods.

