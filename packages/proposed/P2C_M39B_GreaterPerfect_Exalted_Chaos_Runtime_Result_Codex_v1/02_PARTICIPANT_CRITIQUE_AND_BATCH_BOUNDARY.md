# Participant critique and batch-boundary conclusion

## Question raised before implementation

Would admitting Greater/Perfect Exalted while the game-facing base `exalted` row remains an `admission_candidate` create a material inconsistency?

## Conclusion

No blocking mechanics or architecture inconsistency was found.

Runtime admission is deliberately per catalog row. It is not inherited from the family name or from `active_in_current_simulation`. Greater/Perfect Exalted are independent currency rows and compile into the already accepted `ordinary_add` engine primitive plus a catalog-declared MML filter. Therefore their executable kernel is already accepted even though the separate base `exalted` catalog wrapper is not.

This does create a temporary interface/coverage asymmetry: a caller may resolve `greater_exalted` while `exalted` remains fail-closed. That is visible, deterministic, and automatically tested. It does not calculate a different mechanic or silently grant family-wide permission, so widening the authorized batch to base `exalted` was not justified.

## Boundary kept

The implementation admits exactly the four authorized rows. It does not admit base `exalted`, Greater/Perfect Transmutation, Augmentation, Regal, Essence, or any modifier/Omen layer.

MML values are loaded from admitted catalog rows. The code contains an allowlist for the four authorized variant IDs, but no separate mechanics function or per-variant MML table.
