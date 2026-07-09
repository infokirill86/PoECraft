# Risks, Limitations, and Gates

## Risks

1. **Protocol bloat.** Too many instruction files can recreate the long-prompt problem in repo form.
2. **Instruction drift.** Duplicating the same text in `AGENTS.md`, `CLAUDE.md`, skills, and UI will eventually conflict.
3. **False automation.** Persistent instructions reduce prompt length but do not automate Codex/Claude handoff.
4. **Over-reliance on UI settings.** UI instructions may not travel with the repo and may differ by machine/account.
5. **Skill overuse.** Skills are powerful for workflows, but using them as always-on project truth is the wrong fit.
6. **Acceptance confusion.** Role packs must not become accepted-truth ledgers or milestone gates.

## Limitations

- This package does not create `AGENTS.md`, `CLAUDE.md`, `.agents/skills`, or `.claude/skills`.
- Claude-specific loading behavior should be verified by Claude in the user's actual Claude environment before implementation.
- Codex skill behavior was checked against the official Codex manual, but this package does not install or enable a skill.

## Stop triggers for implementation

Stop before implementing role files if:

- `AGENTS.md` or `CLAUDE.md` would exceed a compact always-on size;
- instructions duplicate ledgers or status files;
- role files would claim accepted truth;
- a skill is used to smuggle in automation;
- Claude setup cannot verify `.claude/skills` behavior;
- implementation would touch runtime code, mechanics, data semantics, or accepted ledgers.

