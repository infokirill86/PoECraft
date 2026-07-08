# Claude Audit Request

Please audit `P2C_Repo_Integrity_SHA_Floor_Codex_v1`.

## Audit questions

1. Does `tools/update_sha256sums.py` regenerate the root `SHA256SUMS.txt` deterministically?
2. Does it correctly avoid self-hashing root `SHA256SUMS.txt`?
3. Does it respect git ignored files by using tracked plus untracked non-ignored files?
4. Does `manifest/GitHub_Workflow_Protocol.md` clearly require the update/check commands before push?
5. Does this package correctly record M36 design acceptance without opening M36-A?
6. Are runtime, mechanics, data semantics, operation scope, automation, public numeric release, and SOURCE/PROVENANCE/MML/PD-013 boundaries preserved?

## Requested verdict

Return:

- `GO`, `GO WITH CHANGES`, or `NO-GO`;
- any required corrections;
- whether M36-A remains closed pending a separate ChatGPT/User gate.

