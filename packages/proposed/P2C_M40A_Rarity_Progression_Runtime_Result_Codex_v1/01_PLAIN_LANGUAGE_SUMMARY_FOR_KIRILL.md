# Plain-language summary for Kirill

The engine can now, in the proposed M40-A branch, model the basic crafting ladder:

1. turn a normal item into a magic item and add its first modifier;
2. add another modifier to a magic item when capacity allows;
3. turn a magic item into a rare item and add one modifier;
4. add one modifier to an existing rare item through the base Exalted wrapper.

Greater and Perfect versions do not have copied implementations. They use the same action and pass their threshold from the operation database into the already accepted MML filter.

The important safety rule is “both or neither.” For Transmutation and Regal, the engine calculates against a temporary target-rarity item. Only after a legal modifier is selected are the rarity and modifier committed together. If the item is wrong, full, or has no legal pool, the original item remains unchanged and the currency is not consumed.

This moves P2C closer to a real crafting simulator because it can cover the normal-to-magic-to-rare progression instead of operating only on prepared rare items. It still does not choose routes or advise the player, and M40-A remains proposed until Claude and ChatGPT/User accept it.
