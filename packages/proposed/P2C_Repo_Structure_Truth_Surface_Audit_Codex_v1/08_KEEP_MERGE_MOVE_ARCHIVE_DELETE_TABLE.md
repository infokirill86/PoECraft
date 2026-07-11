# Proposed Keep / Merge / Move / Archive / Delete Table

No action in this table is executed by this audit.

| Surface | Proposal | Reason | Gate level |
|---|---|---|---|
| `src/`, `tests/`, `data/`, `config/`, `schemas/`, `examples/` | Keep | Clean functional separation | None |
| `work/active/ACTIVE_TASK.md` | Keep and slim | Sole live dispatcher | Cleanup gate |
| Three legacy `work/active/*Task.md` files | Delete from current tree after audit | Git/evidence preserve history; path falsely implies live work | Cleanup gate |
| `README.md` | Keep; make ACTIVE_TASK first link | Current entry order hides dispatcher | Cleanup gate |
| `AGENTS.md`, `CLAUDE.md` | Keep; change read order to HEAD → ACTIVE_TASK → validation → context | Prevent stale-state decisions | Cleanup gate |
| `START_HERE.md` | Keep; remove volatile runtime roadmap/current operation/invariant claims | Stable orientation must remain timeless | Cleanup gate + careful accepted-doctrine review |
| `CURRENT_STATUS.md` | Keep; remove transient actor/action routing | Snapshot, not dispatcher | Cleanup gate |
| `Operating_Manifest_v4.md` | Keep; mark accepted baseline and replace volatile operation list with ledger reference | Current file contradicts its accepted status and runtime | Cleanup gate + Claude audit |
| `GitHub_Workflow_Protocol.md` | Keep; remove historical convergence appendix and stale validator/runtime claims | Canonical protocol must contain only binding current rules | Cleanup gate + Claude audit |
| `OPEN_BLOCKERS.md` | Keep; refresh standing summary, preserve open boundaries | Current top-level executable wording is stale | Cleanup gate |
| Accepted packages under `packages/proposed/` | Keep in place | Avoid path churn and broken evidence links | No move |
| `packages/accepted/README.md` | Merge policy into a new package lifecycle index or clarify as reserved | Empty accepted tree conflicts with actual practice | Cleanup gate |
| Packages/reviews | Keep immutable; add lifecycle links | Evidence trail | No delete |
| Empty local M34 directory | Delete locally | Untracked residue only | Local housekeeping |
| Historical appendix in workflow protocol | Remove from canonical file; rely on Git history | It is non-binding history in a binding document | Cleanup gate |

Mass deletion, bulk package moves, and rewriting historical evidence are explicitly not recommended.
