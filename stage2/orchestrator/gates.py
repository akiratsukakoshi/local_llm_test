from __future__ import annotations

import fnmatch
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path

from .contract import Contract, ContractError


@dataclass(frozen=True)
class GateReport:
    passed: bool
    changed_files: tuple[str, ...]
    changed_file_count: int
    changed_lines: int
    violations: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _git(workspace: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["git", *args],
        cwd=workspace,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if check and result.returncode != 0:
        raise ContractError(f"git {' '.join(args)} failed:\n{result.stdout.strip()}")
    return result


def ensure_clean_repository(workspace: Path) -> None:
    if not workspace.is_dir():
        raise ContractError(f"Workspace does not exist: {workspace}. Run the prepare command first.")
    root = Path(_git(workspace, "rev-parse", "--show-toplevel").stdout.strip()).resolve()
    if root != workspace.resolve():
        raise ContractError(f"Workspace must be its own Git repository: expected {workspace}, found {root}")
    status = _git(workspace, "status", "--porcelain").stdout
    if status.strip():
        raise ContractError(
            "Workspace has existing changes. Preserve or discard them manually before starting a new run:\n"
            + status.rstrip()
        )


def _matches(path: str, patterns: tuple[str, ...]) -> bool:
    return any(fnmatch.fnmatchcase(path, pattern) for pattern in patterns)


def changed_files(workspace: Path) -> tuple[str, ...]:
    tracked = _git(workspace, "diff", "--name-only", "-z", "HEAD").stdout.split("\0")
    untracked = _git(workspace, "ls-files", "--others", "--exclude-standard", "-z").stdout.split("\0")
    return tuple(sorted({path for path in [*tracked, *untracked] if path}))


def _changed_line_count(workspace: Path, paths: tuple[str, ...]) -> int:
    total = 0
    tracked_stats = _git(workspace, "diff", "--numstat", "HEAD").stdout.splitlines()
    tracked_names: set[str] = set()
    for line in tracked_stats:
        additions, deletions, name = line.split("\t", 2)
        tracked_names.add(name)
        if additions != "-":
            total += int(additions)
        if deletions != "-":
            total += int(deletions)
    for name in paths:
        if name in tracked_names:
            continue
        file_path = workspace / name
        if file_path.is_file():
            try:
                total += len(file_path.read_text(encoding="utf-8").splitlines())
            except UnicodeDecodeError:
                total += 1
    return total


def inspect_changes(contract: Contract) -> GateReport:
    paths = changed_files(contract.workspace)
    violations: list[str] = []

    for path in paths:
        if _matches(path, contract.read_only_paths):
            violations.append(f"read-only path changed: {path}")
        elif not _matches(path, contract.allowed_paths):
            violations.append(f"path outside allowed_paths changed: {path}")

        if not contract.allow_new_files and not (contract.workspace / path).exists():
            # A deleted tracked file is handled as an allowed-path change, not as a new file.
            continue
        if not contract.allow_new_files:
            tracked = _git(contract.workspace, "ls-files", "--error-unmatch", "--", path, check=False)
            if tracked.returncode != 0:
                violations.append(f"new file is not allowed: {path}")

    line_count = _changed_line_count(contract.workspace, paths)
    if len(paths) > contract.max_changed_files:
        violations.append(
            f"changed file count {len(paths)} exceeds limit {contract.max_changed_files}"
        )
    if line_count > contract.max_changed_lines:
        violations.append(f"changed line count {line_count} exceeds limit {contract.max_changed_lines}")

    diff_check = _git(contract.workspace, "diff", "--check", "HEAD", check=False)
    if diff_check.returncode != 0:
        violations.append("git diff --check failed: " + diff_check.stdout.strip())

    return GateReport(
        passed=not violations,
        changed_files=paths,
        changed_file_count=len(paths),
        changed_lines=line_count,
        violations=tuple(violations),
    )


def current_diff(workspace: Path) -> str:
    return _git(workspace, "diff", "--binary", "HEAD").stdout
