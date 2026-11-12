---
id: T0031
owner: "@codex"
session: codex-20261112-3ad534
needs: []
branch: task/T0031-scaffold-and-index-docs-tutorials-alongside-the-other
worktree: .plan/work/T0031-scaffold-and-index-docs-tutorials-alongside-the-other
status: active
started_at: "2026-11-12T09:45:34Z"
ended_at: —
review: none
preview: none
protocol: adhoc
---
# T0031: Scaffold and index docs/tutorials/ alongside the other standard documentation subdirectories

## Goals
Add `docs/tutorials/` with a `.gitkeep`, as the project setup guidelines list it among the standard documentation subdirectories.
List it in docs/index.md and the README layout.
Make new projects scaffolded by `create` include it.

## Task Execution Steps
- [x] **[Implement]** Write the tests listed in the technical spec.
- [x] **[Verify]**    Run the new tests and capture the expected failures.
- [x] **[Implement]** Implement the change until the new tests pass.
- [x] **[Verify]**    Run the fast suite and the completion check; record output in validation-proof.md.
- [x] **[Doc]**       Update the affected documentation and add a CHANGELOG.md entry.

## Execution Log
- [2026-11-10] **[Doc]**
  Companion task file scaffolded at task creation.

- [2026-11-12] **[Verify]**
  Captured failing-first evidence, 37 passing fast tests, and 16 passing CLI tests. Ruff passed; offline Markdown issues matched baseline.
  - Files touched: 3.
  - Lines touched: 3.
  - Reopenings: 0.

- [2026-11-12] **[Complete]**
  Added the tutorial placeholder, documentation links, changelog entry, and scaffold regression assertion. Recorded verification evidence and completed all execution steps; ready for orchestrator completion.

