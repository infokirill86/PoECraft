# P2C - Accepted Artifacts Ledger

Keep compact. This is not proof by itself; active audits require real bytes.

| Stage | Artifact | Status | SHA256 / note | Path |
|---|---|---|---|---|
| Operating | Operating_Manifest_v4.md | accepted baseline | see file hash in git | manifest/Operating_Manifest_v4.md |
| Operating | Participant_Voice_Charter.md | accepted | see file hash in git | manifest/Participant_Voice_Charter.md |
| M31 | Monte Carlo policy blueprint + C-1 | accepted after folded C-1 | package bytes in archive / add if active | packages/accepted or archive |
| M32 | Seeded MC harness (Layer B) | accepted - User gate 2026-07-07 on Claude GO audit | audited from repo bytes @ fc2c5a5; audit `reviews/M32_Audit_Claude_v1.md` | packages/proposed/P2C_M32_Seeded_MC_Harness_Result_Codex_v1 |
| Repo baseline | GitHub runtime/data/config/schema/tool import (Layer A) | accepted and pinned - User gate 2026-07-08 | provenance: imported from local origin working tree `Documents/GitHub/PoECraft`; byte-verified exact by Claude 79 of 79, 0 differ, 0 missing; Codex package-surface comparison `d20dcd67c5b654802ce13e3cdcf1e805eccb5bf1b45d431beac586a37e4753eb`; no prior formal runtime package existed | `src/p2c_engine/`, `data/`, `config/`, `schemas/`, `tools/validate_*` |
| M33-P0 | Oracle-convergence foundation partial | accepted as partial only - User gate 2026-07-08 after Claude GO WITH CHANGES | shared-kernel enforcement sufficient for P0; not full M33; no claim of statistically proven MC convergence | packages/proposed/P2C_M33_Oracle_Convergence_Result_Codex_v1 |
| M33-P1 | Statistical convergence delta | accepted - User gate 2026-07-08 after Claude GO audit | resolved P0 blocking items: statistical per-branch tolerance, sample-count tiers, fixed seed/divergence policy, broader ordinary-add fixture | packages/proposed/P2C_M33_P1_Statistical_Convergence_Result_Codex_v1 |
| M33 | Oracle-convergence validation | accepted as completed for accepted `ordinary_add` only - User gate 2026-07-08 | validates seeded MC harness convergence against exact/oracle layer for accepted `ordinary_add`; no M34, no optimizer/economics, no public numeric release, no server-truth claim | M33-P0 + M33-P1 + `reviews/M33_P1_Statistical_Convergence_Audit_Claude_v1.md` |
| M34 design | MC-hardening design/definition | accepted as plan - User gate 2026-07-08 after Claude GO audit | design-only plan; recommends M34-A before M34-B; does not authorize M34-B or full M34 acceptance | packages/proposed/P2C_M34_MC_Hardening_Design_Definition_Codex_v1 |

## Note

Layer A acceptance is a project-model GitHub baseline acceptance only. It does not claim server truth and does not close SOURCE/PROVENANCE, MML, or PD-013.

M33 acceptance is scoped to accepted `ordinary_add` only. It does not start M34 and does not close SOURCE/PROVENANCE, MML, or PD-013.

M34 design acceptance is plan acceptance only. M34-A/M34-B/full M34 require separate gates.
