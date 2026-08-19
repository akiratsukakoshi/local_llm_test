import json
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest import mock

from stage2.orchestrator.contract import HarnessConfig, load_contract
from stage2.orchestrator.runner import prepare_workspace, run_contract


class TimingTests(unittest.TestCase):
    def test_dry_run_records_start_finish_and_wall_time(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            fixture = root / "fixtures" / "sample"
            fixture.mkdir(parents=True)
            (fixture / "src.py").write_text("VALUE = 1\n", encoding="utf-8")
            (fixture / "test_src.py").write_text("assert True\n", encoding="utf-8")
            (root / "rules").mkdir()
            (root / "rules" / "common.md").write_text("Do the task.\n", encoding="utf-8")
            (root / "workspaces").mkdir()

            contract_path = root / "task.json"
            contract_path.write_text(
                json.dumps(
                    {
                        "id": "s2-timing-test",
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
            config_path = root / "config.json"
            config_path.write_text("{}\n", encoding="utf-8")

            contract = load_contract(contract_path, root)
            prepare_workspace(contract)
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

            with mock.patch("stage2.orchestrator.runner._new_run_dir", return_value=run_dir):
                returned_dir, result = run_contract(contract, config, dry_run=True)

            self.assertEqual(returned_dir, run_dir)
            self.assertEqual(result["status"], "dry_run")
            self.assertGreaterEqual(result["wall_time_seconds"], 0)
            self.assertLess(result["wall_time_seconds"], 10)
            self.assertLessEqual(
                datetime.fromisoformat(result["started_at"]),
                datetime.fromisoformat(result["finished_at"]),
            )
            persisted = json.loads((run_dir / "result.json").read_text(encoding="utf-8"))
            self.assertEqual(persisted["wall_time_seconds"], result["wall_time_seconds"])


if __name__ == "__main__":
    unittest.main()
