# P2C — GitHub Workflow Protocol

Status: bootstrap v1. This document follows the compact convergence rule: GitHub is the cockpit, not a museum.

## Core workflow
- GitHub is the shared workspace and durable project base.
- Chats are for decisions, reviews, and short commands.
- Store unpacked text/code where practical; avoid ZIPs in git unless bytes are needed for active audit or unpacking is impractical.
- Artifacts needed for active audit must be present as real bytes, not only listed in a ledger.
- Large/offloaded artifacts may be indexed later, but only after real need appears.
- No auto-merge. Accepted truth changes only after Kirill/ChatGPT gate acceptance.

## Supervised auto-run metadata

`work/active/ACTIVE_TASK.md` may include an optional `automation` block. The block is descriptive control metadata, not automation by itself.

- `mode: manual` means Kirill still sends each `Go`.
- `mode: supervised_auto_run` means agents may pass the turn for a limited number of handoffs only when explicitly enabled.
- `enabled: false` means no automated handoff is authorized.
- `max_handoffs` and `current_handoff_count` limit how far a supervised run may continue before stopping for a human.
- `human_gate_required: true` is mandatory. No auto-run may mark anything as accepted, update accepted truth, update accepted ledgers, start a new milestone, or bypass ChatGPT/User authority.
- Any stop trigger in the `automation.stop_on` list must stop the run, set `status: blocked_for_human`, and set `next_actor: chatgpt_user`.

This protocol extension prepares the repo for future controlled short auto-runs. It does not implement GitHub Actions, Codex automation, Claude automation, or any watcher.

## Plain-language summary requirement

Every Codex result package and every Claude audit must include a short human-readable summary section or file. It must explain, in plain language:

- what was done;
- why it matters;
- what changed;
- what was tested;
- what remains proposed or not accepted;
- who is next;
- whether a human decision is required.

This is required because the project is now technical enough that raw paths, hashes, and PASS/FAIL lines are not enough for project control. Technical evidence stays in the package, but each handoff must also explain the meaning of the work for a non-programmer project owner.

## Minimal structure
See repository tree in README and ledger files.

## Handoff header
Each active task should include: task_id, task_type, source_agent, target_agent, allowed_actions, forbidden_actions, stop_triggers, base_commit, expected_output, related_artifacts.

## ACTIVE_TASK schema v2

`work/active/ACTIVE_TASK.md` is a routing/control file only. It is not evidence, not a ledger, and not accepted truth.

The file must be a thin live dispatcher:

- one YAML frontmatter block at the top;
- no prose before the frontmatter;
- exactly one live `status`;
- exactly one live `next_actor`;
- exactly one live `allowed_next_action`;
- no historical task log;
- no old task text below the current task;
- a short human summary may follow the frontmatter, but it must not introduce state that is absent from the machine block.

Mandatory fields:

- `schema_version`
- `repo_head_at_last_update`
- `updated_at_utc`
- `status`
- `next_actor`
- `active_task_id`
- `allowed_next_action`
- `forbidden_next_actions`
- `standing_boundaries_ref`
- `standing_boundaries_apply`
- `current_result_path`
- `current_review_path`
- `acceptance_authority`
- `automation`
- `freshness_rules`
- `stop_conditions`

Allowed `status` values:

- `awaiting_user_gate`
- `ready_for_codex`
- `ready_for_claude`
- `audited_pending_user_gate`
- `blocked_for_human`
- `accepted_closed`

Allowed `next_actor` values:

- `chatgpt_user`
- `codex`
- `claude`
- `blocked`

Status/actor consistency:

- `awaiting_user_gate` requires `next_actor: chatgpt_user`.
- `ready_for_codex` requires `next_actor: codex`.
- `ready_for_claude` requires `next_actor: claude`.
- `audited_pending_user_gate` requires `next_actor: chatgpt_user`.
- `blocked_for_human` requires `next_actor: chatgpt_user` or `next_actor: blocked`.
- `accepted_closed` requires `next_actor: chatgpt_user` or `next_actor: blocked`.

Do not add intermediate "agent is working" states. Agent work-in-progress belongs in the agent's local execution context until committed/pushed.

## ACTIVE_TASK read receipt rule

Do not update `ACTIVE_TASK.md` just to log reads.

Every Codex result package and every Claude review must include:

- `observed_repo_head`;
- `observed_active_task_sha`.

`observed_active_task_sha` must be the SHA-256 of the exact `work/active/ACTIVE_TASK.md` file bytes the actor acted on.

This catches stale raw/cache reads without turning `ACTIVE_TASK.md` into a read log.

## Standing boundaries for active task dispatcher

`ACTIVE_TASK.md` should list task-specific forbidden actions only, then point here with:

```yaml
standing_boundaries_ref: "manifest/GitHub_Workflow_Protocol.md#standing-boundaries-for-active-task-dispatcher"
standing_boundaries_apply: true
```

