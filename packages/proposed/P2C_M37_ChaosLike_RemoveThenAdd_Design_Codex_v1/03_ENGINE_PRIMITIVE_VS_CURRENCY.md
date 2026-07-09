# Engine Primitive vs Currency

## Engine primitive

`remove_then_add` is an engine primitive sequence:

1. build removal pool;
2. select one removable non-fractured installed modifier instance;
3. remove it on a branch-copy;
4. rebuild ordinary add pool from the branch-specific post-removal item;
5. select one legal add candidate;
6. commit the resulting item state.

The primitive is not itself a game-facing currency.

## Game-facing currency candidate

`chaos`, `greater_chaos`, and `perfect_chaos` are game-facing operation rows in `data/operations.yaml`.

They may map onto the `remove_then_add` primitive with different add-side parameters, such as MML for Greater/Perfect modes.

They are currently `admission_candidate`, not accepted executable runtime.

## Admission rule

M37 design may describe how the primitive should work. It must not mark any Chaos-like currency row executable.

Later runtime admission must fail closed unless the row is explicitly admitted by ChatGPT/User after audit.

## Server-truth boundary

This design is PROJECT-MODEL behavior only. It does not claim PoE2 server-truth exact behavior.

