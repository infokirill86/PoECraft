# Engine Primitive vs Currency Catalog Distinction

## Why this distinction matters

The simulator now has accepted runtime pieces and a broader prepared operation catalog. Future work will drift if those are treated as the same thing.

The safe model is:

- engine primitive: reusable internal behavior the runtime can execute after acceptance;
- game-facing currency/catalog entry: a YAML row describing a currency-like operation and its project-scope data;
- accepted executable runtime: an explicitly gated and audited operation/path the engine may execute.

## Current accepted runtime map

| Runtime concept | Current status | Notes |
|---|---|---|
| `ordinary_add` | accepted engine primitive | Not a direct `operations.yaml` row. It is the accepted add primitive used by MC/exact validation and two-step accepted-ordinary-add hardening. |
| base `annulment` | accepted executable runtime | Has an `operations.yaml` row and runtime implementation. Scope is base Annulment only; variants/omens are not accepted. |

## Current catalog-to-primitive relationships

These relationships are design mappings only. They do not accept the listed catalog rows as executable runtime.

| Catalog/currency family | Likely primitive relationship | Runtime admission status now |
|---|---|---|
| Transmutation-like | ordinary add with rarity transition | reference candidate only |
| Augmentation-like | ordinary add with magic-slot side resolution | reference candidate only |
| Regal-like | ordinary add with magic-to-rare transition | reference candidate only |
| Exalted-like | ordinary add primitive | admission candidate, not accepted executable currency wrapper |
| Annulment-like | remove-one-non-fractured primitive | base Annulment accepted; variants/omens not accepted |
| Chaos-like | remove then ordinary add | admission candidate only |
| Alchemy-like | clear/build rare shell plus sequential ordinary add | reference candidate only |
| Fracture-like | set fractured flag on eligible installed modifier | disputed / requires user resolution |
| Astrid-like support augment | state mutation / crafted limit modification | admission candidate only |
| Greater Essence-like | guaranteed crafted install from magic-to-rare | reference candidate only |
| Perfect Essence-like | remove then guaranteed crafted install | admission candidate only |
| Jawbone-like | create unrevealed Desecrated placeholder | blocked/out of scope until separate admission |
| Reveal-like | offer-set generation and placeholder replacement | blocked/out of scope until separate admission |

## Recommended naming rule

Avoid saying "active operation" when the intended meaning is "runtime-executable operation."

Use:

- "project-scope catalog row" for `active_in_current_simulation`;
- "accepted executable runtime" for operations admitted through ChatGPT/User gate after Claude audit;
- "engine primitive" for internal reusable behavior such as `ordinary_add`.
