# Role Enforcement and Prompt Reduction

## Codex role enforcement

`AGENTS.md` now tells Codex to:

- act as builder-critic, not silent executor;
- raise material objections before building;
- include read receipts in packages;
- configure the local hook once per clone;
- run root SHA update/check before push;
- report `ACTIVE_TASK` status and whose turn it is in final responses.

## Claude role enforcement

`CLAUDE.md` now tells Claude to:

- audit framing, not only diff;
- avoid rubber-stamping;
- return `GO`, `GO WITH CHANGES`, or `NO-GO`;
- include a plain-language summary for Kirill;
- return to ChatGPT/Kirill on mechanics/source conflict, accepted-truth change, new operation, public numeric output, optimizer/economics/advice, automation, or boundary closure.

## Shorter future prompts

Future task prompts can be shorter because stable role doctrine now lives in repo.

Prompt can now say:

```text
Go.
Use repo role files and live ACTIVE_TASK.md.
Gate decision: ...
Task-specific scope: ...
```

The prompt still must explicitly state volatile gate decisions, allowed scope, forbidden scope, output path, and next actor.

