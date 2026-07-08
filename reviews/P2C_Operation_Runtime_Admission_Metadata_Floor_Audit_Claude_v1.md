# Operation Runtime-Admission Metadata Floor Audit (Claude)

audit_id: `P2C_Operation_Runtime_Admission_Metadata_Floor_Audit_Claude_v1`
auditor: `claude`
package: `packages/proposed/P2C_Operation_Runtime_Admission_Metadata_Floor_Codex_v1/`
observed_repo_head: `6c9d75d2bb930979b0cf229ceb4b2f6e699dca39`
observed_active_task_sha: `5f467efdf887dbd9de4fe8fd887d443b5776983fd239ddea00b82ede5928322a`  (SHA-256 of the exact `work/active/ACTIVE_TASK.md` bytes audited, at HEAD 6c9d75d, before this review's dispatcher update)
verdict_style: `GO / GO WITH CHANGES / NO-GO`
authority_note: advisory only. This edits accepted data (`operations.yaml`) and a validator; acceptance of the
data change stays with ChatGPT/User.

---

## Plain-language summary
This floor adds the "is it actually runnable?" tag to every currency in the database and wires in a guard so
the engine can never treat "in scope" as "runnable." The classification matches exactly what we agreed in the
reconciliation (only Annulment is marked executable; nothing new became runnable). It also correctly retunes
the model's "fingerprint" so it now tracks only the genuinely-runnable operations — that change is intentional,
explained, and all tests were updated (110 pass). **One real slip: the repo's integrity checksum file was left
out of date** for the edited data — a fresh clone's checksum check fails. I've corrected that checksum as part
of this review and flagged it. **Verdict: GO WITH CHANGES** — the substance is right; the checksum had to be
fixed, and the builder should deliver a consistent checksum next time. The data edit itself is still your gate.

## Verdict
**GO WITH CHANGES.** The classification, validator, and fingerprint retune are correct and match the accepted
reconciliation; nothing new became executable. The one required correction — an inconsistent root
`SHA256SUMS.txt` — has been applied in this audit commit and is flagged below.

## What was verified
- **`operations.yaml` change is purely additive.** 0 deletions; exactly **37** `runtime_admission_status`
  lines added — one per operation. No existing weights, `active_in_current_simulation` flags, or semantics were
  altered.
- **Classification matches the accepted reconciliation exactly.** Distribution:
  `accepted_executable_runtime = 1` (**annulment only**), `admission_candidate = 13` (exalted×3, chaos×3,
  perfect_essence×6, install_astrid), `data_reference_candidate = 18`, `blocked_or_out_of_scope = 4`
  (jawbone×3, reveal_desecrated), `disputed_or_requires_user_resolution = 1` (fracturing_orb). Total 37.
- **Nothing new became executable.** Only `annulment` is `accepted_executable_runtime`; `ordinary_add` remains
  an engine primitive, not a currency row.
- **Fail-closed validation added (`checks.py`) — correct.** `runtime_admission_status` must be a valid enum;
  `accepted_executable_runtime` requires `active_in_current_simulation` AND a handler declaration. This is the
  guard the reconciliation asked for: the active flag alone can never authorize runtime.
- **Semantic-fingerprint retune is intentional, documented, and sound.** `semantic.py` now admits a row into
  the runtime semantic projection only if `runtime_admission_status == accepted_executable_runtime` (not merely
  active). The fingerprint therefore changed `b268eb88… → acc50b83…`; `00_README`/`03` document this and the
  fingerprint tests were updated. This is a *correct improvement*: the runtime semantic fingerprint now tracks
  only the truly-executable surface, and will move on future admission events rather than on catalog/reference
  edits. `validate_foundation` PASS; `validate_m4` PASS.
- **Regression clean:** full suite (excluding the heavy M34-B1 file) = **110 passed**, fingerprint change fully
  absorbed by updated tests. Package numeric-leak scan PASS; package internal `SHA256SUMS` PASS. Ledger diff
  carries only the prior reconciliation acceptance — no self-accept of this floor.

## Required change (applied in this audit commit)
- **Root `SHA256SUMS.txt` was inconsistent at the delivered HEAD.** `check_sha256sums.py` FAILed:
  `data/operations.yaml` (expected `5729ebd…`, got `e0763a9…`) and the floor package's own `SHA256SUMS.txt`
  (expected `eefe2d48…`, got `1dca42b…`) had stale hashes — the builder edited the data but did not refresh the
  root manifest. This defeats the standing SHA-verification rule on a clean clone. I recomputed and corrected
  these entries in this review's commit so the repo integrity check passes again; the **builder should deliver
  a consistent root `SHA256SUMS.txt`** with any data/validator change.

## Minor note (non-blocking)
- **Fingerprint lineage.** The prior fingerprint `b268eb88…` is still recorded in the historical M35-A evidence
  doc (`packages/proposed/P2C_M35A_Annulment_Runtime_Result_Codex_v1/04_TEST_AND_CHECKS_REPORT.md`). That is a
  correct historical record of what was true at M35-A time; leave it. Going forward, `acc50b83…` is the current
  semantic fingerprint as of this floor.

## Boundaries (confirmed)
No operation became newly executable; no heterogeneous chains; no public numeric release; no optimizer/
economics/advice; no automation; no SOURCE/PROVENANCE, MML, or PD-013 closure. The `operations.yaml` edit is a
data change and remains a ChatGPT/User-approved gate; the specific status assignments (esp. `install_astrid`
= `admission_candidate`, `fracturing_orb` = `disputed_or_requires_user_resolution`) are the project-truth
judgments to confirm at that gate.

## Recommendation
Accept the metadata floor (with the root-SHA correction applied). Its proposed later fail-closed runtime
validator — runtime executes only `accepted_executable_runtime` — is already partly realized by the `checks.py`
additions; keep the runtime-execution gate for it explicit when heterogeneous chains are built. After this
floor is accepted, resume M36 heterogeneous-chain design over accepted `ordinary_add` + base Annulment only.
Nothing self-accepts.

---
- author: `claude`
- document_type: `data_and_validator_floor_audit`
- status: `advisory verdict — GO WITH CHANGES (root SHA corrected); data-change acceptance pending ChatGPT/User`
