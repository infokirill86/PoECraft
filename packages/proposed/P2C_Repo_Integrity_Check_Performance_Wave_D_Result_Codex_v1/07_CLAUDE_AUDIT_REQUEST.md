# Claude Audit Request

Please reconstruct and audit Wave D from repository bytes.

Verify:

1. Wave A+B acceptance is recorded without changing its audited scope.
2. Each checksum tool uses one `git cat-file --batch` stream for all tracked index blobs, not one Git process per file.
3. Full verification remains; no changed-file shortcut or cache was introduced.
4. Tracked files still use Git index/normalized bytes and untracked files still use working-tree bytes.
5. Regenerating `SHA256SUMS.txt` from the pre-Wave-D committed tree is byte-identical.
6. Before/after timings are reproducible enough to demonstrate the process-launch speedup.
7. Focused/full tests, semantic fingerprint, ACTIVE_TASK validation, checksums, and pre-push guard pass.
8. No runtime/mechanics/data/admission, evidence movement/rewrite, optimizer/public output, automation, M43, or boundary change entered the delta.
9. Wave D remains proposed and requires a later ChatGPT/User acceptance gate.

Return `GO`, `GO WITH CHANGES`, or `NO-GO`, with a short plain-language summary for Kirill.
