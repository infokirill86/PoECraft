# P2C Post-M35A Next-Wave Design - README

package_id: `P2C_Post_M35A_Next_Wave_Design_Codex_v1`
package_type: `PROJECT_FRONTIER_DESIGN_PROPOSAL`
status: `proposed_for_claude_audit`
author: `codex`
created_utc: `2026-07-08T19:12:32Z`

## Read receipt

- observed_repo_head: `3bb1c555e367af6c1e9ffda7b0954ae60bba0968`
- observed_active_task_sha: `15044714661969d6d1185f76e06459de02073441cccd1a4124c5ee575a5a82a1`
- acted_on_task: `POST_M35A_NEXT_GATE`

## Purpose

This package proposes the next project wave after M35-A accepted base Annulment runtime.

The proposal is design-only. It does not implement heterogeneous chains, does not add new operations, and does not update accepted truth.

## Core recommendation

Recommended next wave:

```text
M36 Heterogeneous Accepted-Operation Chain Design
```

Boundary:

- design only;
- accepted operations only: `ordinary_add` + base `annulment`;
- no Annulment variants or Omens;
- no new executable operation;
- no optimizer/economics/advice;
- no public numeric probability release;
- no SOURCE/PROVENANCE, MML, or PD-013 closure.

## Participant critique

The project should not immediately add a third operation. It now has enough operation breadth to test a more important simulator property: whether accepted operations can be connected into heterogeneous chains with exact/oracle and MC validation, replay, no-transition handling, and terminal aggregation.

Continuing only one-operation hardening would drift back into infrastructure. Jumping to Chaos/Essence/Jawbone/Reveal would move too fast into new mechanics before proving that already accepted operations compose safely.

