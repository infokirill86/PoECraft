# P2C ACTIVE TASK

status: ready_for_claude
next_actor: claude
active_task_id: M32_SEEDED_MC_HARNESS
active_task_file: work/active/M32_Seeded_MC_Harness_Task.md
result_path: packages/proposed/P2C_M32_Seeded_MC_Harness_Result_Codex_v1/
expected_output_dir: packages/proposed/P2C_M32_Seeded_MC_Harness_Result_Codex_v1/
review_output_hint: reviews/M32_Audit_Claude_v1.md
builder_summary: M32 seeded MC harness implemented over accepted ordinary_add only, using the existing ordinary-add pool builder as the shared kernel; deterministic replay, invariants, micro-fixtures, validators, pytest, and real-data smoke checks passed. Documentation-only baseline import inventory added so Claude can audit the GitHub runtime/data/config/schema/tool import separately from the M32 harness.

## Current project checkpoint
- Operating Manifest v4: accepted baseline.
- Participant Voice Charter: accepted and active.
- GitHub workflow: active manual loop, no mailbox automation yet.
- M31 Monte Carlo policy: accepted after folded C-1 correction.
- M26-M30 operation mechanics blueprint: open/context only, not accepted.
- M32 result: ready for Claude audit.

## What Claude should do next
1. Audit the result package at `packages/proposed/P2C_M32_Seeded_MC_Harness_Result_Codex_v1/`.
2. Audit the M32 seeded MC harness for shared-kernel, deterministic replay, invariant, and numeric-public-boundary claims.
3. Audit the baseline import into GitHub using `packages/proposed/P2C_M32_Seeded_MC_Harness_Result_Codex_v1/BASELINE_IMPORT_INVENTORY.md`; verify that imported runtime/data/config/schema/tool support is transparent, scoped, and not silently accepted as project truth.
4. Return audit under `reviews/M32_Audit_Claude_v1.md`.

## Stop conditions still active
STOP_OR_ESCALATION if:
- M32 is found to require new executable mechanics;
- M32 is found to duplicate ordinary-add legality/pool/weight logic for MC;
- seeded replay is not deterministic;
- runtime invariants do not fail closed;
- public output leaks probability values;
- optimizer/advice/ranking or public numeric release appears.
- imported baseline/support files are treated as accepted project truth without Claude audit and ChatGPT/User acceptance.
