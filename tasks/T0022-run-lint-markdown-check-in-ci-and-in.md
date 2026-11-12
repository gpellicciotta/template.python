---
id: T0022
owner: "@claude"
session: claude-20261112-3035aa
needs: []
branch: task/T0022-run-lint-markdown-check-in-ci-and-in
worktree: .plan/work/T0022-run-lint-markdown-check-in-ci-and-in
status: active
started_at: "2026-11-12T10:59:45Z"
ended_at: —
review: none
preview: none
protocol: adhoc
---
# T0022: Run lint-markdown check in CI and in devops.py check so Markdown violations fail the build

## Goals
Make `python scripts/devops.py lint`, and so `check`, also run `lint-markdown check`, as the Markdown guidelines require.
Subclass `PythonProject` in scripts/devops.py and extend its `lint()` rather than adding a separate action.
Run the same check in the CI workflow, installing scripts/requirements.txt so `lint-markdown` is available.
Document the check in docs/devops.md.

## Task Execution Steps
- [x] **[Implement]** Write the tests listed in the technical spec.
- [x] **[Verify]**    Run the new tests and capture the expected failures.
- [x] **[Implement]** Implement the change until the new tests pass.
- [x] **[Verify]**    Run the fast suite and the completion check; record output in validation-proof.md.
- [x] **[Doc]**       Update the affected documentation and add a CHANGELOG.md entry.

## Execution Log
- [2026-11-10] **[Doc]**
  Companion task file scaffolded at task creation.
- [2026-11-12] **[Implement]**
  Added a slow test that `build_cli(tmp_path).project.lint()` fails on a `*` bullet and passes on a `-` bullet.
- [2026-11-12] **[Verify]**
  The new test failed before the change: `lint()` returned True on the violation.
- [2026-11-12] **[Implement]**
  Added `build_project()` in scripts/devops.py; its `PythonProject` subclass runs `lint-markdown check` after ruff.
  CI now installs scripts/requirements.txt and runs `lint-markdown check`.
- [2026-11-12] **[Verify]**
  `python scripts/devops.py check` exited 0, and 1 with a seeded MD005 violation; see validation-proof.md.
- [2026-11-12] **[Doc]**
  Updated docs/devops.md and added a CHANGELOG.md entry.
