# Lightweight Superpowers Benchmark Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use subagent-driven-development (recommended) or executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Execute a 16-run paired benchmark comparing core Codex with a seven-skill Superpowers bundle across planning, debugging, code audit, and parallel audit tasks.

**Architecture:** A self-contained Python fixture repository supplies four frozen tasks and hidden rubrics. A PowerShell setup script creates two temporary `CODEX_HOME` directories that share authentication and system skills but differ in the seven selected Superpowers; a Python runner launches ephemeral Codex CLI sessions and captures JSONL, final responses, patches, timing, and verification results. A deterministic grader handles tests and gold findings, while a rubric grader handles planning quality and produces a compact Markdown report.

**Tech Stack:** PowerShell 7, Python 3 standard library (`unittest`), Git, Codex CLI 0.142.3.

## Global Constraints

- Model: `gpt-5.6-sol`.
- Reasoning effort: `medium`.
- Exactly four tasks, two configurations, and two repetitions: 16 scored executions.
- Maximum two Codex CLI processes at once and four active agents per run.
- B0 contains none of the 13 Obra Superpowers; S1 contains only `brainstorming`, `writing-plans`, `systematic-debugging`, `test-driven-development`, `verification-before-completion`, `dispatching-parallel-agents`, and `subagent-driven-development`.
- Prompts, fixture commits, sandbox, time limit, and tools are identical between paired B0/S1 runs.
- Use fresh run directories and ephemeral Codex sessions; no run may read gold data or sibling results.
- Do not modify or synchronize `C:/Users/Victor/.codex/skills`.
- Do not stage or alter the user's pre-existing working-tree changes.
- Do not add automatic tie-break runs.

---

### Task 1: Create Frozen Fixtures And Rubrics

**Files:**
- Create: `benchmarks/superpowers-light/fixture/README.md`
- Create: `benchmarks/superpowers-light/fixture/src/refunds.py`
- Create: `benchmarks/superpowers-light/fixture/src/checkout.py`
- Create: `benchmarks/superpowers-light/fixture/src/profile_store.py`
- Create: `benchmarks/superpowers-light/fixture/src/session_auth.py`
- Create: `benchmarks/superpowers-light/fixture/src/report_export.py`
- Create: `benchmarks/superpowers-light/fixture/tests/test_checkout.py`
- Create: `benchmarks/superpowers-light/hidden/test_checkout_hidden.py`
- Create: `benchmarks/superpowers-light/evals.json`
- Create: `benchmarks/superpowers-light/gold.json`
- Test: `benchmarks/superpowers-light/tests/test_fixture.py`

**Interfaces:**
- Consumes: the approved four-task design.
- Produces: a deterministic Python fixture, four prompts, hidden tests, and category rubrics.

- [ ] Write the fixture test proving the intended checkout bug fails before agent modification.
- [ ] Run `python -m unittest benchmarks.superpowers-light.tests.test_fixture -v` through discovery and verify failure describes the missing edge-case behavior.
- [ ] Implement the fixture modules with one reproducible checkout defect, three audit findings, and three independent parallel-audit areas.
- [ ] Define four prompts without skill names or configuration hints.
- [ ] Define gold root causes, severities, evidence, and 100-point rubrics.
- [ ] Run the fixture tests and verify the public baseline plus hidden failing condition are reproducible.
- [ ] Commit only Task 1 files.

### Task 2: Build Isolated Configurations And Runner

**Files:**
- Create: `benchmarks/superpowers-light/scripts/build-configs.ps1`
- Create: `benchmarks/superpowers-light/scripts/run_benchmark.py`
- Create: `benchmarks/superpowers-light/tests/test_harness.py`

**Interfaces:**
- Consumes: the local Codex authentication file, `.system` skills, seven repo skill directories, and `evals.json`.
- Produces: temporary B0/S1 homes and 16 isolated run directories under `benchmarks/superpowers-light/results/raw/`.

