#!/usr/bin/env python3
"""Fail-closed validator for the schema-v2 ACTIVE_TASK thin dispatcher."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath
from typing import Any

import yaml


MANDATORY_FIELDS = frozenset(
    {
        "schema_version",
        "repo_head_at_last_update",
        "updated_at_utc",
        "status",
        "next_actor",
        "active_task_id",
        "allowed_next_action",
        "forbidden_next_actions",
        "standing_boundaries_ref",
        "standing_boundaries_apply",
        "current_result_path",
        "current_review_path",
        "acceptance_authority",
        "automation",
        "freshness_rules",
        "stop_conditions",
    }
)
ALLOWED_STATUS_ACTORS = {
    "awaiting_user_gate": frozenset({"chatgpt_user"}),
    "ready_for_codex": frozenset({"codex"}),
    "ready_for_claude": frozenset({"claude"}),
    "audited_pending_user_gate": frozenset({"chatgpt_user"}),
    "blocked_for_human": frozenset({"chatgpt_user", "blocked"}),
    "accepted_closed": frozenset({"chatgpt_user", "blocked"}),
}
LIVE_STATE_KEYS = frozenset(
    {"schema_version", "status", "next_actor", "active_task_id", "allowed_next_action"}
)
CANONICAL_ACTIVE_TASK = PurePosixPath("work/active/ACTIVE_TASK.md")


class ActiveTaskValidationError(ValueError):
    pass


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys at every depth."""


def _construct_unique_mapping(
    loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False
) -> dict[Any, Any]:
    output: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in output:
            raise ActiveTaskValidationError(f"duplicate YAML key: {key!r}")
        output[key] = loader.construct_object(value_node, deep=deep)
    return output


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_unique_mapping
)


def _frontmatter(text: str) -> tuple[dict[str, Any], str]:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise ActiveTaskValidationError(
            "ACTIVE_TASK must begin with one YAML frontmatter block and no preceding prose"
        )
    try:
        closing = lines.index("---", 1)
    except ValueError as exc:
        raise ActiveTaskValidationError("YAML frontmatter closing delimiter is missing") from exc
    if any(line == "---" for line in lines[closing + 1 :]):
        raise ActiveTaskValidationError("multiple frontmatter/live-state blocks are forbidden")
    yaml_text = "\n".join(lines[1:closing])
    try:
        parsed = yaml.load(yaml_text, Loader=UniqueKeyLoader)
    except (yaml.YAMLError, ActiveTaskValidationError) as exc:
        raise ActiveTaskValidationError(f"invalid YAML frontmatter: {exc}") from exc
    if not isinstance(parsed, dict):
        raise ActiveTaskValidationError("YAML frontmatter must be a mapping")
    body = "\n".join(lines[closing + 1 :])
    for line in body.splitlines():
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):(?:\s|$)", line)
        if match and match.group(1) in LIVE_STATE_KEYS:
            raise ActiveTaskValidationError(
                f"duplicated live state outside frontmatter: {match.group(1)}"
            )
    return parsed, body


def _require_string(data: dict[str, Any], field: str) -> str:
    value = data[field]
    if not isinstance(value, str):
        raise ActiveTaskValidationError(f"{field} must be a string")
    return value


def _validate_reference(repo_root: Path, field: str, raw_value: str) -> None:
    if not raw_value:
        return
    path_value = raw_value.split("#", 1)[0]
    pure = PurePosixPath(path_value)
    if pure.is_absolute() or ".." in pure.parts or "\\" in path_value:
        raise ActiveTaskValidationError(f"{field} must be a safe repo-relative path")
    root = repo_root.resolve()
    candidate = (root / Path(*pure.parts)).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise ActiveTaskValidationError(f"{field} escapes the repository") from exc
    if not candidate.exists():
        raise ActiveTaskValidationError(f"{field} references missing path: {path_value}")


