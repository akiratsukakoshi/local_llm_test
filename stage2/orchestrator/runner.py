from __future__ import annotations

import json
import shutil
import subprocess
import time
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from .adapter import run_aider
from .contract import LAB_ROOT, Contract, ContractError, HarnessConfig
from .gates import current_diff, ensure_clean_repository, inspect_changes


def _write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _finish_result(run_dir: Path, result: dict[str, object], started_monotonic: float) -> None:
    result["finished_at"] = datetime.now(timezone.utc).isoformat()
    result["wall_time_seconds"] = round(time.monotonic() - started_monotonic, 3)
    _write_json(run_dir / "result.json", result)


def _run_command(command: tuple[str, ...], cwd: Path, timeout: int) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            command,
            cwd=cwd,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        output = error.stdout or ""
        if isinstance(output, bytes):
            output = output.decode("utf-8", errors="replace")
        return subprocess.CompletedProcess(command, 124, output + f"\nTimed out after {timeout} seconds.\n")


def prepare_workspace(contract: Contract) -> Path:
    if contract.fixture is None:
        raise ContractError("This contract has no fixture; create its workspace manually as a clean Git repository")
    if not contract.fixture.is_dir():
        raise ContractError(f"Fixture directory does not exist: {contract.fixture}")
    if contract.workspace.exists():
        raise ContractError(
            f"Workspace already exists: {contract.workspace}. It was not overwritten. "
            "Use a new task id/workspace or preserve and remove it manually."
        )

    contract.workspace.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(contract.fixture, contract.workspace)
    commands = [
        ("git", "init", "--quiet"),
        ("git", "config", "user.name", "Local LLM Lab"),
        ("git", "config", "user.email", "local-llm-lab@example.invalid"),
        ("git", "add", "."),
        ("git", "commit", "--quiet", "-m", "Initial Stage 2 fixture"),
    ]
    try:
        for command in commands:
            result = _run_command(command, contract.workspace, 30)
            if result.returncode != 0:
                raise ContractError(f"{' '.join(command)} failed:\n{result.stdout}")
    except Exception:
        # Preserve the partially prepared directory for diagnosis; never erase user data automatically.
        raise
    return contract.workspace


