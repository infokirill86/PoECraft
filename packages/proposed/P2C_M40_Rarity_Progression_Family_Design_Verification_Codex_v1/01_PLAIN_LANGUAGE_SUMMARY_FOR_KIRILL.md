# Plain-language summary for Kirill

Today the simulator can add a modifier to a rare item, remove one, and do the accepted Chaos-like remove-then-add operation. It cannot yet model the ordinary early crafting progression from a white item to a blue item and then to a yellow item.

M40 fills that architectural gap without inventing four unrelated implementations:

1. Transmutation changes a normal item to magic and adds one modifier.
2. Augmentation adds the missing modifier to a magic item.
3. Regal changes a magic item to rare and adds one modifier.
4. Exalted adds one modifier to a rare item.

Greater and Perfect versions use the same operation, but filter the add pool by their declared Minimum Modifier Level (MML). The filter already exists as an accepted interface; this design does not close the broader MML evidence question.

The main safety point is atomicity. For Transmutation and Regal, the engine must temporarily evaluate the item at its target rarity so the correct prefix/suffix capacity is used. If no legal modifier can be added, it must not leave behind a partially upgraded item or consume the currency.

The package recommends one broad future M40-A implementation batch for all ten rows. That is efficient because the rows differ only in input/output rarity and MML data. It still requires Claude review of this design and a separate ChatGPT/User authorization before code or runtime admission.
