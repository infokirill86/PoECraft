from __future__ import annotations

import hashlib
import importlib.util
import subprocess
import sys
from pathlib import Path
from types import ModuleType

import pytest


REPO_ROOT = Path(__file__).resolve().parents[2]
UPDATE_TOOL = REPO_ROOT / "tools" / "update_sha256sums.py"
CHECK_TOOL = REPO_ROOT / "tools" / "check_sha256sums.py"


def load_tool(path: Path, module_name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def read_sums(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, rel_path = line.split(maxsplit=1)
        result[rel_path.strip()] = digest
    return result


def test_update_and_check_use_git_normalized_bytes_for_tracked_files(
    tmp_path: Path, monkeypatch
) -> None:
    update_tool = load_tool(UPDATE_TOOL, "p2c_test_update_sha256sums")
    check_tool = load_tool(CHECK_TOOL, "p2c_test_check_sha256sums")

    (tmp_path / "tracked.txt").write_bytes(b"alpha\r\nbeta\r\n")
    (tmp_path / "untracked.txt").write_bytes(b"raw\r\nbytes\r\n")

    monkeypatch.setattr(update_tool, "repo_root", lambda: tmp_path)
    monkeypatch.setattr(
        update_tool,
        "repo_file_paths",
        lambda _root: {
            "tracked.txt": "tracked_index",
            "untracked.txt": "untracked_worktree",
        },
    )
    monkeypatch.setattr(
        update_tool,
        "git_index_blobs",
        lambda _root, rel_paths: {
            rel_path: b"alpha\nbeta\n" for rel_path in rel_paths if rel_path == "tracked.txt"
        },
    )

    assert update_tool.main() == 0

    sums = read_sums(tmp_path / "SHA256SUMS.txt")
    assert sums["tracked.txt"] == hashlib.sha256(b"alpha\nbeta\n").hexdigest()
    assert sums["tracked.txt"] != hashlib.sha256(b"alpha\r\nbeta\r\n").hexdigest()
    assert sums["untracked.txt"] == hashlib.sha256(b"raw\r\nbytes\r\n").hexdigest()

    monkeypatch.setattr(check_tool, "git_root", lambda _start: tmp_path)
    monkeypatch.setattr(
        check_tool,
        "git_list",
        lambda _root, args: {"tracked.txt"} if "--cached" in args else {"untracked.txt"},
    )
    monkeypatch.setattr(
        check_tool,
        "git_index_blobs",
        lambda _root, rel_paths: {
            rel_path: b"alpha\nbeta\n" for rel_path in rel_paths if rel_path == "tracked.txt"
        },
    )
    monkeypatch.setattr(sys, "argv", ["check_sha256sums.py", str(tmp_path / "SHA256SUMS.txt")])

    assert check_tool.main() == 0


@pytest.mark.parametrize(
    ("tool_path", "module_name"),
    (
        (UPDATE_TOOL, "p2c_test_update_sha256sums_batch"),
        (CHECK_TOOL, "p2c_test_check_sha256sums_batch"),
    ),
)
def test_git_index_blobs_reads_multiple_index_entries_in_one_batch(
    tmp_path: Path,
    monkeypatch,
    tool_path: Path,
    module_name: str,
) -> None:
    tool = load_tool(tool_path, module_name)
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / "alpha.txt").write_bytes(b"alpha\r\n")
    (tmp_path / "beta.txt").write_bytes(b"beta\r\n")
    subprocess.run(
        ["git", "-C", str(tmp_path), "add", "alpha.txt", "beta.txt"], check=True
    )
    real_run = subprocess.run
    batch_calls = 0

    def recording_run(*args, **kwargs):
        nonlocal batch_calls
        if list(args[0]) == ["git", "cat-file", "--batch"]:
            batch_calls += 1
        return real_run(*args, **kwargs)

    monkeypatch.setattr(tool.subprocess, "run", recording_run)

    blobs = tool.git_index_blobs(tmp_path, ["alpha.txt", "beta.txt"])

    assert blobs == {"alpha.txt": b"alpha\n", "beta.txt": b"beta\n"}
    assert (tmp_path / "alpha.txt").read_bytes() == b"alpha\r\n"
    assert batch_calls == 1
