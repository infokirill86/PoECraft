# Evidence / Test Map

| Requirement | Evidence |
|---|---|
| Base Chaos remove_then_add happy path | `test_m37a_base_chaos_happy_path_exact_mass_and_combined_add_weights` |
| No removable modifiers -> no-transition/no-consumption | `test_m37a_no_removable_modifiers_no_transition_no_consumption` |
| Fractured modifiers excluded from removal | `test_m37a_fractured_modifiers_are_never_removed_exact_or_mc` |
| Uniform removal over eligible instances | `test_m37a_uniform_removal_over_eligible_non_fractured_instances` |
| Add uses combined generation_weight pool, not fixed side-first split | `test_m37a_base_chaos_happy_path_exact_mass_and_combined_add_weights` |
| Post-removal add pool rebuilt from branch-specific state | `test_m37a_rebuilds_add_pool_from_branch_specific_post_removal_state` |
| Removal succeeds but no add pool -> no partial remove-only result | `test_m37a_empty_post_removal_add_pool_does_not_commit_partial_remove` |
| Duplicate terminal aggregation | `test_m37a_duplicate_terminal_aggregation_sums_paths` |
| Deterministic replay | `test_m37a_same_seed_and_run_id_replay_exactly` |
| Fail-closed non-admitted operation | `test_m37a_fail_closed_non_admitted_operation_and_variants` |
| Negative control / hard-fail diagnostics | `test_m37a_negative_control_fractured_removal_pool_leak_fails` |
| Public summary remains numeric-probability-free | `test_m37a_public_summary_is_numeric_probability_free_metadata` |
| Existing ordinary_add / Annulment / M36-A tests remain passing | `python -m pytest tests/monte_carlo -q` |

## Not covered by M37-A

- Whittling runtime.
- Side Omen runtime.
- Greater/Perfect Chaos MML runtime.
- Public numeric release.
- Optimizer/economics/advice.
- Server-truth probability validation.

