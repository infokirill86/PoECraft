# Plain-Language Summary for Kirill

## What the simulator can do now

P2C can build a quarterstaff through rarity changes, add and remove modifiers, perform Chaos-like replacement, and apply Greater or Perfect Essences. It already knows many useful individual crafting actions.

## What is stopping it from feeling like a route simulator

Those actions still live mostly as separate tools. The accepted mixed-chain layer handles only a very small two-step case. A real crafting route needs several accepted actions in a chosen order, with every later action seeing the actual item produced by the earlier ones.

## Recommended M43

Build the design for a bounded sequence runner: the caller supplies a fixed list of already accepted actions, and P2C evaluates that exact list. The engine does not invent, rank, or recommend a route.

This is now higher value than adding one more currency. It turns the operation collection into the beginning of a usable simulator while staying mechanically conservative: every step still uses an already accepted operation and its existing legality rules.

## What remains separate

Omens are the next strong mechanics-layer candidate because they control Exalted, Annulment, Chaos, and Perfect Essence behavior. They remain a separate gate because the live Omen catalogue and several interaction rules need reconciliation. Fracture is also deferred because the active route intentionally starts from a purchased fractured staff rather than simulating how that base was created.
