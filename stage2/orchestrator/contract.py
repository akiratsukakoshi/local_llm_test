from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any


LAB_ROOT = Path(__file__).resolve().parents[1]
VALID_MODES = {"autonomous", "plan", "delegated"}
TASK_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9._-]{2,79}$")


class ContractError(ValueError):
    """Raised when an experiment contract is unsafe or incomplete."""


@dataclass(frozen=True)
class TestSpec:
    name: str
    command: tuple[str, ...]
    timeout_seconds: int


@dataclass(frozen=True)
class ReviewSpec:
    required: bool
    reviewer: str


@dataclass(frozen=True)
class Contract:
    source_path: Path
    task_id: str
    mode: str
    objective: str
    acceptance_criteria: tuple[str, ...]
    workspace: Path
    fixture: Path | None
    rules: tuple[Path, ...]
    allowed_paths: tuple[str, ...]
    read_only_paths: tuple[str, ...]
    context_paths: tuple[str, ...]
    required_tests: tuple[TestSpec, ...]
    max_attempts: int
    max_changed_files: int
    max_changed_lines: int
    allow_new_files: bool
    review: ReviewSpec


@dataclass(frozen=True)
class HarnessConfig:
    source_path: Path
    adapter: str
    aider_binary: Path
    model: str
    api_base: str
    api_key: str
    edit_format: str
    request_timeout_seconds: int


def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise ContractError(f"File does not exist: {path}") from error
    except json.JSONDecodeError as error:
        raise ContractError(f"Invalid JSON in {path}: {error}") from error
    if not isinstance(value, dict):
        raise ContractError(f"Top-level JSON value must be an object: {path}")
    return value


