# Minimal Cleanup Implementation Plan

## Wave A — routing repair (highest priority)

1. Change README, AGENTS, and CLAUDE read order to verified HEAD → ACTIVE_TASK → validator → context.
2. Remove the three completed task files from `work/active/` current tree.
3. Extend ACTIVE_TASK validator to require exactly one tracked file under `work/active/`.
4. Slim ACTIVE_TASK human summary to actor/action plus one short boundary sentence.
5. Add a binding truth-precedence paragraph to workflow protocol.

## Wave B — canonical truth repair

1. Make START_HERE timeless and remove stale current-operation/fractured-invariant claims.
2. Correct Operating Manifest status and replace volatile runtime inventory with references to accepted ledger/current status.
3. Remove the historical convergence appendix from GitHub Workflow Protocol; Git history remains the archive.
4. Replace stale validator/runtime statements.
5. Make CURRENT_STATUS an accepted/proposed snapshot only; all live routing points to ACTIVE_TASK.
6. Refresh OPEN_BLOCKERS wording without closing any blocker.

## Wave C — evidence lifecycle repair

1. Add compact package lifecycle index.
2. Link A1/A2 and Layer-A source-bundle evidence from accepted ledger.
3. Mark Post-M35A next-wave proposal/review superseded.
4. Document that physical package paths are immutable and folder name is not acceptance authority.

## Wave D — checker scoping

1. Add source-bundle exception support to nested-ZIP checker.
2. Make leak scan accept explicit public surfaces and labels/allowlists.
3. Add canonical-reference/lifecycle checks only if Wave A–C cannot keep the state consistent manually.

## Recommended batching

Waves A and B should be one documentation/tooling cleanup delta because they repair one observed failure and must remain internally consistent. Wave C may join if the diff stays reviewable. Wave D should be separate unless required to make the cleaned structure self-checking.

No runtime, mechanics, data semantics, operation admission, M43-A, public output, optimizer, economics, automation, or boundary closure belongs in these waves.
