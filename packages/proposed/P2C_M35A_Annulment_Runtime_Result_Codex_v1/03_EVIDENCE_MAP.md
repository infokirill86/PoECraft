# Evidence Map

| Requirement | Evidence |
|---|---|
| Fractured modifier is never removed | `test_m35a_fractured_modifier_is_never_removed_by_exact_or_mc_path`; runtime pool validation rejects fractured candidates |
| Shared removal-pool path is load-bearing | `test_m35a_exact_and_mc_use_same_shared_removal_pool_path`; harness default is `build_removal_pool` |
| Empty pool no-transition/no-consumption | `test_m35a_empty_pool_no_transition_no_mutation_and_exact_mass_one` |
| Empty no-transition does not mutate state | Same empty-pool test checks unchanged state hash |
| Exact mass over empty no-transition is complete | Same empty-pool test checks exact terminal distribution status |
| Uniform exact/oracle path probabilities over removable instances | `test_m35a_exact_paths_are_uniform_over_non_fractured_installed_instances` |
| Path identity distinct from terminal identity | `ExactAnnulmentPath.path_key` vs `ExactAnnulmentTerminalOption.terminal_state_hash` |
| Duplicate-instance terminal aggregation | `test_m35a_duplicate_instance_terminal_aggregation_sums_paths` |
| Deterministic replay | `test_m35a_same_seed_and_run_id_replay_exactly` |
| Hard-fail negative control | `test_m35a_negative_control_fails_on_fractured_candidate_leak` |
| Fail-closed unsupported operation variants | `test_m35a_fail_closed_on_unsupported_operation_and_rarity` |
| Existing accepted `ordinary_add` remains unchanged | Monte Carlo suite and full pytest passed |
| No public numeric probability release | Public summaries are metadata-only; leak scan run on package |

