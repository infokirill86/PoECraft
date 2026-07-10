# Test and evidence map

Primary test file: `tests/monte_carlo/test_m41a_greater_essence_runtime.py`.

| Requirement | Evidence |
|---|---|
| Exact eight-row admission | exact activation-set assertion; Perfect rows remain non-admitted |
| Canonical modifier resolution | all eight rows cross-check output data and canonical index |
| Guaranteed deterministic install | all eight expected terminal hashes; exact mass is one |
| No weighted/random draw | zero decision records and zero candidates across seeded replay |
| Preserve existing/fractured mods | fractured-instance atomic preservation test |
| No-transition/no-consumption | invalid rarity, family conflict, and crafted-capacity cases preserve input hash |
| Fail closed on bad data | missing canonical mod, inconsistent output row, and tampered operation contract tests |
| Resolver admission | only exact admitted ids compile; Perfect Essence fails closed |
| Regression safety | M39-B, M40-A, static fingerprint, validators, and full pytest suite |
