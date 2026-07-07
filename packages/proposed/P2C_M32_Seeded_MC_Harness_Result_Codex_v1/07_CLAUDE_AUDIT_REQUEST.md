# Claude Audit Request

Please audit the M32 result.

Verify:

- M32 executes only accepted `ordinary_add`;
- MC and exact paths share the same pool/legality/weight kernel;
- no duplicate ordinary-add pool builder was introduced for MC;
- seed replay is deterministic;
- runtime invariants fail closed;
- known-answer micro-fixtures are adequate for sampler sanity;
- real-data smoke output is numeric-probability-free;
- public docs do not release probability values;
- no optimizer, advice, ranking, EV, budget, expected-attempt, server-truth, MML, PD-013, or source/provenance closure is introduced.

Expected verdict style: GO / GO WITH CHANGES / NO-GO.
