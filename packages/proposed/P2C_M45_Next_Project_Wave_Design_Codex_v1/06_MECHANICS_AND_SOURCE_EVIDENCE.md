# Mechanics and Source Evidence

Checked: 2026-07-11. External evidence supports project-model decisions only; it is not a server-truth claim.

| Evidence | Source | Finding | Design consequence |
|---|---|---|---|
| Accepted route boundary | `config/project_scope.yaml`, `config/initial_states.yaml` | Primary route begins with the required fractured critical staff; fracture acquisition is excluded | Fracture is not the highest-value current wave |
| Resolver seam | `src/p2c_engine/operations/resolver.py` | Active modifier IDs and filter shapes exist but all modifiers currently fail closed | M45 should extend this seam, not create parallel currency functions |
| Prepared Omen data | `data/omens.yaml` | Contains add count, side, Whittling, Crystallisation, Desecrated, Jawbone, and Reveal effect shapes | Catalogue presence is design input, never runtime admission |
| Whittling wording | `https://www.poe2wiki.net/wiki/Omen_of_Whittling` and repo mechanics evidence | Next Chaos removes the lowest modifier-level eligible modifier; tie behavior is not published | Keep existing uniform-tie project policy explicit and source-open |
| Crystallisation wording | `https://www.poe2wiki.net/wiki/Omen_of_Sinistral_Crystallisation` | Next Perfect/Corrupted Essence removes only prefixes (Dextral is the suffix counterpart) | Apply side filter to the accepted feasible-removal pool, not to the guaranteed add |
| Alchemy/Coronation/Greater Annulment history | `https://www.poe2wiki.net/wiki/Omen_of_Greater_Annulment`, official patch history referenced there | These Omens became drop-disabled; their effects still exist in historical data | Require an explicit legacy/version-scope decision before admission |
| Greater Annulment wording | Same source | Says the next Annulment removes two modifiers, but does not establish the exact joint-selection/rollback model | Exclude from clean core pending a mechanics contract |
| Alchemy side wording | `https://www.poe2wiki.net/wiki/Omen_of_Sinistral_Alchemy` | Maximum prefix/suffix outcome, not a simple per-draw side filter | Exclude until legacy/version scope and conditional generation contract are pinned |
| Current Omen catalogue | `https://poe2db.tw/us/Omen` | Equipment Omens span accepted and unaccepted operation families | Inventory must carry effect status separately from runtime admission |
| Source policy | `data/sources.yaml` | Conflicts and patch changes cannot be overwritten automatically | Surface drift and require a later User gate |

## Repository drift finding

`data/omens.yaml` is neither a complete current-availability catalogue nor an admission registry. It contains effects for future Jawbone/Reveal work, while historical Alchemy/Coronation/Greater Annulment records are absent. M45-A must add explicit Omen admission and availability/status metadata or an equivalent validated registry. `active_omen_system: true` in project scope must never mean that every listed Omen is executable.

## Confirmed-enough clean core

The side-filter and Whittling wording is sufficient for a later project-model gate when applied to already accepted pools. Greater Exaltation’s visible “add two” contour is sufficient for design, but the later gate must explicitly ratify sequential accepted-weighted draws, rebuild after the first add, atomic rollback, and no partial result.
