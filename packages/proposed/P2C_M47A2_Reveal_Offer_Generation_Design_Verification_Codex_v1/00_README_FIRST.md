# P2C M47-A2 Reveal Offer Generation Design Verification

Status: **PROPOSED design — ready for Claude audit; no Reveal or Echoes runtime is admitted**.

## Plain-language summary for Kirill

P2C now has the accepted Jawbone step that creates a hidden Desecrated placeholder. The next step is not simply "pick a modifier": the game first generates a random set of three offers, and only then does the player choose one. If the random offer generator is modeled incorrectly, every later probability calculation will be wrong even if the installation code is perfect.

The source check confirms the visible contour: three offers, the player chooses one, the chosen modifier replaces the placeholder on the same side, and Abyssal Echoes can reroll the offers once. Evidence strongly supports at least one compatible exclusive Desecrated offer. However, public sources still do not publish the exact offer weighting/order algorithm, and the insufficient-pool edge is only visible through player bug reports.

Therefore this package proposes a precise, auditable base-Reveal contract but does not promote D3-D5 into accepted mechanics. It recommends a later explicit User gate for D3-A, D4-A, and D5-A. Echoes should reuse the future offer generator but remain a separate implementation gate because reports conflict on whether Ancient Jawbone MML survives a reroll.

## Package map

- `01_PARTICIPANT_AND_ARCHITECTURE_CRITIQUE.md`
- `02_SOURCE_AND_REPO_EVIDENCE.md`
- `03_D3_D5_CANDIDATE_MODEL_TABLE.md`
- `04_EXACT_PROPOSED_OFFER_GENERATION_CONTRACT.md`
- `05_SELECTION_AND_INSTALL_CONTRACT.md`
- `06_ECHOES_INCLUDE_SPLIT_RECOMMENDATION.md`
- `07_FRACTURE_PD013_BOUNDARY.md`
- `08_IMPLEMENTATION_BATCH_AND_USER_DECISIONS.md`
- `09_PROBABILITY_IMPACT_AND_STOP_RULES.md`
- `10_CLAUDE_AUDIT_REQUEST.md`
- `11_READ_RECEIPT.md`
