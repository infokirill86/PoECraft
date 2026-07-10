# Atomicity, No-Transition, and Edge Cases

| Case | Required result |
|---|---|
| Input is not Magic | No transition, no consumption |
| Output row missing or mismatched | Fail closed before mutation |
| Guaranteed family already installed | No transition, no consumption |
| Guaranteed group conflicts with installed group | No transition, no consumption |
| Crafted capacity exhausted | No transition, no consumption |
| Target Rare side capacity would be exceeded | No transition, no consumption |
| Unknown item class / output not applicable | Fail closed |
| Fractured prefix or suffix present | Preserve exactly; it consumes its real side capacity |
| Existing ordinary modifiers | Preserve exactly |
| Existing crafted modifier with Astrid capacity support | Permit only if accepted capacity validation says space remains |
| Duplicate invocation after guaranteed family installed | Second use returns no-transition/no-consumption |
| Unsupported Omen or modifier bundle | Fail closed; no Omen runtime is admitted |
| Perfect/Normal/Lesser/Corrupted Essence id | Fail closed under M41-A |

Atomicity is load-bearing: rarity must never become Rare unless the guaranteed modifier is also legally installed, and the modifier must never be installed while rarity remains Magic.
