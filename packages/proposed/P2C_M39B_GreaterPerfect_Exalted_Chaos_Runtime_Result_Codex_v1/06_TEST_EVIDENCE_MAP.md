# Test and evidence map

Primary M39-B evidence: `tests/monte_carlo/test_m39b_greater_perfect_exalted_chaos_runtime.py`.

| Requirement | Evidence |
|---|---|
| Exactly four new admitted catalog rows | `test_m39b_real_catalog_admits_only_the_authorized_variant_batch` |
| Correct resolver MML plans | `test_m39b_resolver_compiles_four_catalog_rows_with_row_declared_mml` |
| Exalted variants share ordinary add and filter pools | `test_m39b_exalted_variants_share_ordinary_add_and_apply_different_mml_pools` |
| Chaos MML applies after branch removal/rebuild | `test_m39b_chaos_variants_rebuild_branch_pool_then_apply_declared_mml` |
| Base Chaos removal and fractured protection unchanged | `test_m39b_chaos_mml_does_not_change_base_removal_distribution_or_fracture_guard` |
| Empty add pool remains atomic no-transition | `test_m39b_chaos_empty_add_pool_is_atomic_and_aggregates_duplicate_terminal` |
| Duplicate terminal aggregation remains canonical | same atomic empty-pool terminal test |
| Other families and modifier layers fail closed | `test_m39b_non_admitted_families_manual_mml_and_modifiers_remain_fail_closed` |
| Rare-item boundary | `test_m39b_exalted_variants_fail_closed_outside_rare_items` |
| Unexpected admitted transition shape fails closed | `test_m39b_admitted_variant_with_unexpected_transition_shape_fails_closed` |

Existing M37-A, M38-A, M39-A, static-data, foundation, M4, and full-suite regressions also ran.
