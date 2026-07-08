# Task Critique and Selected Boundary

## Critique required by the gate

The user task asks for M34-B design for short accepted-`ordinary_add` sequences. The risky interpretation would be to design a broad generic sequence layer now. That would blur the line between MC hardening and a future planner/strategy engine.

A materially safer boundary is to make M34-B a pinned two-step validation floor first.

## Selected boundary

Use M34-B1 as the required next implementation boundary:

- sequence length: exactly two accepted `ordinary_add` steps;
- operation sequence shape: `ordinary_add -> ordinary_add`;
- operation expansion: none;
- new mechanics: none;
- optimizer/advice/ranking/economics: none;
- public numeric probability release: none.

Later three-step or variable-length sequence validation should require a separate ChatGPT/User gate after M34-B1 audit.

## Why this is safer

The two-step boundary exercises the main new risk without creating a general planner:

- state after step 1 must become the real pre-state for step 2;
- legality and capacity must be rebuilt after step 1;
- the second pool must be generated from the branch state, not from the original state;
- replay/debug traces must show both steps deterministically;
- exact/oracle comparison remains tractable for small fixtures.

This is enough to validate the sequence transition seam. It avoids accidental strategy, route guidance, or operation expansion.

## Consequence for this package

This package designs M34-B as a two-step-first contract. Any implementation authorization should explicitly say whether it authorizes M34-B1 only.
