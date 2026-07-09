# P2C M37 Chaos-like Remove-Then-Add Design - Codex v1

package_id: `P2C_M37_ChaosLike_RemoveThenAdd_Design_Codex_v1`
package_type: `DESIGN_ONLY_PROPOSAL`
status: `proposed_for_claude_audit`

observed_repo_head: `1807b29547c47fb33139f2471fd39e0b3c59a0c6`
observed_active_task_sha: `20644bb694248418058202286c4e03feb0c5f6379fef95e69514fccf0d7a0dff`

## Plain-language summary for Kirill

M36-A proved the engine can safely connect two accepted operations in a fixed chain.

M37 should now design the first real game-facing composite candidate: a Chaos-like operation that removes one removable modifier, rebuilds the add pool from the changed item, then adds one legal modifier.

This is design only. It does not implement Chaos runtime and does not mark Chaos as accepted executable runtime.

The recommended next implementation floor is M37-A base Chaos-like `remove_then_add` only:

- no Omens;
- no Whittling;
- no Chaos variants beyond the base candidate;
- no optimizer/advice/economics;
- no public numeric probability release.

## Files

- `01_PARTICIPANT_CRITIQUE.md`
- `02_SOURCE_DATA_GROUNDING.md`
- `03_ENGINE_PRIMITIVE_VS_CURRENCY.md`
- `04_CHAOSLIKE_CANDIDATE_SEMANTICS.md`
- `05_EDGE_CASE_TABLE.md`
- `06_EXACT_ORACLE_DESIGN.md`
- `07_MC_REPLAY_DIAGNOSTICS_DESIGN.md`
- `08_GATED_SCOPE_AND_M37A_FLOOR_PROPOSAL.md`
- `09_RISKS_STOP_TRIGGERS.md`
- `10_CLAUDE_AUDIT_REQUEST.md`
- `PACKAGE_MANIFEST.md`
- `SHA256SUMS.txt`

