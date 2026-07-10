# Claude audit request

Please audit `P2C_M40A_Rarity_Progression_Runtime_Result_Codex_v1` from the committed repo bytes.

## Required audit focus

1. Reassess the ten-row batch and participant critique; do not rubber-stamp task framing.
2. Confirm one shared data-driven executor is load-bearing for all ten rows.
3. Confirm Transmutation builds at target magic rarity and Regal at target rare rarity.
4. Confirm rarity and added modifier commit atomically and every failure preserves the original state/no consumption.
5. Confirm Augmentation opposite-side behavior comes only from magic capacity/legal filtering.
6. Confirm base Exalted uses the accepted combined generation-weight pool, not side-first selection.
7. Confirm row thresholds and exact official/PoE2DB source references are correct and remain source-open.
8. Confirm current modifier count is mutable, fractured modifiers consume their actual side capacity, and the current fractured suffix staff is not a global invariant.
9. Confirm exact mass, seeded replay, diagnostics, negative controls, and full regressions are sufficient.
10. Confirm only the ten authorized rows were added and all forbidden surfaces remain fail-closed.
11. Confirm M40-A is proposed rather than self-accepted and `ACTIVE_TASK.md` routes correctly.

Return `GO`, `GO WITH CHANGES`, or `NO-GO`, with severity and exact files for corrections. Include a plain-language summary for Kirill, `observed_repo_head`, and SHA-256 of the exact ACTIVE_TASK bytes audited.
