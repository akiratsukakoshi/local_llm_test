import json
import tempfile
import unittest
from pathlib import Path

from stage2.orchestrator.contract import ContractError, load_contract


class ContractTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        (self.root / "rules").mkdir()
        (self.root / "rules" / "common.md").write_text("rules\n", encoding="utf-8")
        (self.root / "fixtures" / "sample").mkdir(parents=True)
        (self.root / "workspaces").mkdir()

    def tearDown(self):
        self.temp_dir.cleanup()

    def write_contract(self, **updates):
        value = {
            "id": "s2-test-001",
            "mode": "autonomous",
            "objective": "Fix the behavior.",
            "acceptance_criteria": ["Tests pass."],
            "workspace": "workspaces/test",
            "fixture": "fixtures/sample",
            "rules": ["rules/common.md"],
            "allowed_paths": ["src.py"],
            "read_only_paths": ["test_src.py"],
            "required_tests": [
                {"name": "unit", "command": ["python3", "-m", "unittest"]}
            ],
        }
        value.update(updates)
        path = self.root / "task.json"
        path.write_text(json.dumps(value), encoding="utf-8")
        return path

    def test_loads_valid_contract(self):
        contract = load_contract(self.write_contract(), self.root)
        self.assertEqual(contract.task_id, "s2-test-001")
        self.assertEqual(contract.allowed_paths, ("src.py",))
        self.assertEqual(contract.required_tests[0].command, ("python3", "-m", "unittest"))

    def test_rejects_workspace_outside_managed_directory(self):
        path = self.write_contract(workspace="other/test")
        with self.assertRaisesRegex(ContractError, "below stage2/workspaces"):
            load_contract(path, self.root)

    def test_rejects_parent_path_pattern(self):
        path = self.write_contract(allowed_paths=["../secret.txt"])
        with self.assertRaisesRegex(ContractError, "safe relative path"):
            load_contract(path, self.root)

    def test_implementation_requires_tests(self):
        path = self.write_contract(required_tests=[])
        with self.assertRaisesRegex(ContractError, "required_tests must not be empty"):
            load_contract(path, self.root)


if __name__ == "__main__":
    unittest.main()
