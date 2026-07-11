# Implementation Report

Changed:

- `tools/update_sha256sums.py`
- `tools/check_sha256sums.py`
- `tests/tools/test_sha256sums_tools.py`

Both tools now:

1. collect all tracked paths required for the operation;
2. send their index expressions to one `git cat-file --batch` invocation;
3. parse each binary blob by the size declared in the batch header;
4. hash the returned exact index bytes;
5. continue reading untracked files directly from the working tree.

The parser fails closed on unexpected object types, malformed sizes, truncated payloads, trailing output, Git failure, or newline-bearing paths unsupported by the line protocol.

The checker still validates every manifest row. No changed-file shortcut, cache, persistent daemon, watcher, GitHub Action, or automation was added.
