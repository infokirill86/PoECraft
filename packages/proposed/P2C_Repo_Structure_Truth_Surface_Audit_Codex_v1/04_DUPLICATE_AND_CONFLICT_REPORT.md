# Duplicate and Conflict Report

## Exact duplicates

- Exact non-empty tracked-file SHA duplicate groups: **zero**.
- General duplicate-byte cleanup is not warranted.

## Load-bearing conflicts

| ID | Severity | Conflict | Why agents fail |
|---|---|---|---|
| TS-01 | Critical | `AGENTS.md`, `CLAUDE.md`, and README route through START_HERE/CURRENT_STATUS before ACTIVE_TASK | A compliant agent can stop on stale state before reaching live routing |
| TS-02 | Critical | `work/active/` contains three historical task files beside `ACTIVE_TASK.md` | Folder name implies four active tasks; old files contain obsolete gates and forbidden/allowed scope |
| TS-03 | High | `START_HERE.md` says only `ordinary_add` is executable and treats fractured-suffix behavior as a fixed global invariant | Contradicts accepted M35–M42 runtime and M40 fractured-prefix/suffix decision |
| TS-04 | High | `manifest/Operating_Manifest_v4.md` labels itself a ratification candidate and lists `ordinary_add` as the only accepted operation | Contradicts ledger acceptance of the manifest and later operation admissions |
| TS-05 | High | `manifest/GitHub_Workflow_Protocol.md` says current runtime is only ordinary_add + Annulment and that ACTIVE_TASK validator is future/deferred | Both claims are obsolete |
| TS-06 | High | Workflow protocol includes a 140-line historical “Source convergence notes” proposal inside the canonical rule file | Mixes rejected/deferred layout ideas, nonexistent paths, and current rules |
| TS-07 | Medium | `CURRENT_STATUS.md` says Claude audit of M43 is next while live ACTIVE_TASK says audit complete and user gate next | CURRENT_STATUS is used as transient routing but is not updated on every handoff |
| TS-08 | Medium | `ledger/OPEN_BLOCKERS.md` top-level executable-surface wording stops at ordinary_add + Annulment | Standing blocker summary is stale even though later clarifications exist |
| TS-09 | Medium | `packages/proposed/` contains 33 ledger-accepted packages while `packages/accepted/` contains only README | Folder name conflicts with lifecycle truth and encourages wrong acceptance inference |
| TS-10 | Low/medium | ACTIVE_TASK human summary repeats a long gate explanation after the machine block | Duplicated state can drift within the same file and defeats “thin dispatcher” intent |

## Non-conflicts

- GitHub `raw/main`, `blob/main`, and commit-pinned URLs are views of the same tracked path, not duplicate files.
- Historical package/review wording is evidence and should not be rewritten merely because it is old.
- `active_in_current_simulation` versus `runtime_admission_status` is already intentionally separated in data/runtime; the stale workflow prose is the defect.
