#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import io
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


def git_index_blobs(root: Path, rel_paths: list[str]) -> dict[str, bytes]:
    """Read all requested index blobs through one git cat-file process."""
    if not rel_paths:
        return {}
    if any("\n" in rel_path or "\r" in rel_path for rel_path in rel_paths):
        raise ValueError("tracked paths containing newlines are unsupported")
    queries = b"".join(f":{rel_path}\n".encode("utf-8") for rel_path in rel_paths)
    result = subprocess.run(
        ["git", "cat-file", "--batch"],
        cwd=root,
        check=True,
        input=queries,
        capture_output=True,
    )
    stream = io.BytesIO(result.stdout)
    blobs: dict[str, bytes] = {}
    for rel_path in rel_paths:
        header = stream.readline().rstrip(b"\n")
        parts = header.rsplit(b" ", 2)
        if len(parts) != 3 or parts[1] != b"blob":
            raise ValueError(f"unexpected git cat-file header for {rel_path}: {header!r}")
        try:
            size = int(parts[2])
        except ValueError as exc:
            raise ValueError(
                f"invalid git cat-file size for {rel_path}: {parts[2]!r}"
            ) from exc
        payload = stream.read(size)
        if len(payload) != size or stream.read(1) != b"\n":
            raise ValueError(f"truncated git cat-file payload for {rel_path}")
        blobs[rel_path] = payload
    if stream.read(1):
        raise ValueError("unexpected trailing git cat-file output")
    return blobs


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
    entries: list[tuple[str, str, PathSource]] = []
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
        entries.append((expected, rel_path, source))

    try:
        tracked_blobs = git_index_blobs(
            root,
            [rel_path for _expected, rel_path, source in entries if source == "tracked_index"],
        )
    except (subprocess.CalledProcessError, ValueError) as exc:
        if isinstance(exc, subprocess.CalledProcessError):
            print(f"ERROR: command failed: {' '.join(exc.cmd)}", file=sys.stderr)
        else:
            print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    for expected, rel_path, source in entries:
        if source == "tracked_index":
            got = sha256_bytes(tracked_blobs[rel_path])
        else:
            got = sha256_worktree(root / rel_path)
        if got != expected:
            print(f"FAIL {rel_path} expected={expected} got={got}")
            ok = False
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
