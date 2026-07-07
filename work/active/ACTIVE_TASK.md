# P2C ACTIVE TASK

status: ready_for_codex
next_actor: codex
active_task_id: M32_A1_A2_BASELINE_HYGIENE
active_task_file: work/active/M32_A1_A2_Baseline_Hygiene_Task.md
expected_output_dir: packages/proposed/P2C_M32_A1_A2_Baseline_Hygiene_Result_Codex_v1/
review_output_hint: reviews/M32_A1_A2_Baseline_Hygiene_Audit_Claude_v1.md

## Gate decision recorded (2026-07-07, User)
- **M32 seeded MC harness (Layer B): ACCEPTED** as a passing milestone, on Claude's GO audit
  (`reviews/M32_Audit_Claude_v1.md`).
- **GitHub baseline import / repo consolidation (Layer A): NOT accepted — remains PROPOSED**, not
  accepted project truth, until required changes A1 and A2 are cleared.

## Current project checkpoint
- Operating Manifest v4: accepted baseline.
- Participant Voice Charter: accepted and active.
- GitHub workflow: active manual loop, no mailbox automation yet.
- M31 Monte Carlo policy: accepted after folded C-1 correction.
- M32 seeded MC harness: accepted (Layer B).
- GitHub baseline import: PROPOSED (Layer A), pending A1/A2 hygiene delta.
- M26-M30 operation mechanics blueprint: open/context only, not accepted.

## What Codex should do
Build the A1/A2 baseline-hygiene delta defined in `work/active/M32_A1_A2_Baseline_Hygiene_Task.md`:
1. A1 — declare reproducible runtime/dev dependencies (PyYAML, jsonschema, pytest, and any other needed
   for clean-clone test reproduction) in repo config.
2. A2 — import the committed tests covering the M32 load-bearing imported kernel
   (legality/pool_builders, legality/predicates, sampling/weighted, sampling/exact, static_data/*,
   domain/*, and any other imported layer M32 depends on) and re-establish the prior accepted package
   SHA/pin for the imported baseline.
3. Run the pre-build critique or write "No material objections; proceeding."
4. Write the result under expected_output_dir; do not create a ZIP if unpacked files are practical.
5. Update this file: status: ready_for_claude, next_actor: claude, result_path, builder_summary.
6. Commit and push.

## Hard constraints for this task
- Do NOT implement new mechanics.
- Do NOT expand beyond baseline hygiene.
- Do NOT accept the imported baseline as project truth (keep it PROPOSED; touch no ledger acceptance row).
- Do NOT start M33 yet.

## Stop conditions
STOP_OR_ESCALATION if:
- required repo files are missing;
- clearing A1/A2 would require new executable mechanics or M33 work;
- the prior accepted package/SHA cannot be located (report it — do not fabricate a pin);
- importing kernel tests would pull in unaccepted mechanics or expand scope beyond baseline hygiene.
