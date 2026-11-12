---
id: T0036
owner: "@claude"
session: claude-20261112-5639c1
needs: []
branch: task/T0036-read-the-cli-author-and-copyright-from-package
worktree: .plan/work/T0036-read-the-cli-author-and-copyright-from-package
status: completed
started_at: "2026-11-12T10:42:16Z"
ended_at: "2026-11-12T10:49:05Z"
review: none
preview: none
protocol: adhoc
usage:
  worker: {turns: 4, duration_s: 698.0, input: 140, output: 40254, cache_read: 4150792, cache_write: 131418}
work_duration: 408.1
completion-commit: 0882cc61536fe9ed76dde1a6f1aa673dca903168
---
# T0036: Read the CLI author and copyright from package metadata instead of hardcoding them in cli.py and _cli_common.py

## Goals
Derive the CLI copyright holder in src/myproject/cli.py from the installed package's author metadata through `importlib.metadata`, keeping pyproject.toml the single source of vendor metadata.
Fall back sensibly when metadata is missing, as the `0.0.0+unknown` version fallback does.
Make scripts/_cli_common.py read the author from pyproject.toml with the standard library instead of the `APP_AUTHOR` constant.
Record whether the copyright year stays a literal or moves into configuration.

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
  Added failing tests: 6 metadata-author cases in test_cli.py, 4 pyproject cases in test_scripts.py.

- [2026-11-12] **[Verify]**
  Captured 11 expected failures before implementing; see validation-proof.md.

- [2026-11-12] **[Implement]**
  cli.py reads Author and Author-email metadata; _cli_common.py reads pyproject authors with tomllib.
  Both fall back to `the template-python authors`.

- [2026-11-12] **[Implement]**
  **[Decided]** The copyright year stays a literal `COPYRIGHT_YEAR = 2026`, the first-publication year in LICENSE.md.
  Configuration would add a custom pyproject table that package metadata cannot carry.

- [2026-11-12] **[Implement]**
  **[Decided]** Replaced the `myproject.cli.COPYRIGHT` and `_cli_common.COPYRIGHT` constants with `copyright_notice()`.
  scripts/devops.py still hardcodes its COPYRIGHT; it is outside this task's declared files.

- [2026-11-12] **[Verify]**
  Fast suite 71 passed, completion check 52 passed, slow suite 26 passed, ruff clean.

- [2026-11-12] **[Doc]**
  Updated docs/requirements.md and added a CHANGELOG.md entry.

- [2026-11-12] **[Verify]**
  Completion validation found 1 errors; pending fix turn 1 of 2.
  - TF016.

- [2026-11-12] **[Complete]**
  Task completed successfully.

