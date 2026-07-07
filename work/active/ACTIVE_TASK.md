# P2C ACTIVE TASK

status: claude_audit_complete
next_actor: chatgpt_user
active_task_id: M32_SEEDED_MC_HARNESS
active_task_file: work/active/M32_Seeded_MC_Harness_Task.md
result_path: packages/proposed/P2C_M32_Seeded_MC_Harness_Result_Codex_v1/
expected_output_dir: packages/proposed/P2C_M32_Seeded_MC_Harness_Result_Codex_v1/
review_output_hint: reviews/M32_Audit_Claude_v1.md
review_path: reviews/M32_Audit_Claude_v1.md
claude_verdict: GO WITH CHANGES (advisory; acceptance stays with ChatGPT/User)
claude_verdict_detail: Layer B (M32 seeded MC harness) = GO, verified by execution — shared kernel, deterministic seed replay, fail-closed invariants, numeric-free public output all confirmed. Layer A (GitHub baseline import) = GO WITH CHANGES; imported baseline must stay PROPOSED, not accepted truth, until required changes are cleared.
claude_required_changes: A1 declare runtime+dev deps in pyproject (yaml, jsonschema, pytest) so a clean clone is reproducible; A2 imported shared kernel has no committed tests and prior accepted package SHA not re-established — import kernel tests via a separate audited baseline delta and pin the SHA before accepting the baseline as truth. Non-blocking: A3 scope the public-numeric-leak tool; B-minor pin real commit SHA in run artifacts instead of the p2c.m32.dev placeholder.
builder_summary: M32 seeded MC harness implemented over accepted ordinary_add only, using the existing ordinary-add pool builder as the shared kernel; deterministic replay, invariants, micro-fixtures, validators, pytest, and real-data smoke checks passed. Documentation-only baseline import inventory added so Claude can audit the GitHub runtime/data/config/schema/tool import separately from the M32 harness.

## Current project checkpoint
- Operating Manifest v4: accepted baseline.
- Participant Voice Charter: accepted and active.
- GitHub workflow: active manual loop, no mailbox automation yet.
- M31 Monte Carlo policy: accepted after folded C-1 correction.
- M26-M30 operation mechanics blueprint: open/context only, not accepted.
- M32 result: ready for Claude audit.

## Claude audit — DONE
Audit complete at repo HEAD `fc2c5a5`. Verdict: **GO WITH CHANGES** (advisory). Full audit in
`reviews/M32_Audit_Claude_v1.md`. Layer B (M32 harness) verified by execution = GO. Layer A (baseline
import) = GO WITH CHANGES; see `claude_required_changes` above.

## What ChatGPT/User should do next (gate decision — nothing auto-accepts)
1. Decide acceptance of M32 (Layer B) on the advisory GO.
2. Keep the imported baseline (Layer A) PROPOSED until required changes A1/A2 are cleared.
3. Route A1/A2 fixes to Codex as a separate audited baseline-hygiene delta if accepted as the plan.

## Stop conditions still active
STOP_OR_ESCALATION if:
- M32 is found to require new executable mechanics;
- M32 is found to duplicate ordinary-add legality/pool/weight logic for MC;
- seeded replay is not deterministic;
- runtime invariants do not fail closed;
- public output leaks probability values;
- optimizer/advice/ranking or public numeric release appears.
- imported baseline/support files are treated as accepted project truth without Claude audit and ChatGPT/User acceptance.
