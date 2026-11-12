---
id: T0025
owner: "@codex"
session: codex-20261112-5631d0
needs: []
branch: task/T0025-add-a-subprocess-end-to-end-test-that
worktree: .plan/work/T0025-add-a-subprocess-end-to-end-test-that
status: active
started_at: "2026-11-12T10:02:28Z"
ended_at: —
review: none
preview: none
protocol: adhoc
---
# T0025: Add a subprocess end-to-end test that runs the installed myproject entry point with realistic arguments

## Goals
Add tests that run the installed `myproject` console script as a subprocess, as the CLI end-to-end testing rules require.
Cover `--version`, `help`, `greet`, `create` into `tmp_path`, an existing destination, and an invalid option.
Assert exit codes 0, 1, and 2 and the expected stdout and stderr content.
Locate the console script next to `sys.executable`, and mark the tests `slow`.

## Task Execution Steps
- [ ] **[Implement]** Write the subprocess tests in tests/test_cli_e2e.py.
- [ ] **[Verify]**    Run pytest -m slow tests/test_cli_e2e.py; record output in validation-proof.md.

## Execution Log
- [2026-11-10] **[Doc]**
  Companion task file scaffolded at task creation.
