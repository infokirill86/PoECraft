# Codex and Claude Loading Model

## Codex

Official Codex manual basis used for this proposal:

- Codex reads `AGENTS.md` before work and builds an instruction chain from global and repo/project files.
- Repo-level `AGENTS.md` is the right place for durable project conventions.
- Codex skills are for reusable workflows and use progressive disclosure: metadata is visible, full `SKILL.md` loads only when selected.
- User/global instructions are better for personal preferences across repositories.

Recommended Codex setup:

1. `AGENTS.md` at repo root for always-on P2C role and routing rules.
2. Optional `.agents/skills/p2c-codex-workflow/SKILL.md` later for repeated package/result workflows.
3. User-level Codex instruction for Kirill's communication preference:
   - concise chat updates;
   - no huge reasoning canvases;
   - final message includes current `ACTIVE_TASK` / whose turn.

Do not put long P2C milestone history in Codex UI instructions or `AGENTS.md`.

## Claude

Recommended Claude setup:

1. `CLAUDE.md` at repo root for always-on project audit role.
2. Optional `.claude/skills/p2c-audit-workflow/SKILL.md` later if Claude setup supports skills and the audit workflow remains repetitive.
3. Claude UI "Instructions for Claude" should stay personal and cross-project:
   - be direct;
   - challenge weak framing;
   - include plain-language summary for Kirill;
   - do not self-accept project truth.

`CLAUDE.md` should point to `manifest/Agent_Role_Pack.md` rather than duplicating all shared role text.

## ChatGPT/Kirill gate process

The gate process should remain outside always-on agent files. A gate prompt still needs to say:

- what is being accepted or authorized;
- exact scope;
- forbidden scope;
- required output;
- next `ACTIVE_TASK` state.

But it should not need to restate the entire role doctrine.

