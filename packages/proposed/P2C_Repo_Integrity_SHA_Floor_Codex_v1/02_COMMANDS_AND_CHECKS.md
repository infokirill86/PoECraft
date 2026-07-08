# Commands and Checks

## Commands run

```text
python tools/update_sha256sums.py
python tools/check_sha256sums.py SHA256SUMS.txt
python tools/check_sha256sums.py packages/proposed/P2C_Repo_Integrity_SHA_Floor_Codex_v1/SHA256SUMS.txt
python tools/check_no_nested_zips.py packages/proposed/P2C_Repo_Integrity_SHA_Floor_Codex_v1
```

## Results

| Check | Result |
|---|---|
| Root SHA256SUMS regenerated mechanically | PASS |
| Root SHA256SUMS verification | PASS |
| Package SHA256SUMS verification | PASS |
| Nested ZIP check | PASS |

## Notes

This floor intentionally does not run mechanics/runtime tests because no mechanics, runtime semantics, data semantics, or operation behavior changed.

