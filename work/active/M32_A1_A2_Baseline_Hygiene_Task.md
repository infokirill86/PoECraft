# P2C M32-A1/A2 — Baseline Hygiene Delta (dependencies + imported-kernel tests/pin)

task_id: M32_A1_A2_BASELINE_HYGIENE
task_type: baseline_hygiene_delta
source_agent: ChatGPT/User gate decision (2026-07-07)
target_agent: Codex
origin: Claude M32 audit `reviews/M32_Audit_Claude_v1.md` (verdict GO WITH CHANGES), required changes A1 + A2
allowed_actions: declare reproducible dependencies; import the committed tests covering the M32 load-bearing imported kernel; re-establish the prior accepted package SHA/pin for the imported baseline; docs
forbidden_actions: new executable mechanics; expanding beyond baseline hygiene; accepting imported baseline as project truth; starting M33; optimizer/advice/ranking; public numeric release; source/provenance/MML/PD-013 closure
expected_output: packages/proposed/P2C_M32_A1_A2_Baseline_Hygiene_Result_Codex_v1/

## Gate decision

- M32 seeded MC harness (Layer B): accepted as passed.
- GitHub baseline import / repo consolidation (Layer A): not accepted; remains PROPOSED.
- M33 is not open.

## Why this task exists

M32 Layer B was accepted at the gate on Claude's GO audit. The GitHub baseline import Layer A was not accepted and remains proposed. This task clears the two required changes from the M32 audit so the imported baseline can later be brought to a gate.

This is a hygiene/transparency delta only. It does not add features and does not itself accept the baseline as truth; acceptance stays with the ChatGPT/User gate after Claude re-audits this result.

## A1 — Declare reproducible runtime/dev dependencies

Problem found in audit: `pyproject.toml` declared zero dependencies, but the runtime imports `yaml` and `jsonschema`, and the test suite needs `pytest`. A fresh clone could not reproduce the tests/smoke claim without an auditor discovering and installing dependencies by hand.

Do:

- declare reproducible runtime and dev dependencies in repo config;
- cover at least PyYAML, jsonschema, pytest, and any other dependency required for clean-clone test reproduction;
- prefer version pins or floors that make a clean clone reproducible;
- document the install and test commands a fresh clone runs;
- provide evidence the validation flow works.

## A2 — Import the M32 load-bearing kernel tests + re-establish the prior accepted SHA/pin

Problem found in audit: the imported kernel M32 depends on was committed without its test suite, and the inventory states the exact prior package pin was not re-established. Inside the repo the kernel's correctness therefore cannot be re-verified by execution; only M32's thin layer was tested.

Do:

- import the committed tests covering the M32 load-bearing imported kernel layers, at minimum:
  - `legality/pool_builders`
  - `legality/predicates`
  - `sampling/weighted`
  - `sampling/exact`
  - `static_data/*`
  - `domain/*`
  - any other imported kernel layer M32 depends on
- wire the imported tests into repo test configuration;
- re-establish the prior accepted package SHA/pin for the imported baseline;
- keep every imported file marked PROPOSED;
- do not update any ledger row to claim the baseline is accepted.

## Pre-build critique

No material objections; proceeding.

Scope risk noted: restoring the old kernel tests touches some functions present in the imported pool-builder module beyond the single M32 ordinary-add lane. This does not open new mechanics or accept them as project truth; it only restores executable coverage for already-imported proposed baseline code.

## Codex completion note

Result produced at:

`packages/proposed/P2C_M32_A1_A2_Baseline_Hygiene_Result_Codex_v1/`

Status after Codex work: ready for Claude audit.

## Stop conditions

STOP_OR_ESCALATION if:

- required repo files are missing;
- clearing A1/A2 would require new executable mechanics or M33 work;
- the prior accepted package/SHA cannot be located;
- importing kernel tests would pull in unaccepted mechanics or expand scope beyond baseline hygiene.