Unless an explicit ChatGPT/User gate overrides them for the current task, standing boundaries are:

- no milestone transition without ChatGPT/User authorization;
- no accepted-truth or ledger acceptance by Codex, Claude, tests, packages, manifests, dashboards, or generated reports;
- no executable mechanics change unless explicitly in scope;
- no operation expansion unless explicitly in scope;
- no optimizer, advice, ranking, economics, EV, cost, budget, or expected-attempts work unless explicitly in scope;
- no public numeric probability release unless explicitly in scope;
- no server-truth claim;
- no SOURCE/PROVENANCE closure unless explicitly gated;
- no MML closure unless explicitly gated;
- no PD-013 closure unless explicitly gated;
- no supervised auto-run enablement unless explicitly gated;
- no GitHub Actions or watcher automation unless explicitly gated;
- no new mailbox or write-location category unless explicitly gated.

## ACTIVE_TASK freshness and fail-closed rules

Agents must stop and report to `chatgpt_user` if:

- current repo HEAD cannot be verified;
- `ACTIVE_TASK.md` frontmatter cannot be parsed;
- mandatory fields are missing;
- enum values are invalid;
- `status` and `next_actor` conflict;
- accepted/proposed/current state is ambiguous;
- raw/cache/HEAD staleness is suspected;
- standing boundaries are missing or unclear;
- the task would require a scope expansion.

## Deferred ACTIVE_TASK validator

A future small validator may check the schema mechanically:

- one machine block;
- mandatory fields;
- enum membership;
- `status`/`next_actor` consistency;
- automation disabled invariants.

This workflow-hygiene patch only documents the validator; it does not add code or tests.

## Participant rule
Codex critiques before building. Claude audits lean but deeply. ChatGPT synthesizes at major gates. Kirill decides.

---

## Source convergence notes

# P2C — Repository Structure: Convergence Proposal (Claude)

Reconciles three drafts: ChatGPT v1 (broad), Claude compact v1 (minimal), Codex v1 (compact +
handoff mailbox). Written per the Participant Voice Charter — I adopt Codex's genuinely better ideas
and flag one material disagreement rather than defend my own draft.

## Verdict
**GO WITH CHANGES.** Codex's draft is the strongest of the three on principle and adds real value my
compact draft lacked. It is still heavier than the stated "максимально компактно" goal in one place:
it stands up an automation mailbox before the manual workflow has run once. Adopt Codex's principles
and tooling; defer its mailbox folders until the manual loop is proven.

## What I adopt from Codex (better than my draft — taken)
- **"Cockpit, not museum."** The repo is the current working project; historical bulk is *indexed*,
  not bulk-imported. This is sharper than my "import gradually" and removes the real bloat risk. Taken.
- **`HISTORICAL_INDEX` instead of dumping old packages** (name | sha256 | status | storage location).
  Bound by the auditor red line below.
- **`tools/` hygiene scripts.** Especially `check_sha256sums.py`, `check_no_nested_zips.py`, and
  `check_public_numeric_leaks.py` — these *automate the standing boundaries* (SHA verification and the
  numeric-free public rule). Strong adopt; this is real project code, not process surface.
- **`.gitignore`**, and the **branch strategy** (`main` = accepted baseline; one `work/<milestone>`
  branch at a time; audit in the same branch under `reviews/`). Taken.
- **The handoff *manifest*** (task_id, source, target, allowed_actions, forbidden_actions,
  stop_triggers, base_commit, expected_output). I adopt the *content* — as a header block on each task
  file and each package README — without the four mailbox folders (see disagreement).

## Material disagreement (Charter escalation — one item)
Codex proposes `handoff/{inbox,outbox,processed,status}` now, **and** keeps `reviews/`, `work/`, and
`packages/{proposed,corrections}`. That gives up to four locations where the same artifact (an audit,
a Codex result) could live — Codex's own text shows the ambiguity ("Claude writes `reviews/claude/…`
**or** `handoff/outbox/…`"). Multiple valid write-locations is the opposite of compact and will make
models guess where to put things.

This also contradicts Codex's **own** rule: *"automation comes after the manual GitHub workflow works
once."* The mailbox is automation infrastructure; building it before the first manual Codex→Claude→Codex
loop is premature. **Recommendation:** carry the manifest as a header now; add `handoff/` only when the
watcher automation is actually built. This keeps Codex's automation vision and sequences it by Codex's
own principle.

## Auditor red line (unchanged, made explicit for the archive)
An index entry is not audit evidence. **Any artifact referenced by an active audit must be present as
real bytes in the repo, not only listed in `HISTORICAL_INDEX`.** Level-3 indexing is only for artifacts
not needed for the next 1–2 gates. This is compatible with Codex's Level 1/2/3 model.

