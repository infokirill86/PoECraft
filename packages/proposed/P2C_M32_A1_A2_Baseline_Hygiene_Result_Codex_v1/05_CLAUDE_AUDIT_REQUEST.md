# Claude Audit Request

Please audit `P2C_M32_A1_A2_Baseline_Hygiene_Result_Codex_v1`.

## Gate context

- M32 Layer B is accepted as passed by the user gate.
- GitHub baseline import Layer A remains proposed, not accepted truth.
- This delta is only for A1 and A2 baseline hygiene.
- M33 is not open.

## Verify A1

- `pyproject.toml` declares the runtime dependencies needed for clean-clone reproduction.
- `pyproject.toml` declares the dev dependency needed to run tests.
- The declared pytest discovery paths include the restored kernel tests and the existing M32 tests.
- No vendored third-party dependencies were added.

## Verify A2

- The restored tests cover the imported load-bearing kernel used by M32:
  - legality pool builders and predicates through behavior;
  - sampling weighted and exact paths;
  - decisions;
  - domain state/model shape;
  - static data loading, validation, fingerprints, and initial state materialization.
- The prior accepted baseline package SHA/pin is re-established for audit traceability without accepting the imported baseline as truth.
- The delta does not import broad new runtime layers beyond the already proposed GitHub baseline.

## Verify boundaries

- No new mechanics.
- No optimizer, advice, ranking, EV, budget, or expected-attempt logic.
- No M33.
- No public numeric probability release.
- No source/provenance, MML, or PD-013 closure.
- No accepted-ledger update claiming baseline acceptance.

Expected verdict style: GO / GO WITH CHANGES / NO-GO.
