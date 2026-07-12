# P2C M47-A2V Reveal Sampling Verification & Decision Support

Status: **PROPOSED evidence-support layer - ready for Claude audit; no Reveal or Echoes runtime is admitted**.

## Plain-language summary for Kirill

We know the visible contour: Reveal shows three offers and the player chooses one. We still do not know the exact hidden sampling algorithm well enough to encode it as project truth. This package creates the smallest practical bridge from uncertainty to a later informed decision:

- a precise in-game capture checklist;
- a canonical observation format;
- an offline validator/analyzer that finds contradictions and reports what the observations cannot distinguish;
- explicit decision criteria for D3, D4, and D5.

The analyzer cannot change runtime, data truth, ledgers, or acceptance state. A clean sample with no contradiction remains evidence, not proof. D4 is deliberately left open unless captures include reproducible item setups and the independently reconstructed eligible pool/weights.

## What changed

- Added `schemas/reveal_observation.schema.yaml`.
- Added `tools/analyze_reveal_observations.py`.
- Added focused tests in `tests/tools/test_reveal_observation_analysis.py`.
- Recorded M47-A2 design acceptance and M47-A2V authorization only.

## Package map

- `01_PARTICIPANT_CRITIQUE.md`
- `02_EVIDENCE_UPDATE.md`
- `03_IN_GAME_CAPTURE_PROTOCOL.md`
- `04_OBSERVATION_SCHEMA_AND_TEMPLATE.md`
- `05_ANALYSIS_TOOL_AND_TESTS.md`
- `06_D3_D5_DECISION_MATRIX.md`
- `07_ECHOES_AND_REMAINING_UNCERTAINTY.md`
- `08_CLAUDE_AUDIT_REQUEST.md`
- `09_READ_RECEIPT.md`
- `10_CHECKS.md`
