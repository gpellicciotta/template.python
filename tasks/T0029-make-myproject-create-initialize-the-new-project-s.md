---
id: T0029
owner: "@codex"
session: codex-20261112-37ae14
needs: []
branch: task/T0029-make-myproject-create-initialize-the-new-project-s
worktree: .plan/work/T0029-make-myproject-create-initialize-the-new-project-s
status: active
started_at: "2026-11-12T08:56:57Z"
ended_at: —
review: agent
preview: none
protocol: standard
---
# T0029: Make myproject create initialize the new project's plan store with plan init --store branch

## Goals
Make `create` run `git init` and `plan init --store branch` in the new project instead of writing a root PLAN.md and `.plan/tasks/.gitkeep` itself.
Stop removing the `.plan/`, `/PLAN.md`, and `/plan.code-workspace` lines from the new `.gitignore`, so the root PLAN.md stays an ignored link.
Make sure AGENTS.md ends up with exactly one plan-managed block.
Fail with exit code 1 and a clear message when `plan` is not on `PATH`, leaving no half-created project.
Update README.md and docs/requirements.md.

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

- [2026-11-12] **[Verify]**
  Verified 43 tests, Ruff, formatting, and isolated package build; recorded red and green evidence.
  - Markdown lint reports existing formatting and external-link issues.
  - Completion check passed 22 tests, including real CLI and plan initialization.

