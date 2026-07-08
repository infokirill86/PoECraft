# P2C Operation Inventory & Admission Reconciliation - Codex v1

package_id: `P2C_Operation_Inventory_Admission_Reconciliation_Codex_v1`
package_type: `OPERATION_FOUNDATION_RECONCILIATION_PROPOSAL`
status: `proposed_for_claude_audit`

observed_repo_head: `ec727da0be3860255b9d82212a28ab998c0d9d1d`
observed_active_task_sha: `de0d03b017f5612faaf0d3f8b7ae69e2d0c1db2d4b064c9a659a7be7b001d350`

## Plain-language summary for Kirill

The repo has two different ideas that currently look too similar:

1. The prepared operation catalog in `data/operations.yaml`.
2. The operations the runtime is actually accepted to execute.

Those are not the same thing.

The catalog is broad: it contains 37 operation/currency rows and 18 rows marked `active_in_current_simulation: true`.

The accepted executable runtime is narrow:

- accepted `ordinary_add` engine primitive;
- accepted base `annulment`.

The main problem is naming: `active_in_current_simulation` can be misread as "the engine can execute this operation now." That is not safe. It currently means closer to "this operation group is part of the prepared project-scope data model."

This package does not change runtime behavior. It inventories the operation catalog, classifies each entry, identifies active-flag mismatches, and proposes an explicit `runtime_admission_status` field so future work cannot confuse catalog readiness with executable acceptance.

## Boundary

This package does not:

- implement runtime code;
- accept M36 heterogeneous chains;
- accept new executable operations;
- close SOURCE/PROVENANCE, MML, or PD-013;
- release public numeric probabilities;
- claim PoE2 server truth;
- enable automation.

## Package files

- `01_OPERATION_INVENTORY_TABLE.md`
- `02_ACCEPTED_RUNTIME_AND_MISMATCH_REPORT.md`
- `03_ENGINE_PRIMITIVE_VS_CURRENCY_CATALOG.md`
- `04_SOURCE_PROVENANCE_CONSISTENCY_CHECK.md`
- `05_PROPOSED_OPERATION_ADMISSION_STATUS_MODEL.md`
- `06_RECOMMENDED_NEXT_WAVE_RISKS_STOP_TRIGGERS.md`
- `07_CLAUDE_AUDIT_REQUEST.md`
- `PACKAGE_MANIFEST.md`
- `SHA256SUMS.txt`
