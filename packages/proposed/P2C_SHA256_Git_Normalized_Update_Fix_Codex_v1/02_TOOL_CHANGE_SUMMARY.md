# Tool change summary

## `tools/update_sha256sums.py`

Changed policy:

- tracked files: hash `git cat-file blob :path` bytes;
- untracked non-ignored files: hash raw working-tree bytes;
- root `SHA256SUMS.txt` remains excluded from its own manifest;
- output remains deterministic sorted LF UTF-8 text.

## `tools/check_sha256sums.py`

The checker now mirrors updater policy:

- tracked manifest entries are verified against Git index bytes;
- untracked entries are verified against raw working-tree bytes;
- missing entries still fail.

This checker update is required because otherwise the updater could produce correct git-normalized hashes while the checker still falsely compared against CRLF working-tree bytes.

## Focused test

Added:

- `tests/tools/test_sha256sums_tools.py`

The test proves:

- tracked CRLF working-tree content is hashed as normalized LF index bytes;
- untracked CRLF content is hashed as raw CRLF bytes;
- the checker validates the generated manifest using the same policy.
