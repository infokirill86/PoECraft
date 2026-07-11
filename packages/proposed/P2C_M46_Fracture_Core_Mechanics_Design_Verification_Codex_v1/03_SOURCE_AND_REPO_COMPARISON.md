# Source and Repository Comparison

External check status: `fresh_external_source_check_performed`

Checked on: `2026-07-12`

All findings are project-model evidence only. No source is treated as server-truth closure.

| Source | Fresh finding | Confidence / use |
|---|---|---|
| GGG official PoE2 0.2.0 notes: `https://www.pathofexile.com/forum/view-thread/3740562/page/1` | Fractures a random modifier on a Rare item with at least four modifiers and locks it in place | Primary confirmation of base contour |
| PoE2DB Fracturing Orb: `https://poe2db.tw/us/Fracturing_Orb` | Current item text matches the official contour and says it cannot be used on Fractured items | Current database confirmation |
| GGG-hosted PoE2 Wiki: `https://www.poe2wiki.net/wiki/Fracturing_Orb` | Rare, at least four, no fractured item; fractured modifier cannot be removed or modified; Desecrated modifiers are described as ineligible while still counting toward the minimum | Strong supporting mechanics source; Desecrated statement conflicts with prepared repo/old emulator observation and therefore does not close PD-013 |
| GGG official PoE2 0.2.0e notes: `https://www.pathofexile.com/forum/view-thread/3754474/page/1` | Divine affecting fractured modifiers was fixed as a bug | Primary support for numerical immutability |
| GGG official PoE1 3.20 notes: `https://www.pathofexile.com/forum/view-thread/3323944/filter-account-type/staff` | Same random-modifier, Rare, at-least-four core; PoE1 adds game-specific restrictions | Analogue only; supports shape, does not import PoE1-only restrictions |
| Craft of Exile current and beta PoE2 interfaces: `https://www.craftofexile.com/?game=poe2`, `https://beta.craftofexile.com/?game=poe2` | Quarterstaff data is present, but the browser-visible interface did not expose an authoritative Fracture contract suitable for resolving PD-013 | Checked but not used as decisive evidence |
| Current player report, supporting only: `https://www.reddit.com/r/PathOfExile2/comments/1twhiik/interactions_between_crafting_and_fracturing/` | Reports that a crafted/Essence modifier can be fractured and remains crafted | Supporting evidence only, not sole authority |

## Repository comparison

| Repository surface | Current state | M46 design consequence |
|---|---|---|
| `data/operations.yaml` / `fracturing_orb` | Rare, four-plus, no existing fracture, uniform installed-instance target; operation disputed and disabled | Retain as candidate input, not runtime authority |
| `data/mechanics_evidence.yaml` / `fracturing_revealed_desecrated` | Craft of Exile observation says eligible; external documentation says ineligible; in-game not tested | Conflict remains open as PD-013; clean M46-A rejects these states |
| `ItemState` / `ModifierInstance` | Canonical per-instance `crafted`, `desecrated`, and `fractured` flags already exist | No new state algebra is required |
| Accepted Annulment/Chaos/Essence paths | Already exclude or preserve fractured modifiers | M46-A can reuse existing immutability invariants and add direct regression proofs |

## Confirmed enough for the clean project model

- Rare quarterstaff input.
- At least four installed explicit modifier instances.
- No existing fractured modifier.
- One eligible installed modifier instance is selected from a combined pool; there is no prefix/suffix side lottery.
- The selected instance alone gains `fractured: true`; all other state is byte-semantically unchanged.
- The operation is atomic and failure is no-transition/no-consumption.

## Still unresolved

- Revealed and unrevealed Desecrated eligibility and minimum-count treatment in runtime.
- Any Jawbone/Reveal/PD-013 interaction.
- Whether future special protected modifier kinds require additional exclusions.
- Server-internal RNG implementation; the later exact project model uses uniform instance selection from the admitted clean pool.
