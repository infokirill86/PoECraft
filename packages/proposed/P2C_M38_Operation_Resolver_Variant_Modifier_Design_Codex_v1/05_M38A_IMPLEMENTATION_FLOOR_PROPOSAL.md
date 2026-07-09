# Recommended M38-A Implementation Floor

## M38-A should implement only resolver skeleton and fail-closed behavior

Recommended M38-A scope:

- create a small resolver module;
- load operation/omen metadata through existing `StaticGameData`;
- support resolving already accepted base operations only:
  - base `chaos`;
  - base `annulment`;
  - accepted `ordinary_add` engine primitive if represented as an internal action request;
- return structured resolved plans;
- reject all Greater/Perfect variants;
- reject all Omen/modifier layers;
- reject unknown/unsupported combinations;
- prove `active_in_current_simulation` cannot authorize execution;
- include tests for fail-closed variant/modifier behavior.

This gives the project the seam it needs without admitting new behavior.

## M38-A should not implement

- Greater Exalted;
- Perfect Exalted;
- Greater Chaos;
- Perfect Chaos;
- Whittling;
- side Omens;
- desecrated-only Omen behavior;
- Essence/Jawbone/Reveal/Fracture/Desecrate;
- route planning;
- optimizer/economics/advice;
- public numeric output.

## Later safe batches after M38-A

After resolver skeleton acceptance, later gates may batch narrowly:

1. Greater/Perfect add-side MML variants for one admitted base shape, if source review agrees.
2. Side-filter Omens for one operation group.
3. Whittling as a removal selection-policy layer, with explicit tie policy.
4. Desecrated-only removal filtering.

Each batch should be accepted only after:

- source/data confirmation;
- resolver fail-closed tests;
- exact/oracle fixture;
- MC/replay fixture if runtime stochastic behavior is admitted;
- regression proving accepted base operations unchanged.

