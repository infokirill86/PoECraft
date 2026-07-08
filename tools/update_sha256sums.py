#!/usr/bin/env python3
"""Regenerate the repository root SHA256SUMS.txt deterministically.

The root checksum file is repository integrity metadata. It must not be
hand-edited because manual updates have drifted repeatedly.

Policy:
- include tracked files plus untracked non-ignored files;
- exclude the root SHA256SUMS.txt itself to avoid self-referential hashes;
- sort paths by POSIX-style repository-relative path;
- write UTF-8 text with LF newlines.
"""
from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path


ROOT_SHA_FILE = "SHA256SUMS.txt"


def repo_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        check=True,
        capture_output=True,
        text=True,
    )
    return Path(result.stdout.strip())


def repo_file_paths(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    paths: list[str] = []
    for raw_path in result.stdout.splitlines():
        rel_path = raw_path.replace("\\", "/")
        if not rel_path or rel_path == ROOT_SHA_FILE:
            continue
        if (root / rel_path).is_file():
            paths.append(rel_path)
    return sorted(set(paths))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    try:
        root = repo_root()
        paths = repo_file_paths(root)
        lines = [f"{sha256_file(root / rel_path)}  {rel_path}" for rel_path in paths]
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
