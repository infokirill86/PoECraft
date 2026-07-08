# P2C M36 Heterogeneous Chain Design - Codex v1

package_id: `P2C_M36_Heterogeneous_Chain_Design_Codex_v1`
package_type: `DESIGN_ONLY_PROPOSAL`
status: `proposed_for_claude_audit`

observed_repo_head: `7286c2436d8b3d5d94aa56a65aa54c77cd2b2a86`
observed_active_task_sha: `5ce04194dd407e85829e4c2a5380bab3b055f2ad5e2170faa1ac610fd106ea90`

## Plain-language summary for Kirill

The simulator can now execute two accepted project-model behaviors:

- `ordinary_add`: add one legal modifier through the accepted add primitive;
- base `annulment`: remove one removable non-fractured modifier.

M36 should design how to safely compose those already accepted behaviors into short fixed chains, for example:

- add then annul;
- annul then add.

This is useful because real crafting is not one isolated click. A useful simulator needs to understand "what state do I get after step one, and what is legal at step two?"

This package is design only. It does not implement mixed chains and does not admit Chaos, Essence, Fracture, Jawbone, Reveal, or any other operation.

## Core recommendation

Proceed with M36 design now, but keep the boundary tight:

- fixed sequences only;
- accepted operations only;
- no planner;
- no optimizer;
- no new operation admission;
- no public numeric release.

The recommended later implementation floor is M36-A: two-step heterogeneous chain runtime hardening over accepted `ordinary_add` and accepted base Annulment only.

## Files

- `01_PARTICIPANT_CRITIQUE.md`
- `02_DESIGN_CONTRACT.md`
- `03_ACCEPTED_OPERATION_SET.md`
- `04_CHAIN_MODEL.md`
- `05_EXACT_ORACLE_PLAN.md`
- `06_MC_REPLAY_DIAGNOSTICS_PLAN.md`
- `07_VALIDATOR_FAIL_CLOSED_REQUIREMENTS.md`
- `08_BATCHED_GATED_SCOPE_AND_RISKS.md`
- `09_M36A_IMPLEMENTATION_FLOOR_PROPOSAL.md`
- `10_CLAUDE_AUDIT_REQUEST.md`
- `PACKAGE_MANIFEST.md`
- `SHA256SUMS.txt`
