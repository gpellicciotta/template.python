---
task: T0023
round: 1
verdict: approved
reviewer: "@claude"
reviewed_at: 2026-11-12T09:59:23Z
reviewed_commit: "a6506dc"
base_commit: "4b7ef6a"
branch: task/T0023-split-the-tests-into-fast-and-slow-suites
---
# Review Findings: Task T0023 (Round 1)

## Summary
Approved. The work meets every goal in the task file.
- `pyproject.toml` adds `pytest-xdist` to the `dev` extra next to the existing `pytest-timeout`.
- `addopts = "-n auto --timeout=30 -m 'not slow'"` matches the Python guidelines; the `slow` marker is registered.
- Script subprocess tests are now marked `slow`. The CLI, scaffold, and isolation integration tests were already marked.
- CI runs the fast suite and `pytest -q -m slow --timeout=120` as separate steps.
- `scripts/devops.py` is unchanged, as the task specified; `test --slow` and `check` come from support-python v3.0.0.
- `README.md`, `docs/devops.md`, and `CHANGELOG.md` document both suites.

Reviewer verification on commit `a6506dc`, run in the task worktree:
- `.venv/Scripts/python -m pytest -q`: 33 passed (4.62s).
- `.venv/Scripts/python -m pytest -q -m slow --timeout=120`: 19 passed (12.13s).
- `--collect-only -q` collects 33 tests by default and 19 with `-m slow`, with no overlap.
- `ruff check .` and `ruff format --check .`: clean.
- `python scripts/devops.py check`: lint, both suites (33 and 19 passed), and build all succeeded.
- `git status --short` was clean afterward.

## Defects
None blocking. Minor nits, optional:
- In `docs/devops.md`, the comment on the `test --slow` line does not line up with the other comments.
- In `README.md` "Running Tests", a `powershell` block is followed by a `bash` block. The surrounding sections use `powershell`.
- The default `-m 'not slow'` also deselects a slow test requested by node ID (for example `pytest tests/test_cli.py::test_create_scaffolds_renamed_project`), unless `-m slow` is passed too. The guideline-mandated `addopts` causes this, so it is not a defect. A one-line doc hint would help.

## Process Gaps
None blocking.
- The Execution Log reports 5 files touched, but the diff touches 6 (`.github/workflows/ci.yml`, `CHANGELOG.md`, `README.md`, `docs/devops.md`, `pyproject.toml`, `tests/test_scripts.py`).
- The technical spec lists `tests/test_cli.py` as a declared file, but it was not changed. Its scope notes explain why, so this is fine.

## Required Rework
None.
