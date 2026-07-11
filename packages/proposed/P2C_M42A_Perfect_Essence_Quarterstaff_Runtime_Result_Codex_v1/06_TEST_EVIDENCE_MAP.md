# Test and evidence map

Primary test file: `tests/monte_carlo/test_m42a_perfect_essence_runtime.py`.

| Requirement | Evidence |
|---|---|
| Exact six-row admission | exact operation-set assertion; no Seeking/Infinite |
| Shared executor/canonical outputs | all six rows resolve and execute through one harness |
| Free target side | all eligible non-fractured instances remain in the pool |
| Full target side | prefix and suffix fixtures retain only capacity-creating removals |
| Empty feasible pool | unchanged no-transition/no-consumption before draw |
| Uniform exact selection | equal exact path mass and exact normalization |
| Fractured exclusion | fractured instances never appear in feasible metadata |
| `crafted_count > 0` | unchanged fail-closed result and zero decisions |
| Family/group conflict | shared canonical conflict check fails unchanged |
| Atomicity | no remove-only terminal; fixed modifier count; fractured preservation |
| Replay and seeded consistency | identical replay and one removal decision per sample |
| Bad data / unprepared row | missing canonical mod and Perfect Seeking fail closed |
| Regression | M39-B, M40-A, M41-A, foundation admission, fingerprint, full suite |
