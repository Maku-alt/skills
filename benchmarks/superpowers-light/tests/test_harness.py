import importlib.util
import json
import os
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = ROOT / "scripts" / "run_benchmark.py"
BUILDER_PATH = ROOT / "scripts" / "build-configs.ps1"
SELECTED = {
    "brainstorming",
    "writing-plans",
    "systematic-debugging",
    "test-driven-development",
    "verification-before-completion",
    "dispatching-parallel-agents",
    "subagent-driven-development",
}


def load_runner():
    spec = importlib.util.spec_from_file_location("benchmark_runner", RUNNER_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class HarnessTests(unittest.TestCase):
    def test_sensitive_runtime_and_raw_results_are_ignored(self) -> None:
        completed = subprocess.run(
            [
                "git",
                "check-ignore",
                "benchmarks/superpowers-light/.runtime/probe",
                "benchmarks/superpowers-light/results/raw/probe",
                "benchmarks/superpowers-light/results/pilot/probe",
            ],
            cwd=ROOT.parents[1],
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertEqual(len(completed.stdout.splitlines()), 3)

    def test_runner_and_builder_exist(self) -> None:
        self.assertTrue(RUNNER_PATH.is_file(), "run_benchmark.py is missing")
        self.assertTrue(BUILDER_PATH.is_file(), "build-configs.ps1 is missing")

    @unittest.skipUnless(RUNNER_PATH.is_file(), "runner not implemented")
    def test_matrix_has_sixteen_runs_and_identical_paired_prompts(self) -> None:
        runner = load_runner()
        evals = json.loads((ROOT / "evals.json").read_text(encoding="utf-8"))["evals"]

        matrix = runner.build_matrix(evals)

        self.assertEqual(len(matrix), 16)
        for task in {run["task_id"] for run in matrix}:
            prompts = {run["prompt"] for run in matrix if run["task_id"] == task}
            configs = [run["config"] for run in matrix if run["task_id"] == task]
            self.assertEqual(len(prompts), 1)
            self.assertEqual(configs.count("B0"), 2)
            self.assertEqual(configs.count("S1"), 2)

    @unittest.skipUnless(RUNNER_PATH.is_file(), "runner not implemented")
    def test_random_order_is_deterministic_and_not_grouped_by_config(self) -> None:
        runner = load_runner()
        evals = json.loads((ROOT / "evals.json").read_text(encoding="utf-8"))["evals"]
        matrix = runner.build_matrix(evals)

        first = runner.randomized_order(matrix, seed=5602)
        second = runner.randomized_order(matrix, seed=5602)

        self.assertEqual(first, second)
        self.assertNotEqual([run["config"] for run in first], sorted(run["config"] for run in first))
        self.assertEqual({run["run_id"] for run in first}, {run["run_id"] for run in matrix})

    @unittest.skipUnless(RUNNER_PATH.is_file(), "runner not implemented")
    def test_codex_home_is_resolved_before_child_changes_directory(self) -> None:
        runner = load_runner()

        self.assertTrue(hasattr(runner, "resolve_codex_home"))
        resolved = runner.resolve_codex_home(Path("relative-homes"), "B0")

        self.assertTrue(resolved.is_absolute())
        self.assertEqual(resolved.name, "B0")

    @unittest.skipUnless(RUNNER_PATH.is_file(), "runner not implemented")
    def test_run_artifact_paths_are_absolute_before_child_changes_directory(self) -> None:
        runner = load_runner()
        self.assertTrue(hasattr(runner, "resolve_run_paths"))

        artifact, workspace, final = runner.resolve_run_paths(Path("relative-results"), "run-1")

        self.assertTrue(artifact.is_absolute())
        self.assertTrue(workspace.is_absolute())
        self.assertTrue(final.is_absolute())
        self.assertEqual(workspace.parent, artifact)
        self.assertEqual(final.parent, artifact)

    @unittest.skipUnless(RUNNER_PATH.is_file(), "runner not implemented")
    def test_explicit_codex_executable_is_resolved_absolutely(self) -> None:
        runner = load_runner()
        self.assertTrue(hasattr(runner, "resolve_codex_executable"))
        with tempfile.TemporaryDirectory() as temporary:
            executable = Path(temporary) / "codex.cmd"
            executable.write_text("@echo off", encoding="utf-8")

            resolved = runner.resolve_codex_executable(executable)

            self.assertEqual(resolved, executable.resolve())

    @unittest.skipUnless(RUNNER_PATH.is_file(), "runner not implemented")
    def test_safe_remove_tree_handles_read_only_files_inside_allowed_root(self) -> None:
        runner = load_runner()
        self.assertTrue(hasattr(runner, "safe_remove_tree"))
        with tempfile.TemporaryDirectory() as temporary:
            allowed_root = Path(temporary)
            target = allowed_root / "old-run"
            target.mkdir()
            locked = target / "object"
            locked.write_text("data", encoding="utf-8")
            os.chmod(locked, stat.S_IREAD)

            runner.safe_remove_tree(target, allowed_root)

            self.assertFalse(target.exists())

    @unittest.skipUnless(BUILDER_PATH.is_file(), "builder not implemented")
    def test_config_builder_isolates_selected_skills(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            source_home = base / "source-home"
            source_skills = base / "source-skills"
            output = base / "output"
            source_home.mkdir()
            source_skills.mkdir()
            (source_home / "auth.json").write_text("secret-auth", encoding="utf-8")
            (source_home / "config.toml").write_text("must-not-copy", encoding="utf-8")
            (source_skills / ".system").mkdir()
            (source_skills / ".system" / "marker.txt").write_text("system", encoding="utf-8")
            for name in SELECTED:
                skill = source_skills / name
                skill.mkdir()
                (skill / "SKILL.md").write_text(f"# {name}", encoding="utf-8")

            completed = subprocess.run(
                [
                    "powershell",
                    "-NoProfile",
                    "-File",
                    str(BUILDER_PATH),
                    "-SourceCodexHome",
                    str(source_home),
                    "-SourceSkills",
                    str(source_skills),
                    "-OutputRoot",
                    str(output),
                ],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
            b0 = {path.name for path in (output / "B0" / "skills").iterdir()}
            s1 = {path.name for path in (output / "S1" / "skills").iterdir()}
            self.assertEqual(b0, {".system"})
            self.assertEqual(s1, SELECTED | {".system"})
            self.assertFalse((output / "B0" / "config.toml").exists())
            self.assertEqual((output / "B0" / "auth.json").read_text(encoding="utf-8"), "secret-auth")
            manifest = (output / "inventory.json").read_text(encoding="utf-8")
            self.assertNotIn("secret-auth", manifest)


if __name__ == "__main__":
    unittest.main()
