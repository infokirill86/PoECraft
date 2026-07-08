# Layer A Source-Bundle Byte-Verification Audit (Claude)

audit_id: `LayerA_Source_Bundle_Byte_Verification_Audit_Claude_v1`
auditor: `claude`
package: `packages/proposed/P2C_Source_Bundle_Byte_Verification_Result_Codex_v1/`
repo_head_audited: `85f40cb`
base_commit: `b199bf6`
verdict_style: `GO / GO WITH CHANGES / NO-GO`
authority_note: advisory only. Claude does not accept or close. Acceptance stays with ChatGPT/User.

---

## Plain-language summary
Codex tried to prove the imported code is byte-for-byte the same as an earlier "accepted" package. It
compared against three archived ZIPs and honestly reported **0 matches** — because those ZIPs contain only
documents/ledgers, not the actual code. That part is truthful, not an overclaim. **But the real source of
the imported code was sitting right here on the machine** — the original local working tree at
`Documents/GitHub/PoECraft`, which Codex's own earlier inventory had even pointed to. I compared the repo's
Layer A against it directly: **all 79 source files match byte-for-byte, 0 differ.** So the import did not
corrupt or alter anything — it is a faithful copy of its origin. The one thing still genuinely open: that
origin was a *working tree*, never a formally *accepted* package, so there is no historical "accepted SHA"
to point back to. **Verdict: GO WITH CHANGES** — the package is honest but reached the wrong conclusion by
using the wrong source; the working-tree comparison should be folded in. Layer A stays NOT accepted; the
gate now has a clean, well-supported choice (below). No milestone (M33) starts here.

## Verdict
**GO WITH CHANGES.** The deliverable is honest and integrity-clean and correctly keeps Layer A on HOLD, but
its central conclusion ("no byte-level matches; provenance gap") is materially incomplete: it did not
compare against the actual origin source tree, which is present locally and yields an exact match.

## What was executed / reconstructed
- **Source ZIPs are genuine but doc-only.** The three `SOURCE_BYTES/*.zip` are byte-identical to the prior
  accepted copies in `Downloads/` (SHA match), so their provenance is real — but they contain **0 `.py`**;
  only README/ledger/register docs. They cannot byte-verify any runtime/data/config/schema file.
- **Codex's 0-match count is real and honestly reported.** Independently confirmed a repo source file
  (`legality/pool_builders.py`) does not appear in any source ZIP entry. `02_BYTE_COMPARISON_REPORT.md`,
  `03_GAPS_AND_LIMITS.md`, and `00_README` state 0 matches / a provenance gap without overclaiming, and keep
  Layer A HOLD. Package `SHA256SUMS.txt` self-check: 13/13 clean. Ledgers untouched since `b199bf6`.
- **The correct source exists locally and matches exactly.** `Documents/GitHub/PoECraft` is the original
  pre-GitHub working tree named in `BASELINE_IMPORT_INVENTORY.md` §5. Comparing the repo's Layer A surfaces
  (`src/`, `data/`, `config/`, `schemas/`, `tools/validate_*`) against it: **79 source files, 79 byte-identical,
  0 differ, 0 missing** (the only non-matches were local `__pycache__/*.pyc` build artifacts, not source).

## What this proves — and what it does not
- **Proven: import fidelity.** The GitHub Layer A import is a faithful, unaltered copy of the local baseline
  it came from. Nothing was corrupted or silently changed in the migration.
- **Still open: formal prior acceptance.** The origin is a *working tree*, not a gated/accepted package with
  an accepted SHA. There appears to be no historical accepted ZIP for the runtime code (only doc-rollups were
  ever packaged). So "byte-verified against a prior *accepted* package" cannot be satisfied — because that
  package never existed. This is the same class as the standing **open, non-blocking SOURCE/PROVENANCE**
  boundary the project already accepts under "project-model truth, not server truth."

## Required change (fold into the package record)
- Supersede the "no matches / provenance gap" framing with the working-tree comparison result
  (repo Layer A == `Documents/GitHub/PoECraft`, 79/79 exact). The gap was a *wrong-source* artifact, not an
  unverifiable import. A short Codex delta (or an appended note) should record this so the package stands on
  its own.

## Recommendation to the gate (advisory — your decision, with ChatGPT/Codex)
Two clean paths; the hunt for a "prior accepted runtime ZIP" is not one of them (it does not exist):
1. **Accept-and-pin now (recommended).** Declare the current repo Layer A the accepted baseline package and
   pin its SHA going forward, with provenance recorded as "imported from local working tree, byte-verified
   79/79; no prior formal packaging (runtime lived as a working tree)." This converts an open-ended provenance
   hunt into a one-time gate action, and it is well-supported: import fidelity is proven and the kernel is
   already tested (A2) and reproducible (A1).
2. **Hold under the standing provenance-open rule.** Keep Layer A proposed and treat the missing formal
   acceptance as the existing open SOURCE/PROVENANCE boundary — consistent with how the project already treats
   data provenance — deciding acceptance later.

## Boundary checks (all clear)
No new mechanics; no M33; no optimizer/advice/ranking/EV; no public numeric probability release; no
source/provenance, MML, or PD-013 closure; no accepted-ledger truth update. Layer A remains HOLD / NOT
ACCEPTED in the package and in this audit.

---
- author: `claude`
- document_type: `source_bundle_byte_verification_audit`
- status: `advisory verdict — GO WITH CHANGES; Layer A acceptance pending ChatGPT/User`
