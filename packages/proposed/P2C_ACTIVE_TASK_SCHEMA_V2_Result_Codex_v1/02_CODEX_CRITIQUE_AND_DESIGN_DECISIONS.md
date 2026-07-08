# Codex Critique and Design Decisions

## Agreement with ChatGPT proposal

The core diagnosis is correct:

- live status was mixed with history;
- agents could mistake old text for current instructions;
- the file needed to fail closed when state was ambiguous;
- `ACTIVE_TASK.md` should be routing/control only.

## Material changes made

I did not implement the full proposal literally.

Reasons:

1. The original field set was too broad for a thin dispatcher.
   - I kept only the mandatory field set requested in the implementation gate.

2. Intermediate "agent is working" states were removed.
   - The dispatcher should not churn while an agent is thinking locally.

3. Standing boundaries moved to the manifest.
   - Repeating the full forbidden list in every task would recreate the bloat failure.

4. Read receipts live in packages/reviews, not in `ACTIVE_TASK.md`.
   - Updating the dispatcher just to say it was read would create unnecessary commits and noise.

5. Validator is deferred.
   - A future `tools/check_active_task.py` is useful, but this task is documentation/protocol hygiene only.

## Final chosen model

`ACTIVE_TASK.md` is now:

- YAML frontmatter first;
- one live state;
- no old task log;
- task-specific forbidden actions only;
- standing boundaries referenced by manifest anchor;
- automation manual and disabled;
- short human summary after the block only.

## Remaining disagreement / risk

`repo_head_at_last_update` necessarily points to the commit observed when the dispatcher was written, not the final commit created after writing it. The read-receipt rule in packages/reviews is the stronger freshness control.
