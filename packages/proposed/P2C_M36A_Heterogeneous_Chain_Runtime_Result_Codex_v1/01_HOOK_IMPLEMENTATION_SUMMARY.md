# Hook Implementation Summary

## Added file

- `tools/hooks/pre-push`

## Setup command

```text
git config core.hooksPath tools/hooks
```

## Hook behavior

The hook runs:

```text
python tools/update_sha256sums.py
python tools/check_sha256sums.py SHA256SUMS.txt
```

If `tools/update_sha256sums.py` changes root `SHA256SUMS.txt`, the hook blocks the push and prints a message telling the actor to stage and commit the regenerated file.

## Boundary

This is local Git hook enforcement only.

It is not GitHub Actions, not watcher automation, and not supervised auto-run.