def _validate_single_tracked_dispatcher(path: Path, repo_root: Path) -> None:
    root = repo_root.resolve()
    try:
        relative = path.resolve().relative_to(root)
    except ValueError as exc:
        raise ActiveTaskValidationError("ACTIVE_TASK must be inside the repository") from exc
    relative_posix = PurePosixPath(relative.as_posix())
    if relative_posix != CANONICAL_ACTIVE_TASK:
        raise ActiveTaskValidationError(
            f"live dispatcher must be {CANONICAL_ACTIVE_TASK}, got {relative_posix}"
        )

    result = subprocess.run(
        ["git", "-C", str(root), "ls-files", "--", "work/active"],
        capture_output=True,
        text=True,
        stdin=subprocess.DEVNULL,
        check=False,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or "git ls-files failed"
        raise ActiveTaskValidationError(
            f"cannot verify tracked work/active files: {detail}"
        )
    tracked = tuple(
        sorted(
            line.strip().replace("\\", "/")
            for line in result.stdout.splitlines()
            if line.strip()
        )
    )
    expected = (CANONICAL_ACTIVE_TASK.as_posix(),)
    if tracked != expected:
        raise ActiveTaskValidationError(
            "work/active must contain exactly one tracked file, "
            f"{CANONICAL_ACTIVE_TASK}; found {list(tracked)}"
        )


def validate_active_task(path: Path, repo_root: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ActiveTaskValidationError(f"ACTIVE_TASK file is missing: {path}")
    _validate_single_tracked_dispatcher(path, repo_root)
    data, _body = _frontmatter(path.read_text(encoding="utf-8"))

    missing = MANDATORY_FIELDS - set(data)
    extra = set(data) - MANDATORY_FIELDS
    if missing:
        raise ActiveTaskValidationError(f"missing mandatory schema-v2 fields: {sorted(missing)}")
    if extra:
        raise ActiveTaskValidationError(f"unexpected root fields in thin dispatcher: {sorted(extra)}")
    if str(data["schema_version"]) != "2.0":
        raise ActiveTaskValidationError("schema_version must be 2.0")

    head = _require_string(data, "repo_head_at_last_update")
    if not re.fullmatch(r"[0-9a-f]{40}", head):
        raise ActiveTaskValidationError("repo_head_at_last_update must be a full lowercase Git SHA")
    updated = _require_string(data, "updated_at_utc")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", updated):
        raise ActiveTaskValidationError("updated_at_utc must use YYYY-MM-DDTHH:MM:SSZ")

    status = _require_string(data, "status")
    actor = _require_string(data, "next_actor")
    if status not in ALLOWED_STATUS_ACTORS:
        raise ActiveTaskValidationError(f"unsupported status: {status!r}")
    if actor not in ALLOWED_STATUS_ACTORS[status]:
        raise ActiveTaskValidationError(
            f"inconsistent status/next_actor: {status!r} -> {actor!r}"
        )
    for field in ("active_task_id", "allowed_next_action", "acceptance_authority"):
        if not _require_string(data, field).strip():
            raise ActiveTaskValidationError(f"{field} must not be empty")
    if data["acceptance_authority"] != "chatgpt_user":
        raise ActiveTaskValidationError("acceptance_authority must remain chatgpt_user")

    forbidden = data["forbidden_next_actions"]
    stops = data["stop_conditions"]
    if not isinstance(forbidden, list) or not forbidden or not all(
        isinstance(value, str) and value for value in forbidden
    ):
        raise ActiveTaskValidationError("forbidden_next_actions must be a non-empty string list")
    if not isinstance(stops, list) or not stops or not all(
        isinstance(value, str) and value for value in stops
    ):
        raise ActiveTaskValidationError("stop_conditions must be a non-empty string list")
    if not isinstance(data["automation"], dict):
        raise ActiveTaskValidationError("automation must be a mapping")
    if not isinstance(data["freshness_rules"], dict):
        raise ActiveTaskValidationError("freshness_rules must be a mapping")
    if data["standing_boundaries_apply"] is not True:
        raise ActiveTaskValidationError("standing_boundaries_apply must be true")

    standing = _require_string(data, "standing_boundaries_ref")
    result_path = _require_string(data, "current_result_path")
    review_path = _require_string(data, "current_review_path")
    _validate_reference(repo_root, "standing_boundaries_ref", standing)
    _validate_reference(repo_root, "current_result_path", result_path)
    _validate_reference(repo_root, "current_review_path", review_path)
    if status == "ready_for_claude" and not result_path:
        raise ActiveTaskValidationError("ready_for_claude requires an existing current_result_path")
    if status == "audited_pending_user_gate" and not review_path:
        raise ActiveTaskValidationError(
            "audited_pending_user_gate requires an existing current_review_path"
        )
    return data


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default="work/active/ACTIVE_TASK.md")
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args(argv)
    repo_root = Path(args.repo_root).resolve()
    path = Path(args.path)
    if not path.is_absolute():
        path = repo_root / path
    try:
        data = validate_active_task(path, repo_root)
    except (OSError, UnicodeError, ActiveTaskValidationError) as exc:
        print(f"ACTIVE_TASK_SCHEMA_V2: FAIL: {exc}", file=sys.stderr)
        return 1
    print(
        "ACTIVE_TASK_SCHEMA_V2: PASS: "
        f"status={data['status']} next_actor={data['next_actor']} "
        f"active_task_id={data['active_task_id']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
