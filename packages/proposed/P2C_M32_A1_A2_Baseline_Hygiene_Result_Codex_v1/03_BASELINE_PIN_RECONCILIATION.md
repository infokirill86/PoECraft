# Baseline Pin Reconciliation

Status: proposed provenance reconciliation; not accepted truth.

## Purpose

Claude's A2 finding noted that the prior accepted package SHA/pin was not re-established for the imported GitHub baseline material.

This delta re-establishes the audit-facing prior baseline pin set from the repository historical index, without claiming that the imported GitHub baseline is accepted truth.

## Candidate prior accepted baseline pins

| Artifact | SHA256 | Status in repo index | Use in this delta |
|---|---|---|---|
| `P2C_Baseline_Rollup_ChatGPT_accepted_v1.zip` | `2d30f6cf6dcaf045bd64d8902e28b44e99cabf418bd9861672633a7bc9d23c84` | local / migration-indexed | candidate prior accepted baseline pin |
| `P2C_Baseline_Rollup_Delta_ChatGPT_accepted_v1_1.zip` | `20ebfe60f492168423c959dcfe684a3be70863bc6255b10a326ac03408600b42` | local / migration-indexed | candidate prior accepted delta pin |
| `P2C_Baseline_Rollup_Spot_Audit_Claude_v1_1.md` | `69d5d180ef4be21004a8733e9e39acb99acd1814ec1a90af645df71440fe087c` | local / migration-indexed | candidate audit reference pin |

## Important limitation

The historical index is provenance metadata, not active audit evidence by itself. This delta does not embed historical ZIP packages and does not update accepted ledgers.

If Claude needs byte-level comparison against the prior accepted packages, the next step should be a separate SOURCE_BUNDLE or FULL_REPRODUCIBILITY_BUNDLE request. This A1/A2 hygiene delta only restores the pin record and restores executable tests for the imported kernel already present in the GitHub repo.

## Acceptance boundary

The imported GitHub baseline remains proposed until Claude audit and ChatGPT/User acceptance.
