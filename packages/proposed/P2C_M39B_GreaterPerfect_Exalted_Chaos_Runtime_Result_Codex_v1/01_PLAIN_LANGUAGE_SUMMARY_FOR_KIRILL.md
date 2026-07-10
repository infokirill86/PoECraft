# Plain-language summary for Kirill

P2C can now propose executing the stronger Exalted and Chaos variants without inventing four separate mechanics implementations.

- Greater/Perfect Exalted reuse the already trusted "add one legal modifier" engine. Their only additional input is the fixed minimum modifier level stored in the operation catalog.
- Greater/Perfect Chaos reuse the already trusted base Chaos process: choose a removable non-fractured modifier, remove it on a branch copy, rebuild the legal add pool, filter that rebuilt pool by the variant's minimum level, then add and commit atomically.

Why this matters: the simulator gains four real game-facing catalog operations while keeping one shared mechanics kernel. A bug fix to ordinary add or base Chaos therefore remains shared instead of being copied into variant-specific functions.

The base game-facing `exalted` row is still not admitted. That is intentional in this floor: its mechanics already exist as accepted `ordinary_add`, but accepting its catalog wrapper is a separate permission decision. This asymmetry is visible and fail-closed; it does not make the four admitted variants use an untrusted mechanic.

What remains proposed: all M39-B code/data changes and the four runtime admissions. Claude is next. ChatGPT/User acceptance is still required after audit.
