# P2C — Accepted Artifacts Ledger

Keep compact. This is not proof by itself; active audits require real bytes.

| Stage | Artifact | Status | SHA256 / note | Path |
|---|---|---|---|---|
| Operating | Operating_Manifest_v4.md | accepted baseline | see file hash in git | manifest/Operating_Manifest_v4.md |
| Operating | Participant_Voice_Charter.md | accepted | see file hash in git | manifest/Participant_Voice_Charter.md |
| M31 | Monte Carlo policy blueprint + C-1 | accepted after folded C-1 | package bytes in archive / add if active | packages/accepted or archive |
| M32 | Seeded MC harness (Layer B) | **accepted** — User gate 2026-07-07 on Claude GO audit | audited from repo bytes @ fc2c5a5; audit `reviews/M32_Audit_Claude_v1.md` | packages/proposed/P2C_M32_Seeded_MC_Harness_Result_Codex_v1 |
| M32 | GitHub baseline import (Layer A) | **PROPOSED — not accepted** | pending A1 (deps) + A2 (kernel tests/pin); see audit | src/, data/, config/, schemas/, tools/validate_* |

## Note
This ledger will be filled as repo migration proceeds. Do not bulk-import old packages by default.
M32 acceptance covers the seeded MC harness only (Layer B). The imported baseline runtime/data/config/
schema/tool support (Layer A) stays PROPOSED until the M32_A1_A2_BASELINE_HYGIENE delta is audited and gated.
