# Current Simulator Capability Map

## Accepted executable capabilities

| Capability | Accepted surface |
|---|---|
| Weighted ordinary add | `ordinary_add` engine primitive |
| Rarity progression | Base/Greater/Perfect Transmutation, Augmentation, and Regal |
| Rare add | Base/Greater/Perfect Exalted |
| Remove | Base Annulment |
| Remove then add | Base/Greater/Perfect Chaos-like |
| Guaranteed Magic-to-Rare add | Eight Greater Essence quarterstaff rows |
| Feasible remove plus guaranteed add | Six Perfect Essence quarterstaff rows |
| MML filtering | Accepted interface and admitted row thresholds; broader MML remains open |
| Resolver | Single-operation admission/compilation seam |
| Exact and seeded MC | Accepted within the admitted operation floors |
| Mixed chain | Fixed two-step `ordinary_add`/Annulment M36-A surface only |

## Missing product capabilities

| Missing capability | Consequence |
|---|---|
| Bounded mixed sequences across all accepted operations | Cannot execute a realistic multi-currency route as one reproducible run |
| Omen modifier layer | Cannot model directional or behavior-changing meta-crafts |
| Conditional decisions/retries | Cannot express a strategy; deliberately later and separately gated |
| Longer route evaluation | Cannot propagate accepted operations through a complete user-authored route |
| Additional mechanics | Fracture, Alchemy, Desecrate/Jawbone/Reveal, and Essence repeat rules remain absent or gated |
| Public result release | Numeric probability release remains closed |

## Current architectural assets

- `OperationResolver` already compiles admitted single operations and fails closed on unsupported modifiers.
- Each accepted operation family has an exact/MC-capable harness or shared add kernel.
- Canonical state hashing, rational exact mass, replay traces, pool digests, and deterministic seeds already exist.
- M36-A proves branch-specific rebuild and mixed-operation execution, but hardcodes a two-step/narrow operation boundary.

M43-A should compose these assets rather than create a second operation framework.
