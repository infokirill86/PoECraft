# P2C Agent Role Packs Implementation

package_id: `P2C_Agent_Role_Packs_Implementation_Codex_v1`
package_type: `WORKFLOW_PROTOCOL_IMPLEMENTATION_PROPOSED_DELTA`
status: `proposed_for_claude_audit`
author: `codex`
created_utc: `2026-07-09T15:11:48Z`

## Read receipt

- observed_repo_head: `52aa38e7e062ff6c6bc705909502a546b474f0c4`
- observed_active_task_sha: `4600b5f2f9aeb4e9c33802e0eaca2fd9bff3dde0133d9064e1431e48d206785b`
- active_task_path: `work/active/ACTIVE_TASK.md`

## Plain-language summary for Kirill

This implementation creates the small persistent role files that should reduce future long prompts.

Now the repo has:

- `AGENTS.md` for Codex;
- `CLAUDE.md` for Claude;
- `manifest/Agent_Role_Pack.md` as the shared role pointer.

The files are intentionally short. They do not repeat the full Participant Voice Charter or workflow protocol. Instead, they point to the accepted manifest files and say how Codex/Claude should behave by default.

Nothing here changes crafting runtime, mechanics, operation data, or accepted source truth.

