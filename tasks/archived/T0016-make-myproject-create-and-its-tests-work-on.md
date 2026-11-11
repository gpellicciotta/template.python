---
id: T0016
owner: "@claude-code"
needs: []
branch: —
worktree: —
status: completed
started_at: "2026-11-10T15:09:02Z"
ended_at: "2026-11-10T15:13:42Z"
review: agent
preview: none
protocol: standard
review_status: approved
review_round: 1
reviewed_by: "@claude-code-subagent"
completion-commit: 137e8e190ada4b59a12e47110e6d8b2e3d097598
---
# T0016: Make myproject create and its tests work on a fresh clone, where the plan branch store leaves no PLAN.md

## Goals
Since the plan branch store (commit 6da116c), a clone has no `PLAN.md`, so `find_template_root` fails.
That breaks `myproject create`, two `tests/test_cli.py` tests, and GitHub CI on `main`.
Locate the template root by `pyproject.toml`, `CHANGELOG.md`, and `src/myproject/` only.
Skip the template's `.plan/` and `plan.code-workspace` when copying; keep writing a fresh `PLAN.md` and `.plan/tasks/.gitkeep`.
Drop the `.plan/`, `/PLAN.md`, and `/plan.code-workspace` ignore lines from the new project's `.gitignore`, so git tracks those files.

Specifications: [technical-spec.md](T0016-make-myproject-create-and-its-tests-work-on/technical-spec.md).
Completion check: `pytest -q` passes on a fresh clone after `python scripts/bootstrap-dev-environment.py`
Size estimate: 4 files, 90 lines

## Task Execution Steps
- [x] **[Implement]** Add failing scaffold tests for a template root without `PLAN.md` and with a stale `.plan/`.
- [x] **[Verify]**    Run the new tests and record their failure output.
- [x] **[Implement]** Change the root markers, copy exclusions, and `.gitignore` rewrite in `scaffold.py`.
- [x] **[Verify]**    Run lint, the full suite, and the fresh-clone bootstrap; record output.
- [x] **[Doc]**       Update `docs/requirements.md` and CHANGELOG.md.
- [x] **[Review]**    Obtain review approval of the finished work before completion.

## Execution Log
- [2026-11-10] **[Doc]**
  Companion task file scaffolded at task creation.

- [2026-11-10] **[Verify]**
  Two new scaffold tests failed, then passed after the fix; fresh-clone bootstrap passes all 28 tests and scaffolded projects track PLAN.md.

- [2026-11-10] **[Review]**
  Round 1 requested (mode: agent).

- [2026-11-10] **[Implement]**
  Applied review follow-ups: nested .plan and CRLF test cases, real-template .gitignore assertion, simpler tasks dir helper, doc fixes.
  - Undeclared files touched: tests/test_cli.py, README.md.

- [2026-11-10] **[Review]**
  Round 1 approved by @claude-code-subagent.
  - Round 1 approved; its four minor follow-ups were then applied.

- [2026-11-10] **[Verify]**
  Recorded task outcomes.
  - Files touched: 6.
  - Lines touched: 84.
  - Reopenings: 0.

- [2026-11-10] **[Complete]**
  Task completed successfully.

