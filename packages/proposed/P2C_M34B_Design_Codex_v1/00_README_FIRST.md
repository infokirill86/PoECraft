# M34-B Design Package — README

package_id: `P2C_M34B_Design_Codex_v1`
package_type: `DESIGN_ONLY_PROPOSED_DELTA`
status: `proposed_for_claude_audit`
author: `codex`

observed_repo_head: `2bfc98f9a9042bf331422af94e8e033141019002`
observed_active_task_sha: `1d0bcc120770bf3857e0815bec5ce6e435098bfad147fd94fee727f7a3cf719b`

## Plain-language summary

This package defines M34-B as a design-only next step after accepted M34-A.

M34-B is not implementation. It does not add code, tests, mechanics, operations, optimizer behavior, economics, or public probability release.

The safer boundary selected here is:

- M34-B1: validate a pinned two-step sequence composed only of accepted `ordinary_add` steps.
- Later expansion beyond two steps is deferred to a separate gate after M34-B1 audit.

Why this matters: M34-A proved single-step Monte Carlo hardening across multiple seeds. M34-B should now check the next real risk: whether state, legality, and pools are rebuilt correctly after one accepted ordinary add before a second accepted ordinary add.

## Files

- `01_TASK_CRITIQUE_AND_BOUNDARY.md`
- `02_DESIGN_CONTRACT_PINNED_SCOPE.md`
- `03_SEQUENCE_MODEL_DEFINITION.md`
- `04_ACCEPTED_AND_FORBIDDEN_INPUTS.md`
- `05_VALIDATION_PLAN.md`
- `06_REPLAY_AND_DIAGNOSTICS_PLAN.md`
- `07_EXACT_ORACLE_COMPARISON_PLAN.md`
- `08_ACCEPTANCE_CRITERIA_AND_NON_GOALS.md`
- `09_RISK_REGISTER.md`
- `10_CLAUDE_AUDIT_REQUEST.md`
- `PACKAGE_MANIFEST.md`
- `SHA256SUMS.txt`

## Human decision status

This package is proposed only. Claude audit is requested next. ChatGPT/User acceptance is required before any M34-B implementation starts.
