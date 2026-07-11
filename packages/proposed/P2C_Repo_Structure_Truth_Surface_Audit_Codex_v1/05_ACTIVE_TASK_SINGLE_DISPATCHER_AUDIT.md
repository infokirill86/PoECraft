# ACTIVE_TASK Single-Dispatcher Audit

## Current dispatcher

`work/active/ACTIVE_TASK.md` passes schema-v2 validation:

- status: `audited_pending_user_gate`;
- next actor: `chatgpt_user`;
- active task: `M43_NEXT_PROJECT_WAVE_DESIGN`;
- result and review paths exist;
- automation remains manual/disabled.

## Structural violation around it

Four tracked files exist under `work/active/`:

1. `ACTIVE_TASK.md` — live dispatcher;
2. `LayerA_Source_Bundle_Byte_Verification_Task.md` — completed historical task;
3. `M32_A1_A2_Baseline_Hygiene_Task.md` — completed historical task;
4. `M32_Seeded_MC_Harness_Task.md` — completed historical task.

The last three explicitly contain obsolete project states. They should not remain in a directory whose semantic contract is “live routing only.” Git history and their result/review evidence already preserve the history.

## Validator gap

`tools/validate_active_task.py` validates only `ACTIVE_TASK.md`. It does not fail when sibling task files exist under `work/active/`.

Recommended later correction:

- require exactly one tracked file under `work/active/`;
- require it to be named `ACTIVE_TASK.md`;
- reject additional tracked siblings;
- keep the human summary to a short restatement of actor/action, with no new gate reasoning.

No files are removed by this audit.
