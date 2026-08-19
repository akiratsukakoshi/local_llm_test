from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .contract import ContractError, load_contract, load_harness_config
from .runner import prepare_workspace, record_review, run_contract


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Stage 2 local coding-agent experiment harness")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate", help="Validate a task contract without making changes")
    validate.add_argument("contract")

    prepare = subparsers.add_parser("prepare", help="Copy a fixture into an isolated Git workspace")
    prepare.add_argument("contract")

    run = subparsers.add_parser("run", help="Run one controlled Aider/Qwen experiment")
    run.add_argument("contract")
    run.add_argument(
        "--config",
        default="stage2/configs/aider-qwen38.json",
        help="Harness configuration JSON",
    )
    run.add_argument("--dry-run", action="store_true", help="Build prompts and commands without contacting the model")

    review = subparsers.add_parser("review", help="Record the human or upstream-AI review decision")
    review.add_argument("run_dir")
    review.add_argument("--decision", required=True, choices=("approve", "request_changes", "reject"))
    review.add_argument("--reviewer", required=True)
    review.add_argument("--notes", default="")
    return parser


def _summary(contract) -> dict[str, object]:
    return {
        "id": contract.task_id,
        "mode": contract.mode,
        "workspace": str(contract.workspace),
        "fixture": str(contract.fixture) if contract.fixture else None,
        "rules": [str(path) for path in contract.rules],
        "allowed_paths": list(contract.allowed_paths),
        "read_only_paths": list(contract.read_only_paths),
        "tests": [list(test.command) for test in contract.required_tests],
        "max_attempts": contract.max_attempts,
        "review_required": contract.review.required,
    }


def main(argv: list[str] | None = None) -> None:
    args = _parser().parse_args(argv)
    try:
        if args.command == "validate":
            contract = load_contract(args.contract)
            print(json.dumps(_summary(contract), indent=2, ensure_ascii=False))
            return

        if args.command == "prepare":
            contract = load_contract(args.contract)
            workspace = prepare_workspace(contract)
            print(f"Prepared clean Git workspace: {workspace}")
            return

        if args.command == "run":
            contract = load_contract(args.contract)
            config = load_harness_config(args.config)
            run_dir, result = run_contract(contract, config, dry_run=args.dry_run)
            print(json.dumps(result, indent=2, ensure_ascii=False))
            print(f"Run artifacts: {run_dir}")
            if result["status"] not in {"dry_run", "success", "planned", "awaiting_review"}:
                raise SystemExit(1)
            return

        if args.command == "review":
            result = record_review(Path(args.run_dir), args.decision, args.reviewer, args.notes)
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return

        raise AssertionError("unreachable")
    except ContractError as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(2) from error
