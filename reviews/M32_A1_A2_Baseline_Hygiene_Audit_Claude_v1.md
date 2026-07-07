# M32 A1/A2 Baseline-Hygiene + Auto-Run Protocol Audit (Claude)

audit_id: `M32_A1_A2_Baseline_Hygiene_Audit_Claude_v1`
auditor: `claude`
package: `packages/proposed/P2C_M32_A1_A2_Baseline_Hygiene_Result_Codex_v1/`
repo_head_audited: `85b0236`
base_commit: `e981202`
verdict_style: `GO / GO WITH CHANGES / NO-GO`
authority_note: advisory only. Claude does not accept or close. Acceptance stays with ChatGPT/User.

---

## Plain-language summary
Codex fixed the two things I flagged in the previous audit, and added a safe "future automation, switched
off" note. **On my own clean run, everything works: 86 of 86 tests pass, the integrity checks match, and
nothing was quietly marked as accepted.** The forgotten dependencies are now written down, the borrowed
engine finally has its own tests back, and the record of where that engine came from is restored (as a
traceable note, not yet a byte-for-byte re-check — that last step belongs to the later "accept the whole
imported code" gate). The automation block is pure documentation: it is turned off, cannot accept anything,
and cannot start the next milestone. Verdict: **GO**. Next: this goes to you / ChatGPT to decide whether the
imported baseline (Layer A) is now ready to be accepted, or held for the byte-level bundle first. No new
milestone (M33) starts here.

## Verdict
- **A — A1/A2 baseline hygiene: GO.**
- **B — supervised auto-run protocol metadata: GO.**
- **Overall: GO** (advisory). Two forward, non-blocking notes for the eventual Layer-A acceptance gate below.

## What was executed / reconstructed
- **Full test suite, clean run: 86 passed** (restored decisions, domain, legality, sampling, static_data
  + the M32 Monte Carlo suite). Foundation and M4 validators run and emit their fingerprints.
- Integrity: root `SHA256SUMS.txt` → `PASS`; package `SHA256SUMS.txt` recomputed independently, 7/7 match.
- Reproducibility note: on this Windows machine a bare `pytest` first produced 20 `PermissionError`
  setup errors on the default `pytest-of-infok` temp dir. Pointing pytest at a writable `--basetemp`
  gave 86/86. This is an **environment/temp-dir quirk, not a code or test defect** — see forward note 2.

## A — A1/A2 findings (GO)
- **A1 (dependencies) — cleared.** `pyproject.toml` now declares runtime deps `PyYAML>=6.0,<7` and
  `jsonschema>=4.0,<5`, dev dep `pytest>=8.0,<9`, and widens `testpaths` to the restored kernel test
  dirs plus `tests/monte_carlo`. These are exactly the imports that a fresh clone previously lacked;
  the suite now resolves and runs from the declared config. No vendored third-party code added.
- **A2 (kernel tests) — cleared.** Restored tests cover the load-bearing imported kernel M32 depends on:
  legality pool-builders/predicates (through behavior), sampling weighted + exact, decisions, domain
  state/model shape, and static-data loading/validation/fingerprints/initial-state. Verified by execution,
  not by claim.
- **Baseline pin — re-established as traceability, honestly scoped.** `03_BASELINE_PIN_RECONCILIATION.md`
  records candidate prior accepted baseline SHAs from the historical index and explicitly states the index
  is provenance metadata, not byte-level audit evidence, deferring any byte comparison to a separate
  SOURCE_BUNDLE. This matches what A2 asked for (re-establish the pin/traceability) without overclaiming.
- **No silent acceptance — confirmed.** `git diff e981202..HEAD -- ledger/` is empty (ledgers untouched);
  all delta files are marked PROPOSED; `PACKAGE_MANIFEST.md` states "No accepted-ledger update."

## B — supervised auto-run protocol metadata findings (GO)
- **Documentation/protocol only — confirmed.** The only manifest change is
  `manifest/GitHub_Workflow_Protocol.md` (+27 lines) plus the descriptive `automation` block in
  `ACTIVE_TASK.md`. No executable code.
- **No real automation — confirmed.** No `.github/` directory, no workflow YAML, no watcher / cron /
  scheduler code anywhere in the delta.
- **Canonical values — confirmed present:** `mode: manual`, `enabled: false`, `max_handoffs: 0`,
  `human_gate_required: true`.
- **Human gate authority mandatory — confirmed.** Protocol states no auto-run may mark anything accepted,
  update accepted truth, update accepted ledgers, start a new milestone, or bypass ChatGPT/User authority;
  every `stop_on` trigger forces `status: blocked_for_human`, `next_actor: chatgpt_user`.
- **Cannot accept truth / update ledgers / start M33 — confirmed** by the protocol text and stop triggers
  (`accepted_truth_update_needed`, `milestone_transition`, `max_handoffs_reached`).
- **Plain-language summary requirement — present** (`GitHub_Workflow_Protocol.md` §"Plain-language summary
  requirement": every Codex result and Claude audit must include a short human-readable summary of what was
  done, why, what changed, what was tested, what stays proposed, who is next, and whether a human must decide).

## Forbidden-scope checks (all clear)
No code feature implemented (config + restored tests + docs only); no M33; no new mechanics; no
optimizer/advice/ranking/EV; no public numeric probability release; no source/provenance, MML, or PD-013
closure; no accepted-ledger truth update.

## Forward, non-blocking notes (for the later Layer-A acceptance gate — not defects here)
1. **Traceability ≠ byte-verification.** The imported baseline is now *traceable* (pin recorded) but not
   yet *byte-verified in-repo* against the prior accepted package. Byte-level comparison via a separate
   SOURCE_BUNDLE / FULL_REPRODUCIBILITY_BUNDLE remains the step before Layer A is accepted as truth.
   Codex already flags this in `03_BASELINE_PIN_RECONCILIATION.md`; it is the natural next request.
2. **Clean-clone robustness on Windows.** A bare `pytest` hit a temp-dir permission error on this machine;
   the suite passes with a writable `--basetemp`. Worth a one-line note in the run docs (or a repo-local
   temp default) so A1's "clean clone reproduces" promise holds on Windows without the auditor knowing the trick.

## Recommendation
- **A1 and A2 are delivered and verified by execution → GO.** The imported baseline (Layer A) can be taken
  to its acceptance gate at ChatGPT/User discretion; forward note 1 is the remaining condition if you want
  byte-level assurance before accepting Layer A as truth.
- **The auto-run protocol metadata is safe (docs-only, disabled, human gate mandatory) → GO.** It does not
  authorize any automation.
- Nothing here self-accepts or self-closes; advisory input to the gate. M33 stays closed.

---
- author: `claude`
- document_type: `baseline_hygiene_and_protocol_audit`
- status: `advisory verdict — GO; acceptance pending ChatGPT/User`
