# Edge cases and stop conditions

| Case | Proposed M44-A behavior | Reason |
|---|---|---|
| Normal quarterstaff, no explicit modifiers | Build isolated Rare state and attempt four legal selections | Confirmed public input contour. |
| Magic quarterstaff with non-fractured explicits | Discard original explicits in the working copy, then generate four new modifiers | Official patch wording confirms originals are not retained. |
| Any fractured explicit modifier | Fail unchanged before mutation | Joint Alchemy/fracture behavior is not directly verified. |
| Fewer than four legal sequential selections | Whole operation fails unchanged and unconsumed | Atomicity; never emit a partial Rare result. |
| Unsupported variant or active modifier | Fail closed in resolver | M44 is base Alchemy only. |
| Exact ceiling exceeded | Structured exact stop, no result substitution | Preserves M43-A honesty rule. |
| Canonical data mismatch | Fail closed with evidence | Prevents parallel or guessed modifier identity. |

Stop M44-A implementation if:

- trusted sources conflict with the replacement/four-modifier contour;
- implementation requires modifying accepted ordinary-add legality or weights;
- fractured behavior must be broadened to complete the core;
- a special item class or Omen/modifier layer becomes necessary;
- exact evaluation can only complete through silent truncation or approximation;
- runtime admission would widen beyond base Alchemy;
- public numeric output, planner/optimizer behavior, automation, or open-boundary closure enters scope.
