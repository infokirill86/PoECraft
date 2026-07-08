# Split Recommendation

## Recommendation

Split M34 into M34-A and M34-B.

## M34-A

M34-A should cover:

- multi-seed single-step convergence behavior;
- deterministic replay across a fixed seed set;
- tolerance breach diagnostics;
- negative-control failure reporting;
- package/report leak safety.

Why first:

M34-A keeps the state transition shape close to M33 while hardening the statistical confidence layer.

## M34-B

M34-B should cover:

- short accepted-ordinary-add sequences;
- branch-state pool rebuilds;
- full-sequence replay/debug diagnostics;
- terminal canonical identity;
- no-transition behavior inside a sequence.

Why second:

Sequence validation adds more moving parts. It should build on M34-A's multi-seed and diagnostic base.

## Why not one large milestone

One combined M34 would be possible but higher risk:

- harder audit;
- more failure causes mixed together;
- more chance of accidental operation expansion;
- harder to keep public numeric output safe.

Small split keeps momentum while preserving audit quality.
