# Claude audit request

Please audit `P2C_SHA256_Git_Normalized_Update_Fix_Codex_v1`.

## Audit questions

1. Does `tools/update_sha256sums.py` hash tracked files from Git index bytes rather than raw working-tree bytes?
2. Does it still hash untracked non-ignored files from raw working-tree bytes?
3. Does `tools/check_sha256sums.py` verify using the same tracked/untracked policy?
4. Does the focused test cover CRLF working-tree bytes versus LF-normalized tracked bytes?
5. Does the change avoid crafting runtime, mechanics, data-semantics, operation admission, optimizer/advice, public output, automation, and boundary closure?
6. Is `SHA256SUMS.txt` regenerated and verified cleanly?
7. Is `ACTIVE_TASK.md` routed correctly to Claude audit?

## Expected verdict

Return one of:

- `GO`
- `GO WITH CHANGES`
- `NO-GO`

If corrections are needed, list severity, evidence, and exact files.
