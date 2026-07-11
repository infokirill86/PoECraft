# P2C Codex Instructions

Read before project work, in this order:

1. Fetch/pull and verify the current remote `main` HEAD.
2. Read `work/active/ACTIVE_TASK.md` from that verified HEAD.
3. Run `python tools/validate_active_task.py` and stop if it fails.
4. Read `CURRENT_STATUS.md` and the relevant accepted-ledger rows.
5. Read `START_HERE.md`, `manifest/Agent_Role_Pack.md`, and only the stable protocol sections needed by the live task.

`ACTIVE_TASK.md` is the sole live routing source. Orientation, status, manifests,
packages, and reviews must not override its current actor/action. If routing and
accepted truth conflict, stop for ChatGPT/User.

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
- Definition of done: the commit is pushed, remote `main` equals local `HEAD`, and commit-pinned `ACTIVE_TASK.md` names the intended next actor.

Final response:

- State what changed.
- State checks run.
- State current `ACTIVE_TASK.md` status, next actor, active task id, allowed next action, and whose turn it is.
