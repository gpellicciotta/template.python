---
id: T0038
owner: "@codex"
session: codex-20261112-acac25
needs: []
branch: task/T0038-resolve-version-with-support-python-get-package-version
worktree: .plan/work/T0038-resolve-version-with-support-python-get-package-version
status: completed
started_at: "2026-11-12T09:27:49Z"
ended_at: "2026-11-12T09:31:24Z"
review: none
preview: none
protocol: adhoc
usage:
  worker: {turns: 4, duration_s: 371.6, input: 179158, output: 9020, cache_read: 1408768, cache_write: 0}
work_duration: 214.7
completion-commit: 3ea6b8a051be58fa45d19fc7f93de01e1b6d4a04
---
# T0038: Resolve __version__ with support_python.get_package_version so the CLI shows -pre instead of the rc0 form

## Goals
Installed metadata shows `3.0.0-pre` as `3.0.0rc0`, so `myproject.__version__` is the rc0 form; support-python v3.0.0 `ToolHarness` already maps it back for `--version`.
Resolve `__version__` in src/myproject/__init__.py with `support_python.get_package_version("template-python")`, which maps `rc0` back to `-pre` and falls back to `0.0.0+unknown`.
Make sure `create` still rewrites the distribution name in new projects.

## Task Execution Steps
- [x] **[Implement]** Write the tests listed in the technical spec.
- [x] **[Verify]**    Run the new tests and capture the expected failures.
- [x] **[Implement]** Implement the change until the new tests pass.
- [x] **[Verify]**    Run the fast suite and the completion check; record output in validation-proof.md.
- [x] **[Doc]**       Add a CHANGELOG.md entry.

## Execution Log
- [2026-11-10] **[Doc]**
  Companion task file scaffolded at task creation.

- [2026-11-12] **[Verify]**
  Normalized prerelease versions and preserved release and missing-metadata behavior; scaffold rewriting passed. Validation evidence records the initial guard failure.
  - Files touched: 2.
  - Lines touched: 25.
  - Reopenings: 0.

- [2026-11-12] **[Implement]**
  Committed the verified resolver change locally. All execution steps passed; the orchestrator retains lifecycle completion.

- [2026-11-12] **[Verify]**
  Completion validation found 1 errors; pending fix turn 1 of 2.
  - TF020.

- [2026-11-12] **[Implement]**
  Added regression tests for prerelease normalization, release preservation, missing metadata, and scaffold distribution-name rewriting before implementation.

- [2026-11-12] **[Doc]**
  Added the user-facing changelog entry and recorded failing-first and passing verification output in the validation proof.

- [2026-11-12] **[Complete]**
  Task completed successfully.

