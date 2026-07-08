# P2C ACTIVE TASK

status: ready_for_claude
next_actor: claude
active_task_id: M33_ORACLE_CONVERGENCE
active_task_file: packages/proposed/P2C_M33_Oracle_Convergence_Result_Codex_v1/00_README_FIRST.md
result_path: packages/proposed/P2C_M33_Oracle_Convergence_Result_Codex_v1/
review_output_hint: reviews/M33_Oracle_Convergence_Audit_Claude_v1.md
base_commit: a27d09a
gate_decision: M33 authorized by ChatGPT/User on 2026-07-08.
builder_summary: M33 added test-only oracle-convergence validation for accepted `ordinary_add`. The accepted M32 seeded Monte Carlo harness is compared to exact/oracle branch expectations on small fake known-answer fixtures. No runtime mechanics were changed. No public numeric probability values were released. M34 remains closed.

## Gate decision recorded (2026-07-08, User)

- Authorize M33.
- Use the PoECraft GitHub repo and `ACTIVE_TASK.md`.
- Validate accepted M32 seeded Monte Carlo harness against exact/oracle layer for accepted `ordinary_add` only.
- Keep numeric probability evidence internal or quarantined unless existing rules explicitly allow publication.
- Prepare Claude audit request.
- Do not enable supervised auto-run.
- Do not add GitHub Actions.

## Current project checkpoint

- Operating Manifest v4: accepted baseline.
- Participant Voice Charter: accepted and active.
- GitHub workflow: active manual loop, no mailbox automation yet.
- GitHub baseline import Layer A: accepted and pinned as project-model GitHub baseline.
- M31 Monte Carlo policy: accepted after folded C-1 correction.
- M32 seeded MC harness: accepted (Layer B).
- A1/A2 baseline hygiene: accepted.
- Supervised auto-run protocol metadata: accepted documentation-only metadata, still disabled.
- M33 oracle-convergence result: ready for Claude audit.
- SOURCE/PROVENANCE, MML, and PD-013 remain open.
- M34: not open.

## M33 result summary

Added:

- `tests/monte_carlo/test_m33_oracle_convergence.py`
- `packages/proposed/P2C_M33_Oracle_Convergence_Result_Codex_v1/`

The M33 test layer covers:

- two-branch ordinary-add oracle fixture;
- three-branch ordinary-add oracle fixture;
- empty-pool no-transition oracle fixture;
- shared injected pool-builder proof for exact/oracle and Monte Carlo paths.

## Validation summary

Executed checks:

- `python -m pytest tests/monte_carlo/test_m33_oracle_convergence.py -q`
- `python -m pytest tests/monte_carlo -q`
- `python tools/validate_foundation.py`
- `python tools/validate_m4.py`
- `python -m pytest -q`
- `python tools/check_public_numeric_leaks.py packages/proposed/P2C_M33_Oracle_Convergence_Result_Codex_v1`
- `python tools/check_sha256sums.py packages/proposed/P2C_M33_Oracle_Convergence_Result_Codex_v1/SHA256SUMS.txt`
- `python tools/check_sha256sums.py SHA256SUMS.txt`
- `git diff --check`

All checks passed.

## What Claude should do next

Audit:

- `tests/monte_carlo/test_m33_oracle_convergence.py`
- `packages/proposed/P2C_M33_Oracle_Convergence_Result_Codex_v1/`
- this `ACTIVE_TASK.md`

Return GO, GO WITH CHANGES, or NO-GO.

## What ChatGPT/User should do after Claude

Make an explicit gate decision.

No artifact in this commit accepts M33 automatically.

## Optional automation control (inactive)

This block is metadata only. It does not enable automation by itself.

```yaml
automation:
  mode: manual
  enabled: false
  max_handoffs: 0
  current_handoff_count: 0
  human_gate_required: true
  allowed_next_actors:
    - codex
    - claude
  stop_on:
    - NO_GO
    - GO_WITH_CHANGES_REQUIRES_DESIGN_DECISION
    - scope_expansion
    - missing_required_bytes
    - sha_mismatch
    - test_failure
    - dependency_or_provenance_uncertainty
    - builder_auditor_conflict
    - accepted_truth_update_needed
    - milestone_transition
    - max_handoffs_reached
```

Manual mode means Kirill still sends each `Go`.

Future `supervised_auto_run` mode, if explicitly enabled later, means agents may pass the turn for a limited number of handoffs. It still cannot accept project truth, start a new milestone, update accepted ledgers, or bypass ChatGPT/User authority. Any listed stop trigger must set `status: blocked_for_human` and `next_actor: chatgpt_user`.

## Stop conditions still active

STOP_OR_ESCALATION if:

- the task starts M34;
- the task changes executable mechanics beyond test-only oracle validation;
- operation expansion beyond accepted `ordinary_add` appears;
- public output leaks probability values;
- optimizer/advice/ranking, economics, EV, or expected-attempts work appears;
- source/provenance, MML, or PD-013 closure is claimed;
- supervised auto-run or GitHub Actions are enabled.
