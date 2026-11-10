---
id: T0027
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
# T0027: Add the standard --format text|json option to the myproject greet and create actions

## Goals
Add the `--format text|json` option to the `greet` and `create` actions with `ToolHarness.add_format_option`, as the CLI guidelines require.
In `json` mode, print exactly one JSON document on stdout, such as the greeting or the created project's path, and write all log entries to stderr.
Keep the `text` output unchanged as the default.
Document the option and its JSON fields in README.md and docs/requirements.md.

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
