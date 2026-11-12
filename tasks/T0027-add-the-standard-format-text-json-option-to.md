---
id: T0027
owner: "@claude"
session: claude-20261112-bd3fd9
needs: []
branch: task/T0027-add-the-standard-format-text-json-option-to
worktree: .plan/work/T0027-add-the-standard-format-text-json-option-to
status: active
started_at: "2026-11-12T10:06:40Z"
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
- [x] **[Implement]** Write the tests listed in the technical spec.
- [x] **[Verify]**    Run the new tests and capture the expected failures.
- [x] **[Implement]** Implement the change until the new tests pass.
- [x] **[Verify]**    Run the fast suite and the completion check; record output in validation-proof.md.
- [x] **[Doc]**       Update the affected documentation and add a CHANGELOG.md entry.
- [ ] **[Review]**    Obtain review approval of the finished work before completion.

## Execution Log
- [2026-11-10] **[Doc]**
  Companion task file scaffolded at task creation.

- [2026-11-12] **[Implement]**
  Added --format text|json to greet and create; json mode emits one object on stdout, logs on stderr.
  - Failed create prints no JSON document.

- [2026-11-12] **[Verify]**
  Ran the completion check and devops check; all lint, fast, slow, and build steps passed.
  - Proof recorded in validation-proof.md.
  - Files touched: 4.
  - Lines touched: 112.
  - Reopenings: 0.

