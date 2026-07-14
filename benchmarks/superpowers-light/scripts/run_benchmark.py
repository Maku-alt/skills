from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import os
import random
import shutil
import stat
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MODEL = "gpt-5.6-sol"
REASONING_EFFORT = "medium"


def build_matrix(evals: list[dict[str, str]]) -> list[dict[str, Any]]:
    matrix: list[dict[str, Any]] = []
    for item in evals:
        for repetition in (1, 2):
            for configuration in ("B0", "S1"):
                matrix.append(
                    {
                        "run_id": f"{item['id']}-r{repetition}-{configuration.lower()}",
                        "task_id": item["id"],
                        "repetition": repetition,
                        "config": configuration,
                        "prompt": item["prompt"],
                    }
                )
    return matrix


def randomized_order(matrix: list[dict[str, Any]], seed: int) -> list[dict[str, Any]]:
    ordered = [dict(item) for item in matrix]
    random.Random(seed).shuffle(ordered)
    return ordered


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def resolve_codex_home(homes_root: Path, configuration: str) -> Path:
    return (homes_root / configuration).resolve()


def run_command(
    command: list[str],
    *,
    cwd: Path,
    env: dict[str, str] | None = None,
    timeout: int | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        env=env,
        text=True,
        capture_output=True,
        check=False,
        timeout=timeout,
    )


def safe_remove_tree(path: Path, allowed_root: Path) -> None:
    resolved_path = path.resolve()
    resolved_root = allowed_root.resolve()
    if resolved_path == resolved_root or resolved_root not in resolved_path.parents:
        raise ValueError(f"refusing to remove path outside allowed root: {resolved_path}")

    def remove_read_only(function, target, _error) -> None:
        os.chmod(target, stat.S_IWRITE)
        function(target)

    shutil.rmtree(resolved_path, onerror=remove_read_only)


def initialize_run_directory(run_dir: Path, allowed_root: Path) -> None:
    if run_dir.exists():
        safe_remove_tree(run_dir, allowed_root)
    shutil.copytree(ROOT / "fixture", run_dir)
    commands = [
        ["git", "init", "-q"],
        ["git", "config", "user.email", "benchmark@example.invalid"],
        ["git", "config", "user.name", "Benchmark Runner"],
        ["git", "add", "."],
        ["git", "commit", "-qm", "fixture baseline"],
    ]
    for command in commands:
        completed = run_command(command, cwd=run_dir)
        if completed.returncode != 0:
            raise RuntimeError(completed.stdout + completed.stderr)


def extract_usage(events_path: Path) -> dict[str, int]:
    usage = {"input_tokens": 0, "cached_input_tokens": 0, "output_tokens": 0}
    if not events_path.exists():
        return usage
    for line in events_path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        stack: list[Any] = [event]
        while stack:
            value = stack.pop()
            if isinstance(value, dict):
                for key, nested in value.items():
                    if key in usage and isinstance(nested, int):
                        usage[key] = max(usage[key], nested)
                    elif isinstance(nested, (dict, list)):
                        stack.append(nested)
            elif isinstance(value, list):
                stack.extend(value)
    return usage


def verification_results(run_dir: Path, task_id: str) -> dict[str, Any]:
    result: dict[str, Any] = {}
    public = run_command(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py", "-v"],
        cwd=run_dir,
    )
    result["public_tests"] = {
        "exit_code": public.returncode,
        "output": public.stdout + public.stderr,
    }
    if task_id == "bugfix":
        hidden = run_command(
            [
                sys.executable,
                "-m",
                "unittest",
                "discover",
                "-s",
                str(ROOT / "hidden"),
                "-p",
                "test_checkout_hidden.py",
                "-v",
            ],
            cwd=run_dir,
        )
        result["hidden_tests"] = {
            "exit_code": hidden.returncode,
            "output": hidden.stdout + hidden.stderr,
        }
    return result


