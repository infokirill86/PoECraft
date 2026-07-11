# Package and Review Lifecycle Report

## Inventory

- Tracked package directories under `packages/proposed/`: 37.
- Package directories explicitly referenced by accepted ledger: 33.
- Current audited but not accepted M43 package: 1.
- Other reviewed/supporting/superseded package directories without direct accepted-ledger package reference: 3.
- Review files: 40, including proposal audits, re-audits, and one README.
- `packages/accepted/`: README only.

## Underlinked or ambiguous package surfaces

| Package | Actual lifecycle | Required future record |
|---|---|---|
| `P2C_M32_A1_A2_Baseline_Hygiene_Result_Codex_v1` | A1/A2 accepted in CURRENT_STATUS/DECISIONS | Add direct accepted-ledger row/path |
| `P2C_Source_Bundle_Byte_Verification_Result_Codex_v1` | Supporting evidence for accepted Layer A import fidelity | Link package and both audits from Repo baseline ledger row |
| `P2C_Post_M35A_Next_Wave_Design_Codex_v1` | Reviewed GO WITH CHANGES; superseded by accepted operation reconciliation | Mark explicitly `superseded`, keep immutable evidence |
| `P2C_M43_Next_Project_Wave_Design_Codex_v1` | Claude GO, pending ChatGPT/User direction decision | Remain proposed/current until gate |

## Reviews without direct canonical filename reference

The reference scan found early proposal/re-audit files that are evidence but are not directly named in current accepted/status surfaces, including:

- `ACTIVE_TASK_SCHEMA_V2_Proposal_Audit_Claude_v1.md`;
- Layer-A initial audit and re-audit;
- M32 A1/A2 audit;
- M33 P0 audit;
- M34 design/M34-A audits;
- Post-M35A next-wave audit.

These are not safe to call garbage. Most are superseded or supporting evidence. They need lifecycle links, not deletion.

## Recommended path policy

Do not mass-move 33 accepted package directories. That would create hundreds of changed paths and break immutable references.

Instead:

1. Treat package path as immutable origin location.
2. Add one compact `packages/PACKAGE_LIFECYCLE_INDEX.md` generated or checked against ledgers.
3. Define `packages/proposed/` as “created as proposed,” not current acceptance status.
4. Keep accepted truth exclusively in the accepted ledger.
5. Remove or repurpose the empty `packages/accepted/README.md` only after the policy is accepted.
