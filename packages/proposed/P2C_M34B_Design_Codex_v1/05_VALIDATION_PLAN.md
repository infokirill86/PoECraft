# Validation Plan

## Validation goal

M34-B1 validation should prove that the MC harness can execute a short accepted-ordinary-add sequence without losing state, replay, or legality correctness between steps.

## Required checks

M34-B1 implementation should include checks for:

1. Pinned contract.
   - sequence length is exactly two;
   - both operations are accepted `ordinary_add`;
   - no other operation id appears.

2. State transition linkage.
   - step 1 pre-state hash equals step 0 post-state hash;
   - terminal state hash is derived from the final state after both steps.

3. Pool rebuild.
   - root pool is built from `S0`;
   - branch pool is built from `S1`;
   - branch pool digest changes when legality changes;
   - branch pool does not include candidates blocked by the newly installed step 0 modifier.

4. Legality rebuild.
   - capacity rules apply after step 0;
   - family blocks apply after step 0;
   - group blocks apply after step 0;
   - unknown modifier ids fail closed.

5. Deterministic replay.
   - same seed and run id reproduce the same full sequence trace;
   - different seeds may produce different traces, but each trace remains valid.

6. Exact/oracle comparison where tractable.
   - exact path enumeration is used for small fixtures;
   - MC observed terminal counts are compared to exact terminal expectations under the pinned tolerance policy;
   - public reports stay numeric-probability-free.

7. Negative control.
   - include at least one explicitly marked negative-control case proving the sequence diagnostics can fail.

## Ceiling policy

M34-B1 should have explicit ceilings before execution:

- maximum sequence steps: two;
- maximum exact path count: small enough for deterministic audit;
- maximum terminal count: small enough for deterministic audit;
- maximum sample tier: inherited from the accepted M34-A contract unless a later gate changes it.

If a ceiling is exceeded, the implementation should stop and report the ceiling breach rather than silently reducing validation.

## Required public evidence

Public result docs should report:

- pass/fail status;
- fixture ids;
- sequence ids;
- seed ids;
- sample tier ids;
- path/terminal counts;
- replay status;
- oracle comparison status;
- leak-scan status;
- whether numeric probability values were kept out of public docs.
