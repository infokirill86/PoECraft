# Prompt Reduction Policy

## Current problem

Per-task prompts have been carrying too much stable doctrine:

- agent roles;
- participant critique duty;
- no self-acceptance;
- source/provenance boundaries;
- plain-language summary requirements;
- package hygiene;
- Active Task handoff style.

This creates long chats and increases the chance that one prompt omits a critical rule.

## Proposed future prompt pattern

Future prompts should be shorter:

```text
Go.
Use repo role pack and live ACTIVE_TASK.md.

Gate decision:
...

Task-specific scope:
...

Task-specific forbidden actions:
...

Required output:
...
```

The stable role doctrine should come from:

- `AGENTS.md` for Codex;
- `CLAUDE.md` for Claude;
- `manifest/Agent_Role_Pack.md` for shared rules;
- `manifest/GitHub_Workflow_Protocol.md` for dispatcher/checksum/package protocol.

## What must still be explicit in each prompt

Do not hide volatile decisions in role files. Each gate still needs explicit:

- accepted/proposed/current state;
- current authorization;
- exact allowed scope;
- exact forbidden scope for the task;
- required output path;
- next `ACTIVE_TASK` transition;
- whether implementation is authorized.

## What should not be repeated

Avoid repeating every time:

- "act as project participant";
- "do not silently execute";
- "do not self-accept";
- "include plain-language summary";
- "ChatGPT/User is acceptance gate";
- "standing boundaries remain open";
- "final message includes Active Task and whose turn".

Those should be in the role pack and only referenced.

