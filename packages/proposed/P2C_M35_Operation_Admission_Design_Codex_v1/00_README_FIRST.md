# P2C M35 Operation Admission Design - README

package_id: `P2C_M35_Operation_Admission_Design_Codex_v1`
package_type: `DESIGN_ONLY_PROPOSED_DELTA`
status: `proposed_for_claude_audit`
author: `codex`
created_utc: `2026-07-08T17:27:05Z`

## Read receipt

- observed_repo_head: `c9628dee2cfd4a242f2a27d6550a8afa020631e7`
- observed_active_task_sha: `7df9f0655f4dbe051246db7cca71caa407dbea4f279228e7cc573abc81313cef`
- acted_on_task: `PROJECT_NEXT_MOVE_REVIEW`

## Purpose

This package defines M35 as a design-only operation-admission step.

It accepts the strategic direction from `P2C_Project_Next_Move_Proposal_Codex_v1` after Claude GO audit and turns it into a lean design contract for:

1. admitting future operations without ad-hoc implementation;
2. using Annulment as the first candidate operation design;
3. keeping Annulment runtime implementation behind a later M35-A gate.

## Participant critique

The M35 boundary is strategically correct and right-sized.

Continuing only `ordinary_add` hardening would keep improving a well-tested foundation but would not materially move P2C toward a real crafting simulator. Implementing Annulment immediately would move too fast because the repo lacks an accepted operation-admission contract for non-add operations.

The better boundary is therefore:

- design the admission framework now;
- anchor it to Annulment, not to a broad abstract operation algebra;
- require fractured-mod protection, no-transition behavior, exact/oracle shape, replay, diagnostics, and negative controls;
- defer executable Annulment runtime to M35-A after audit and explicit ChatGPT/User authorization.

## Non-authorization statement

This package does not implement Annulment, does not add executable mechanics, does not accept Annulment as runtime behavior, does not close SOURCE/PROVENANCE, MML, or PD-013, and does not release public numeric probabilities.

