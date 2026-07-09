# Claude Audit Request

Please audit `P2C_Agent_Role_Packs_Design_Codex_v1`.

## Requested verdict

Return:

- `GO`
- `GO WITH CHANGES`
- `NO-GO`

## Audit focus

Check whether this proposal:

1. correctly separates UI personalization, repo-level instructions, shared role pack, and optional skills;
2. keeps `AGENTS.md` and `CLAUDE.md` compact rather than turning them into history dumps;
3. avoids duplicating the same doctrine across many files;
4. preserves ChatGPT/Kirill as acceptance gate;
5. preserves Codex as builder-critic and Claude as auditor-designer;
6. correctly defers skills until proven necessary;
7. avoids runtime code, mechanics, operation admission, automation, and accepted-truth changes;
8. actually reduces future prompt length without hiding volatile gate decisions.

## Claude-specific check requested

Please verify from your environment whether:

- root `CLAUDE.md` is the correct persistent repo instruction surface;
- `.claude/skills/.../SKILL.md` is appropriate for optional future audit workflow packaging;
- any proposed Claude instruction surface should be changed before implementation.

If Claude-specific assumptions are wrong, mark them as required corrections.

