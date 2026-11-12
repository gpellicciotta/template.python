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
usage:
  worker: {turns: 6, duration_s: 1431.4, input: 149424, output: 29996, cache_read: 5866752, cache_write: 0}
  review: {turns: 2, duration_s: 423.6, input: 84, output: 22220, cache_read: 2379238, cache_write: 111790}
work_duration: 764.8
review_status: pending
review_round: 2
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

- [2026-11-12] **[Verify]**
  Completion validation found 1 errors; pending fix turn 1 of 2.
  - TF020.

- [2026-11-12] **[Implement]**
  Added command-order, missing-plan, failure-cleanup, fake-executable, and real CLI integration tests.

- [2026-11-12] **[Verify]**
  Confirmed five expected failures before implementing plan initialization; captured terminal output in validation-proof.md.

- [2026-11-12] **[Implement]**
  Replaced generated plan files with Git and branch-store initialization, preserving ignore rules and refreshing the managed instructions block.

- [2026-11-12] **[Doc]**
  Documented required tools and branch-store behavior; added the breaking CLI changelog entry.

- [2026-11-12] **[Review]**
  Round 1 requested (mode: agent).

- [2026-11-12] **[Review]**
  Round 1 rejected by @claude: The core change works.
  - Findings: [review-findings-1.md](T0029-make-myproject-create-initialize-the-new-project-s/review-findings-1.md).

- [2026-11-12] **[Implement]**
  Addressed review findings with read-only Git cleanup, resolved test executables, missing-Git coverage, and corrected inherited project instructions.

- [2026-11-12] **[Verify]**
  Corrected earlier completion evidence: it required a PYTHONPATH override. The revised completion command passes 24 tests without that override; the full suite passes 45.

- [2026-11-12] **[Review]**
  Round 2 requested (mode: agent).

