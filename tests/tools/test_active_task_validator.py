from __future__ import annotations

import importlib.util
import subprocess
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "tools/validate_active_task.py"
SPEC = importlib.util.spec_from_file_location("p2c_validate_active_task", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


@dataclass(frozen=True)
class _Result:
    returncode: int
    stderr: str


def _run(root: Path, path: Path) -> _Result:
    try:
        VALIDATOR.validate_active_task(path, root)
    except (OSError, UnicodeError, VALIDATOR.ActiveTaskValidationError) as exc:
        return _Result(1, str(exc))
    return _Result(0, "")


def _task_path(root: Path) -> Path:
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    active = root / "work/active"
    active.mkdir(parents=True, exist_ok=True)
    task = active / "ACTIVE_TASK.md"
    task.write_text("placeholder\n", encoding="utf-8")
    subprocess.run(
        ["git", "-C", str(root), "add", "work/active/ACTIVE_TASK.md"], check=True
    )
    return task


def _valid_task(root: Path) -> str:
    (root / "manifest").mkdir(parents=True, exist_ok=True)
    (root / "manifest/GitHub_Workflow_Protocol.md").write_text("# boundaries\n")
    (root / "result").mkdir(exist_ok=True)
    return """---
schema_version: "2.0"
repo_head_at_last_update: "0123456789abcdef0123456789abcdef01234567"
updated_at_utc: "2026-07-10T18:00:00Z"
status: "ready_for_claude"
next_actor: "claude"
active_task_id: "TEST_TASK"
allowed_next_action: "claude_audit_test"
forbidden_next_actions:
  - "scope_expansion"
standing_boundaries_ref: "manifest/GitHub_Workflow_Protocol.md#boundaries"
standing_boundaries_apply: true
current_result_path: "result"
current_review_path: ""
acceptance_authority: "chatgpt_user"
automation: {}
freshness_rules: {}
stop_conditions:
  - "Stop on invalid state."
---

# Active task

Next actor: Claude.
"""


def test_live_active_task_passes() -> None:
    result = _run(ROOT, ROOT / "work/active/ACTIVE_TASK.md")
    assert result.returncode == 0, result.stderr


def test_valid_minimal_dispatcher_passes(tmp_path: Path) -> None:
    task = _task_path(tmp_path)
    task.write_text(_valid_task(tmp_path), encoding="utf-8")
    result = _run(tmp_path, task)
    assert result.returncode == 0, result.stderr


def test_missing_or_invalid_frontmatter_fails(tmp_path: Path) -> None:
    task = _task_path(tmp_path)
    task.write_text("# no frontmatter\n", encoding="utf-8")
    result = _run(tmp_path, task)
    assert result.returncode == 1
    assert "must begin" in result.stderr


def test_missing_mandatory_field_fails(tmp_path: Path) -> None:
    task = _task_path(tmp_path)
    task.write_text(_valid_task(tmp_path).replace('active_task_id: "TEST_TASK"\n', ""))
    result = _run(tmp_path, task)
    assert result.returncode == 1
    assert "missing mandatory" in result.stderr


def test_duplicate_yaml_live_state_fails(tmp_path: Path) -> None:
    task = _task_path(tmp_path)
    task.write_text(
        _valid_task(tmp_path).replace(
            'status: "ready_for_claude"',
            'status: "ready_for_claude"\nstatus: "awaiting_user_gate"',
        )
    )
    result = _run(tmp_path, task)
    assert result.returncode == 1
    assert "duplicate YAML key" in result.stderr


def test_inconsistent_status_actor_fails(tmp_path: Path) -> None:
    task = _task_path(tmp_path)
    task.write_text(_valid_task(tmp_path).replace('next_actor: "claude"', 'next_actor: "codex"'))
    result = _run(tmp_path, task)
    assert result.returncode == 1
    assert "inconsistent status/next_actor" in result.stderr


def test_missing_referenced_result_or_review_path_fails(tmp_path: Path) -> None:
    task = _task_path(tmp_path)
    task.write_text(_valid_task(tmp_path).replace('current_result_path: "result"', 'current_result_path: "missing"'))
    result = _run(tmp_path, task)
    assert result.returncode == 1
    assert "references missing path" in result.stderr

    task.write_text(
        _valid_task(tmp_path).replace(
            'current_review_path: ""', 'current_review_path: "reviews/missing.md"'
        )
    )
    result = _run(tmp_path, task)
    assert result.returncode == 1
    assert "references missing path" in result.stderr


def test_duplicated_live_state_below_frontmatter_fails(tmp_path: Path) -> None:
    task = _task_path(tmp_path)
    task.write_text(_valid_task(tmp_path) + '\nstatus: "ready_for_claude"\n')
    result = _run(tmp_path, task)
    assert result.returncode == 1
    assert "duplicated live state outside frontmatter" in result.stderr


def test_extra_tracked_active_file_fails(tmp_path: Path) -> None:
    task = _task_path(tmp_path)
    task.write_text(_valid_task(tmp_path), encoding="utf-8")
    legacy = tmp_path / "work/active/LEGACY_TASK.md"
    legacy.write_text("historical task\n", encoding="utf-8")
    subprocess.run(
        ["git", "-C", str(tmp_path), "add", "work/active/LEGACY_TASK.md"], check=True
    )
    result = _run(tmp_path, task)
    assert result.returncode == 1
    assert "exactly one tracked file" in result.stderr


def test_untracked_active_sibling_does_not_create_second_dispatcher(tmp_path: Path) -> None:
    task = _task_path(tmp_path)
    task.write_text(_valid_task(tmp_path), encoding="utf-8")
    (tmp_path / "work/active/LOCAL_NOTE.md").write_text("untracked local note\n")
    result = _run(tmp_path, task)
    assert result.returncode == 0, result.stderr
