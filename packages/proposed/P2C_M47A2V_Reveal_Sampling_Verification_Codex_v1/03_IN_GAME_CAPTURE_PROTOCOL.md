# In-Game Capture Protocol for Kirill

## Purpose

Capture reproducible internal evidence for D3-D5. Do not use these observations as crafting advice or publish inferred probabilities.

## Base D3/D4 setup

1. Use a Rare quarterstaff at item level 82.
2. Use `preserved_jawbone` for the primary no-MML setup.
3. Do not activate Echoes, named-Lich, Necromancy, Omen of Light, or other modifiers.
4. Create two reproducible setup families:
   - prefix placeholder: suffix capacity full and prefix has capacity;
   - suffix placeholder: prefix capacity full and suffix has capacity.
5. Keep the installed modifier IDs, families, groups, item level, Jawbone row, and placeholder side identical within each setup family.
6. Independently reconstruct the compatible eligible offer pool from the project data before examining aggregate results. Save tier-row identities and generation weights where available.

## Exact action and record

For every observation:

1. Screenshot/copy the item before Jawbone, including item class, item level, rarity, and installed modifiers.
2. Apply the Jawbone and screenshot the hidden placeholder state.
3. Use Reveal once.
4. Screenshot the full three-offer window before selecting anything.
5. Record each offer's modifier ID, tier, family, groups, exclusive flag, and display position.
6. Record success/failure. On failure, record whether the item/placeholder changed and whether currency was consumed.
7. Do not omit inconvenient windows. Give every attempt a unique observation ID.

## Capture sizes

- Pilot: 12 total windows, split across both sides, to verify that the form and screenshots are sufficient.
- D3 falsification pass: at least 30 successful windows per side in a setup where at least one compatible exclusive row is independently known.
- D4 screening: approximately 300 homogeneous windows for the same setup and eligible-pool snapshot. If candidate models remain close, pre-register a follow-up of 1,000 or more before collecting it.
- D5: only use a setup that the reconstructed pool predicts cannot produce three compatible offers. Seek 10 repeatable attempts while recording failure, post-state, and consumption.

These are evidence-gathering targets, not statistical proof thresholds and not public probability claims. One verified structural counterexample can reject a candidate; absence of a counterexample cannot prove the server algorithm.

## What observations distinguish

| Observation | Distinguishes |
|---|---|
| Successful window with a known compatible exclusive pool but zero exclusives | Rejects D3-A guarantee |
| Offer outside independently reconstructed eligible pool | Rejects current compatibility/MML contour or exposes data mismatch |
| Same-family/group-conflicting offers | Challenges sequential blocking order in D4-A |
| Homogeneous repeated windows with full pool/weights | Screens tier-row weighting against family-first alternatives |
| Position patterns | Screens display-order behavior only; does not prove independence |
| Insufficient-pool failure with unchanged item and no consumption | Supports D5-A fail-closed contour |
| Failure that consumes or mutates | Rejects D5-A |
