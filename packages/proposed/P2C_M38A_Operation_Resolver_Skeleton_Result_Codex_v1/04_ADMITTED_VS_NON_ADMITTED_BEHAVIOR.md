# Admitted vs non-admitted behavior table

| Request shape | M38-A behavior | Reason |
|---|---|---|
| `ordinary_add` | resolves to `OrdinaryAddOperation` | accepted engine primitive |
| `annulment` | resolves to `AnnulmentOperation` | accepted executable runtime row |
| `chaos` | resolves to `ChaosLikeOperation` | accepted executable runtime row |
| `exalted` | fail closed | active catalog row, but not runtime-admitted |
| `greater_chaos` | fail closed | active catalog row, but not runtime-admitted |
| `perfect_chaos` | fail closed | active catalog row, but not runtime-admitted |
| `chaos` + `variant_id: greater` | fail closed | variants are not admitted in M38-A |
| `annulment` + `variant_id: perfect` | fail closed | variants are not admitted in M38-A |
| `chaos` + `whittling` | fail closed | modifier layers are not admitted in M38-A |
| `chaos` + side Omen | fail closed | modifier layers are not admitted in M38-A |
| unknown currency | fail closed | not an accepted engine primitive or known admitted operation row |

The resolver never treats `active_in_current_simulation: true` as runtime permission.

