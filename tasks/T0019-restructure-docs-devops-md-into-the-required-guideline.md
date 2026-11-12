---
id: T0019
owner: "@claude"
session: claude-20261112-911a7f
needs: []
branch: task/T0019-restructure-docs-devops-md-into-the-required-guideline
worktree: .plan/work/T0019-restructure-docs-devops-md-into-the-required-guideline
status: active
started_at: "2026-11-12T10:38:30Z"
ended_at: —
review: none
preview: none
protocol: adhoc
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
  Restructured docs/devops.md into Development Environment and Versioning and Releasing first; dropped mail-utils.
  Manual release now freezes as `[released: <date>]` in its own commit and reopens `-pre` in a separate commit after tagging.
  Added a Docs entry to CHANGELOG.md; committed 0b261f4 on the task branch.
- [2026-11-12] **[Verify]**
  `lint-markdown check docs/devops.md` and `CHANGELOG.md`: passed. Fast tests not run: the worktree has no .venv; docs-only change.
