# Batching and separate gates

## What can be batched safely later

The following can be batched after Claude/User acceptance of this design, if the implementation floor remains narrow:

1. A shared MML filter adapter in the resolver/operation plan layer.
2. Fail-closed tests proving non-admitted Greater/Perfect rows cannot execute.
3. Fixture tests proving MML filters add pools using the existing `apply_family_mml` behavior.
4. Future admission of Greater/Perfect Exalted and Greater/Perfect Chaos as a small batch, because they map onto accepted runtime capabilities.

## Why Greater/Perfect Exalted and Chaos are the best first runtime candidates

Greater/Perfect Exalted:

- base behavior is a one-mod ordinary add on rare item;
- accepted engine primitive already exists as `ordinary_add`;
- variant behavior is MML on the add pool.

Greater/Perfect Chaos:

- base Chaos-like remove-then-add runtime is already accepted;
- variant behavior is MML on the branch-specific post-removal add pool;
- removal mechanics stay base Chaos-like unless a separate admitted modifier layer changes them.

## What must stay behind separate gates

| Topic | Why gated |
|---|---|
| Greater/Perfect Transmutation | Base transmutation wrapper changes rarity from normal to magic and is not accepted runtime. |
| Greater/Perfect Augmentation | Magic-item side capacity wrapper is not accepted runtime. |
| Greater/Perfect Regal | Magic-to-rare rarity transition and rare pool-build wrapper are not accepted runtime. |
| Greater/Perfect Essence | Uses guaranteed crafted output and, for Perfect Essence, remove+guaranteed crafted behavior; not MML-only. |
| Whittling/Omen layer | Removal selection modifier layer with unresolved tie behavior; not an add-pool MML filter. |
| Side/desecrated filters | Modifier layers requiring separate semantics and source verification. |
| Jawbone/reveal MML | Different operation family and reveal offer-set model. |
| MML closure | Source/provenance and server-truth exactness remain open. |

## Risk of over-batching

If all Greater/Perfect rows are admitted together, the project would mix at least three different mechanic families:

- MML ordinary add;
- rarity-transition wrappers;
- guaranteed Essence output.

That would hide review-relevant mechanics behind one label and increase audit risk.

