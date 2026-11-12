---
id: T0025
owner: "@claude"
session: claude-20261112-9d968e
needs: []
branch: task/T0025-add-a-subprocess-end-to-end-test-that
worktree: .plan/work/T0025-add-a-subprocess-end-to-end-test-that
status: completed
started_at: "2026-11-12T10:02:28Z"
ended_at: "2026-11-12T10:06:19Z"
review: none
preview: none
protocol: adhoc
usage:
  worker: {turns: 4, duration_s: 358.2, input: 84, output: 13816, cache_read: 1920936, cache_write: 79740}
work_duration: 230.6
contributors: "@codex"
completion-commit: e35716a866ca5b509493b4be4539baf12335d661
---
# T0025: Add a subprocess end-to-end test that runs the installed myproject entry point with realistic arguments

## Goals
Add tests that run the installed `myproject` console script as a subprocess, as the CLI end-to-end testing rules require.
Cover `--version`, `help`, `greet`, `create` into `tmp_path`, an existing destination, and an invalid option.
Assert exit codes 0, 1, and 2 and the expected stdout and stderr content.
Locate the console script next to `sys.executable`, and mark the tests `slow`.

## Task Execution Steps
- [x] **[Implement]** Write the subprocess tests in tests/test_cli_e2e.py.
- [x] **[Verify]**    Run pytest -m slow tests/test_cli_e2e.py; record output in validation-proof.md.

## Execution Log
- [2026-11-10] **[Doc]**
  Companion task file scaffolded at task creation.

- [2026-11-12] **[Implement]**
  Added tests/test_cli_e2e.py: five slow subprocess tests of the console script next to `sys.executable`.
  Covered `--version`, `help`, `greet Gio`, `create demo` then a repeated `create`, and `--bogus` (exit codes 0, 1, 2).
  Added a DevEx entry to CHANGELOG.md.

- [2026-11-12] **[Verify]**
  `python -m pytest -m slow tests/test_cli_e2e.py`: 5 passed; `python -m pytest`: 33 passed; ruff clean.
  Evidence in validation-proof.md.

- [2026-11-12] **[Complete]**
  Task completed successfully.

