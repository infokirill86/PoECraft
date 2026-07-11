# P2C — Stable Project Orientation

Purpose: reconstruct the project identity and collaboration model after the live
dispatcher has been read. This file is not routing, accepted truth, or task
authorization. Current actor/action lives only in `work/active/ACTIVE_TASK.md`;
accepted scope lives in the ledgers; the compact project snapshot lives in
`CURRENT_STATUS.md`.

## 1. What P2C is

P2C is a Path of Exile 2 crafting simulator. The primary product lane is a
physical quarterstaff route, but current starts, item states, accepted operations,
and executable scope are intentionally not enumerated here because they change.
Use `config/`, `CURRENT_STATUS.md`, and `ledger/ACCEPTED_ARTIFACTS.md` for the
current project-model basis.

Model: item = state; crafting action = state transition; probability = mass over
reachable states. Exact rational execution is the oracle for tractable lanes.
Seeded Monte Carlo is the scalable execution direction. Exact and MC must share
the same accepted mechanics, legality, pool, and weight kernels.

Data is project-model accepted truth, not a server-truth claim.

## 2. Roles

- **Kirill / ChatGPT:** product direction, synthesis, gates, and final acceptance.
- **Codex:** builder-critic, implementer, verifier, and package producer.
- **Claude:** independent auditor-designer and contradiction finder.

All participants have a duty to raise material correctness, source, foundation,
cost, safety, maintainability, or direction concerns. Taste-only objections do not
justify delay. Full doctrine lives in `manifest/Participant_Voice_Charter.md` and
`manifest/Agent_Role_Pack.md`.

## 3. Boot and handoff rule

1. Verify current remote `main` HEAD.
2. Read exact `work/active/ACTIVE_TASK.md` bytes from that HEAD.
3. Run `python tools/validate_active_task.py`.
4. Read only the current package/review and relevant accepted/status context.

If live routing and accepted truth appear inconsistent, stop for ChatGPT/User.
Do not choose another status-like document.

## 4. Pre-task self-check

1. Does the task change accepted truth, executable mechanics, fractured behavior,
   public numeric output, optimizer/advice, or a standing boundary? If yes, require
   the appropriate explicit gate.
2. Is the change reconstructible and automatically testable?
3. Does the mechanic fit the accepted state model?
4. Am I silently assuming source or mechanics certainty?
5. Is there a material objection or safer/broader boundary that must be stated?

## 5. Step-size rule

Batch work when it is reconstructible, automatically testable, truth-neutral,
and does not cross a gate. Separate review is required for silent-corruption risk,
accepted-truth change, executable mechanics, public values, optimizer/advice, or
standing-boundary changes.

Change workflow only after an observed failure demonstrates the need. The current
single-dispatcher cleanup is such a repair; speculative process growth is not.

## 6. Standing authority and boundaries

Only operations and mechanics accepted in `ledger/ACCEPTED_ARTIFACTS.md` and
`ledger/DECISIONS.md` may execute. Do not hardcode that changing inventory in
orientation or protocol files.

No package, audit, test, manifest, dashboard, Codex output, or Claude output can
self-accept. ChatGPT/User acceptance is required. Public numeric release,
optimizer/economics/advice, automation, server-truth framing, and closure of
SOURCE/PROVENANCE, MML, or PD-013 remain separately gated unless the accepted
ledgers explicitly say otherwise.

## 7. Repository roles

- `work/active/ACTIVE_TASK.md` — sole live dispatcher.
- `CURRENT_STATUS.md` — compact snapshot, not routing.
- `ledger/` — accepted truth, decisions, blockers, historical index.
- `manifest/` — stable process doctrine.
- `packages/` and `reviews/` — immutable evidence, not acceptance authority.
- `config/`, `data/`, `src/`, `tests/`, `schemas/`, `tools/` — project model and implementation.

Package directory names do not determine lifecycle status; the accepted ledger does.

## 8. Communication and honest limits

Explain outcomes to Kirill in plain language, then add concise technical detail.
Keep long evidence in repository files rather than chat.

A new session reconstructs state from Git; it does not inherit memory. The system
therefore relies on verified HEAD, one live dispatcher, explicit acceptance, and
independent audit rather than perfect model recall.

---

- document type: stable orientation
- routing authority: none
- accepted-truth authority: none
- current-state authority: none
