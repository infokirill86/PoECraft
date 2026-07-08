# Later M36-A Implementation Floor Proposal

This is a proposal for a later gate. It is not authorized by this package.

## Recommended M36-A scope

Implement two-step heterogeneous chain hardening over accepted operations only:

- `ordinary_add -> annulment`;
- `annulment -> ordinary_add`.

## Required pins before running M36-A

- accepted operation registry;
- fixed chain specs;
- max sequence length: 2;
- exact enumeration ceilings;
- seed list;
- sample tiers;
- tolerance policy;
- replay trace schema;
- no-transition chain policy;
- negative-control requirements.

## Required evidence

M36-A should return:

- exact/oracle terminal aggregation proof;
- branch-specific state transition proof;
- pool/replacement rebuild proof after every step;
- MC comparison proof against exact for tractable fixtures;
- replay determinism proof;
- negative-control failure proof;
- fail-closed proof for unaccepted operation refs;
- boundary report confirming no new operation admission.

## Acceptance criteria

M36-A should be accepted only if:

- accepted `ordinary_add` and base Annulment behavior remain unchanged;
- mixed-chain exact and MC paths share accepted operation kernels;
- terminal mass sums exactly in oracle fixtures;
- runtime permission cannot be inferred from `active_in_current_simulation`;
- no public numeric probability release occurs;
- no optimizer/advice/ranking/economics behavior appears.
