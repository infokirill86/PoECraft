# P2C M35-A Annulment Runtime Result - README

package_id: `P2C_M35A_Annulment_Runtime_Result_Codex_v1`
package_type: `IMPLEMENTATION_RESULT_DELTA`
status: `proposed_for_claude_audit`
author: `codex`
created_utc: `2026-07-08T17:27:05Z`

## Read receipt

- observed_repo_head: `b085bfca15b312c1f840114cc9133b7c6b2c59e1`
- observed_active_task_sha: `cb2af7bc9811812781ede7cfbe244aee5a2187d55cbbfe2666d309a70f53768f`
- acted_on_task: `M35_OPERATION_ADMISSION_DESIGN`

## Purpose

This package reports the M35-A Annulment Runtime Admission implementation.

M35-A admits only base Annulment runtime behavior as a proposed implementation for audit. It does not self-accept Annulment, does not accept full M35, and does not authorize additional operations.

## Scope guard

Implemented:

- base Annulment runtime harness;
- exact/oracle enumeration;
- seeded MC sampling and deterministic replay;
- shared removal-pool dependency;
- fractured-removal protection;
- empty-pool no-transition/no-consumption;
- duplicate-instance terminal aggregation;
- fail-closed unsupported operation checks;
- tests and validation evidence.

Not implemented:

- Chaos;
- Essence;
- Fracture;
- Desecrate;
- Jawbone;
- Reveal;
- optimizer/economics/advice;
- public numeric probability release;
- automation.

