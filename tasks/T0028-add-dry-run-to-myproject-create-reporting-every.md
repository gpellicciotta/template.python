---
id: T0028
owner: ~
needs: ['T0027', 'T0029']
branch: —
worktree: —
status: ready
started_at: —
ended_at: —
review: agent
preview: none
protocol: standard
---
# T0028: Add --dry-run to myproject create, reporting every planned change without writing anything

## Goals
Add `--dry-run` to the `create` action, as the CLI guidelines require for actions that write files.
A dry run reports the destination, copied files, renames, rewrites, reset files, and the `plan init` step, and writes nothing.
It exits with code 1 on an existing destination or an invalid name, as the real run would.
Support `--format json` for the planned changes.
Document the option in README.md and docs/requirements.md.

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
