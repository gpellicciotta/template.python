---
id: T0023
owner: "@codex"
session: codex-20261112-6bed62
needs: []
branch: task/T0023-split-the-tests-into-fast-and-slow-suites
worktree: .plan/work/T0023-split-the-tests-into-fast-and-slow-suites
status: active
started_at: "2026-11-12T09:53:22Z"
ended_at: —
review: agent
preview: none
protocol: standard
---
# T0023: Split the tests into fast and slow suites with pytest-xdist, pytest-timeout, a slow marker, and a CI slow run

## Goals
Add `pytest-xdist` and `pytest-timeout` to the `dev` extra.
Register the `slow` marker and set `addopts = "-n auto --timeout=30 -m 'not slow'"`, as the Python guidelines show.
Mark integration, end-to-end, subprocess, git, and build tests as `slow`.
Run the fast suite and `pytest -m slow --timeout=120` as separate CI steps.
Rely on support-python v3.0.0: `devops.py test --slow` runs `pytest -m slow --timeout=120`, and `check` runs both suites, so scripts/devops.py needs no change.
Document both suite commands in docs/devops.md and README.md.

## Task Execution Steps
- [x] **[Implement]** Write the tests listed in the technical spec.
- [x] **[Verify]**    Run the new tests and capture the expected failures.
- [x] **[Implement]** Implement the change until the new tests pass.
- [x] **[Verify]**    Run the fast suite and the completion check; record output in validation-proof.md.
- [x] **[Doc]**       Update the affected documentation and add a CHANGELOG.md entry.
- [ ] **[Review]**    Obtain review approval of the finished work before completion.

## Execution Log
- [2026-11-10] **[Doc]**
  Companion task file scaffolded at task creation.

- [2026-11-12] **[Verify]**
  Fast suite passed. Awaited slow-suite execution through terminal task 44527.
  - Command: python -m pytest -m slow --timeout=120.

- [2026-11-12] **[Verify]**
  Created a worktree-local environment for public devops checks; dependency installation used terminal task 15641.
  - Command: .venv/Scripts/python -m pip install --no-cache-dir -e .[dev].

- [2026-11-12] **[Verify]**
  Ran python scripts/devops.py check through terminal task 49689; child commands and process IDs appear in validation evidence.

- [2026-11-12] **[Verify]**
  Standalone slow command ran through terminal task 36797 with pytest process 45200.
  - Command: python scripts/devops.py test --slow.

- [2026-11-12] **[Verify]**
  Passed 33 fast tests, 19 slow tests, devops check, standalone slow command, Markdown lint, and diff checks.
  - Counted files touched: 5; lines touched: 83; reopenings: 0.
  - Verbatim command output: companion validation-proof.md.

