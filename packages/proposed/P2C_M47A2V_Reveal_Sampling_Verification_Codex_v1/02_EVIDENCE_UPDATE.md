# Evidence Update

## Confirmed contour, not exact sampling

| Evidence | Supports | Does not establish |
|---|---|---|
| GGG 0.3.0 notes | Jawbone creates a hidden modifier; Reveal presents three choices and the player selects one | D3 guarantee, D4 weighting/order, D5 insufficient-set behavior |
| PoE2DB Omen catalog | Echoes rerolls the choices once; named-Lich and Necromancy effects are independent modifier layers | Base Reveal sampling or Ancient-MML persistence |
| PoE2 Wiki Desecrated modifier page | At least one compatible exclusive contour; more than one exclusive may appear; ordinary rows retain normal-looking weights; Echoes rerolls once | Exact mixture or sequential sampling unit |
| Community 563-window ring dataset | Every recorded window contained an exclusive offer | Quarterstaff behavior, exact D3 guarantee, D4 algorithm |
| GGG 0.3.0b staff reply | Echoes-after-reveal was a bug; Echoes must be active before revealing | Whether all stored Jawbone constraints persist during reroll |
| GGG bug reports for `Could not generate mod` | A failure contour exists when offers cannot be generated | Whether currency is consumed and whether state remains unchanged |
| GGG Ancient+Echoes report | Rerolls below Ancient MML have been observed/reported | Whether that behavior is intended, a bug, or current server policy |
| PoE1 veiled analogue | Three random offers followed by one player choice is an established analogous contour | PoE2 D3-D5 algorithm or weights |

## Repository-data comparison

- `data/mechanics_evidence.yaml` correctly records three offers/one installed choice and `sampling_algorithm_closed: false`; the accepted Jawbone clean core also keeps `reveal_runtime_admitted: false` and `d3_d5_closed: false`.
- `data/mechanics_evidence.yaml` now records M47-A2 as accepted design-only and each D3-A/D4-A/D5-A candidate as not accepted.
- `data/omens.yaml` contains prepared candidate policies for named-Lich guarantees and `stored_desecration_constraints_persist` under Echoes. Their rows remain runtime-blocked/reference-only and are not proof of D3/D4 or Ancient-MML persistence.
- `data/operations.yaml` contains a `reveal_handler` catalog/architecture contour, but that does not admit Reveal runtime and does not publish the hidden offer sampler.
- `data/sources.yaml` identifies PoE2DB Desecrated data as checked for modifiers/tags; it does not turn catalog rows or prepared policies into sampling evidence.

Result: repository data and accepted status agree that the contour is prepared but the probability-bearing sampler is still open. Where candidate YAML is more specific than public evidence, M47-A2V treats it as a model to test, not a fact.

## Source links

- GGG 0.3.0: <https://www.pathofexile.com/forum/view-thread/3826682>
- PoE2DB Omens: <https://poe2db.tw/us/Omen>
- PoE2 Wiki Desecrated modifier: <https://www.poe2wiki.net/wiki/Desecrated_modifier>
- Community 563-window dataset: <https://www.reddit.com/r/PathOfExile2/comments/1uslcts/i_desecrated_more_than_500_rings_here_is_what_i/>
- GGG Echoes timing clarification: <https://www.pathofexile.com/forum/view-thread/3840893/filter-account-type/staff>
- GGG insufficient-offer reports: <https://www.pathofexile.com/forum/view-thread/3846552> and <https://www.pathofexile.com/forum/view-thread/3831699>
- GGG Ancient+Echoes MML report: <https://www.pathofexile.com/forum/view-thread/3860899>
- PoE1 analogue: <https://www.poewiki.net/wiki/Veiled_modifier>

## Evidence conclusion

The visible three-offer/one-choice contour is strong enough to retain as accepted design context. D3-A, D4-A, and D5-A remain candidate project models. Prepared YAML is input to comparison, not proof. No source inspected publishes enough detail to accept the exact D4 sampler.
