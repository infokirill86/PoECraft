# Canonical Structure and Truth Precedence

## Recommended canonical map

| Question | Canonical surface | Must not answer it |
|---|---|---|
| What is the live handoff? | `work/active/ACTIVE_TASK.md` at verified remote HEAD | README, START_HERE, CURRENT_STATUS, package prose, review prose |
| What has ChatGPT/User accepted? | `ledger/ACCEPTED_ARTIFACTS.md` plus `ledger/DECISIONS.md` | package folder name, Claude verdict, tests, CURRENT_STATUS alone |
| What is the compact accepted/project snapshot? | `CURRENT_STATUS.md` | ACTIVE_TASK history or package history |
| What rules are stable? | accepted files under `manifest/` | old package proposals or review text |
| What behavior can runtime execute? | accepted ledger + `runtime_admission_status`/accepted primitive registry + code/tests | `active_in_current_simulation`, README, old manifests |
| What proves a result? | immutable package bytes + matching Claude review | ledger summary by itself |
| Where is history? | Git history + `ledger/HISTORICAL_INDEX.md` + immutable evidence | `work/active/` |

## Required agent boot order

1. Fetch/pull and verify remote `main` HEAD.
2. Read exact `work/active/ACTIVE_TASK.md` bytes from that HEAD.
3. Run `tools/validate_active_task.py`.
4. If and only if the actor/action matches, read `CURRENT_STATUS.md` and relevant accepted-ledger rows.
5. Read stable role/doctrine files needed for the task.
6. Read only the result/review paths named by the dispatcher.

This order is fail-closed: if routing and accepted truth conflict, stop for ChatGPT/User rather than choosing a convenient document.

## Important `repo_head_at_last_update` clarification

The field records the input HEAD observed when the dispatcher was written. It is not expected to equal the commit that contains the updated dispatcher, because embedding that commit SHA would be self-referential. Freshness comes from reading the dispatcher at verified remote HEAD and checking its read receipt, not from demanding equality with the containing commit.
