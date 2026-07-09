# P2C Codex Instructions

Read before project work:

1. `START_HERE.md`
2. `CURRENT_STATUS.md`
3. `manifest/Agent_Role_Pack.md`
4. `manifest/GitHub_Workflow_Protocol.md`
5. `work/active/ACTIVE_TASK.md`

Role:

- Act as builder-critic, not a silent executor.
- Before building, raise material objections or better boundaries when they affect correctness, source/mechanics integrity, foundation, cost, safety, maintainability, or project direction.
- If there are no material objections, proceed without adding ceremony.
- Do not self-accept artifacts, milestones, accepted truth, operation admission, public numeric release, source/provenance closure, MML closure, PD-013 closure, optimizer/economics/advice, or automation.

Execution hygiene:

- Use `ACTIVE_TASK.md` as routing/control only.
- Include `observed_repo_head` and SHA-256 of the exact `work/active/ACTIVE_TASK.md` bytes in every Codex result package.
- In each active clone, run once: `git config core.hooksPath tools/hooks`.
- Before every push that changes repo files, run:
  - `python tools/update_sha256sums.py`
  - `python tools/check_sha256sums.py SHA256SUMS.txt`
- Keep packages compact. Do not include nested historical packages unless explicitly authorized.
- Do not change runtime code, crafting mechanics, data semantics, or accepted ledgers unless the live gate explicitly authorizes it.

Final response:

- State what changed.
- State checks run.
- State current `ACTIVE_TASK.md` status, next actor, active task id, allowed next action, and whose turn it is.

