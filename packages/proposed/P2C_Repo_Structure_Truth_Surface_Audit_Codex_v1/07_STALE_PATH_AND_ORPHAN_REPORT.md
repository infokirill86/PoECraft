# Stale Path and Orphan Report

## Canonical stale paths/content

The workflow protocol's appended historical proposal references paths that are not part of the accepted current layout, including:

- `reviews/claude/...`;
- `work/completed/`;
- `packages/superseded/`;
- a multi-file handoff header contract not represented in schema v2.

These references are inside the canonical protocol and can mislead agents even when they were originally presented as deferred or rejected ideas.

## Historical evidence references

The broad backtick-path scan found old evidence references such as `tools/check_active_task.py` and baseline modules not imported into the final tree. These occur inside immutable packages/reviews and describe proposals or known baseline gaps. Do not rewrite them; lifecycle context is sufficient.

## Local-only residue

An empty local directory exists:

`packages/proposed/P2C_M34_Next_Wave_Design_Codex_v1/`

It has no tracked files and does not exist in GitHub history as a directory. It may be removed locally after the audit; no repository commit is needed.

`git count-objects` also reports a zero-byte linked-worktree metadata residue under the external parent repository. It is local Git administration, not a tracked PoECraft structural defect. Do not clean it from this task.

## Archive scan

Three tracked ZIPs exist only inside the explicit Layer-A source-byte verification bundle. This is a permitted full-reproducibility/source-bundle exception, not ordinary-package recursion. The current `check_no_nested_zips.py` has no exception model and therefore reports them as failures.
