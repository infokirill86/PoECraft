# Source and Repository Evidence

Fresh external check: `2026-07-12`.

| Source | Supported facts | Limitation / decision consequence |
|---|---|---|
| [GGG Content Update 0.3.0](https://www.pathofexile.com/forum/view-thread/3826682) | Ancient bones add hidden modifiers; Well of Souls presents three options and the player selects one | Does not publish category composition, weights, conflict order, or insufficient-pool behavior |
| [PoE2DB Omen catalog](https://poe2db.tw/us/Omen) | Echoes permits one reroll on the next Desecrated reveal; named-Lich Omens guarantee a random named-Lich modifier; Necromancy restricts side | Does not define the offer generator or constraint-persistence order |
| [PoE2 Wiki Desecrated modifier](https://www.poe2wiki.net/wiki/Desecrated_modifier) | Placeholder side is fixed; three offers; at least one compatible exclusive offer when eligible; more than one exclusive may appear; regular weights appear normal and exclusive weights appear uneven; Echoes rerolls once | Community documentation, not an official exact RNG contract |
| [Player dataset: 563 valid reveal windows](https://www.reddit.com/r/PathOfExile2/comments/1uslcts/i_desecrated_more_than_500_rings_here_is_what_i/) | Every observed window contained an exclusive option; independent-slot composition is inconsistent with the observations | Rings rather than quarterstaves; does not identify the exact sampling algorithm |
| [GGG 0.3.0b patch note](https://www.pathofexile.com/forum/view-thread/3840893/filter-account-type/staff) | Echoes being usable after an item was already revealed was a bug; the modifier must be active before Reveal | Does not say whether all stored constraints persist during reroll |
| [Official bug report: could not generate mod](https://www.pathofexile.com/forum/view-thread/3846552) and [second low-level report](https://www.pathofexile.com/forum/view-thread/3831699) | Reveal can visibly fail with "Crafting failed: Could not generate mod" when no valid output can be built | Reports do not prove currency/placeholder consumption semantics or the exact trigger threshold |
| [Ancient + Echoes MML report](https://www.pathofexile.com/forum/view-thread/3860899) | Multiple observations report rerolled offers below the Ancient minimum | Could be a bug or intended reroll rule; it conflicts with the repository's automatic `stored_desecration_constraints_persist: true` assumption |
| `data/operations.yaml` | Prepared candidate: tier-row weighted sequential draws without replacement, compatibility blocking, display permutation, atomic failure | Candidate only; D3-D5 are not accepted |
| `data/reveal_sampling_contract.yaml` | Prepared structural offer contract | Cannot substitute for external evidence or User approval |
| `data/omens.yaml` | Prepared Echoes/Lich/Necromancy interfaces | Runtime status remains blocked/reference-only |

## Evidence conclusion

- Confirmed enough for design: three offers, explicit player choice, fixed placeholder side, ordinary plus exclusive sources, at least one compatible exclusive strongly supported, one Echoes reroll.
- Not confirmed enough for runtime truth: exact tier/family sampling unit, exact weights, without-replacement implementation order, display-order role, D5 consumption semantics, and Echoes MML/constraint persistence.
- No source conflict is silently resolved here.
