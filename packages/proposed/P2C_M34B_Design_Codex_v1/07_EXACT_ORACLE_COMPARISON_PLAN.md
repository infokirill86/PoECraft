# Exact / Oracle Comparison Plan

## Purpose

M34-B1 should compare seeded MC sequence behavior against the exact/oracle layer for small, tractable two-step fixtures.

The comparison is a project-model validation. It is not a server-truth probability claim.

## Exact sequence enumeration

For exact/oracle comparison:

1. Build the step 0 pool from `S0`.
2. Enumerate each legal step 0 branch.
3. Apply the accepted ordinary-add transition for that branch to produce `S1`.
4. Build the step 1 pool from that branch-specific `S1`.
5. Enumerate each legal step 1 branch.
6. Aggregate terminal canonical state identity across all paths that end in the same terminal state.

This explicitly checks the core M34-B risk: branch-state pool rebuilds.

## MC comparison

MC comparison should:

- use the same accepted pool and transition kernel as exact enumeration;
- use pinned seeds and sample tiers;
- compare terminal-state observations to exact terminal expectations;
- use the inherited M34-A statistical envelope unless a later gate pins a replacement;
- fail hard on non-negative-control tolerance breaches.

## Public numeric boundary

Exact rational values, empirical proportions, fractions, decimals, and percentages must not appear in public reports unless a later explicit release gate authorizes them.

Public docs may report only:

- status;
- row/count metadata;
- seed/tier ids;
- fixture ids;
- path counts;
- terminal counts;
- hashes;
- leak-scan result;
- pass/fail booleans.

## Tractability stop rule

If exact enumeration becomes too large for the pinned M34-B1 ceiling, the implementation must stop or shrink the fixture. It must not replace oracle comparison with unreviewed approximate-only validation.
