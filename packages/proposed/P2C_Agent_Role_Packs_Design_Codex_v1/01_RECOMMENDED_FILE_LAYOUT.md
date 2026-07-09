# Recommended File Layout

## Proposed first implementation

```text
AGENTS.md
CLAUDE.md
manifest/Agent_Role_Pack.md
```

This is the smallest useful layout.

## Optional later additions

```text
.agents/skills/p2c-codex-workflow/SKILL.md
.claude/skills/p2c-audit-workflow/SKILL.md
```

These should be deferred until the root files prove insufficient. Skills are useful for repeatable workflows, but adding them too early risks protocol bloat.

## What belongs where

| Surface | Scope | Recommended content | Do not put here |
|---|---|---|---|
| Codex UI/user-level instructions | Kirill's personal preferences across projects | concise communication style, final Active Task line, avoid huge chat canvases | P2C accepted truth, mechanics policy, per-milestone gates |
| Root `AGENTS.md` | Codex repo behavior | load order, role, must-read files, stop triggers, package hygiene, final summary rule | long history, full milestone logs, copied ledgers |
| Codex repo skill under `.agents/skills` | optional repeatable procedure | only if a workflow needs richer step-by-step instructions or helper scripts | standing project role rules that should always apply |
| Root `CLAUDE.md` | Claude repo behavior | auditor role, hostile review expectations, must-read files, verdict format, correction corridor | full duplicated role pack, long project history |
| Claude `.claude/skills/.../SKILL.md` | optional repeatable audit procedure | only if Claude workflow needs reusable procedural detail | simple standing role rules |
| Claude UI instructions | Kirill's personal preference for Claude across projects | concise review style, "challenge weak framing" preference | project-specific accepted truth |
| `manifest/Agent_Role_Pack.md` | shared P2C role contract | common role definitions, critique duty, stop/gate triggers, plain-language rule | volatile current task details |
| `work/active/ACTIVE_TASK.md` | live dispatcher only | one current status, next actor, allowed next action | history, role doctrine, evidence, accepted truth |
| ledgers/status/reviews/packages | durable project record | accepted artifacts, decisions, evidence, audit results | live dispatch or personal preferences |

## Why not duplicate everything everywhere

Duplicating the same role text into `AGENTS.md`, `CLAUDE.md`, UI instructions, and skills will drift. The repo should have one shared role source, then thin agent-specific entry files that point to it.

Recommended pattern:

```text
AGENTS.md  -> read manifest/Agent_Role_Pack.md + ACTIVE_TASK.md
CLAUDE.md  -> read manifest/Agent_Role_Pack.md + ACTIVE_TASK.md
```

