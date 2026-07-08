# Proposed Pass/Fail Criteria

## Global criteria

M34 should pass only if:

- all tests are deterministic under fixed seeds;
- exact/oracle and MC paths continue to use the accepted shared kernel;
- every public report remains numeric-release safe;
- every failure mode produces actionable replay/debug metadata;
- SOURCE/PROVENANCE, MML, and PD-013 remain open;
- no forbidden scope is entered.

## Multi-seed convergence criteria

Predeclare:

- seed list;
- sample-count tiers;
- tolerance/confidence policy;
- maximum allowed per-branch breaches;
- whether any breach is hard failure or whether aggregate seed-level criteria are used.

Recommended P2C-safe rule:

- no branch may exceed the predeclared statistical envelope for any seed/tier unless the test is explicitly a negative-control test;
- deterministic replay of the same seed/run id must reproduce the same result;
- failure must identify exact seed, branch, tier, and scaled deviation category.

## Sequence criteria

For short accepted-ordinary-add sequences:

- every step must use accepted `ordinary_add`;
- every branch state must rebuild pools through the accepted pool builder;
- replay must reproduce the same trajectory for the same seed/run id;
- terminal identity must be stable and canonical;
- no partial hidden mechanics may be introduced;
- no operation other than accepted `ordinary_add` may execute.

## Diagnostics criteria

Failure reports must include enough information to reproduce:

- fixture id;
- seed;
- run id;
- sample count tier;
- step index;
- decision id;
- pool digest;
- selected key when relevant;
- pre/post state hash;
- invariant or tolerance rule that failed.

## Public-output criteria

Public package docs may include:

- pass/fail status;
- row counts;
- seed identifiers;
- sample-count identifiers;
- hash/digest identifiers;
- file names;
- qualitative diagnostic category.

Public package docs must not include:

- probability values;
- percentages;
- decimal probability estimates;
- rational probability displays;
- success chance tables;
- expected attempts;
- EV/cost/ranking/advice output.
