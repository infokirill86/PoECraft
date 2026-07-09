# Claude audit request

Please audit `P2C_M39_GreaterPerfect_MML_Design_Verification_Codex_v1`.

## Audit questions

1. Did Codex correctly inventory every Greater/Perfect row in `data/operations.yaml`?
2. Did Codex correctly separate MML ordinary-add / remove-then-add variants from Essence guaranteed-output mechanics?
3. Does the proposed MML filter model match current repo behavior in `src/p2c_engine/legality/pool_builders.py`?
4. Is the conclusion sound that MML applies to add pools and not to base removal selection?
5. Is Greater/Perfect Chaos correctly modeled as base removal plus MML-filtered branch-specific add pool, without admitting runtime here?
6. Is the recommended future batching boundary safe: Greater/Perfect Exalted + Greater/Perfect Chaos first, with Transmutation/Augmentation/Regal/Essence separated?
7. Did the package avoid claiming MML closure, server truth, source/provenance closure, or runtime admission?
8. Did `ACTIVE_TASK.md` route correctly to Claude using schema v2?

## Expected verdict format

Return one of:

- `GO`
- `GO WITH CHANGES`
- `NO-GO`

If `GO WITH CHANGES` or `NO-GO`, please list required corrections with severity and exact files.

## Boundaries to enforce

- no runtime implementation;
- no Greater/Perfect runtime acceptance;
- no MML closure;
- no Whittling/Omen runtime;
- no new operation admission;
- no public numeric probability release;
- no optimizer/economics/advice;
- no SOURCE/PROVENANCE or PD-013 closure;
- no automation.

