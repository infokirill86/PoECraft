# Participant and architecture critique

## Is M40 the right next broad wave?

Yes. After M39-B, the project has proven shared ordinary-add, MML filtering, resolver admission, and data-driven Greater/Perfect variants, but it still cannot traverse the basic rarity ladder. Adding more rare-item-only variants would deepen one end of the simulator while leaving its most recognizable crafting progression absent.

## Is the batch too broad?

No. The ten rows share one load-bearing shape:

`validated catalog row -> optional target-rarity working state -> shared ordinary weighted add pool -> optional MML -> atomic commit`

They do not introduce removal, guaranteed tagged modifiers, Omens, side overrides, multiple adds, or a planner. Splitting base and Greater/Perfect versions would create repeated gates without isolating a distinct mechanic.

## Is the batch too narrow?

No. Alchemy, Essences, Omens, and other operation families would add different counts, guaranteed outputs, or modifier layers. Including them would turn a coherent one-add admission into a generalized operation framework.

## Should base Exalted be included?

Yes. The base wrapper requires no new mechanic: it compiles directly to accepted `ordinary_add` with a rare input and no MML. Leaving it closed while Greater/Perfect Exalted are executable is a catalog/runtime asymmetry. M40 is the cleanest gate in which to resolve that asymmetry.

## Material architectural correction

Do not implement rarity progression by mutating the item first and then hoping to roll back. Also do not call the existing add builder on the original normal or magic state when the currency changes rarity.

- Transmutation needs magic-side capacity while its input is normal.
- Regal needs rare-side capacity while its input is magic.

The executor should construct an isolated working state with the target/pool-build rarity, build and sample the shared add pool there, validate the terminal state, and only then commit. This preserves correct capacity semantics and atomic failure.

## Conclusion

This is the widest safe next family. It advances the product rather than adding infrastructure for its own sake, while staying reconstructible and automatically testable through existing kernels.
