# Source and repository comparison

## Sources checked

| Source | Evidence | Assessment |
|---|---|---|
| [Official Path of Exile 2 patch notes for the Magic-item Alchemy change](https://www.pathofexile.com/forum/view-thread/3862213/page/1) | Alchemy became usable on Magic items; original Magic modifiers are not retained. | Primary confirmation for Magic input and replacement. |
| [PoE2DB Currency](https://poe2db.tw/us/Currency) | Current tooltip: Normal or Magic becomes Rare with four random modifiers. | Trusted project-data confirmation for input, output, and count. |
| [PoE2DB Atziri's Temple](https://poe2db.tw/us/Atziris_Temple) | Alchemy workbench uses the same Normal/Magic-to-Rare-with-four wording. | Supporting independent data surface. |
| [PoE2 Wiki rarity](https://www.poe2wiki.net/wiki/Rarity) | Records that current modifiers are not retained and describes ordinary Rare prefix/suffix capacity. | Supporting community synthesis, not sole authority. |
| [PoE2 Wiki Fracturing Orb](https://www.poe2wiki.net/wiki/Fracturing_Orb) | Fractured modifiers cannot be removed or modified; fractured items are at least Magic. | Supporting evidence for the unresolved interaction. |
| PoE1 analogue | Classic Alchemy applies to Normal items and generates a Rare roll; it does not answer the newer PoE2 Magic-input rule. | Context only; not used to decide PoE2 behavior. |

## Repository comparison

`data/operations.yaml` currently records:

- input rarity `normal` or `magic`;
- atomic Rare output;
- discard all explicit modifiers;
- empty Rare shell;
- four ordinary weighted additions;
- `active_in_current_simulation: false`;
- `runtime_admission_status: data_reference_candidate`.

The first four behavioral points agree with the official/current tooltip contour. The final two correctly keep Alchemy non-executable.

The repository goes beyond public wording when it specifies sequential use of ordinary weighted add pools. That is a proposed project-model execution shape, not verified server truth. The implementation gate must state this explicitly.

## No silent conflict resolution

No checked trusted source contradicted the current Normal/Magic, replacement, Rare-output, or four-modifier contour. The fractured-input interaction and exact internal selection algorithm remain unresolved rather than silently inferred.
