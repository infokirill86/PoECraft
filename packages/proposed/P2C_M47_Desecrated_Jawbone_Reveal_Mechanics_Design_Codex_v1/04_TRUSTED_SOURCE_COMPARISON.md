# Trusted-Source Comparison

Fresh source check performed: `2026-07-12`.

| Source | What it supports | Limitation / design consequence |
|---|---|---|
| [GGG Content Update 0.3.0](https://www.pathofexile.com/forum/view-thread/3826682) | Ancient bones add hidden Abyssal modifiers; Well of Souls reveals the modifier and presents three choices | Does not publish side selection, full-item replacement, weights, compatibility, or Fracture interaction |
| [PoE2DB Gnawed Jawbone](https://poe2db.tw/us/Gnawed_Jawbone) | Rare weapon/quiver applicability and the prepared item-level ceiling | Does not expose internal transition probabilities |
| [PoE2DB Preserved Jawbone](https://poe2db.tw/us/Preserved_Jawbone) | Rare weapon/quiver applicability | Does not expose internal transition probabilities |
| [PoE2DB Ancient Jawbone](https://poe2db.tw/us/Ancient_Jawbone) | Rare weapon/quiver applicability and displayed MML | Exact Reveal sampling remains hidden |
| [PoE2 Wiki Ancient Jawbone](https://www.poe2wiki.net/wiki/Ancient_Jawbone) | MML family-fallback explanation consistent with the accepted project MML policy | Community documentation; project-model corroboration, not server truth |
| [PoE2 Wiki Desecrated modifier](https://www.poe2wiki.net/wiki/Desecrated_modifier) | hidden placeholder, one-of-three Reveal choice, side capacity, full-item random removal, normal single-Desecrated limit, ordinary and exclusive Reveal contour | Says regular weights appear usual and exclusive weights uneven; does not provide a complete exact algorithm |
| [PoE2DB Omen catalog](https://poe2db.tw/us/Omen) | current wording for Necromancy, named-Lich, Echoes, Light, and Putrefaction effects | Wording does not fully specify composition order or internal randomness |
| [PoE2 Wiki Fracturing Orb](https://www.poe2wiki.net/wiki/Fracturing_Orb) | Desecrated state counts toward the Fracture minimum but is not an eligible Fracture target | Conflicts with the repository's preserved Craft of Exile observation for revealed Desecrated eligibility |
| [Craft of Exile PoE2](https://www.craftofexile.com/?game=poe2) | useful independent emulator/data comparison; the repository preserves an earlier observed revealed-Desecrated eligibility result | The current static-web pass did not reproduce an authoritative contract; the preserved observation remains conflicting supporting evidence only, not a freshly confirmed rule |

## Result

Trusted-source agreement is strong enough for the state contour and operation applicability, but not for exact Jawbone side/replacement selection or exact Reveal offer generation. The Fracture conflict remains material. These gaps require explicit project-model decisions before runtime admission.
