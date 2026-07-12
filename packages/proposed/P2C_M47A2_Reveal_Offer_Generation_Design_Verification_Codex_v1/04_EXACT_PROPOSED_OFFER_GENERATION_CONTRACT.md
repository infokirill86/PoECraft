# Exact Proposed Offer-Generation Contract

This is the exact **candidate contract** for a later gate. It is not accepted runtime behavior.

## Input

`RevealRequest`:

- current immutable `ItemState`;
- exactly one canonical hidden `DesecratedPlaceholder`;
- placeholder side;
- source Jawbone row;
- stored MML;
- optional separately admitted modifier constraints;
- deterministic run/decision identifiers.

## Eligibility pipeline

1. Load canonical ordinary and exclusive Desecrated modifier tier rows from the shared modifier index.
2. Fix the side to the placeholder side.
3. Filter by item class and item level.
4. Apply stored Jawbone MML using the accepted family-internal MML interface; no fallback rule may be invented here beyond the existing accepted project model.
5. Block rows conflicting with installed families/groups.
6. Apply only separately admitted modifier constraints. Base Reveal supplies none.
7. Fail closed on missing canonical data, contradictory metadata, or unsupported constraints.

## Offer generation under candidate D3-A/D4-A

1. Build ordinary, exclusive, and combined eligible views over the same canonical row identities.
2. If a compatible exclusive view is non-empty, draw one exclusive tier row through the shared exact/seeded weighted chooser.
3. Block its family/groups.
4. Draw remaining rows sequentially from the current combined view, weight-proportionally and without replacement, blocking family/groups after each draw.
5. Require a complete compatible three-offer set.
6. Record offer-set identity independently from display order and independently from the eventual player selection.
7. Exact path mass is the product of the sequential generation decisions. Duplicate offer-set identities reached by different paths aggregate canonically.

## Output

`RevealOfferSet`:

- stable offer-set ID;
- three canonical offer IDs when completed;
- each offer's canonical modifier row and side;
- ordered generation trace;
- presentation order trace;
- pool digests after every filtering/blocking stage;
- exact path metadata internally;
- no installed terminal state yet.

## Failure

Candidate D5-A returns a structured failure with stage/category/digest diagnostics. The source item and placeholder remain unchanged and nothing is consumed. No smaller set and no silent filter relaxation is allowed.
