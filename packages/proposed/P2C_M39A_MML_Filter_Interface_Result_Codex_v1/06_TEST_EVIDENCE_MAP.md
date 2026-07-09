# Test and evidence map

## New/updated tests

File: `tests/monte_carlo/test_m38a_operation_resolver.py`

| Evidence | Test |
|---|---|
| Resolver reports M39-A schema version | `test_m38a_schema_and_single_operation_contract_are_pinned` |
| Explicit MML compiles into `OrdinaryAddOperation` | `test_m39a_explicit_mml_filter_compiles_to_ordinary_add_and_narrows_pool` |
| MML narrows add pool through shared builder | `test_m39a_explicit_mml_filter_compiles_to_ordinary_add_and_narrows_pool` |
| Greater/Perfect rows remain not admitted | `test_m38a_does_not_infer_runtime_permission_from_active_catalog_flag` |
| MML does not admit base Chaos / Greater variant behavior | `test_m39a_mml_filter_does_not_admit_catalog_or_greater_perfect_runtime` |
| Unsupported variants fail closed | `test_m38a_rejects_greater_perfect_variant_layers_for_admitted_base_currency` |
| Invalid MML thresholds fail closed | `test_m39a_mml_filter_fails_closed_on_invalid_thresholds` |
| Public summary stays metadata-only | `test_m38a_public_summary_is_metadata_only` |

## Validation commands

```text
python tools/validate_foundation.py
PASS

python tools/validate_m4.py
PASS

python -m pytest tests/monte_carlo/test_m38a_operation_resolver.py tests/legality/test_m5_pool_builders.py -q
22 passed

python -m pytest -q
151 passed
```

Repo integrity commands were run after package/status updates.

