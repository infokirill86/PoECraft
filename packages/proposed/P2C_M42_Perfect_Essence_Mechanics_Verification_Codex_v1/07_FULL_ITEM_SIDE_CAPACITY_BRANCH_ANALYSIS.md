# Full-item and side-capacity branch analysis

Example: a full Rare item has three prefixes and three suffixes; the selected Perfect Essence guarantees a prefix.

| Candidate model | Result | Evidence posture |
|---|---|---|
| Uniform over all removable instances, opposite-side removal becomes rollback | Some selected paths consume no currency and return unchanged | Compatible with literal unqualified “random,” but not supported by observed behavior |
| Currency is unusable whenever target side is full | Rejects even though removing a target-side mod could make space | Inconsistent with reports of successful full-item use |
| Filter removal pool to outcomes that allow guaranteed add | Only removable prefixes are eligible when prefix side is full; all removable instances may be eligible when target side already has space | Best match to community observations and atomic semantics; exact primary wording is absent |

Recommended project-model candidate for a later explicit gate:

1. Build the removable non-fractured instance pool.
2. Retain only removal instances whose branch-specific post-removal state can accept the guaranteed modifier by family/group, item class, target-side capacity, and crafted-capacity policy.
3. Base selection is uniform over that feasible pool.
4. If the feasible pool is empty, return no-transition/no-consumption before any draw.
5. Omen filters, when separately admitted later, intersect this pool and do not redefine base Perfect Essence.

This recommendation is not accepted truth in M42. Claude and ChatGPT/User must review it because it changes exact probabilities relative to the current unconditioned YAML wording.
