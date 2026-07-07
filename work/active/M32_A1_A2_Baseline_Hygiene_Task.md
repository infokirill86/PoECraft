# P2C M32-A1/A2 — Baseline Hygiene Delta (dependencies + imported-kernel tests/pin)

task_id: M32_A1_A2_BASELINE_HYGIENE
task_type: baseline_hygiene_delta
source_agent: ChatGPT/User gate decision (2026-07-07)
target_agent: Codex
origin: Claude M32 audit `reviews/M32_Audit_Claude_v1.md` (verdict GO WITH CHANGES), required changes A1 + A2
allowed_actions: declare reproducible dependencies; import the committed tests covering the M32 load-bearing imported kernel; re-establish the prior accepted package SHA/pin for the imported baseline; docs
forbidden_actions: new executable mechanics; expanding beyond baseline hygiene; accepting imported baseline as project truth; starting M33; optimizer/advice/ranking; public numeric release; source/provenance/MML/PD-013 closure
expected_output: packages/proposed/P2C_M32_A1_A2_Baseline_Hygiene_Result_Codex_v1/

## Why this task exists

M32 (Layer B — the seeded MC harness) was **accepted** at the gate on Claude's GO audit.
The GitHub baseline import (Layer A) was **NOT accepted** and remains PROPOSED. This task clears the
two required changes from the M32 audit so the imported baseline can later be brought to a gate.

This is a hygiene/transparency delta only. It does not add features and does not itself accept the
baseline as truth — acceptance stays with the ChatGPT/User gate after Claude re-audits this delta.

## A1 — Declare reproducible runtime/dev dependencies

Problem found in audit: `pyproject.toml` declares **zero dependencies**, but the runtime imports
`yaml` and `jsonschema`, and the test suite needs `pytest`. A fresh clone cannot reproduce the
"tests/smoke passed" claim without an auditor discovering and installing dependencies by hand.

Do:
- Declare reproducible runtime + dev dependencies in repo config (`pyproject.toml`
  `[project].dependencies` / an optional `[project.optional-dependencies].dev`, or an equivalent
  pinned `requirements` file the repo standardizes on). Cover at least:
  - `PyYAML` (imported as `yaml`)
  - `jsonschema`
  - `pytest`
  - any other dependency required for a clean-clone test + smoke reproduction
- Prefer version pins or floors that make a clean clone reproducible.
- Document the exact install + test/smoke commands a fresh clone runs (in the package README or repo docs).
- Provide evidence the flow works from a clean environment (e.g., install from the declared config,
  then run the M32 suite and smoke).

## A2 — Import the M32 load-bearing kernel tests + re-establish the prior accepted SHA/pin

Problem found in audit: the imported kernel M32 depends on was committed **without its test suite**
(`BASELINE_IMPORT_INVENTORY.md` §5 confirms the local `tests/*` were intentionally left untracked),
and the inventory states the "exact prior package pin is not re-established." Inside the repo the
kernel's correctness therefore cannot be re-verified by execution — only M32's thin layer is tested.

Do:
- Import (via this separate audited delta) the committed tests covering the M32 load-bearing imported
  kernel layers, at minimum:
  - `legality/pool_builders`
  - `legality/predicates`
  - `sampling/weighted`
  - `sampling/exact`
  - `static_data/*`
  - `domain/*`
  - any other imported kernel layer M32 depends on
- Wire the imported tests into the repo test configuration so a clean clone runs them
  (note: current `pyproject.toml` `testpaths` is narrowed to `tests/monte_carlo` — widen appropriately
  without breaking the M32 suite).
- Re-establish the prior accepted package SHA/pin for the imported baseline: record which prior
  accepted local package the imported `src/p2c_engine/*`, `data/*`, `config/*`, `schemas/*`, and
  `tools/validate_*` came from, with its SHA, so the import is traceable rather than free-floating.
- Keep every imported file marked PROPOSED. Do not update any ledger row to claim the baseline is accepted.

## Pre-build critique (required before building)

State material objections / improvements / scope risks, or write
"No material objections; proceeding." STOP_OR_ESCALATION if the task appears to require anything on the
forbidden list.

## Required output structure

Place result under: `packages/proposed/P2C_M32_A1_A2_Baseline_Hygiene_Result_Codex_v1/`

Recommended files:
- 00_README_FIRST.md
- 01_A1_DEPENDENCY_REPRODUCIBILITY_REPORT.md
- 02_A2_KERNEL_TEST_IMPORT_AND_PIN_REPORT.md
- 03_CLEAN_CLONE_REPRODUCTION_EVIDENCE.md
- 04_CLAUDE_AUDIT_REQUEST.md
- PACKAGE_MANIFEST.md
- SHA256SUMS.txt
- repo changes: dependency config, imported kernel tests, updated test config, updated BASELINE_IMPORT_INVENTORY pin

Do not include old ZIPs or bulk historical artifacts.

## Stop conditions

STOP_OR_ESCALATION if:
- required repo files are missing;
- clearing A1/A2 would require new executable mechanics or M33 work;
- the prior accepted package/SHA cannot be located (report it — do not fabricate a pin);
- importing kernel tests would pull in unaccepted mechanics or expand scope beyond baseline hygiene.

## After completion

Update `work/active/ACTIVE_TASK.md`:
- status: ready_for_claude
- next_actor: claude
- result_path: packages/proposed/P2C_M32_A1_A2_Baseline_Hygiene_Result_Codex_v1/
- builder_summary: concise summary

Then commit and push.
