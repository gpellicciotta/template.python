---
id: T0019
owner: ~
needs: ['T0020']
branch: —
worktree: —
status: ready
started_at: —
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
- [ ] **[Read]**      Read the devops.md rules in the project setup and change management guidelines.
- [ ] **[Doc]**       Restructure docs/devops.md and rewrite the manual release steps.
- [ ] **[Verify]**    Run lint-markdown check on docs/devops.md.

## Execution Log
- [2026-11-10] **[Doc]**
  Companion task file scaffolded at task creation.
