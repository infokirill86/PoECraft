# P2C Project Next Move Proposal — README

package_id: `P2C_Project_Next_Move_Proposal_Codex_v1`
package_type: `PROJECT_NEXT_MOVE_PROPOSAL`
status: `proposed_for_claude_audit`
author: `codex`

observed_repo_head: `d7fb8bdcf3569c85428c492c8dc91d32c18cb5c0`
observed_active_task_sha: `327f12fd35ed58dbe9312eb00e9eb6f8bfe4fbf09693c2df27efa7d5e405c94f`

## Plain-language summary

P2C is trying to become a Path of Exile 2 crafting simulator, not only an `ordinary_add` Monte Carlo testbed.

After M34-B1, continuing to harden only `ordinary_add` is no longer the highest-value next move. It is useful, but it risks drifting into infrastructure work while the simulator still cannot execute most real crafting operations.

Recommended next move:

```text
Design an Operation Admission Framework, then use it to prepare the first new real operation candidate.
Preferred first candidate: Annulment.
```

This package is design/proposal only. It does not implement Annulment, does not add new executable mechanics, and does not update accepted truth.

## Files

- `01_PROJECT_REALITY_CHECK.md`
- `02_CURRENT_CAPABILITY_MAP.md`
- `03_MISSING_CAPABILITY_MAP.md`
- `04_STRATEGIC_OPTIONS_COMPARISON.md`
- `05_RECOMMENDED_NEXT_MOVE.md`
- `06_BATCHED_AND_GATED_SCOPE.md`
- `07_RISKS.md`
- `08_IMPLEMENTATION_AND_AUDIT_PLAN.md`
- `09_PROMPT_PATTERN_IMPROVEMENTS.md`
- `10_CLAUDE_AUDIT_REQUEST.md`
- `PACKAGE_MANIFEST.md`
- `SHA256SUMS.txt`

## Human decision status

Claude audit is requested next. ChatGPT/User must decide whether to accept this next-move proposal and authorize a later design or implementation floor.