## Final compact layout
```
p2c/
  START_HERE.md
  CURRENT_STATUS.md
  README.md                 # ~5 lines → points to the two files above
  .gitignore

  manifest/
    Operating_Manifest_v4.md
    GitHub_Workflow_Protocol.md
    Participant_Voice_Charter.md

  ledger/
    ACCEPTED_ARTIFACTS.md   # stage | artifact | status | sha256 | path
    DECISIONS.md            # accepted pivots
    OPEN_BLOCKERS.md         # standing gated items
    HISTORICAL_INDEX.md      # superseded/large packages: name | sha256 | status | storage (NOT bulk-imported)

  work/active/              # current floor task(s); each task file carries the handoff header
  reviews/                  # audits; author + stage in filename (e.g. M32_Audit_Claude_v1.md)
  packages/
    accepted/               # unpacked accepted packages
    proposed/               # Codex outputs pending acceptance (corrections carry status here too)

  src/p2c_core/
  tests/
  examples/
  tools/                    # check_sha256sums.py, check_no_nested_zips.py, check_public_numeric_leaks.py
```
Process surface = root docs + `manifest/` + `ledger/` + `work/` + `reviews/` + `packages/`.
Real project code = `src/` + `tests/` + `examples/` + `tools/`.

## Deferred until a real need (process-change rule — add on observed failure, not upfront)
- `handoff/{inbox,outbox,processed,status}` mailbox → add when watcher automation is built.
- `reviews/{claude,codex,chatgpt}` split → one `reviews/`, author in the filename.
- `work/completed/`, `packages/superseded/` → git history + `HISTORICAL_INDEX`.
- `artifacts/{quarantine,external_index}` → none until a large or quarantined artifact actually exists.

## Handoff header (adopt now — top of each `work/active/*` task file and package README)
```
task_id / task_type / source_agent / target_agent /
allowed_actions / forbidden_actions / stop_triggers /
base_commit / expected_output / related_artifacts
```

## File lifecycle, checkpoints, backups, cleanup
Kirill's question — right now we only *create*; what happens locally, where are the backup
checkpoints, and how/when do we clean up junk. Answer, made explicit:

- **Nothing is ever lost.** Every commit is an automatic checkpoint of the whole tree. Removing a file
  from the working folder does not destroy it — git history keeps every prior version, recoverable.
  Git is the infinite undo. This is why we do **not** need a `trash/` folder (a junk folder becomes
  junk itself and clutters the repo).
- **Local stays untouched now.** Migration only *copies* current-good material in. The full historical
  pile stays on Kirill's machine as `P2C_FULL_ARCHIVE/` (Backup Layer 2), untouched; it is **not**
  bulk-imported into the repo (cockpit-not-museum).
- **Three backup layers.** (1) GitHub `main` = current truth, an off-machine copy the moment we push.
  (2) local `P2C_FULL_ARCHIVE/` = old + large bulk. (3) at gate boundaries, a **named tag** (e.g.
  `M31-accepted`) as a return point; **GitHub Releases** only for heavy reproducibility bundles when
  size forces it (no LFS/Releases before then).
- **Cleanup = at gate boundaries, not daily.** When a package is superseded, its files leave
  `packages/` and it becomes **one line** in `HISTORICAL_INDEX` (name | sha256 | status | storage).
  Obsolete → from a pile of files to a single indexed row. Day-to-day we do not clean, to avoid churn.
- **Auditor red line (repeat, binding):** anything referenced by an *active* audit must be present as
  real bytes in the repo — only artifacts not needed for the next 1–2 gates may live as an index row.

## File formats (model interaction)
Docs/tasks/reviews/status/ledger → **Markdown (.md)**. Code → `.py`. Data → `.json`. Everything
**unpacked**; no ZIPs in the repo where unpacking is practical.

## First commit (minimum)
`START_HERE.md`, `CURRENT_STATUS.md`, `README.md`, `.gitignore`, the three `manifest/` files, the four
`ledger/` files. Then `src/ tests/ examples/ tools/`, then compact accepted packages starting from
**M31 / M31-C1** and current baselines — not the whole history.

## Migration sequence
1. Create private repo; clone. 2. Root files + `.gitignore`. 3. `manifest/` + `ledger/`.
4. `src/ tests/ examples/ tools/`. 5. Compact accepted packages from M31/M31-C1 forward.
6. `HISTORICAL_INDEX` (index, not bulk import). 7. Update `CURRENT_STATUS`.
8. Run **one manual** Codex→Claude→Codex loop through GitHub. 9. Only then consider the `handoff/`
   mailbox + watcher automation.

## Tradeoff (per Charter)
Going compact + deferring the mailbox costs one thing: when automation is built, you add `handoff/`
then — near-zero cost. Benefits: fewer places to write, faster model load, matches the compactness
goal, and automation is built on a proven manual loop instead of guessed upfront. Net favors this.

---
- author: `claude`
- status: `convergence proposal — folds ChatGPT v1 + Claude v1 + Codex v1; out for Codex/ChatGPT/User confirmation`
