# Commands and results

## Repo/head checks

```text
git status --short --branch
## codex/m38a-resolver-skeleton

git rev-parse HEAD
963a61f110a56ee72477a1266d0f6c35ca177a96

git rev-parse origin/main
963a61f110a56ee72477a1266d0f6c35ca177a96
```

## Active task read receipt

```text
SHA-256(work/active/ACTIVE_TASK.md)
65abec924e219d1ab220443594287f886d3b3ede36db015293f69af8c97dcb42
```

## Local data inspected

- `data/operations.yaml`
- `data/omens.yaml`
- `data/mechanics_evidence.yaml`
- `data/sources.yaml`
- `CURRENT_STATUS.md`
- `ledger/ACCEPTED_ARTIFACTS.md`
- `ledger/DECISIONS.md`
- `src/p2c_engine/legality/pool_builders.py`

## External sources checked

- PoE2DB Currency page
- Path of Exile 0.5.0 official patch notes
- Craft of Exile PoE2 landing page / registered project source

## Repo integrity checks

```text
git config core.hooksPath tools/hooks
error: could not lock config file C:/Users/infok/Documents/GitHub/PoECraft/.git/config: Permission denied

git config --get core.hooksPath
tools/hooks
```

Interpretation: the local worktree already reports `tools/hooks` as the active hook path. The attempted write failed because this is a linked worktree using the common Git config outside the current writable root.

```text
python tools/update_sha256sums.py
UPDATED SHA256SUMS.txt: 447 entries

python tools/check_sha256sums.py SHA256SUMS.txt
PASS
```

## Runtime tests

Runtime tests were not run before package assembly because this is documentation/design verification only and no runtime code or data semantics were changed.

Repo integrity checks were run after package creation and ACTIVE_TASK update.