def _string(data: dict[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ContractError(f"{key} must be a non-empty string")
    return value.strip()


def _string_list(data: dict[str, Any], key: str, *, required: bool = False) -> tuple[str, ...]:
    value = data.get(key, [])
    if not isinstance(value, list) or any(not isinstance(item, str) or not item.strip() for item in value):
        raise ContractError(f"{key} must be a list of non-empty strings")
    result = tuple(item.strip() for item in value)
    if required and not result:
        raise ContractError(f"{key} must not be empty")
    return result


def _bounded_int(data: dict[str, Any], key: str, default: int, minimum: int, maximum: int) -> int:
    value = data.get(key, default)
    if not isinstance(value, int) or isinstance(value, bool) or not minimum <= value <= maximum:
        raise ContractError(f"{key} must be an integer from {minimum} through {maximum}")
    return value


def _safe_relative(value: str, key: str) -> PurePosixPath:
    if "\\" in value:
        raise ContractError(f"{key} must use forward slashes: {value}")
    path = PurePosixPath(value)
    if path.is_absolute() or not path.parts or any(part in {"", ".", ".."} for part in path.parts):
        raise ContractError(f"{key} must be a safe relative path: {value}")
    return path


def _resolve_inside(root: Path, value: str, key: str) -> Path:
    relative = _safe_relative(value, key)
    resolved = (root / Path(*relative.parts)).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError as error:
        raise ContractError(f"{key} escapes the Stage 2 directory: {value}") from error
    return resolved


def _validate_patterns(values: tuple[str, ...], key: str) -> tuple[str, ...]:
    for value in values:
        _safe_relative(value, key)
    return values


def load_contract(path: str | Path, lab_root: Path = LAB_ROOT) -> Contract:
    source_path = Path(path).resolve()
    data = _load_json(source_path)

    task_id = _string(data, "id")
    if not TASK_ID_PATTERN.fullmatch(task_id):
        raise ContractError("id must contain only lowercase letters, digits, dots, underscores, or hyphens")

    mode = _string(data, "mode")
    if mode not in VALID_MODES:
        raise ContractError(f"mode must be one of: {', '.join(sorted(VALID_MODES))}")

    workspace = _resolve_inside(lab_root, _string(data, "workspace"), "workspace")
    workspace_root = (lab_root / "workspaces").resolve()
    try:
        workspace.relative_to(workspace_root)
    except ValueError as error:
        raise ContractError("workspace must be below stage2/workspaces") from error

    fixture_value = data.get("fixture")
    fixture = None
    if fixture_value is not None:
        if not isinstance(fixture_value, str) or not fixture_value.strip():
            raise ContractError("fixture must be a non-empty string or null")
        fixture = _resolve_inside(lab_root, fixture_value.strip(), "fixture")
        fixture_root = (lab_root / "fixtures").resolve()
        try:
            fixture.relative_to(fixture_root)
        except ValueError as error:
            raise ContractError("fixture must be below stage2/fixtures") from error

    rule_values = _string_list(data, "rules", required=True)
    rules = tuple(_resolve_inside(lab_root, value, "rules") for value in rule_values)
    rule_root = (lab_root / "rules").resolve()
    for rule in rules:
        try:
            rule.relative_to(rule_root)
        except ValueError as error:
            raise ContractError("all rules must be below stage2/rules") from error

    allowed_paths = _validate_patterns(_string_list(data, "allowed_paths"), "allowed_paths")
    read_only_paths = _validate_patterns(_string_list(data, "read_only_paths"), "read_only_paths")
    context_paths = _validate_patterns(_string_list(data, "context_paths"), "context_paths")
    if mode != "plan" and not allowed_paths:
        raise ContractError("allowed_paths must not be empty for implementation modes")

    raw_tests = data.get("required_tests", [])
    if not isinstance(raw_tests, list):
        raise ContractError("required_tests must be a list")
    tests: list[TestSpec] = []
    for index, raw_test in enumerate(raw_tests):
        if not isinstance(raw_test, dict):
            raise ContractError(f"required_tests[{index}] must be an object")
        name = _string(raw_test, "name")
        command = raw_test.get("command")
        if not isinstance(command, list) or not command or any(
            not isinstance(part, str) or not part for part in command
        ):
            raise ContractError(f"required_tests[{index}].command must be a non-empty string list")
        timeout = _bounded_int(raw_test, "timeout_seconds", 120, 1, 3600)
        tests.append(TestSpec(name=name, command=tuple(command), timeout_seconds=timeout))

    if mode != "plan" and not tests:
        raise ContractError("required_tests must not be empty for implementation modes")

    raw_review = data.get("review", {})
    if not isinstance(raw_review, dict):
        raise ContractError("review must be an object")
    required = raw_review.get("required", True)
    if not isinstance(required, bool):
        raise ContractError("review.required must be a boolean")
    reviewer = raw_review.get("reviewer", "human")
    if not isinstance(reviewer, str) or not reviewer.strip():
        raise ContractError("review.reviewer must be a non-empty string")

    allow_new_files = data.get("allow_new_files", False)
    if not isinstance(allow_new_files, bool):
        raise ContractError("allow_new_files must be a boolean")

    return Contract(
        source_path=source_path,
        task_id=task_id,
        mode=mode,
        objective=_string(data, "objective"),
        acceptance_criteria=_string_list(data, "acceptance_criteria", required=True),
        workspace=workspace,
        fixture=fixture,
        rules=rules,
        allowed_paths=allowed_paths,
        read_only_paths=read_only_paths,
        context_paths=context_paths,
        required_tests=tuple(tests),
        max_attempts=_bounded_int(data, "max_attempts", 3, 1, 10),
        max_changed_files=_bounded_int(data, "max_changed_files", 5, 1, 100),
        max_changed_lines=_bounded_int(data, "max_changed_lines", 300, 1, 10000),
        allow_new_files=allow_new_files,
        review=ReviewSpec(required=required, reviewer=reviewer.strip()),
    )


def load_harness_config(path: str | Path, lab_root: Path = LAB_ROOT) -> HarnessConfig:
    source_path = Path(path).resolve()
    data = _load_json(source_path)
    adapter = _string(data, "adapter")
    if adapter != "aider":
        raise ContractError("The current implementation supports only the aider adapter")

    binary_value = _string(data, "aider_binary")
    binary_path = Path(binary_value)
    if not binary_path.is_absolute():
        binary_path = (lab_root / binary_path).resolve()

    api_base = _string(data, "api_base").rstrip("/")
    if not api_base.startswith(("http://", "https://")):
        raise ContractError("api_base must be an HTTP or HTTPS URL")

    return HarnessConfig(
        source_path=source_path,
        adapter=adapter,
        aider_binary=binary_path,
        model=_string(data, "model"),
        api_base=api_base,
        api_key=_string(data, "api_key"),
        edit_format=_string(data, "edit_format"),
        request_timeout_seconds=_bounded_int(data, "request_timeout_seconds", 900, 10, 3600),
    )
