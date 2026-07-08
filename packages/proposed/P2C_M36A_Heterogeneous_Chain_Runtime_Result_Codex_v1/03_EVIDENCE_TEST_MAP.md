# Evidence / Test Map

| Requirement | Evidence |
|---|---|
| Hook setup documented | `tools/hooks/pre-push`, `manifest/GitHub_Workflow_Protocol.md`, `01_HOOK_IMPLEMENTATION_SUMMARY.md` |
| Hook/check commands run | `04_COMMANDS_AND_RESULTS.md` |
| add -> annul | `test_m36a_add_then_annul_aggregates_duplicate_terminal_and_mass_one` |
| annul -> add | `test_m36a_annul_then_add_rebuilds_add_pool_from_branch_specific_state` |
| Branch-specific pool rebuild | `test_m36a_annul_then_add_rebuilds_add_pool_from_branch_specific_state` |
| Exact rational mass conservation to 1 | add->annul and annul->add exact distribution tests |
| Terminal aggregation | add->annul aggregation test |
| Fail-closed non-admitted operation | `test_m36a_fail_closed_on_active_catalog_row_without_runtime_admission` |
| Runtime admission status required | `test_m36a_fail_closed_if_annulment_row_is_not_runtime_admitted` |
| Fractured protection through chain | `test_m36a_fractured_modifier_is_protected_through_exact_and_mc_chain` |
| Deterministic replay | `test_m36a_same_seed_and_run_id_replay_exactly` |
| Negative control | `test_m36a_negative_control_fractured_removal_pool_leak_fails` |
| Reject non-M36-A sequence shape | `test_m36a_rejects_sequences_that_are_not_two_step_heterogeneous` |
| Public summary remains numeric-probability-free | `test_m36a_public_summary_is_numeric_probability_free_metadata` |
| Existing accepted ordinary_add/Annulment behavior remains passing | M34-B1 + M35-A + full pytest regression |
