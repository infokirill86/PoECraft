# P2C Agent Role Packs Design

package_id: `P2C_Agent_Role_Packs_Design_Codex_v1`
package_type: `WORKFLOW_PROTOCOL_DESIGN_ONLY_PROPOSED_DELTA`
status: `proposed_for_claude_audit`
author: `codex`
created_utc: `2026-07-09T14:21:31Z`

## Read receipt

- observed_repo_head: `800daa1becae9fc42fcbd794e9b6f86cd84661bb`
- observed_active_task_sha: `96d7ae141c5ce4153b6e72435d7863319fb70f3ad842c3d0af6c28170ad7f4fe`
- active_task_path: `work/active/ACTIVE_TASK.md`

## Plain-language summary for Kirill

The project is now too mature to keep repeating long role instructions in every chat prompt. The stable parts should live in the repository, while short gate prompts should say only what is new.

Recommended direction:

1. Add a small root `AGENTS.md` for Codex.
2. Add a small root `CLAUDE.md` for Claude.
3. Add one shared role file, proposed as `manifest/Agent_Role_Pack.md`, to avoid copying the same rules into both files.
4. Keep personal communication preferences in UI/user-level instructions, not in project truth files.
5. Add repo-scoped Codex/Claude skills only later, if repeated workflows still need procedural detail after the root files exist.

This package is design-only. It does not create those role files yet.

## Why this matters

The goal is to make every agent start from the same stable role contract:

- Codex is a builder-critic, not a silent executor.
- Claude is an auditor-designer, not only a typo checker.
- ChatGPT/Kirill remain the acceptance gate.
- All agents must surface better boundaries, source/mechanics doubts, and over-expansion risks.
- Every result must include a short plain-language summary for Kirill.

The practical result should be shorter future prompts: instead of restating the whole project philosophy, a task can say: "Use repo role pack, follow ACTIVE_TASK, do M38-A."

