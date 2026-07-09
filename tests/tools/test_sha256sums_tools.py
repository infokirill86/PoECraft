from __future__ import annotations

import hashlib
import importlib.util
import sys
from pathlib import Path
from types import ModuleType


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
        "git_index_bytes",
        lambda _root, rel_path: b"alpha\nbeta\n" if rel_path == "tracked.txt" else b"",
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
        "git_index_bytes",
        lambda _root, rel_path: b"alpha\nbeta\n" if rel_path == "tracked.txt" else b"",
    )
    monkeypatch.setattr(sys, "argv", ["check_sha256sums.py", str(tmp_path / "SHA256SUMS.txt")])

    assert check_tool.main() == 0
