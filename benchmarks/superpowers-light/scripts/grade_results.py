from __future__ import annotations

import argparse
import json
import math
import re
import statistics
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def expectation(text: str, passed: bool, evidence: str) -> dict[str, Any]:
    return {"text": text, "passed": bool(passed), "evidence": evidence}


def classify_execution(metadata: dict[str, Any], events: str) -> str:
    if metadata.get("status") == "timeout":
        return "task_failure"
    if metadata.get("exit_code") == 0:
        return "valid"
    infrastructure_markers = (
        "usage limit",
        "requires a newer version of codex",
        "model metadata",
        "authentication",
    )
    lowered = events.lower()
    if any(marker in lowered for marker in infrastructure_markers):
        return "infrastructure_failure"
    return "task_failure"


def grade_bugfix(metadata: dict[str, Any], diff: str, final: str) -> dict[str, Any]:
    verification = metadata.get("verification", {})
    public_passed = verification.get("public_tests", {}).get("exit_code") == 0
    hidden_passed = verification.get("hidden_tests", {}).get("exit_code") == 0
    root_cause = bool(re.search(r"quantity\s*<=\s*0", diff)) and "ValueError" in diff
    changed_files = set(re.findall(r"^diff --git a/(.+?) b/", diff, flags=re.MULTILINE))
    allowed = {"src/checkout.py", "tests/test_checkout.py"}
    narrow_scope = bool(changed_files) and changed_files <= allowed
    verification_claim = public_passed and hidden_passed
    clear_handoff = 20 <= len(final.strip()) <= 2000 and bool(
        re.search(r"test|verif|pass", final, flags=re.IGNORECASE)
    )
    checks = [
        ("Public and hidden acceptance tests pass", hidden_passed, "Hidden test exit code is 0", 45),
        (
            "The root cause rejects every non-positive quantity with ValueError",
            root_cause,
            "Patch contains quantity <= 0 and raises ValueError" if root_cause else "Required guard not found",
            20,
        ),
        (
            "The patch is narrowly scoped to checkout code and its tests",
            narrow_scope,
            f"Changed files: {sorted(changed_files)}",
            15,
        ),
        (
            "Verification evidence confirms public and hidden behavior",
            verification_claim,
            f"public={public_passed}, hidden={hidden_passed}",
            15,
        ),
        (
            "The final handoff is concise and reports verification",
            clear_handoff,
            f"Final response length: {len(final)} characters",
            5,
        ),
    ]
    return {
        "score": sum(points for _, passed, _, points in checks if passed),
        "expectations": [expectation(text, passed, evidence) for text, passed, evidence, _ in checks],
    }


def match_findings(text: str, findings: list[dict[str, Any]]) -> set[str]:
    lowered = text.lower()
    matched: set[str] = set()
    for finding in findings:
        terms = [term.lower() for term in finding["terms"]]
        if sum(term in lowered for term in terms) >= 2:
            matched.add(finding["id"])
    return matched


def candidate_finding_count(text: str) -> int:
    lines = text.splitlines()
    candidates = [
        line
        for line in lines
        if re.search(r"\b(critical|high|medium|low)\b", line, flags=re.IGNORECASE)
        and (line.lstrip().startswith(("-", "#", "*")) or "severity" in line.lower())
    ]
    return len(candidates)


FINDING_FILES = {
    "sql_injection": "profile_store.py",
    "path_traversal": "profile_store.py",
    "password_hash": "profile_store.py",
    "cumulative_refund": "refunds.py",
    "predictable_token": "session_auth.py",
    "missing_expiry": "session_auth.py",
    "arbitrary_export_path": "report_export.py",
    "csv_injection": "report_export.py",
}


