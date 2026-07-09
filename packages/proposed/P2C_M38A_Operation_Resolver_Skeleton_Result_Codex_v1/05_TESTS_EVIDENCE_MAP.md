# Tests and evidence map

Added test file:

- `tests/monte_carlo/test_m38a_operation_resolver.py`

Evidence coverage:

| Evidence requirement | Test coverage |
|---|---|
| schema and single-operation contract pinned | `test_m38a_schema_and_single_operation_contract_are_pinned` |
| accepted `ordinary_add` dispatch | `test_m38a_schema_and_single_operation_contract_are_pinned` |
| accepted base Annulment dispatch | `test_m38a_resolves_only_already_accepted_catalog_runtime_operations` |
| accepted base Chaos-like dispatch | `test_m38a_resolves_only_already_accepted_catalog_runtime_operations` |
| active catalog row is not enough for execution | `test_m38a_does_not_infer_runtime_permission_from_active_catalog_flag` |
| Greater/Perfect variant layers fail closed | `test_m38a_rejects_greater_perfect_variant_layers_for_admitted_base_currency` |
| Omen/Whittling modifier layers fail closed | `test_m38a_rejects_omen_and_modifier_layers_without_admitting_filter_runtime` |
| revoked runtime status fails closed | `test_m38a_fail_closed_when_catalog_runtime_status_is_revoked` |
| unknown currency fails closed | `test_m38a_rejects_unknown_currency_or_operation` |
| public summary is metadata-only | `test_m38a_public_summary_is_metadata_only` |

No public numeric probability release is introduced.

