---
id: T0032
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
# T0032: Make the bootstrap script CLI follow the CLI guidelines: -v as --verbose, help --verbose, errors on stderr

## Goals
Make `-v` mean `--verbose` in scripts/_cli_common.py, keeping `--version` for the version, as the CLI guidelines require.
Support `help --verbose`, and add `--debug` or record why the bootstrap is exempt.
Print the header line, usage, actions, options, and exit codes like `ToolHarness` help, using the standard library only.
Send failure messages to stderr with `**[ERROR]**` tags, including the fallback messages in scripts/devops.py.
Use the same copyright line as `myproject`, and remove the unused duplicate `get_project_version` from scripts/_cli_common.py.

## Task Execution Steps
- [ ] **[Implement]** Write the tests listed in the technical spec.
- [ ] **[Verify]**    Run the new tests and capture the expected failures.
- [ ] **[Implement]** Implement the change until the new tests pass.
- [ ] **[Verify]**    Run the fast suite and the completion check; record output in validation-proof.md.
- [ ] **[Doc]**       Update the affected documentation and add a CHANGELOG.md entry.

## Execution Log
- [2026-11-10] **[Doc]**
  Companion task file scaffolded at task creation.