def grade_audit(final: str, gold: dict[str, Any], *, parallel: bool, events: str) -> dict[str, Any]:
    findings = gold["findings"]
    matched = match_findings(final, findings)
    total = len(findings)
    weights = {item["name"]: item["points"] for item in gold["rubric"]}
    recall_score = weights["recall"] * len(matched) / total
    candidates = max(candidate_finding_count(final), len(matched))
    precision_ratio = len(matched) / candidates if candidates else 0
    precision_score = weights["precision"] * min(1.0, precision_ratio)
    lowered = final.lower()
    severity_hits = sum(
        1 for finding in findings if finding["id"] in matched and finding["severity"].lower() in lowered
    )
    evidence_hits = sum(
        1
        for finding in findings
        if finding["id"] in matched
        and FINDING_FILES[finding["id"]] in lowered
        and bool(re.search(r"(?:line|:)\s*\d+", lowered))
    )
    expectations = [
        expectation(
            f"Finds gold root cause: {finding['id']}",
            finding["id"] in matched,
            "Matched at least two root-cause terms" if finding["id"] in matched else "Insufficient root-cause evidence",
        )
        for finding in findings
    ]
    expectations.append(
        expectation(
            "Avoids unsupported extra actionable findings",
            candidates <= total + 1,
            f"Detected {candidates} severity-labelled candidates for {total} gold findings",
        )
    )
    if parallel:
        files_covered = all(name in lowered for name in ("refunds.py", "session_auth.py", "report_export.py"))
        used_agents = "spawn_agent" in events or "collaboration" in events
        division_score = weights["division"] if files_covered else 0
        integration_ok = len(matched) >= 3 and candidates <= total + 1
        integration_score = weights["integration"] if integration_ok else 0
        expectations.extend(
            [
                expectation(
                    "Covers all three independent audit areas",
                    files_covered,
                    f"files_covered={files_covered}, subagent_signal={used_agents}",
                ),
                expectation(
                    "Integrates findings into a deduplicated prioritized report",
                    integration_ok,
                    f"matched={len(matched)}, candidates={candidates}",
                ),
            ]
        )
        score = recall_score + precision_score + division_score + integration_score
    else:
        severity_score = weights["severity"] * severity_hits / total
        evidence_score = weights["evidence"] * evidence_hits / total
        expectations.extend(
            [
                expectation(
                    "Assigns supported severity to matched findings",
                    severity_hits == len(matched) and bool(matched),
                    f"severity_hits={severity_hits}, matched={len(matched)}",
                ),
                expectation(
                    "Provides exact file and line evidence",
                    evidence_hits == len(matched) and bool(matched),
                    f"evidence_hits={evidence_hits}, matched={len(matched)}",
                ),
            ]
        )
        score = recall_score + precision_score + severity_score + evidence_score
    clarity = 100 <= len(final.strip()) <= 12000
    score += weights["clarity"] if clarity else 0
    expectations.append(
        expectation("The report is readable and bounded", clarity, f"Output length: {len(final)} characters")
    )
    return {"score": round(min(100, score), 2), "expectations": expectations}


PLANNING_CHECKS = {
    "requirements": [
        ("exact decimal arithmetic", ("decimal", "float")),
        ("currency precision and rounding", ("round", "minor unit")),
        ("provider failure behavior", ("provider", "timeout", "unavailable")),
        ("idempotent execution", ("idempoten",)),
        ("cumulative refund limit", ("cumulative", "captured")),
        ("exchange-rate audit trail", ("audit", "rate", "quote")),
        ("tests and verification", ("test", "verify")),
        ("rollout or migration", ("rollout", "migration")),
    ]
}


