#!/usr/bin/env python3
"""Regenerate the repository root SHA256SUMS.txt deterministically.

The root checksum file is repository integrity metadata. It must not be
hand-edited because manual updates have drifted repeatedly.

Policy:
- include tracked files plus untracked non-ignored files;
- hash tracked files from Git index bytes, not raw working-tree bytes;
- hash untracked files from raw working-tree bytes;
- exclude the root SHA256SUMS.txt itself to avoid self-referential hashes;
- sort paths by POSIX-style repository-relative path;
- write UTF-8 text with LF newlines.
"""
from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path
from typing import Literal


ROOT_SHA_FILE = "SHA256SUMS.txt"
PathSource = Literal["tracked_index", "untracked_worktree"]


def repo_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        check=True,
        capture_output=True,
        text=True,
    )
    return Path(result.stdout.strip())


def _git_list(root: Path, args: list[str]) -> list[str]:
    result = subprocess.run(
        ["git", *args, "-z"],
        cwd=root,
        check=True,
        capture_output=True,
    )
    return [
        raw_path.decode("utf-8").replace("\\", "/")
        for raw_path in result.stdout.split(b"\0")
        if raw_path
    ]


def repo_file_paths(root: Path) -> dict[str, PathSource]:
    paths: dict[str, PathSource] = {}
    for raw_path in _git_list(root, ["ls-files", "--cached"]):
        rel_path = raw_path.replace("\\", "/")
        if rel_path and rel_path != ROOT_SHA_FILE:
            paths[rel_path] = "tracked_index"
    for raw_path in _git_list(root, ["ls-files", "--others", "--exclude-standard"]):
        rel_path = raw_path.replace("\\", "/")
        if rel_path and rel_path != ROOT_SHA_FILE and (root / rel_path).is_file():
            paths.setdefault(rel_path, "untracked_worktree")
    return dict(sorted(paths.items()))


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


def sha256_worktree_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    try:
        root = repo_root()
        paths = repo_file_paths(root)
        lines: list[str] = []
        for rel_path, source in paths.items():
            if source == "tracked_index":
                digest = sha256_bytes(git_index_bytes(root, rel_path))
            else:
                digest = sha256_worktree_file(root / rel_path)
            lines.append(f"{digest}  {rel_path}")
        (root / ROOT_SHA_FILE).write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
        print(f"UPDATED {ROOT_SHA_FILE}: {len(lines)} entries")
        return 0
    except subprocess.CalledProcessError as exc:
        print(f"ERROR: command failed: {' '.join(exc.cmd)}", file=sys.stderr)
        if exc.stderr:
            print(exc.stderr, file=sys.stderr)
        return exc.returncode or 1


if __name__ == "__main__":
    raise SystemExit(main())