def render_prompt(contract: Contract, attempt: int, previous_failure: str | None) -> str:
    lines = [
        f"# Task {contract.task_id}",
        "",
        f"Mode: {contract.mode}",
        f"Attempt: {attempt} of {contract.max_attempts}",
        "",
        "## Objective",
        "",
        contract.objective,
        "",
        "## Acceptance criteria",
        "",
    ]
    lines.extend(f"- {criterion}" for criterion in contract.acceptance_criteria)
    lines.extend(
        [
            "",
            "## Enforced scope",
            "",
            "Editable path patterns:",
            *(f"- `{pattern}`" for pattern in contract.allowed_paths),
            "",
            "Read-only path patterns:",
            *(f"- `{pattern}`" for pattern in contract.read_only_paths),
            "",
        ]
    )
    if contract.mode == "plan":
        lines.extend(
            [
                "Do not edit files. Return a concrete implementation plan, risks, files likely to change, and validation steps.",
                "The outer harness will reject any filesystem change.",
            ]
        )
    elif contract.mode == "delegated":
        lines.extend(
            [
                "Treat this task packet as the authoritative upstream specification.",
                "Implement it without expanding scope. Report any ambiguity instead of inventing requirements.",
                "Do not claim completion; the upstream reviewer makes the final decision.",
            ]
        )
    else:
        lines.extend(
            [
                "Inspect the supplied files, implement the smallest correct change, and leave verification to the outer harness.",
                "Do not run shell commands; the outer harness runs only the tests declared in the task contract.",
            ]
        )

    if previous_failure:
        lines.extend(
            [
                "",
                "## Previous verification failure",
                "",
                "The outer harness ran the approved tests and received:",
                "",
                "```text",
                previous_failure[-12000:],
                "```",
                "",
                "Correct the implementation based on this evidence.",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def _new_run_dir(contract: Contract, lab_root: Path = LAB_ROOT) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    base = lab_root / "runs" / f"{stamp}-{contract.task_id}"
    candidate = base
    suffix = 1
    while candidate.exists():
        suffix += 1
        candidate = Path(f"{base}-{suffix}")
    candidate.mkdir(parents=True)
    return candidate


def run_contract(contract: Contract, config: HarnessConfig, *, dry_run: bool = False) -> tuple[Path, dict[str, object]]:
    for rule in contract.rules:
        if not rule.is_file():
            raise ContractError(f"Rule file does not exist: {rule}")
    ensure_clean_repository(contract.workspace)

    started_at = datetime.now(timezone.utc)
    started_monotonic = time.monotonic()
    run_dir = _new_run_dir(contract)
    shutil.copy2(contract.source_path, run_dir / "contract.json")
    shutil.copy2(config.source_path, run_dir / "harness-config.json")

    result: dict[str, object] = {
        "task_id": contract.task_id,
        "mode": contract.mode,
        "status": "running",
        "workspace": str(contract.workspace),
        "run_dir": str(run_dir),
        "attempts": 0,
        "tests_passed": False,
        "review_required": contract.review.required,
        "reviewer": contract.review.reviewer,
        "started_at": started_at.isoformat(),
    }
    _write_json(run_dir / "result.json", result)

    previous_failure: str | None = None
    for attempt in range(1, contract.max_attempts + 1):
        result["attempts"] = attempt
        prompt_path = run_dir / f"prompt-{attempt}.md"
        prompt_path.write_text(render_prompt(contract, attempt, previous_failure), encoding="utf-8")

        adapter_result = run_aider(
            contract,
            config,
            prompt_path,
            run_dir,
            dry_run=dry_run,
        )
        (run_dir / f"aider-attempt-{attempt}.log").write_text(adapter_result.output, encoding="utf-8")
        _write_json(run_dir / f"aider-command-{attempt}.json", list(adapter_result.command))

        if dry_run:
            result["status"] = "dry_run"
            _finish_result(run_dir, result, started_monotonic)
            return run_dir, result

        if adapter_result.returncode != 0:
            result["status"] = "adapter_error"
            result["adapter_returncode"] = adapter_result.returncode
            _finish_result(run_dir, result, started_monotonic)
            return run_dir, result

        gate_report = inspect_changes(contract)
        _write_json(run_dir / f"gate-attempt-{attempt}.json", gate_report.to_dict())
        if not gate_report.passed:
            result["status"] = "gate_blocked"
            result["gate_violations"] = list(gate_report.violations)
            (run_dir / "final.diff").write_text(current_diff(contract.workspace), encoding="utf-8")
            _finish_result(run_dir, result, started_monotonic)
            return run_dir, result

        if contract.mode == "plan":
            if gate_report.changed_files:
                result["status"] = "gate_blocked"
                result["gate_violations"] = ["plan mode produced filesystem changes"]
            else:
                result["status"] = "awaiting_review" if contract.review.required else "planned"
            _finish_result(run_dir, result, started_monotonic)
            return run_dir, result

        failures: list[str] = []
        for test in contract.required_tests:
            test_result = _run_command(test.command, contract.workspace, test.timeout_seconds)
            log = (
                f"$ {' '.join(test.command)}\n"
                f"exit_code={test_result.returncode}\n\n"
                f"{test_result.stdout}"
            )
            (run_dir / f"test-{attempt}-{test.name}.log").write_text(log, encoding="utf-8")
            if test_result.returncode != 0:
                failures.append(log)

        post_test_gate = inspect_changes(contract)
        _write_json(run_dir / f"gate-post-test-attempt-{attempt}.json", post_test_gate.to_dict())
        if not post_test_gate.passed:
            result["status"] = "gate_blocked"
            result["gate_violations"] = list(post_test_gate.violations)
            (run_dir / "final.diff").write_text(current_diff(contract.workspace), encoding="utf-8")
            _finish_result(run_dir, result, started_monotonic)
            return run_dir, result

        if not failures:
            result["tests_passed"] = True
            result["status"] = "awaiting_review" if contract.review.required else "success"
            (run_dir / "final.diff").write_text(current_diff(contract.workspace), encoding="utf-8")
            _finish_result(run_dir, result, started_monotonic)
            return run_dir, result

        previous_failure = "\n\n".join(failures)
        if attempt == contract.max_attempts:
            result["status"] = "tests_failed"
            result["last_test_failure"] = previous_failure[-12000:]
            (run_dir / "final.diff").write_text(current_diff(contract.workspace), encoding="utf-8")
            _finish_result(run_dir, result, started_monotonic)
            return run_dir, result

    raise AssertionError("unreachable")


def record_review(run_dir: Path, decision: str, reviewer: str, notes: str) -> dict[str, object]:
    run_dir = run_dir.resolve()
    runs_root = (LAB_ROOT / "runs").resolve()
    try:
        run_dir.relative_to(runs_root)
    except ValueError as error:
        raise ContractError("Review target must be below stage2/runs") from error

    result_path = run_dir / "result.json"
    if not result_path.is_file():
        raise ContractError(f"Run result does not exist: {result_path}")
    result = json.loads(result_path.read_text(encoding="utf-8"))
    if result.get("status") != "awaiting_review":
        raise ContractError(f"Run is not awaiting review; current status is {result.get('status')}")

    status_by_decision = {
        "approve": "approved",
        "request_changes": "changes_requested",
        "reject": "rejected",
    }
    if decision not in status_by_decision:
        raise ContractError(f"Unsupported review decision: {decision}")
    result["status"] = status_by_decision[decision]
    result["review"] = {
        "decision": decision,
        "reviewer": reviewer,
        "notes": notes,
        "recorded_at": datetime.now(timezone.utc).isoformat(),
    }
    _write_json(result_path, result)
    (run_dir / "review.md").write_text(
        "# Review\n\n"
        f"- Decision: `{decision}`\n"
        f"- Reviewer: `{reviewer}`\n\n"
        "## Notes\n\n"
        f"{notes.strip() or 'No notes supplied.'}\n",
        encoding="utf-8",
    )
    return result