def grade_planning(final: str, gold: dict[str, Any]) -> dict[str, Any]:
    lowered = final.lower()
    requirements = PLANNING_CHECKS["requirements"]
    checks: list[dict[str, Any]] = []
    passed_requirements = 0
    for label, terms in requirements:
        passed = all(term in lowered for term in terms)
        passed_requirements += int(passed)
        checks.append(expectation(f"Plan covers {label}", passed, f"Required terms: {terms}"))
    requirement_score = 35 * passed_requirements / len(requirements)
    decisions = all(term in lowered for term in ("currency", "decimal", "provider", "idempoten"))
    execution = all(term in lowered for term in ("src/", "tests/", "python"))
    risks = all(term in lowered for term in ("concurr", "rollback", "failure"))
    clarity = 500 <= len(final.strip()) <= 20000 and bool(re.search(r"^#{1,3} ", final, re.MULTILINE))
    checks.extend(
        [
            expectation("Plan makes explicit technical decisions", decisions, "currency/decimal/provider/idempotency decisions"),
            expectation("Plan names exact files, tests, and commands", execution, "src/, tests/, and python command references"),
            expectation("Plan addresses concurrency, rollback, and failure risks", risks, "risk terms present"),
            expectation("Plan is structured and bounded", clarity, f"Output length: {len(final)} characters"),
        ]
    )
    score = requirement_score + (20 if decisions else 0) + (25 if execution else 0) + (15 if risks else 0) + (5 if clarity else 0)
    return {"score": round(score, 2), "expectations": checks}


def execution_metrics(events: str, final: str) -> dict[str, Any]:
    tool_calls = len(re.findall(r'"type":"command_execution"', events)) // 2
    errors = len(re.findall(r'"type":"error"', events))
    subagents = len(re.findall(r"spawn_agent|collaboration", events, flags=re.IGNORECASE))
    return {
        "tool_calls": {"command_execution": tool_calls, "subagent_signals": subagents},
        "total_tool_calls": tool_calls + subagents,
        "errors_encountered": errors,
        "output_chars": len(final),
        "transcript_chars": len(events),
    }


