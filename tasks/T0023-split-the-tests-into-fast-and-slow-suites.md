---
id: T0023
owner: ~
needs: []
branch: —
worktree: —
status: ready
started_at: —
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
Make releases run the slow suite too, for example by extending `check()` in a `PythonProject` subclass in scripts/devops.py.
Document both suite commands in docs/devops.md and README.md.

## Task Execution Steps
- [ ] **[Implement]** Write the tests listed in the technical spec.
- [ ] **[Verify]**    Run the new tests and capture the expected failures.
- [ ] **[Implement]** Implement the change until the new tests pass.
- [ ] **[Verify]**    Run the fast suite and the completion check; record output in validation-proof.md.
- [ ] **[Doc]**       Update the affected documentation and add a CHANGELOG.md entry.
- [ ] **[Review]**    Obtain review approval of the finished work before completion.

## Execution Log
- [2026-11-10] **[Doc]**
  Companion task file scaffolded at task creation.
