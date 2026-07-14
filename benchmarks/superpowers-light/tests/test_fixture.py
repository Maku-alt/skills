import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixture"
HIDDEN = ROOT / "hidden"


def run_unittest(path: Path, pattern: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            str(path),
            "-p",
            pattern,
            "-v",
        ],
        cwd=FIXTURE,
        text=True,
        capture_output=True,
        check=False,
    )


class FixtureTests(unittest.TestCase):
    def test_pristine_fixture_has_passing_public_tests_and_failing_hidden_bug(self) -> None:
        self.assertTrue(FIXTURE.is_dir(), "fixture directory is missing")
        self.assertTrue(HIDDEN.is_dir(), "hidden-test directory is missing")
        public = run_unittest(FIXTURE / "tests", "test_*.py")
        hidden = run_unittest(HIDDEN, "test_checkout_hidden.py")

        self.assertEqual(public.returncode, 0, public.stdout + public.stderr)
        self.assertEqual(hidden.returncode, 1, hidden.stdout + hidden.stderr)
        self.assertIn("negative_quantity", hidden.stdout + hidden.stderr)

    def test_eval_matrix_contains_four_frozen_tasks(self) -> None:
        path = ROOT / "evals.json"
        self.assertTrue(path.is_file(), "evals.json is missing")
        payload = json.loads(path.read_text(encoding="utf-8"))

        self.assertEqual(
            [item["id"] for item in payload["evals"]],
            ["planning", "bugfix", "audit", "parallel_audit"],
        )
        self.assertTrue(all(item["prompt"].strip() for item in payload["evals"]))
        self.assertTrue(
            all("superpower" not in item["prompt"].lower() for item in payload["evals"])
        )

    def test_gold_defines_a_100_point_rubric_for_each_task(self) -> None:
        path = ROOT / "gold.json"
        self.assertTrue(path.is_file(), "gold.json is missing")
        gold = json.loads(path.read_text(encoding="utf-8"))

        self.assertEqual(set(gold), {"planning", "bugfix", "audit", "parallel_audit"})
        for task in gold.values():
            self.assertEqual(sum(dimension["points"] for dimension in task["rubric"]), 100)


if __name__ == "__main__":
    unittest.main()
