# Implementation Plan

## Recommended next floor: Agent Role Pack Implementation

If this design passes Claude audit and ChatGPT/User acceptance, implement a compact documentation-only floor:

1. Add root `AGENTS.md`.
2. Add root `CLAUDE.md`.
3. Add `manifest/Agent_Role_Pack.md`.
4. Update `manifest/GitHub_Workflow_Protocol.md` only if a short reference to the role pack is needed.
5. Do not add skills yet.
6. Do not update accepted truth except to record the workflow-hygiene acceptance after audit/gate.

## Acceptance criteria for implementation floor

- Root `AGENTS.md` is concise and points to shared role pack.
- Root `CLAUDE.md` is concise and points to shared role pack.
- Shared role pack contains common doctrine once.
- No runtime code changes.
- No crafting mechanics changes.
- No operation admission.
- No automation enablement.
- `ACTIVE_TASK.md` remains thin dispatcher.
- Root SHA checks pass.

## Deferred skill floor

After at least a few tasks using root role files, decide whether skills are still needed.

Add Codex skill only if:

- Codex repeatedly needs a procedural package/result checklist;
- `AGENTS.md` would become too long if it carried that procedure;
- the skill can be repo-scoped and concise.

Add Claude skill only if:

- Claude's actual environment supports repo skills;
- audits still need repeatable procedural scaffolding beyond `CLAUDE.md`;
- the skill remains audit-specific, not accepted-truth storage.

