---
id: T0028
owner: "@claude"
session: claude-20261112-1fa377
needs: []
branch: task/T0028-add-dry-run-to-myproject-create-reporting-every
worktree: .plan/work/T0028-add-dry-run-to-myproject-create-reporting-every
status: active
started_at: "2026-11-12T10:15:15Z"
ended_at: —
review: agent
preview: none
protocol: standard
usage:
  worker: {turns: 6, duration_s: 1373.6, input: 248, output: 88704, cache_read: 12054954, cache_write: 245516}
  review: {turns: 2, duration_s: 234.4, input: 48, output: 14840, cache_read: 1017902, cache_write: 90252}
work_duration: 807.2
review_status: pending
review_round: 2
---
# T0028: Add --dry-run to myproject create, reporting every planned change without writing anything

## Goals
Add `--dry-run` to the `create` action, as the CLI guidelines require for actions that write files.
A dry run reports the destination, copied files, renames, rewrites, reset files, and the `plan init` step, and writes nothing.
It exits with code 1 on an existing destination or an invalid name, as the real run would.
Support `--format json` for the planned changes.
Document the option in README.md and docs/requirements.md.

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
  Added plan_project() and create --dry-run in text and JSON; create_project now runs the shared plan.

- [2026-11-12] **[Verify]**
  Completion check, fast suite, and devops check passed; proof in validation-proof.md.
  - Two runs hit a transient home-guard failure from ~/.claude.json writes.

- [2026-11-12] **[Implement]**
  Size note: 6 counted files, 427 lines exceed the typical line; one feature, the planner and flag cannot merge apart usefully.

- [2026-11-12] **[Verify]**
  Completion validation found 1 errors; pending fix turn 1 of 2.
  - TF020.

- [2026-11-12] **[Doc]**
  Documented create --dry-run in README.md and docs/requirements.md and added a CHANGELOG.md entry.

- [2026-11-12] **[Review]**
  Round 1 requested (mode: agent).

- [2026-11-12] **[Review]**
  Round 1 rejected by @claude-2: The implementation meets every functional goal and the CLI guidelines' dry-run rule.
  - Findings: [review-findings-1.md](T0028-add-dry-run-to-myproject-create-reporting-every/review-findings-1.md).

- [2026-11-12] **[Doc]**
  Addressed review round 1: moved the README initialization-failure sentence back to the real-run create paragraph; lint passes.

- [2026-11-12] **[Review]**
  Round 2 requested (mode: agent).

