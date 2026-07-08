# Accepted Runtime vs Active Flag Mismatch Report

## Accepted executable runtime today

| Runtime unit | Kind | Accepted scope | Evidence path |
|---|---|---|---|
| `ordinary_add` | engine primitive | Accepted project-model ordinary add primitive and sequence hardening over accepted ordinary add. It is not a direct `operations.yaml` currency row. | `src/p2c_engine/monte_carlo/ordinary_add.py`; M32, M33, M34-A, M34-B1 ledgers and audits |
| `annulment` | game-facing operation row plus runtime implementation | Accepted base Annulment runtime only. Removes exactly one removable non-fractured installed modifier instance. No variants/omens accepted. | `data/operations.yaml`; `src/p2c_engine/monte_carlo/annulment.py`; M35-A ledger and audit |

## Current active flag interpretation

`active_in_current_simulation` currently follows `config/project_scope.yaml`:

- if an operation group is listed under `active_operation_groups`, rows in that group must have `active_in_current_simulation: true`;
- if an operation group is listed under `reference_only_operation_groups`, rows in that group must have `active_in_current_simulation: false`;
- validators enforce this cross-file relationship in `src/p2c_engine/static_data/checks.py`.

This is useful as a project-scope/data-projection flag, but unsafe as an executable-runtime flag.

## Mismatch summary

Rows with `active_in_current_simulation: true`: 18.

Rows accepted as executable runtime: only `annulment` among `operations.yaml` rows.

Rows where `active_in_current_simulation: true` but executable runtime is not accepted:

| operation_id | group | reason this is a mismatch |
|---|---|---|
| `exalted` | `exalted` | The accepted `ordinary_add` primitive exists, but this currency wrapper and omen handling are not separately accepted as executable runtime. |
| `greater_exalted` | `exalted` | Same as `exalted`; MML remains project-model assumption and wrapper admission is not accepted. |
| `perfect_exalted` | `exalted` | Same as `exalted`; MML remains project-model assumption and wrapper admission is not accepted. |
| `chaos` | `chaos` | Remove-then-add composition is not accepted executable runtime. |
| `greater_chaos` | `chaos` | Remove-then-add plus MML is not accepted executable runtime. |
| `perfect_chaos` | `chaos` | Remove-then-add plus MML is not accepted executable runtime. |
| `install_astrid` | `support_augment` | Support augment state mutation is prepared data, not accepted runtime. |
| `perfect_essence_abrasion` | `perfect_essence` | Perfect Essence remove-plus-guaranteed crafted install is not accepted runtime. |
| `perfect_essence_flames` | `perfect_essence` | Same as other Perfect Essences. |
| `perfect_essence_ice` | `perfect_essence` | Same as other Perfect Essences. |
| `perfect_essence_electricity` | `perfect_essence` | Same as other Perfect Essences. |
| `perfect_essence_battle` | `perfect_essence` | Same as other Perfect Essences. |
| `perfect_essence_haste` | `perfect_essence` | Same as other Perfect Essences. |
| `gnawed_jawbone` | `jawbone` | Jawbone placeholder creation remains behind separate operation admission and source/provenance gates. |
| `preserved_jawbone` | `jawbone` | Same as other Jawbones. |
| `ancient_jawbone` | `jawbone` | Same as other Jawbones plus MML dependency. |
| `reveal_desecrated` | `reveal` | Reveal/Lich/Abyssal/PD-013-related mechanics remain separately gated. |

## Important non-mismatch

`annulment` has `active_in_current_simulation: true` and is now accepted as executable runtime, but only for base Annulment semantics accepted in M35-A.

The row also contains references to omen filters. Those variants are not accepted merely because the row is active. This is another reason an explicit runtime admission field is needed.

## Conclusion

The active flag should not be used as the single source for runtime executability.

Recommended fix: preserve `active_in_current_simulation` as project-scope/data-projection metadata, and add explicit `runtime_admission_status` metadata for executable admission.
