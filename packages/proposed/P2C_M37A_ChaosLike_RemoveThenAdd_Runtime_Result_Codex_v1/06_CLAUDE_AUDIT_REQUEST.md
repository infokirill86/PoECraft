# Claude Audit Request

Please audit `P2C_M37A_ChaosLike_RemoveThenAdd_Runtime_Result_Codex_v1`.

## Audit focus

1. Does M37-A implement only base Chaos-like `remove_then_add`?
2. Does it use the M37 mechanics policy correctly:
   - uniform combined removal pool;
   - combined generation_weight ordinary-add pool;
   - no side-first base behavior;
   - Whittling/Omen layers excluded?
3. Does the proposed metadata change admit only base `chaos`, leaving `greater_chaos` and `perfect_chaos` candidates?
4. Does the runtime fail closed on non-admitted operations and variants?
5. Does removal happen only on a branch-copy?
6. Is the add pool rebuilt from the branch-specific post-removal state?
7. Is the operation atomic, with no partial remove-only terminal?
8. Are exact path masses multiplied and terminal states aggregated canonically?
9. Are fractured modifiers protected?
10. Do deterministic replay, diagnostics, and negative controls exist?
11. Did accepted ordinary_add, Annulment, and M36-A behavior remain unchanged?
12. Are public docs numeric-probability-free and boundary-safe?

## Requested verdict

Return:

- `GO`, `GO WITH CHANGES`, or `NO-GO`;
- required corrections, if any;
- whether ChatGPT/User may accept M37-A after corrections;
- any boundaries that must remain closed.