def execute_run(
    item: dict[str, Any],
    *,
    homes_root: Path,
    results_root: Path,
    timeout_seconds: int,
) -> dict[str, Any]:
    artifact_dir = results_root / item["run_id"]
    workspace = artifact_dir / "workspace"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    initialize_run_directory(workspace, results_root)
    final_path = artifact_dir / "final.md"
    events_path = artifact_dir / "events.jsonl"
    codex = shutil.which("codex")
    if not codex:
        raise RuntimeError("codex executable not found")
    command = [
        codex,
        "exec",
        "--ignore-user-config",
        "--ephemeral",
        "--json",
        "--skip-git-repo-check",
        "-m",
        MODEL,
        "-c",
        f'model_reasoning_effort="{REASONING_EFFORT}"',
        "-s",
        "workspace-write",
        "-C",
        str(workspace),
        "-o",
        str(final_path),
        item["prompt"],
    ]
    environment = os.environ.copy()
    environment["CODEX_HOME"] = str(resolve_codex_home(homes_root, item["config"]))
    started = time.monotonic()
    status = "completed"
    try:
        completed = run_command(
            command,
            cwd=workspace,
            env=environment,
            timeout=timeout_seconds,
        )
        events_path.write_text(completed.stdout, encoding="utf-8")
        (artifact_dir / "stderr.log").write_text(completed.stderr, encoding="utf-8")
        exit_code = completed.returncode
    except subprocess.TimeoutExpired as error:
        status = "timeout"
        exit_code = 124
        events_path.write_text(error.stdout or "", encoding="utf-8")
        (artifact_dir / "stderr.log").write_text(error.stderr or "", encoding="utf-8")
    duration = time.monotonic() - started
    diff = run_command(["git", "diff", "--no-ext-diff", "--binary"], cwd=workspace)
    (artifact_dir / "changes.diff").write_text(diff.stdout, encoding="utf-8")
    verification = verification_results(workspace, item["task_id"])
    metadata = {
        **item,
        "status": status,
        "exit_code": exit_code,
        "duration_seconds": round(duration, 3),
        "model": MODEL,
        "reasoning_effort": REASONING_EFFORT,
        "prompt_sha256": sha256_text(item["prompt"]),
        "usage": extract_usage(events_path),
        "verification": verification,
    }
    (artifact_dir / "run.json").write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return metadata


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--homes-root", type=Path, required=True)
    parser.add_argument("--results-root", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=5602)
    parser.add_argument("--max-workers", type=int, default=2)
    parser.add_argument("--timeout-seconds", type=int, default=1800)
    parser.add_argument("--pilot", action="store_true")
    args = parser.parse_args()

    evals = json.loads((ROOT / "evals.json").read_text(encoding="utf-8"))["evals"]
    if args.pilot:
        planning = next(item for item in evals if item["id"] == "planning")
        matrix = [
            {
                "run_id": f"planning-pilot-{configuration.lower()}",
                "task_id": "planning",
                "repetition": 0,
                "config": configuration,
                "prompt": planning["prompt"],
            }
            for configuration in ("B0", "S1")
        ]
    else:
        matrix = randomized_order(build_matrix(evals), args.seed)
    args.results_root.mkdir(parents=True, exist_ok=True)
    (args.results_root / "run-order.json").write_text(
        json.dumps(matrix, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.max_workers) as executor:
        futures = [
            executor.submit(
                execute_run,
                item,
                homes_root=args.homes_root,
                results_root=args.results_root,
                timeout_seconds=args.timeout_seconds,
            )
            for item in matrix
        ]
        for future in concurrent.futures.as_completed(futures):
            metadata = future.result()
            print(
                json.dumps(
                    {
                        "run_id": metadata["run_id"],
                        "status": metadata["status"],
                        "exit_code": metadata["exit_code"],
                        "duration_seconds": metadata["duration_seconds"],
                    }
                ),
                flush=True,
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
