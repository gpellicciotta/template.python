---
id: T0032
owner: "@claude"
session: claude-20261112-ad105b
needs: []
branch: task/T0032-make-the-bootstrap-script-cli-follow-the-cli
worktree: .plan/work/T0032-make-the-bootstrap-script-cli-follow-the-cli
status: active
started_at: "2026-11-12T10:32:27Z"
ended_at: —
review: none
preview: none
protocol: adhoc
---
# T0032: Make the bootstrap script CLI follow the CLI guidelines: -v as --verbose, help --verbose, errors on stderr

## Goals
Make `-v` mean `--verbose` in scripts/_cli_common.py, keeping `--version` for the version, as the CLI guidelines require.
Support `help --verbose`, and add `--debug` or record why the bootstrap is exempt.
Print the header line, usage, actions, options, and exit codes like `ToolHarness` help, using the standard library only.
Send failure messages to stderr with `**[ERROR]**` tags, including the fallback messages in scripts/devops.py.
Use the same copyright line as `myproject`, and remove the unused duplicate `get_project_version` from scripts/_cli_common.py.

## Task Execution Steps
- [x] **[Implement]** Write the tests listed in the technical spec.
- [x] **[Verify]**    Run the new tests and capture the expected failures.
- [x] **[Implement]** Implement the change until the new tests pass.
- [x] **[Verify]**    Run the fast suite and the completion check; record output in validation-proof.md.
- [x] **[Doc]**       Update the affected documentation and add a CHANGELOG.md entry.

## Execution Log
- [2026-11-10] **[Doc]**
  Companion task file scaffolded at task creation.

- [2026-11-12] **[Decided]**
  Exempted the bootstrap from --debug; it writes no operational logs, so it has no threshold to lower. Recorded the reason in its docstring and docs/devops.md.

- [2026-11-12] **[Implement]**
  Added stdlib help sections, -v as --verbose with step commands, and **[ERROR]** stderr messages; touched undeclared README.md and docs/devops.md.

- [2026-11-12] **[Verify]**
  Recorded task outcomes; script tests, fast suite, and ruff pass.
  - Files touched: 6.
  - Lines touched: 305.
  - Reopenings: 0.

