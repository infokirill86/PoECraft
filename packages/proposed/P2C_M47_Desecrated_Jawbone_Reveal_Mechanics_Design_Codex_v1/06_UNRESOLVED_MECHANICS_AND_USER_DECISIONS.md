# Unresolved Mechanics and Required User Decisions

M47-A runtime should not be authorized until these are explicitly answered.

| Decision | Exact question | Source-safe options |
|---|---|---|
| `M47-D1` Jawbone side with available capacity | When both sides have capacity, how is placeholder side selected? When only one side has capacity, must that side be used without removal? | adopt free-side-first with a pinned tie rule; or adopt the prepared legal-side lottery as project policy |
| `M47-D2` full-item replacement | On a globally full item, is one removable non-fractured installed instance selected uniformly from a combined pool, with placeholder side inherited from the removed instance? | adopt combined-instance replacement; or require in-game confirmation before implementation |
| `M47-D3` Reveal offer composition | Must every valid endgame set contain an exclusive Desecrated offer, and how are ordinary versus exclusive rows combined? | adopt the current community-documented guarantee where eligible; or keep exclusive composition source-open and implement no runtime |
| `M47-D4` Reveal sampling | What exact weighted-without-replacement algorithm, family/group blocking order, and display-order treatment define the offer set? | approve the prepared sequential project model; approve another explicit model; or require empirical verification |
| `M47-D5` insufficient compatible pool | If a complete compatible offer set cannot be built, is the Reveal action refused without consuming or does it show fewer offers? | approve atomic fail-closed; or require source/in-game confirmation |
| `M47-D6` revealed removal behavior | Are revealed Desecrated instances ordinary eligible targets for base Annulment/Chaos, and can Omen of Light target hidden placeholders or revealed instances only? | separate revealed-only removal from placeholder behavior; require explicit confirmation for placeholder removal |
| `M47-D7` Fracture/PD-013 | Are revealed Desecrated instances excluded from Fracture like placeholders, or eligible as the preserved emulator observation suggests? | documentation model: counts but excluded; emulator model: revealed eligible; no silent default |
| `M47-D8` Echoes and Lich exactness | Is an Echoes reroll an independent complete set, and how is a named-Lich guarantee placed inside the offer sampling process? | retain current prepared project policies only after explicit gate; otherwise keep modifiers blocked |

The repository contains candidate answers for all these questions. None becomes accepted merely because it is already encoded in YAML or tested as a foundation prototype.
