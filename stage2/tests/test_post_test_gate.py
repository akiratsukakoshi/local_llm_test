import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from stage2.orchestrator.adapter import AdapterResult
from stage2.orchestrator.contract import Contract, HarnessConfig, ReviewSpec, TestSpec
from stage2.orchestrator.runner import run_contract


class PostTestGateTests(unittest.TestCase):
    def test_blocks_test_created_read_only_change(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            workspace = root / "workspace"
            workspace.mkdir()
            (workspace / "src.py").write_text("VALUE = 1\n", encoding="utf-8")
            (workspace / "test_src.py").write_text("assert True\n", encoding="utf-8")
            subprocess.run(["git", "init", "--quiet"], cwd=workspace, check=True)
            subprocess.run(["git", "config", "user.name", "Test"], cwd=workspace, check=True)
            subprocess.run(
                ["git", "config", "user.email", "test@example.invalid"], cwd=workspace, check=True
            )
            subprocess.run(["git", "add", "."], cwd=workspace, check=True)
            subprocess.run(["git", "commit", "--quiet", "-m", "initial"], cwd=workspace, check=True)

            contract_path = root / "contract.json"
            contract_path.write_text("{}\n", encoding="utf-8")
            config_path = root / "config.json"
            config_path.write_text("{}\n", encoding="utf-8")
            contract = Contract(
                source_path=contract_path,
                task_id="s2-post-test-gate",
                mode="autonomous",
                objective="Exercise the post-test gate.",
                acceptance_criteria=("Unsafe test effects are blocked.",),
                workspace=workspace,
                fixture=None,
                rules=(),
                allowed_paths=("src.py",),
                read_only_paths=("test_src.py",),
                context_paths=(),
                required_tests=(
                    TestSpec(
                        name="mutating-test",
                        command=(
                            "python3",
                            "-c",
                            "from pathlib import Path; Path('test_src.py').write_text('assert False\\n')",
                        ),
                        timeout_seconds=10,
                    ),
                ),
                max_attempts=1,
                max_changed_files=1,
                max_changed_lines=10,
                allow_new_files=False,
                review=ReviewSpec(required=True, reviewer="human"),
            )
            config = HarnessConfig(
                source_path=config_path,
                adapter="aider",
                aider_binary=Path("/bin/true"),
                model="openai/test",
                api_base="http://127.0.0.1:9/v1",
                api_key="local",
                edit_format="whole",
                request_timeout_seconds=10,
            )
            run_dir = root / "run"
            run_dir.mkdir()

            with mock.patch("stage2.orchestrator.runner._new_run_dir", return_value=run_dir), mock.patch(
                "stage2.orchestrator.runner.run_aider",
                return_value=AdapterResult(returncode=0, command=("aider",), output="no edit"),
            ):
                _, result = run_contract(contract, config)

            self.assertEqual(result["status"], "gate_blocked")
            self.assertIn("read-only path changed: test_src.py", result["gate_violations"])
            self.assertTrue((run_dir / "gate-post-test-attempt-1.json").is_file())


if __name__ == "__main__":
    unittest.main()
