# File-Role Inventory

Observed tracked tree: 601 files, approximately 1.92 MB of working-tree bytes.

| Surface | Tracked files | Intended role | Audit judgment |
|---|---:|---|---|
| Root | 9 | Entry points, roles, status, dependency config, integrity manifest | Good shape; entry/read order is wrong |
| `config/` | 4 | Project scope and initial-state configuration | Keep |
| `data/` | 9 | Project-model mechanics/static data | Keep |
| `examples/` | 2 | Small usage fixtures | Keep |
| `ledger/` | 4 | Accepted artifacts, decisions, blockers, historical index | Keep; refresh stale/underlinked rows later |
| `manifest/` | 4 | Stable doctrine and workflow | Keep; canonical files contain stale/history content |
| `packages/` | 418 | Immutable result/design evidence | Keep bytes; lifecycle naming/index needs repair |
| `reviews/` | 40 | Claude audit evidence | Keep bytes; improve lifecycle links |
| `schemas/` | 2 | Data contracts | Keep |
| `src/` | 70 | Runtime implementation | Keep; not changed by audit |
| `tests/` | 27 | Verification | Keep; not changed by audit |
| `tools/` | 8 | Validators/integrity tooling | Keep; two scanners need scoped contracts |
| `work/` | 4 | Live routing only | Defect: four tracked files under `work/active/` |

## Root entry files

| File | Intended role | Finding |
|---|---|---|
| `README.md` | Five-line orientation | Omits the live dispatcher from its start order |
| `AGENTS.md` | Codex role/read order | Places live dispatcher fifth |
| `CLAUDE.md` | Claude role/read order | Places live dispatcher fifth |
| `START_HERE.md` | Stable project orientation | Contains volatile, now-false runtime/invariant statements |
| `CURRENT_STATUS.md` | Compact project snapshot | Contains transient next-actor prose that is already stale after M43 audit |
| `SHA256SUMS.txt` | Generated integrity map | Healthy and verified |
| `pyproject.toml` | Runtime/dev dependencies and test config | Keep |
| `.gitignore`, `.gitattributes` | Local hygiene/text normalization | Keep |

## Physical-size conclusion

No structural bloat emergency exists. The Git object pack is about 1.21 MiB; packages are individually small, with the largest audited package surface under 50 KB. The issue is truth routing and lifecycle clarity, not storage size.
