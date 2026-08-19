import subprocess
import tempfile
import unittest
from pathlib import Path

from stage2.orchestrator.contract import Contract, ReviewSpec
from stage2.orchestrator.gates import ensure_clean_repository, inspect_changes


class GateTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.workspace = Path(self.temp_dir.name) / "repo"
        self.workspace.mkdir()
        (self.workspace / "src.py").write_text("VALUE = 1\n", encoding="utf-8")
        (self.workspace / "test_src.py").write_text("assert True\n", encoding="utf-8")
        self.git("init", "--quiet")
        self.git("config", "user.name", "Test")
        self.git("config", "user.email", "test@example.invalid")
        self.git("add", ".")
        self.git("commit", "--quiet", "-m", "initial")

    def tearDown(self):
        self.temp_dir.cleanup()

    def git(self, *args):
        subprocess.run(["git", *args], cwd=self.workspace, check=True, stdout=subprocess.PIPE)

    def contract(self, **updates):
        values = {
            "source_path": self.workspace / "contract.json",
            "task_id": "s2-test-gate",
            "mode": "autonomous",
            "objective": "Test gates",
            "acceptance_criteria": ("Pass",),
            "workspace": self.workspace,
            "fixture": None,
            "rules": (),
            "allowed_paths": ("src.py",),
            "read_only_paths": ("test_src.py",),
            "context_paths": (),
            "required_tests": (),
            "max_attempts": 1,
            "max_changed_files": 1,
            "max_changed_lines": 10,
            "allow_new_files": False,
            "review": ReviewSpec(required=True, reviewer="human"),
        }
        values.update(updates)
        return Contract(**values)

    def test_allows_bounded_edit(self):
        ensure_clean_repository(self.workspace)
        (self.workspace / "src.py").write_text("VALUE = 2\n", encoding="utf-8")
        report = inspect_changes(self.contract())
        self.assertTrue(report.passed)
        self.assertEqual(report.changed_files, ("src.py",))

    def test_blocks_read_only_edit(self):
        (self.workspace / "test_src.py").write_text("assert False\n", encoding="utf-8")
        report = inspect_changes(self.contract())
        self.assertFalse(report.passed)
        self.assertIn("read-only path changed: test_src.py", report.violations)

    def test_blocks_new_file(self):
        (self.workspace / "new.py").write_text("NEW = True\n", encoding="utf-8")
        report = inspect_changes(self.contract(allowed_paths=("*.py",), max_changed_files=3))
        self.assertFalse(report.passed)
        self.assertIn("new file is not allowed: new.py", report.violations)

    def test_blocks_excessive_diff(self):
        (self.workspace / "src.py").write_text("\n".join(f"line_{index} = {index}" for index in range(20)) + "\n")
        report = inspect_changes(self.contract(max_changed_lines=5))
        self.assertFalse(report.passed)
        self.assertTrue(any("changed line count" in violation for violation in report.violations))


if __name__ == "__main__":
    unittest.main()
