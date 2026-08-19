from __future__ import annotations

import json
import subprocess
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path

from .contract import Contract, ContractError, HarnessConfig


@dataclass(frozen=True)
class AdapterResult:
    returncode: int
    command: tuple[str, ...]
    output: str


def _expand_workspace_files(workspace: Path, patterns: tuple[str, ...]) -> tuple[Path, ...]:
    root = workspace.resolve()
    matches: set[Path] = set()
    for pattern in patterns:
        for candidate in workspace.glob(pattern):
            if not candidate.is_file():
                continue
            resolved = candidate.resolve()
            try:
                resolved.relative_to(root)
            except ValueError as error:
                raise ContractError(f"Matched file escapes workspace through a symlink: {candidate}") from error
            matches.add(resolved)
    return tuple(sorted(matches))


def check_endpoint(config: HarnessConfig) -> None:
    request = urllib.request.Request(
        f"{config.api_base}/models",
        headers={"Authorization": f"Bearer {config.api_key}"},
    )
    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            if not 200 <= response.status < 300:
                raise ContractError(f"Model endpoint returned HTTP {response.status}")
    except (urllib.error.URLError, TimeoutError) as error:
        raise ContractError(
            f"Model endpoint is unavailable at {config.api_base}. "
            "Start the approved GPU endpoint and SSH tunnel before a live run."
        ) from error


def build_aider_command(
    contract: Contract,
    config: HarnessConfig,
    prompt_path: Path,
    run_dir: Path,
) -> tuple[str, ...]:
    if not config.aider_binary.is_file():
        raise ContractError(f"Aider binary does not exist: {config.aider_binary}")

    editable = _expand_workspace_files(contract.workspace, contract.allowed_paths)
    context = _expand_workspace_files(
        contract.workspace,
        tuple(dict.fromkeys([*contract.read_only_paths, *contract.context_paths])),
    )
    read_only_set = set(context)
    editable = tuple(path for path in editable if path not in read_only_set)

    command: list[str] = [
        str(config.aider_binary),
        "--model",
        config.model,
        "--openai-api-base",
        config.api_base,
        "--openai-api-key",
        config.api_key,
        "--edit-format",
        "ask" if contract.mode == "plan" else config.edit_format,
        "--timeout",
        str(config.request_timeout_seconds),
        "--message-file",
        str(prompt_path),
        "--exit",
        "--no-auto-commits",
        "--no-dirty-commits",
        "--no-gitignore",
        "--no-suggest-shell-commands",
        "--map-tokens",
        "0",
        "--input-history-file",
        str(run_dir / ".aider.input.history"),
        "--chat-history-file",
        str(run_dir / ".aider.chat.history.md"),
        "--llm-history-file",
        str(run_dir / ".aider.llm.history"),
        "--no-show-model-warnings",
        "--no-check-update",
        "--no-analytics",
        "--no-pretty",
    ]

    for rule in contract.rules:
        command.extend(["--read", str(rule)])
    for path in context:
        command.extend(["--read", str(path)])

    if contract.mode == "plan":
        for path in editable:
            command.extend(["--read", str(path)])
    else:
        for path in editable:
            command.extend(["--file", str(path)])

    return tuple(command)


def run_aider(
    contract: Contract,
    config: HarnessConfig,
    prompt_path: Path,
    run_dir: Path,
    *,
    dry_run: bool,
) -> AdapterResult:
    command = build_aider_command(contract, config, prompt_path, run_dir)
    if dry_run:
        return AdapterResult(returncode=0, command=command, output=json.dumps(command, indent=2))

    check_endpoint(config)
    result = subprocess.run(
        command,
        cwd=contract.workspace,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=config.request_timeout_seconds + 30,
        check=False,
    )
    return AdapterResult(returncode=result.returncode, command=command, output=result.stdout)
