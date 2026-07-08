# Proposed Prompt Pattern Improvements

## Problem

The current workflow is safe but can bias agents into executor mode or micro-step mode.

Codex and Claude are already told to critique. The next improvement is to require the critique to be structured around product direction, not only local task safety.

## Recommended standing block for project-fork prompts

Add this block when choosing the next milestone:

```text
Project reality check:
1. What product capability are we trying to unlock?
2. What can the simulator do today?
3. What capability is missing before the product becomes more useful?
4. Is the proposed next step product-moving or just infrastructure-hardening?
5. What is the widest safe batch that remains reconstructible, automatically testable, and truth-neutral?
6. What must stay gated?
7. What would you recommend if you were not merely executing the prompt?
```

## Recommended Codex behavior

Codex should:

- challenge small prompts that continue infrastructure work without product payoff;
- propose a wider design wave when safe;
- explicitly identify the first later implementation floor;
- keep implementation closed unless authorized.

## Recommended Claude behavior

Claude should:

- audit whether Codex chose the right strategic boundary;
- challenge over-hardening and infrastructure drift;
- challenge premature mechanics admission;
- verify split-out gates are explicit;
- verify the proposal remains truth-neutral.

## What not to add now

Do not implement new automation or a prompt validator now.

The current issue is strategic framing, not machine enforcement.
