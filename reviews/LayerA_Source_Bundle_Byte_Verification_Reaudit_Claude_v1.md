# Layer A Source-Bundle Byte-Verification RE-AUDIT (Claude)

audit_id: `LayerA_Source_Bundle_Byte_Verification_Reaudit_Claude_v1`
auditor: `claude`
supersedes_change_from: `reviews/LayerA_Source_Bundle_Byte_Verification_Audit_Claude_v1.md` (GO WITH CHANGES)
package: `packages/proposed/P2C_Source_Bundle_Byte_Verification_Result_Codex_v1/`
repo_head_audited: `18f6f6a`
verdict_style: `GO / GO WITH CHANGES / NO-GO`
authority_note: advisory only. Claude does not accept or close. Acceptance stays with ChatGPT/User.

---

## Plain-language summary
This is the follow-up check after Codex fixed what I flagged last time. Codex folded my finding into the
package: it now says plainly that the old "0 matches" was a wrong-source comparison against document-only
ZIPs, and it records that the imported code matches its real origin (the local working tree) byte-for-byte.
Codex also re-ran the comparison itself. **I re-checked its numbers against the actual files, row by row:
75 of 75 match, 0 differ, 0 missing — genuine, not just claimed.** Package integrity is clean and nothing
was quietly accepted. **Verdict: GO** — the correction is done and verified. The only thing still open is a
decision for you/ChatGPT: how to treat "the code has no earlier *formally accepted* package" — that is a
gate choice, not a defect.

## Verdict
**GO.** The required change from the prior audit is properly folded in and independently verified. Layer A
import fidelity is now documented in the package with correct, non-fabricated evidence, and the honest
fidelity-vs-formal-acceptance distinction is preserved. Layer A correctly remains HOLD / NOT ACCEPTED.

## What was executed / reconstructed
- **Correction folded in.** New `05_WORKING_TREE_COMPARISON_CORRECTION.md`; `02_BYTE_COMPARISON_REPORT.md`
  and `03_GAPS_AND_LIMITS.md` now mark the old `0/75` ZIP result as superseded wrong-source evidence
  (preserved, not deleted) and point to `Documents/GitHub/PoECraft` as the true origin.
- **Codex's own recalculation independently re-verified.** `WORKING_TREE_BYTE_COMPARISON.csv` (75 rows,
  columns repo_path / repo_sha256 / origin_working_tree_path / origin_sha256 / status). I recomputed every
  row's SHA against both the repo and the origin working tree: **75 identical, 0 differ, 0 missing** — the
  claimed result is real.
- **Integrity + boundaries clean.** Package `SHA256SUMS.txt` self-check 15/15. Ledgers untouched since the
  prior audit. No new mechanics, no M33, no optimizer/advice, no public numeric release, no source/provenance
  or MML or PD-013 closure, no accepted-ledger update. Layer A stays HOLD in the package.
- **Count reconciliation is honest.** My prior audit counted 79 Layer A source files; Codex's package-surface
  list counts 75. The package explains the difference (broader Layer A source count vs package imported-baseline
  surface list); both reach the same conclusion and neither overclaims.

## Standing conclusion (unchanged, now fully evidenced in-package)
- **Proven: import fidelity.** GitHub Layer A is a faithful, unaltered byte-for-byte copy of its local origin.
- **Still open: formal prior acceptance.** No accepted runtime package/SHA ever existed (runtime lived as a
  working tree). This is a gate decision, of the same class as the standing open SOURCE/PROVENANCE boundary.

## Recommendation to the gate (advisory — unchanged)
1. **Accept-and-pin now (recommended):** declare the current repo Layer A the accepted baseline and pin its
   SHA, provenance recorded as "byte-verified to local origin working tree; no prior formal packaging." One
   clean gate action; well-supported (fidelity proven, kernel tested via A2, reproducible via A1).
2. **Hold under the provenance-open rule** and decide later.

Nothing here self-accepts. This closes the byte-verification work; the Layer A acceptance decision is the
gate's. M33 stays closed until that decision.

---
- author: `claude`
- document_type: `source_bundle_byte_verification_reaudit`
- status: `advisory verdict — GO; Layer A acceptance pending ChatGPT/User`
