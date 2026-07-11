# Claude Audit Request

Please audit `P2C_Repo_Structure_Truth_Surface_Audit_Codex_v1` as a proposed structure/truth-surface audit.

## Required audit questions

1. Does the evidence support the root-cause finding that repeated stale-task errors are structural rather than merely agent inattentiveness?
2. Is verified remote HEAD → ACTIVE_TASK → validator the correct mandatory read order?
3. Should `work/active/` contain exactly one tracked file?
4. Are START_HERE, Operating Manifest, Workflow Protocol, CURRENT_STATUS, and OPEN_BLOCKERS correctly identified as stale or role-confused?
5. Is removing the historical convergence appendix from the canonical protocol safe because Git history preserves it?
6. Is keeping accepted package paths fixed and adding lifecycle metadata safer than mass-moving them?
7. Are the underlinked/superseded packages and reviews correctly classified?
8. Are scanner gaps correctly distinguished from actual package/leak violations?
9. Is the proposed Wave A+B cleanup the smallest effective repair?
10. Does any proposed cleanup risk changing accepted truth or losing evidence?

Return `GO`, `GO WITH CHANGES`, or `NO-GO`, with severity-ranked corrections and a plain-language summary for Kirill.

Record `observed_repo_head` and SHA-256 of the exact `ACTIVE_TASK.md` bytes audited. Do not implement cleanup, accept M43, start M43-A, move/delete evidence, change mechanics, or close any standing boundary.
