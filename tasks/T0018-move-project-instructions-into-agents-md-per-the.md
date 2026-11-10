---
id: T0018
owner: "@claude-code"
needs: []
branch: —
worktree: —
status: completed
started_at: "2026-11-10T17:17:14Z"
ended_at: "2026-11-10T17:19:27Z"
review: none
preview: none
protocol: adhoc
completion-commit: 7f08f067fc5ee16d579c0dc74b16dbf2e7ed09c5
---
# T0018: Move project instructions into AGENTS.md per the agent-file layout, reducing CLAUDE.md to an @AGENTS.md import

## Goals
Make CLAUDE.md contain only `@AGENTS.md`, moving all project instructions into AGENTS.md.
Keep the plan-managed block first in AGENTS.md and drop its duplicate from CLAUDE.md.
Structure the rest as a `#` title with a summary, then `Commands`, `Architecture`, `Project Conventions`, and `Boundaries`.
Describe template.python itself instead of `<Fill in ...>` placeholders, and keep AGENTS.md under 150 lines.
Drop the copied guideline and logging sections; the logging copy contradicts the logging guidelines.

Completion check: `lint-markdown check AGENTS.md CLAUDE.md` reports no issues and `pytest` passes.

### Declared Files
- AGENTS.md
- CLAUDE.md

Size estimate: 2 files, 200 lines

## Task Execution Steps
- [x] **[Read]**      Read the Agent Instruction Files section of the project setup guidelines.
- [x] **[Doc]**       Rewrite AGENTS.md and reduce CLAUDE.md to the import.
- [x] **[Verify]**    Run lint-markdown on both files and the fast test suite.

## Execution Log
- [2026-11-10] **[Doc]**
  Companion task file scaffolded at task creation.

- [2026-11-10] **[Doc]**
  Rewrote AGENTS.md around template.python and reduced CLAUDE.md to the import.
  - Undeclared files: README.md and CHANGELOG.md, to keep references current.

- [2026-11-10] **[Verify]**
  lint-markdown passed on AGENTS.md and CLAUDE.md; 28 tests passed.
  - Files touched: 4.
  - Lines touched: 173.
  - Reopenings: 0.

- [2026-11-10] **[Complete]**
  Task completed successfully.

