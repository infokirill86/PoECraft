# P2C Repo Integrity SHA Floor - Codex v1

package_id: `P2C_Repo_Integrity_SHA_Floor_Codex_v1`
package_type: `REPO_HYGIENE_RESULT_DELTA`
status: `proposed_for_claude_audit`

observed_repo_head: `4e560c6b7a20e9b1cee6d79e52b68b7eaabd9aff`
observed_active_task_sha: `6e1f7bc1e20076e1aa002a886f079ad84132d1174a13db68f90ddcbf8f98c043`

## Plain-language summary for Kirill

The root `SHA256SUMS.txt` file drifted again because it was being maintained manually. That file is the repo's integrity checklist: it says "this file should have this exact byte fingerprint."

This package adds the smallest practical fix:

- a new deterministic updater: `tools/update_sha256sums.py`;
- a workflow rule that says root `SHA256SUMS.txt` must be regenerated mechanically before push;
- a verification step that checks the regenerated file.

This is repo hygiene only. It does not start M36-A, does not implement heterogeneous chains, does not add a new operation, and does not change mechanics/data semantics.

## Current gate result recorded

The M36 heterogeneous-chain design is recorded as accepted after Claude `GO WITH CHANGES` audit, but only as design. M36-A implementation remains closed until a separate explicit ChatGPT/User gate.

