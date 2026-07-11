# Risks and Rollback Plan

## Risks

| Risk | Mitigation |
|---|---|
| Removing stale prose accidentally changes accepted truth | Cleanup must replace volatile claims with ledger references, not invent new truth; Claude audits the delta |
| Deleting legacy task files loses evidence | Git history plus packages/reviews retain it; verify references before removal |
| Moving accepted packages breaks links | Do not move packages; add lifecycle metadata instead |
| New index becomes another competing truth surface | Index is lifecycle/navigation only; accepted ledger remains authority |
| ACTIVE_TASK becomes too small to enforce safety | Keep mandatory schema and standing-boundary reference; remove only duplicated prose/sibling files |
| Tooling changes create false confidence | Add focused tests and known negative controls; keep local/manual |
| M43 decision is lost during hygiene work | Record M43 as Claude-GO/proposed and return to its user gate after cleanup |

## Rollback

- Perform cleanup in one dedicated commit.
- Do not squash away the pre-cleanup checkpoint.
- Verify every removed path exists in the parent commit.
- If Claude finds a regression, revert the cleanup commit as a unit; do not hand-restore selected files.
- Re-run ACTIVE_TASK validation, reference checks, root SHA, full pytest, foundation/M4 validators, and pre-push hook before publication.

The audit itself is documentation only and requires no rollback beyond reverting its single package/status commit.
