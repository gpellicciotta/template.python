---
id: T0015
owner: "@claude-code"
needs: []
branch: —
worktree: —
status: completed
started_at: "2026-11-10T14:51:36Z"
ended_at: "2026-11-10T14:57:51Z"
review: agent
preview: none
protocol: standard
review_status: approved
review_round: 2
reviewed_by: "@claude-code-subagent"
completion-commit: 6da116c4c91d3f1c6b443860b742324d4f3c1882
---
# T0015: Migrate the myproject CLI from build_action_parser, print_help, and print_version to the support-python v2.0.0 ToolHarness

## Goals
Pin `support-python` at `v2.0.0` in `pyproject.toml`; v1.0.0's `build_action_parser`, `print_help`, and `print_version` are gone.
Rebuild `src/myproject/cli.py` on `ToolHarness` with `greet [NAME]` and `create PROJECT_NAME [-o DIR]` actions.
Route CLI output through the handler's `CliLogger` instead of `print`.
Accept the v2 conventions: `-v` means `--verbose`, `--version` shows the version, and help uses the harness layout.
Tracks support.python T0046 for this consumer.

Specifications: [technical-spec.md](T0015-migrate-the-myproject-cli-from-build-action-parser/technical-spec.md).
Completion check: `.venv/Scripts/python -m pytest -q` and `.venv/Scripts/myproject help`
Size estimate: 6 files, 200 lines

## Task Execution Steps
- [x] **[Implement]** Rewrite `tests/test_cli.py` for the harness behavior from the technical spec.
- [x] **[Verify]**    Run the rewritten tests against the v1 CLI and record the failures.
- [x] **[Implement]** Pin support-python v2.0.0 and rebuild `cli.py` on `ToolHarness`.
- [x] **[Verify]**    Run lint, the full suite, and the installed `myproject` commands; record output.
- [x] **[Doc]**       Update `README.md`, `CLAUDE.md`, and CHANGELOG.md.
- [x] **[Review]**    Obtain review approval of the finished work before completion.

## Execution Log
- [2026-11-10] **[Doc]**
  Companion task file scaffolded at task creation.

- [2026-11-10] **[Verify]**
  Rewrote CLI tests, proved 7 failures on v1, migrated cli.py to ToolHarness; lint and 23 tests pass.

- [2026-11-10] **[Review]**
  Round 1 requested (mode: agent).

- [2026-11-10] **[Review]**
  Round 1 rejected by @claude-code-subagent: help greet omits positional argument docs; proof lacks help output; requirements.md undeclared; CLAUDE.md logging bullet stale.

- [2026-11-10] **[Implement]**
  Addressed review round 1: documented positional arguments in action details, added help greet test, refreshed proof, declared requirements.md, fixed CLAUDE.md banner note.

- [2026-11-10] **[Review]**
  Round 2 requested (mode: agent).

- [2026-11-10] **[Review]**
  Round 2 approved by @claude-code-subagent.
  - Round 2: all four round-1 findings fixed; 24 tests pass.

- [2026-11-10] **[Verify]**
  Recorded task outcomes.
  - Files touched: 7.
  - Lines touched: 207.
  - Reopenings: 0.

- [2026-11-10] **[Complete]**
  Task completed successfully.

