---
id: T0019
owner: "@claude"
session: claude-20261112-911a7f
needs: []
branch: task/T0019-restructure-docs-devops-md-into-the-required-guideline
worktree: .plan/work/T0019-restructure-docs-devops-md-into-the-required-guideline
status: completed
started_at: "2026-11-12T10:38:30Z"
ended_at: "2026-11-12T10:41:54Z"
review: none
preview: none
protocol: adhoc
usage:
  worker: {turns: 4, duration_s: 294.2, input: 104, output: 22710, cache_read: 2271382, cache_write: 125490}
work_duration: 203.0
completion-commit: 462228a9873e8662b43c5228722f94668a94de85
---
# T0019: Restructure docs/devops.md into the required guideline sections and fix the manual release commit order

## Goals
Start docs/devops.md with `Development Environment` (`Prerequisites`, `Setup`), then `Versioning and Releasing` (`Updating Versions`, `Making a Release`).
Under `Updating Versions`, state that pyproject.toml holds the version and that plan task completion raises the patch.
Fix the manual release steps: the release commit carries no `-pre` heading, and the next `-pre` heading follows in a separate commit after tagging.
Move the remaining content after those sections and drop the `mail-utils` mention.

Completion check: `lint-markdown check docs/devops.md` reports no issues.

### Declared Files
- docs/devops.md

Size estimate: 1 file, 150 lines

## Task Execution Steps
- [x] **[Read]**      Read the devops.md rules in the project setup and change management guidelines.
- [x] **[Doc]**       Restructure docs/devops.md and rewrite the manual release steps.
- [x] **[Verify]**    Run lint-markdown check on docs/devops.md.

## Execution Log
- [2026-11-10] **[Doc]**
  Companion task file scaffolded at task creation.

- [2026-11-12] **[Doc]**
  Restructured docs/devops.md with the required sections first and dropped mail-utils.
  Manual releases now freeze in their own commit and reopen `-pre` in a separate commit.

- [2026-11-12] **[Verify]**
  Markdown lint passed, and the fast suite passed 61 tests; see validation-proof.md.

- [2026-11-12] **[Verify]**
  Completion validation found 2 errors; pending fix turn 1 of 2.
  - TF016.
  - TF018.

- [2026-11-12] **[Complete]**
  Task completed successfully.

