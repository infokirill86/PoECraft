# Human Summary

## What was done

`ACTIVE_TASK.md` was converted from a loose Markdown status note into a strict thin dispatcher.

It now starts with one machine-readable YAML frontmatter block and keeps only the current live task state. A short human summary follows the block.

## Why it matters

The project had a repeated failure where agents saw old task history inside `ACTIVE_TASK.md` and repeated work that had already been completed. This patch removes that failure mode by making the file a cockpit indicator, not a history document.

## What changed

Updated:

- `work/active/ACTIVE_TASK.md`
- `manifest/GitHub_Workflow_Protocol.md`

Added:

- `packages/proposed/P2C_ACTIVE_TASK_SCHEMA_V2_Result_Codex_v1/`

## What remains proposed

The schema is proposed for Claude audit. It is not accepted truth yet.

## Who is next

Next actor: Claude.

## Human decision required

Yes. ChatGPT/User must accept or reject the schema after Claude audit.
