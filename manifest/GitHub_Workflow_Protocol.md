# P2C GitHub Workflow Protocol

Status: accepted workflow protocol. This file contains stable binding rules only.
Live routing belongs in `work/active/ACTIVE_TASK.md`; accepted truth belongs in the
ledgers; history belongs in Git and `ledger/HISTORICAL_INDEX.md`.

## Core workflow

- GitHub is the shared workspace and durable project base.
- Chats carry gates, decisions, reviews, and short commands.
- No auto-merge or agent self-acceptance.
- Artifacts needed for active audit must exist as real bytes.
- Keep ordinary packages unpacked and compact; historical bulk is indexed.
- Package/review paths are immutable evidence paths. Their directory names do not
  determine current acceptance status.

## Truth precedence and mandatory read order

For every Codex/Claude project action:

1. Fetch/pull and verify current remote `main` HEAD.
2. Read `work/active/ACTIVE_TASK.md` from that verified HEAD.
3. Run `python tools/validate_active_task.py`.
4. Read the result/review path named by the dispatcher.
5. Read `CURRENT_STATUS.md` and relevant accepted-ledger rows.
6. Read stable orientation/doctrine only as needed.

Truth roles:

- live actor/action: `work/active/ACTIVE_TASK.md` only;
- accepted artifacts/decisions: `ledger/ACCEPTED_ARTIFACTS.md` and `ledger/DECISIONS.md`;
- compact snapshot: `CURRENT_STATUS.md` (never live routing);
- stable rules: accepted files in `manifest/`;
- evidence: packages and reviews (never acceptance authority).

If routing and accepted truth conflict, stop for ChatGPT/User. Do not select a
different status-like document.

`repo_head_at_last_update` is the input HEAD observed when a dispatcher is written,
not the self-referential SHA of the commit containing that update. Freshness comes
from verified remote HEAD plus exact-byte read receipts.

## Root SHA256SUMS workflow

The root `SHA256SUMS.txt` is generated, never hand-edited.

Before push:

```bash
python tools/update_sha256sums.py
python tools/check_sha256sums.py SHA256SUMS.txt
```

Enable the committed local hook once per clone:

```bash
git config core.hooksPath tools/hooks
```

This is local integrity enforcement, not GitHub Actions or watcher automation.

## ACTIVE_TASK schema v2

`work/active/ACTIVE_TASK.md` is routing/control only: not evidence, ledger, history,
or accepted truth. It must be the only tracked file under `work/active/`.

Requirements:

- one YAML frontmatter block at the top and no prose before it;
- exactly one live `status`, `next_actor`, and `allowed_next_action`;
- no old task text or historical task siblings;
- optional body limited to a short restatement of machine state;
- body introduces no state absent from frontmatter.

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

Allowed status/actor pairs:

| Status | Allowed next actor |
|---|---|
| `awaiting_user_gate` | `chatgpt_user` |
| `ready_for_codex` | `codex` |
| `ready_for_claude` | `claude` |
| `audited_pending_user_gate` | `chatgpt_user` |
| `blocked_for_human` | `chatgpt_user` or `blocked` |
| `accepted_closed` | `chatgpt_user` or `blocked` |

Do not add “agent is working” states.

## ACTIVE_TASK validation and read receipts

`tools/validate_active_task.py` is implemented and runs from the pre-push hook. It
validates the schema, unique keys, status/actor consistency, referenced paths, and
the single tracked dispatcher contract.

Do not update ACTIVE_TASK merely to log reads. Every Codex result package and every
Claude review records:

- `observed_repo_head`;
- `observed_active_task_sha` (SHA-256 of exact bytes acted on).

## Standing boundaries for active task dispatcher

ACTIVE_TASK lists task-specific prohibitions and references this section with:

```yaml
standing_boundaries_ref: "manifest/GitHub_Workflow_Protocol.md#standing-boundaries-for-active-task-dispatcher"
standing_boundaries_apply: true
```

Unless an explicit ChatGPT/User gate overrides the exact item for the live task:

- no milestone transition or accepted-truth update by an agent/test/package/report;
- no executable mechanics or operation expansion;
- no optimizer, advice, ranking, economics, EV, cost, budget, or expected attempts;
- no public numeric probability release or server-truth claim;
- no SOURCE/PROVENANCE, MML, or PD-013 closure;
- no supervised auto-run, GitHub Actions, or watcher automation;
- no new write-location/mailbox category.

## Operation catalog vs runtime admission

`active_in_current_simulation` is project-scope/catalog metadata, not executable
permission. Runtime execution requires an accepted engine primitive or explicit
accepted admission metadata such as:

```yaml
runtime_admission_status: accepted_executable_runtime
```

The changing executable inventory is never hardcoded in this protocol. Read it
from accepted ledgers and the admitted runtime registry. Candidate/reference/
blocked/disputed rows are not executable merely because they exist in data.

## Freshness and fail-closed rules

Stop and report to ChatGPT/User if:

- current remote HEAD cannot be verified;
- ACTIVE_TASK cannot be parsed or validated;
- more than one tracked file exists under `work/active/`;
- status and actor conflict;
- result/review references are missing when required;
- accepted/proposed/current state is ambiguous;
- raw/cache/HEAD staleness is suspected;
- standing boundaries are missing or unclear;
- the task would require scope expansion.

## Supervised auto-run metadata

The optional `automation` block is descriptive control metadata only.

- `mode: manual` means Kirill sends each `Go`.
- `enabled: false` means no automated handoff.
- Auto-run can never accept truth, start a milestone, update accepted ledgers, or
  bypass the human gate.
- Any stop trigger returns control to ChatGPT/User.

No automation is enabled by this protocol.

## Plain-language summary requirement

Every Codex result and Claude audit explains:

- what was done and why it matters;
- what changed and was tested;
- what remains proposed/not accepted;
- who is next and whether a human decision is required.

Technical evidence stays in the package. Chat summaries remain readable for a
non-programmer project owner.

## Participant rule

Codex critiques before building. Claude audits framing and evidence without
rubber-stamping. ChatGPT synthesizes at major gates. Kirill decides. Historical
proposals do not live inside this binding protocol; Git history preserves them.
