# Mechanics and Source Evidence

Checked: 2026-07-11. External evidence is project-model support, not a server-truth claim.

| Evidence | Location | Finding | M43 use |
|---|---|---|---|
| Accepted runtime rows | `data/operations.yaml`, accepted ledgers | Rarity, Exalted, Annulment, Chaos-like, Greater Essence, and Perfect Essence rows are explicitly runtime-admitted | Defines the only catalog operations M43 may execute |
| Accepted primitive | M32–M34 evidence | `ordinary_add` is an accepted engine primitive outside the currency catalogue | May be referenced explicitly without making catalog activity an admission signal |
| Resolver | `src/p2c_engine/operations/resolver.py` | Single-operation compilation already checks runtime admission and current-state preconditions | Must be invoked per branch at each sequence step |
| Existing mixed chain | M36-A package/runtime | Proves exact mass multiplication, branch-specific rebuild, terminal aggregation, seeded replay, and fail-closed admission for a narrow two-step surface | Reuse and generalize; do not duplicate |
| Active route configuration | `config/initial_states.yaml`, `config/project_scope.yaml` | Primary route starts from a purchased fractured Rare quarterstaff; process of obtaining the fracture is explicitly excluded | Explains why Fracture is not selected now |
| Fracturing wording | `https://poe2db.tw/us/Fractured_Modifiers` | Fractures a random modifier on a Rare item with at least four modifiers and locks it | Supports future clean core, not this wave |
| Omen catalogue | `https://poe2db.tw/us/Omen` | Current equipment Omens modify Exalted, Annulment, Chaos, Perfect Essence, and other operations | Establishes high future product value, not admission |
| Official patch 0.3.0 | `https://www.pathofexile.com/forum/view-thread/3826682` | Removed Greater Annulment and the old Alchemy/Coronation side Omens | Confirms an Omen inventory reconciliation is required before broad admission |
| Alchemy wording | PoE2DB currency/item-rarity catalogue | Upgrades a Normal or Magic item to Rare with four modifiers | Supports a later atomic multi-add wave |
| Perfect Essence accepted floor | M42-A package/audit | Six rows use terminal-feasible removal plus guaranteed add with temporary `crafted_count == 0` | M43 inherits it unchanged; repeat semantics remain closed |

## Source conclusion

No new external mechanics decision is necessary for bounded sequence execution. Every step inherits an already accepted project-model contract. External checks instead explain why Fracture, Omens, Alchemy, and Essence repeat behavior remain separate gates.

## Important repository drift note

`data/omens.yaml` includes current Crystallisation effects and excludes several officially removed older Omens, but it has no independent runtime-admission field. A future Omen wave must reconcile the complete live equipment-crafting inventory and define modifier admission explicitly rather than interpreting catalogue presence as permission.