- [ ] Write harness tests for the 4×2×2 matrix, randomized order, configuration inventories, and prompt equality.
- [ ] Run `python -m unittest discover -s benchmarks/superpowers-light/tests -p "test_harness.py" -v` and verify the tests fail before implementation.
- [ ] Implement config creation without printing or persisting authentication content in benchmark artifacts.
- [ ] Implement run-directory cloning, ephemeral `codex exec --json`, a 30-minute timeout, two-process concurrency, and event/timing capture.
- [ ] Record the final response, Git diff, public tests, hidden tests for bugfix runs, exit status, duration, and token data when present.
- [ ] Run harness tests and `git diff --check`.
- [ ] Commit only Task 2 files.

### Task 3: Pilot And Execute The 16 Runs

**Files:**
- Create: `benchmarks/superpowers-light/results/pilot/`
- Create: `benchmarks/superpowers-light/results/raw/`
- Create: `benchmarks/superpowers-light/results/run-order.json`

**Interfaces:**
- Consumes: Task 1 fixtures and Task 2 runner.
- Produces: one unscored isolation pilot and 16 complete scored run artifacts.

- [ ] Run one unscored planning pilot under B0 and S1 to verify skill isolation, auth, output capture, and prompt equality.
- [ ] Inspect only infrastructure artifacts; correct runner faults without comparing candidate quality.
- [ ] Freeze a balanced randomized order for the 16 scored runs.
- [ ] Execute all runs with at most two CLI processes concurrently.
- [ ] Poll active processes frequently enough to provide user progress updates within 60 seconds.
- [ ] Rerun only documented infrastructure failures; never rerun a legitimate task failure.
- [ ] Verify 16 final responses, 16 event logs, 16 timing records, and matching paired input hashes.

### Task 4: Grade, Aggregate, And Report

**Files:**
- Create: `benchmarks/superpowers-light/scripts/grade_results.py`
- Create: `benchmarks/superpowers-light/tests/test_grading.py`
- Create: `benchmarks/superpowers-light/results/grading.json`
- Create: `benchmarks/superpowers-light/results/benchmark.json`
- Create: `benchmarks/superpowers-light/results/report.md`
- Create: `benchmarks/superpowers-light/results/review.html`

**Interfaces:**
- Consumes: blinded run artifacts, hidden tests, and `gold.json`.
- Produces: per-run 0–100 scores, paired category deltas, cost metrics, blind examples, and keep/conditional/simplify/remove/not-evaluated recommendations.

- [ ] Write grading tests for deterministic bug scores, audit recall/precision, critical-failure caps, and paired aggregation.
- [ ] Run `python -m unittest discover -s benchmarks/superpowers-light/tests -p "test_grading.py" -v` and verify failure before implementation.
- [ ] Implement deterministic grading and opaque B0/S1 labels.
- [ ] Grade planning dimensions from the frozen rubric with evidence for every awarded score.
- [ ] Aggregate mean quality, paired deltas, time, tokens, tool calls, and agent usage without merging cost into quality.
- [ ] Generate `review.html` with the existing skill-creator static viewer when compatible; otherwise include blind side-by-side outputs in `report.md`.
- [ ] Apply the approved 4-point quality and 15% cost thresholds, preserving “inconclusive” when repetitions disagree.
- [ ] Run all benchmark tests and `git diff --check`.
- [ ] Commit code and redacted reports without auth files, temporary homes, full transcripts containing secrets, or oversized artifacts.

## Self-Review

- The plan implements exactly 16 scored runs and no automatic tie-breakers.
- It tests the seven approved skills as a bundle and explicitly avoids causal claims about individual skills.
- The same model, reasoning effort, prompts, source, tools, and agent access apply to both configurations.
- Hidden tests and gold data are unavailable to runners.
- Existing user changes and runtime skills remain outside the benchmark's mutation scope.
