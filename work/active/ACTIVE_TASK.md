# P2C ACTIVE TASK

status: ready_for_codex
next_actor: codex
active_task_id: M32_SEEDED_MC_HARNESS
active_task_file: work/active/M32_Seeded_MC_Harness_Task.md
expected_output_dir: packages/proposed/P2C_M32_Seeded_MC_Harness_Result_Codex_v1/
review_output_hint: reviews/M32_Audit_Claude_v1.md

## Current project checkpoint
- Operating Manifest v4: accepted baseline.
- Participant Voice Charter: accepted and active.
- GitHub workflow: active manual loop, no mailbox automation yet.
- M31 Monte Carlo policy: accepted after folded C-1 correction.
- M26-M30 operation mechanics blueprint: open/context only, not accepted.
- Next work: M32 seeded Monte Carlo harness over accepted ordinary_add only.

## What Codex should do first
1. Pull latest repo state.
2. Read:
   - START_HERE.md
   - CURRENT_STATUS.md
   - manifest/Operating_Manifest_v4.md
   - manifest/GitHub_Workflow_Protocol.md
   - manifest/Participant_Voice_Charter.md
   - this ACTIVE_TASK.md
   - active_task_file above
3. Run pre-build critique:
   - material objections or improvements;
   - scope risks;
   - whether task should proceed;
   - or write: "No material objections; proceeding."

## What Codex should do after completion
1. Write the result under expected_output_dir.
2. Do not create a ZIP if unpacked files are practical.
3. Update this file:
   - status: ready_for_claude
   - next_actor: claude
   - result_path: expected_output_dir
   - builder_summary: short summary of what was built
4. Commit and push.

## Stop conditions
STOP_OR_ESCALATION if:
- required repo files are missing;
- M31 accepted status is unclear;
- task would require new executable mechanics;
- task would require optimizer/advice/ranking;
- task would require public numeric release;
- exact and MC cannot share one mechanics/pool/legality/weight kernel;
- seeded replay cannot be made deterministic.
