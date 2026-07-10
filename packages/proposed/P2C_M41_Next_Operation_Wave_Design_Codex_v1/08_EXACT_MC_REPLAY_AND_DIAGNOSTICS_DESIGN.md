# Exact, MC, Replay, and Diagnostics Design

## Exact/oracle

Greater Essence is deterministic after validation:

- legal transition: one terminal with exact rational mass `1/1`;
- illegal transition: explicit no-transition/no-consumption terminal with exact rational mass `1/1`;
- total exact mass must equal one;
- no weighted ordinary-add candidates or hidden branches may appear.

The oracle must verify the exact installed `mod_id`, target Rare rarity, preserved prior modifiers, crafted flag, and canonical terminal key.

## Monte Carlo

There is no stochastic selection in the clean Greater Essence core. Seeded MC is still useful as an execution-path parity check:

- every seed must return the same terminal and trace for the same input;
- empirical terminal identity must match the exact terminal;
- any seed-dependent outcome is a hard failure;
- no numeric probability publication is authorized.

## Replay trace

Required fields:

- run id and seed;
- input state digest;
- operation id and operation-row digest;
- output-row/modifier digest;
- precondition results;
- target-rarity working-state digest;
- terminal/no-transition code;
- final state digest;
- consumption boolean.

## Hard-fail diagnostics

Diagnostics must name the operation id, input state, failed contract, expected and observed row metadata, and whether any mutation occurred. Negative controls must prove mismatched operation/output metadata, unsupported Essence tiers, and precondition bypasses fail closed.
