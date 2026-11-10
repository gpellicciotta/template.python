---
id: T0018
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
- [ ] **[Read]**      Read the Agent Instruction Files section of the project setup guidelines.
- [ ] **[Doc]**       Rewrite AGENTS.md and reduce CLAUDE.md to the import.
- [ ] **[Verify]**    Run lint-markdown on both files and the fast test suite.

## Execution Log
- [2026-11-10] **[Doc]**
  Companion task file scaffolded at task creation.
