---
id: T0034
owner: "@codex"
session: codex-20261112-061531
needs: []
branch: task/T0034-put-one-argument-per-line-in-every-call
worktree: .plan/work/T0034-put-one-argument-per-line-in-every-call
status: active
started_at: "2026-11-12T09:42:12Z"
ended_at: —
review: none
preview: none
protocol: adhoc
---
# T0034: Put one argument per line in every call or signature split across lines

## Goals
Put one argument or parameter per line in every call or signature that is split across lines, as the Python guidelines require.
Add magic trailing commas so `ruff format` keeps that layout, for example in src/myproject/cli.py, scripts/bootstrap-dev-environment.py, and tests/test_scripts.py.
Join split calls that fit within 132 characters.

## Task Execution Steps
- [x] **[Implement]** Add trailing commas to the split calls and run ruff format.
- [x] **[Verify]**    Run ruff check, ruff format --check, and the fast suite.

## Execution Log
- [2026-11-12] **[Decided]**
  Kept this formatting-only change behavior-neutral; existing unit and CLI integration tests provide regression coverage.

- [2026-11-12] **[Implement]**
  Added trailing commas and formatted three calls. Included the newly identified split call in tests/test_cli.py.
  tests/test_scripts.py already complied. No split calls fit within 132 characters when joined.

- [2026-11-10] **[Doc]**
  Companion task file scaffolded at task creation.

- [2026-11-12] **[Verify]**
  Passed Ruff checks, Markdown lint, 37 fast tests, and the affected slow CLI test; Python ASTs remained unchanged.
  - Files touched: 3.
  - Lines touched: 13.
  - Reopenings: 0.

- [2026-11-12] **[Complete]**
  Committed formatting and changelog changes locally; recorded passing verification evidence and completed both execution steps.

