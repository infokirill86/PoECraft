#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path
from typing import Literal


PathSource = Literal["tracked_index", "untracked_worktree"]


def git_root(start: Path) -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=start,
        check=True,
        capture_output=True,
        text=True,
    )
    return Path(result.stdout.strip())


def git_list(root: Path, args: list[str]) -> set[str]:
    result = subprocess.run(
        ["git", *args, "-z"],
        cwd=root,
        check=True,
        capture_output=True,
    )
    return {
        raw_path.decode("utf-8").replace("\\", "/")
        for raw_path in result.stdout.split(b"\0")
        if raw_path
    }


def path_source(root: Path, rel_path: str, tracked: set[str], untracked: set[str]) -> PathSource | None:
    if rel_path in tracked:
        return "tracked_index"
    if rel_path in untracked and (root / rel_path).is_file():
        return "untracked_worktree"
    return None


def git_index_bytes(root: Path, rel_path: str) -> bytes:
    result = subprocess.run(
        ["git", "cat-file", "blob", f":{rel_path}"],
        cwd=root,
        check=True,
        capture_output=True,
    )
    return result.stdout


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_worktree(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    file = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("SHA256SUMS.txt")
    if not file.exists():
        print(f"MISSING {file}")
        return 2
    try:
        root = git_root(file.parent)
        tracked = git_list(root, ["ls-files", "--cached"])
        untracked = git_list(root, ["ls-files", "--others", "--exclude-standard"])
    except subprocess.CalledProcessError as exc:
        print(f"ERROR: command failed: {' '.join(exc.cmd)}", file=sys.stderr)
        return exc.returncode or 1

    ok = True
    for line in file.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) < 2:
            continue
        expected, rel_path = parts[0], parts[-1].lstrip("*")
        source = path_source(root, rel_path, tracked, untracked)
        if source is None:
            print(f"MISSING {rel_path}")
            ok = False
            continue
        if source == "tracked_index":
            got = sha256_bytes(git_index_bytes(root, rel_path))
        else:
            got = sha256_worktree(root / rel_path)
        if got != expected:
            print(f"FAIL {rel_path} expected={expected} got={got}")
            ok = False
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
