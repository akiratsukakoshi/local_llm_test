import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from stage2.orchestrator.adapter import build_aider_command
from stage2.orchestrator.contract import HarnessConfig, load_contract
from stage2.orchestrator.runner import prepare_workspace, render_prompt


class RunnerTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        (self.root / "fixtures" / "sample").mkdir(parents=True)
        (self.root / "fixtures" / "sample" / "src.py").write_text("VALUE = 1\n", encoding="utf-8")
        (self.root / "fixtures" / "sample" / "test_src.py").write_text("assert True\n", encoding="utf-8")
        (self.root / "rules").mkdir()
        (self.root / "rules" / "common.md").write_text("Do the task.\n", encoding="utf-8")
        (self.root / "workspaces").mkdir()
        self.contract_path = self.root / "task.json"
        self.contract_path.write_text(
            json.dumps(
                {
                    "id": "s2-runner-test",
                    "mode": "autonomous",
                    "objective": "Change VALUE.",
                    "acceptance_criteria": ["The test passes."],
                    "workspace": "workspaces/sample",
                    "fixture": "fixtures/sample",
                    "rules": ["rules/common.md"],
                    "allowed_paths": ["src.py"],
                    "read_only_paths": ["test_src.py"],
                    "required_tests": [
                        {"name": "unit", "command": ["python3", "-m", "unittest"]}
                    ],
                }
            ),
            encoding="utf-8",
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_prepare_creates_clean_git_workspace(self):
        contract = load_contract(self.contract_path, self.root)
        workspace = prepare_workspace(contract)
        self.assertTrue((workspace / ".git").is_dir())
        status = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=workspace,
            text=True,
            stdout=subprocess.PIPE,
            check=True,
        ).stdout
        self.assertEqual(status, "")

    def test_prompt_includes_enforced_scope_and_failure(self):
        contract = load_contract(self.contract_path, self.root)
        prompt = render_prompt(contract, 2, "expected 2, got 1")
        self.assertIn("`src.py`", prompt)
        self.assertIn("`test_src.py`", prompt)
        self.assertIn("expected 2, got 1", prompt)

    def test_aider_command_keeps_tests_read_only(self):
        contract = load_contract(self.contract_path, self.root)
        prepare_workspace(contract)
        run_dir = self.root / "run"
        run_dir.mkdir()
        prompt = run_dir / "prompt.md"
        prompt.write_text("task\n", encoding="utf-8")
        config = HarnessConfig(
            source_path=self.root / "config.json",
            adapter="aider",
            aider_binary=Path("/bin/true"),
            model="openai/test",
            api_base="http://127.0.0.1:8000/v1",
            api_key="local",
            edit_format="whole",
            request_timeout_seconds=60,
        )
        command = build_aider_command(contract, config, prompt, run_dir)
        file_arguments = [command[index + 1] for index, value in enumerate(command[:-1]) if value == "--file"]
        read_arguments = [command[index + 1] for index, value in enumerate(command[:-1]) if value == "--read"]
        self.assertIn(str((contract.workspace / "src.py").resolve()), file_arguments)
        self.assertNotIn(str((contract.workspace / "test_src.py").resolve()), file_arguments)
        self.assertIn(str((contract.workspace / "test_src.py").resolve()), read_arguments)


if __name__ == "__main__":
    unittest.main()
