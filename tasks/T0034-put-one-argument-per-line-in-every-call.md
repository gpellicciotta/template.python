---
id: T0034
owner: ~
needs: []
branch: —
worktree: —
status: ready
started_at: —
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
- [ ] **[Implement]** Add trailing commas to the split calls and run ruff format.
- [ ] **[Verify]**    Run ruff check, ruff format --check, and the fast suite.

## Execution Log
- [2026-11-10] **[Doc]**
  Companion task file scaffolded at task creation.
