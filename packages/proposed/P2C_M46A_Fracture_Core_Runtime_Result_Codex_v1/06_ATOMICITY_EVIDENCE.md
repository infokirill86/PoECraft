# Atomicity Evidence

Fracture builds and validates the complete candidate pool before any selection. The original immutable `ItemState` is never modified in place.

Invalid rarity, insufficient installed modifiers, an existing fracture, Desecrated state, an unrevealed placeholder, unknown installed data, invalid source state, unsupported operation form, or an empty pool returns explicit no-transition/no-consumption with the original state hash unchanged.

On success, one terminal state is constructed and validated before it is returned. There is no intermediate caller-visible mutation.
