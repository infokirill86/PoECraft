# Plain-language summary for Kirill

Perfect Essence now has a proposed executable model for the six staff Essences already in our database. The engine first determines which existing modifiers may be removed without breaking the guaranteed add. It randomly chooses one of those valid removals, builds the result on an isolated copy, and installs the exact Essence modifier. Only the complete remove-plus-add result is committed.

If the needed prefix or suffix side is full, only removals from that side remain eligible. Fractured modifiers are never eligible. If no valid removal exists, or if the item already contains a crafted modifier, the operation does nothing and consumes nothing.

This does not implement replacing an earlier Essence modifier. It also does not add Perfect Seeking/Infinite, Omens, Whittling, or any other Essence tier.
