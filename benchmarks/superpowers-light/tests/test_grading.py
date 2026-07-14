import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GRADER_PATH = ROOT / "scripts" / "grade_results.py"


def load_grader():
    spec = importlib.util.spec_from_file_location("benchmark_grader", GRADER_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class GradingTests(unittest.TestCase):
    def test_grader_exists(self) -> None:
        self.assertTrue(GRADER_PATH.is_file(), "grade_results.py is missing")

    @unittest.skipUnless(GRADER_PATH.is_file(), "grader not implemented")
    def test_usage_limit_is_infrastructure_failure_not_zero_score(self) -> None:
        grader = load_grader()
        metadata = {"exit_code": 1, "status": "completed"}
        events = "You've hit your usage limit. try again later"

        result = grader.classify_execution(metadata, events)

        self.assertEqual(result, "infrastructure_failure")

    @unittest.skipUnless(GRADER_PATH.is_file(), "grader not implemented")
    def test_complete_bugfix_receives_full_deterministic_score(self) -> None:
        grader = load_grader()
        metadata = {
            "exit_code": 0,
            "verification": {
                "public_tests": {"exit_code": 0},
                "hidden_tests": {"exit_code": 0},
            },
        }
        diff = """diff --git a/src/checkout.py b/src/checkout.py
+    if quantity <= 0:
+        raise ValueError("quantity must be positive")
diff --git a/tests/test_checkout.py b/tests/test_checkout.py
+    def test_rejects_non_positive_quantity(self):
"""
        final = "Validated the narrow checkout change. Public and new quantity tests pass."

        result = grader.grade_bugfix(metadata, diff, final)

        self.assertEqual(result["score"], 100)
        self.assertTrue(all(item["passed"] for item in result["expectations"]))

    @unittest.skipUnless(GRADER_PATH.is_file(), "grader not implemented")
    def test_finding_matching_requires_multiple_root_cause_terms(self) -> None:
        grader = load_grader()
        findings = [
            {
                "id": "sql_injection",
                "terms": ["sql injection", "parameterized", "find_by_email"],
            },
            {
                "id": "path_traversal",
                "terms": ["path traversal", "username", "save_avatar"],
            },
        ]
        text = "find_by_email has SQL injection; use a parameterized query. username is mentioned."

        matched = grader.match_findings(text, findings)

        self.assertEqual(matched, {"sql_injection"})

    @unittest.skipUnless(GRADER_PATH.is_file(), "grader not implemented")
    def test_aggregation_excludes_infrastructure_failures(self) -> None:
        grader = load_grader()
        runs = [
            {"configuration": "with_skill", "score": 80, "time_seconds": 20, "tokens": 100},
            {"configuration": "with_skill", "status": "infrastructure_failure"},
            {"configuration": "without_skill", "score": 60, "time_seconds": 10, "tokens": 50},
        ]

        summary = grader.aggregate_runs(runs)

        self.assertEqual(summary["with_skill"]["quality"]["mean"], 80)
        self.assertEqual(summary["with_skill"]["valid_runs"], 1)
        self.assertEqual(summary["with_skill"]["infrastructure_failures"], 1)
        self.assertEqual(summary["without_skill"]["quality"]["mean"], 60)


if __name__ == "__main__":
    unittest.main()
