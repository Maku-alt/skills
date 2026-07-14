from __future__ import annotations

import argparse
import json
import random
import shutil
from pathlib import Path
from typing import Any


TASK_ORDER = {"planning": 1, "bugfix": 2, "audit": 3, "parallel_audit": 4}


def sanitized_grading(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        key: payload[key]
        for key in ("expectations", "summary", "execution_metrics", "timing")
        if key in payload
    }


def prepare_workspace(
    raw_root: Path,
    viewer_root: Path,
    mapping_path: Path,
    *,
    seed: int,
) -> dict[str, Any]:
    run_dirs = sorted(
        path
        for path in raw_root.iterdir()
        if path.is_dir() and (path / "run.json").is_file()
    )
    valid: list[tuple[Path, dict[str, Any]]] = []
    for run_dir in run_dirs:
        metadata = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
        if metadata.get("exit_code") == 0 and (run_dir / "final.md").is_file():
            valid.append((run_dir, metadata))

    if viewer_root.exists():
        shutil.rmtree(viewer_root)
    viewer_root.mkdir(parents=True)
    labels = [f"candidate-{index:02d}" for index in range(1, len(valid) + 1)]
    random.Random(seed).shuffle(labels)
    mapping: dict[str, str] = {}

    for label, (run_dir, metadata) in zip(labels, valid):
        candidate = viewer_root / label
        outputs = candidate / "outputs"
        outputs.mkdir(parents=True)
        mapping[label] = metadata["run_id"]
        eval_id = TASK_ORDER[metadata["task_id"]] * 10 + int(metadata["repetition"])
        eval_metadata = {
            "eval_id": eval_id,
            "eval_name": metadata["task_id"].replace("_", " ").title(),
            "prompt": metadata["prompt"],
            "assertions": [],
        }
        (candidate / "eval_metadata.json").write_text(
            json.dumps(eval_metadata, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        final = (run_dir / "final.md").read_text(encoding="utf-8", errors="replace")
        final = final.replace(metadata["run_id"], label)
        (outputs / "final.md").write_text(final, encoding="utf-8")
        diff_path = run_dir / "changes.diff"
        if diff_path.is_file() and diff_path.stat().st_size:
            shutil.copy2(diff_path, outputs / "changes.diff")
        grading_path = run_dir / "grading.json"
        if grading_path.is_file():
            grading = json.loads(grading_path.read_text(encoding="utf-8"))
            (candidate / "grading.json").write_text(
                json.dumps(sanitized_grading(grading), indent=2, ensure_ascii=False),
                encoding="utf-8",
            )

    mapping_path.parent.mkdir(parents=True, exist_ok=True)
    mapping_path.write_text(json.dumps(mapping, indent=2), encoding="utf-8")
    return {"runs": len(valid), "viewer_root": str(viewer_root), "mapping": str(mapping_path)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-root", type=Path, required=True)
    parser.add_argument("--viewer-root", type=Path, required=True)
    parser.add_argument("--mapping", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=5602)
    args = parser.parse_args()
    result = prepare_workspace(
        args.raw_root,
        args.viewer_root,
        args.mapping,
        seed=args.seed,
    )
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
