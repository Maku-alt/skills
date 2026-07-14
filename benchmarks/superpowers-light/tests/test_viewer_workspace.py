import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PREPARER_PATH = ROOT / "scripts" / "prepare_viewer.py"


def load_preparer():
    spec = importlib.util.spec_from_file_location("viewer_preparer", PREPARER_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class ViewerWorkspaceTests(unittest.TestCase):
    def test_preparer_exists(self) -> None:
        self.assertTrue(PREPARER_PATH.is_file(), "prepare_viewer.py is missing")

    @unittest.skipUnless(PREPARER_PATH.is_file(), "preparer not implemented")
    def test_workspace_uses_opaque_ids_and_keeps_mapping_outside(self) -> None:
        preparer = load_preparer()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            raw = root / "raw"
            viewer = root / "viewer"
            mapping = raw / "blind-map.json"
            for run_id, config in (("audit-r1-b0", "B0"), ("audit-r1-s1", "S1")):
                run = raw / run_id
                run.mkdir(parents=True)
                (run / "run.json").write_text(
                    json.dumps(
                        {
                            "run_id": run_id,
                            "task_id": "audit",
                            "repetition": 1,
                            "config": config,
                            "prompt": "Audit the target",
                            "exit_code": 0,
                        }
                    ),
                    encoding="utf-8",
                )
                (run / "final.md").write_text("Finding with evidence", encoding="utf-8")
                (run / "changes.diff").write_text("", encoding="utf-8")
                (run / "grading.json").write_text(
                    json.dumps(
                        {
                            "configuration": "with_skill" if config == "S1" else "without_skill",
                            "expectations": [],
                            "summary": {"passed": 0, "failed": 0, "total": 0, "pass_rate": 0},
                        }
                    ),
                    encoding="utf-8",
                )

            result = preparer.prepare_workspace(raw, viewer, mapping, seed=5602)

            self.assertEqual(result["runs"], 2)
            self.assertTrue(mapping.is_file())
            self.assertFalse((viewer / "blind-map.json").exists())
            candidates = sorted(path.name for path in viewer.iterdir() if path.is_dir())
            self.assertEqual(candidates, ["candidate-01", "candidate-02"])
            viewer_text = "\n".join(
                path.read_text(encoding="utf-8")
                for path in viewer.rglob("*")
                if path.is_file()
            )
            for forbidden in ("audit-r1-b0", "audit-r1-s1", "with_skill", "without_skill", '"B0"', '"S1"'):
                self.assertNotIn(forbidden, viewer_text)


if __name__ == "__main__":
    unittest.main()
