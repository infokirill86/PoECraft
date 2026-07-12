# D1-D5 Evidence Table

Fresh check date: `2026-07-12`.

| Decision | Repository candidate | Trusted/source evidence | Closure status |
|---|---|---|---|
| D1 side selection | uniform over all free-or-replaceable sides; selected full side may replace | [Desecrated modifier documentation](https://www.poe2wiki.net/wiki/Desecrated_modifier) says the placeholder occupies one side and removal occurs if modifiers are full; [Necromancy wording](https://poe2db.tw/us/Omen) proves side can be forced | single-free-side/no-removal is evidence-supported but still needs User ratification; both-free side distribution remains unknown |
| D2 full replacement | choose side, then uniform removable instance on that side | game tooltip reproduced by current documentation and [GGG forum report](https://www.pathofexile.com/forum/view-thread/3859174) says a full item removes a random modifier | fact of removal is supported; combined-uniform versus side-first distribution remains unpublished |
| D3 exclusive guarantee | offer process may include ordinary and exclusive rows but does not encode a mandatory exclusive slot separately | [Desecrated modifier documentation](https://www.poe2wiki.net/wiki/Desecrated_modifier) states at least one exclusive offer where eligible; a recent [large player dataset](https://www.reddit.com/r/PathOfExile2/comments/1uslcts/i_desecrated_more_than_500_rings_here_is_what_i/) supports structured ordinary/exclusive composition | strong supporting evidence, but quarterstaff-specific in-game confirmation or explicit User policy is still required |
| D4 exact offer sampling | sequential weight-proportional tier-row draws without replacement; block selected family/groups; randomize display | official [0.3.0 description](https://www.pathofexile.com/forum/view-thread/3826682) confirms only three choices; public sources do not expose the exact algorithm; recent player research says ordinary and exclusive weights differ and much larger datasets are needed | unresolved; candidate YAML must not be promoted automatically |
| D5 insufficient pool | fail crafting without consumption when a full compatible set cannot be built | no official, PoE2DB, wiki, Craft of Exile, or reliable player source found describing this edge | unresolved and potentially unreachable in normal quarterstaff data; explicit fail-closed policy or controlled in-game evidence required |

## PoE1 analogy

PoE1 veiled/crafting offer systems are useful architectural analogies for an offer-set decision followed by one installed choice, but their internal rules are not evidence for PoE2 Desecrated weighting or failure semantics and are not imported.
