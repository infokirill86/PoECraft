# Commands and Results

Observed at repo HEAD `0cc9f14290469ea6ba143a6113506ad90f4d859b`.

| Check | Result |
|---|---|
| `git pull --ff-only` and remote/local HEAD comparison | PASS |
| `git ls-files` inventory | 601 tracked files |
| Tracked working-tree size | approximately 1.92 MB |
| Exact non-empty tracked-file SHA duplicate scan | zero duplicate groups |
| Package lifecycle matrix | 37 tracked package directories; 33 directly accepted-ledger referenced |
| Review inventory | 40 tracked review files |
| `python tools/check_sha256sums.py SHA256SUMS.txt` | PASS |
| `python tools/validate_active_task.py` | PASS |
| Canonical backtick-path scan | historical/stale workflow refs and historical evidence refs found; classified in report |
| Nested-ZIP checker | expected FAIL on three explicit source-bundle ZIPs; checker lacks exception model |
| Repo-wide numeric leak checker | non-actionable FAIL with many code/test/version/data false positives; checker scope defect |

No runtime tests were required to discover the structure defects. The later cleanup delta should run the full suite because it will change validators and canonical routing documents.