def grade_run(run_dir: Path, gold: dict[str, Any]) -> dict[str, Any]:
    metadata = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
    events = (run_dir / "events.jsonl").read_text(encoding="utf-8", errors="replace")
    final_path = run_dir / "final.md"
    final = final_path.read_text(encoding="utf-8", errors="replace") if final_path.exists() else ""
    diff = (run_dir / "changes.diff").read_text(encoding="utf-8", errors="replace")
    status = classify_execution(metadata, events)
    if status == "infrastructure_failure":
        result = {
            "status": status,
            "score": None,
            "expectations": [],
            "summary": {"passed": 0, "failed": 0, "total": 0, "pass_rate": None},
            "evidence": "Execution rejected by shared infrastructure before task completion",
        }
    elif metadata["task_id"] == "bugfix":
        result = {"status": status, **grade_bugfix(metadata, diff, final)}
    elif metadata["task_id"] == "planning":
        result = {"status": status, **grade_planning(final, gold["planning"])}
    elif metadata["task_id"] == "audit":
        result = {"status": status, **grade_audit(final, gold["audit"], parallel=False, events=events)}
    else:
        result = {
            "status": status,
            **grade_audit(final, gold["parallel_audit"], parallel=True, events=events),
        }
    if result.get("score") is not None:
        passed = sum(item["passed"] for item in result["expectations"])
        total = len(result["expectations"])
        result["summary"] = {
            "passed": passed,
            "failed": total - passed,
            "total": total,
            "pass_rate": round(result["score"] / 100, 4),
        }
    result["execution_metrics"] = execution_metrics(events, final)
    result["timing"] = {"executor_duration_seconds": metadata["duration_seconds"]}
    result["run_id"] = metadata["run_id"]
    result["task_id"] = metadata["task_id"]
    result["configuration"] = "with_skill" if metadata["config"] == "S1" else "without_skill"
    result["run_number"] = metadata["repetition"]
    result["tokens"] = sum(metadata.get("usage", {}).values())
    (run_dir / "grading.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return result


def metric_summary(values: list[float]) -> dict[str, float | None]:
    if not values:
        return {"mean": None, "stddev": None, "min": None, "max": None}
    return {
        "mean": round(statistics.mean(values), 3),
        "stddev": round(statistics.pstdev(values), 3),
        "min": round(min(values), 3),
        "max": round(max(values), 3),
    }


def aggregate_runs(runs: list[dict[str, Any]]) -> dict[str, Any]:
    summary: dict[str, Any] = {}
    for configuration in ("with_skill", "without_skill"):
        selected = [run for run in runs if run.get("configuration") == configuration]
        valid = [run for run in selected if isinstance(run.get("score"), (int, float))]
        summary[configuration] = {
            "valid_runs": len(valid),
            "infrastructure_failures": sum(
                run.get("status") == "infrastructure_failure" for run in selected
            ),
            "quality": metric_summary([float(run["score"]) for run in valid]),
            "time_seconds": metric_summary([float(run["time_seconds"]) for run in valid]),
            "tokens": metric_summary([float(run["tokens"]) for run in valid]),
        }
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-root", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    args = parser.parse_args()
    gold = json.loads((ROOT / "gold.json").read_text(encoding="utf-8"))
    graded: list[dict[str, Any]] = []
    for run_dir in sorted(path for path in args.raw_root.iterdir() if path.is_dir()):
        if not (run_dir / "run.json").exists():
            continue
        result = grade_run(run_dir, gold)
        metadata = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
        result["time_seconds"] = metadata["duration_seconds"]
        graded.append(result)
    summary = aggregate_runs(graded)
    args.output_root.mkdir(parents=True, exist_ok=True)
    (args.output_root / "grading.json").write_text(
        json.dumps(graded, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    benchmark_runs = []
    for run in graded:
        benchmark_runs.append(
            {
                "eval_id": run["task_id"],
                "eval_name": run["task_id"].replace("_", " ").title(),
                "configuration": run["configuration"],
                "run_number": run["run_number"],
                "result": {
                    "pass_rate": None if run.get("score") is None else run["score"] / 100,
                    "passed": run["summary"]["passed"],
                    "failed": run["summary"]["failed"],
                    "total": run["summary"]["total"],
                    "time_seconds": run["time_seconds"],
                    "tokens": run["tokens"],
                    "tool_calls": run["execution_metrics"]["total_tool_calls"],
                    "errors": run["execution_metrics"]["errors_encountered"],
                    "status": run["status"],
                },
                "expectations": run["expectations"],
                "notes": [],
            }
        )
    benchmark = {
        "metadata": {
            "skill_name": "selected-superpowers-bundle",
            "executor_model": "gpt-5.6-sol",
            "reasoning_effort": "medium",
            "evals_run": ["planning", "bugfix", "audit", "parallel_audit"],
            "runs_per_configuration": 2,
            "complete": len(graded) == 16 and all(run.get("score") is not None for run in graded),
        },
        "runs": benchmark_runs,
        "run_summary": summary,
        "notes": [
            "Infrastructure failures are excluded from quality and cost aggregates.",
            "Automated rubric scores are directional and require blind human review before skill changes.",
        ],
    }
    (args.output_root / "benchmark.json").write_text(
        json.dumps(benchmark, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    report = [
        "# Superpowers lightweight benchmark",
        "",
        f"Status: {'complete' if benchmark['metadata']['complete'] else 'incomplete'}",
        "",
        "| Configuration | Valid | Infrastructure failures | Mean quality | Mean seconds | Mean tokens |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for configuration in ("with_skill", "without_skill"):
        item = summary[configuration]
        report.append(
            f"| {configuration} | {item['valid_runs']} | {item['infrastructure_failures']} | "
            f"{item['quality']['mean']} | {item['time_seconds']['mean']} | {item['tokens']['mean']} |"
        )
    report.extend(
        [
            "",
            "No keep/remove decision is valid until all 16 runs are complete and blind review is submitted.",
        ]
    )
    (args.output_root / "report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(json.dumps({"runs": len(graded), "summary": summary}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
