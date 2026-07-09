# Claude Audit Request

Please audit `P2C_M37_ChaosLike_RemoveThenAdd_Design_Codex_v1`.

## Audit focus

1. Is Chaos-like remove_then_add the right next design move after accepted M36-A?
2. Does the package clearly distinguish engine primitive from game-facing currency rows?
3. Does it correctly ground itself in `data/operations.yaml`, `data/sources.yaml`, and `data/mechanics_evidence.yaml`?
4. Does it correctly state that Chaos-like rows are `admission_candidate`, not accepted executable runtime?
5. Does it avoid inferring executable permission from `active_in_current_simulation`?
6. Are remove-first, non-fractured-only removal, branch-specific add-pool rebuild, exact path product, and terminal aggregation specified correctly?
7. Are no-removable, post-removal-empty-add-pool, full/partial item, duplicate terminal, and fractured-only edge cases handled?
8. Does the proposed M37-A floor stay narrow enough?
9. Are Greater/Perfect MML, Whittling, Omens, variants, public numeric release, optimizer/economics/advice, and boundary closures kept gated?

## Requested verdict

Return:

- `GO`, `GO WITH CHANGES`, or `NO-GO`;
- required corrections, if any;
- whether M37-A base Chaos-like runtime is a safe next implementation floor after corrections.

