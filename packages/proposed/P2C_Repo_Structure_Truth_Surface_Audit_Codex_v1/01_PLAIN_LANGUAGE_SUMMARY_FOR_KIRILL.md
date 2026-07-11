# Plain-Language Summary for Kirill

## What went wrong

The repeated wrong-task answers are not mainly a model-attention problem and not a `raw/main` versus `blob/main` problem.

The repository gives an agent several plausible answers to “what should I do now?”:

- `AGENTS.md` and `CLAUDE.md` tell the agent to read `START_HERE.md` and `CURRENT_STATUS.md` before `ACTIVE_TASK.md`;
- those earlier documents contain old runtime and next-step statements;
- `work/active/` contains three completed M32/Layer-A task files beside the real dispatcher;
- the workflow protocol contains an old repository proposal appended inside the current rule file;
- `CURRENT_STATUS.md` can become stale as soon as Claude updates only `ACTIVE_TASK.md` after an audit.

So an agent can follow the documented read order and still reach the wrong conclusion.

## What is healthy

The code/data/test layout is sensible. The repository is about 1.9 MB of tracked working-tree data, has no exact duplicate tracked files, and contains no general package-bloat problem. `ACTIVE_TASK.md` itself parses correctly and points to the audited M43 design.

## Recommended fix

Make remote HEAD plus `work/active/ACTIVE_TASK.md` the first read, not the fifth. Keep only that one tracked file in `work/active/`. Remove volatile operation lists from stable manifests, strip the historical appendix out of the workflow protocol, and make package lifecycle explicit without physically moving accepted evidence.

No cleanup is performed by this audit package.
