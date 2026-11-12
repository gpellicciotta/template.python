---
id: T0021
owner: "@claude"
session: claude-20261112-745bbb
needs: []
branch: task/T0021-fix-all-lint-markdown-issues-bold-lead-ins
worktree: .plan/work/T0021-fix-all-lint-markdown-issues-bold-lead-ins
status: completed
started_at: "2026-11-12T10:49:26Z"
ended_at: "2026-11-12T10:59:26Z"
review: none
preview: none
protocol: adhoc
usage:
  worker: {turns: 4, duration_s: 1090.2, input: 328, output: 70352, cache_read: 13253344, cache_write: 223840}
work_duration: 600.4
completion-commit: d81c9987853456d7358f78215d35c216243de92b
---
# T0021: Fix all lint-markdown issues, bold lead-ins, placeholder syntax, backslash paths, and stale references in the docs

## Goals
Fix every `lint-markdown check` issue in README.md, docs/index.md, docs/requirements.md, and the active CHANGELOG.md version.
Replace bold lead-in labels, which the Markdown guidelines reserve for glossaries.
Convert placeholders such as `<project-name>`, `v<version>`, `X.Y.Z`, and `{{package_name}}` to `{{kebab-case}}` form.
Replace `.venv\Scripts\...` paths with forward slashes and cross-platform commands.
Fix stale references: coordinating-work guidelines, `general-guidelines.md#cli`, the logging guideline link, and the README layout.
Exclude the finalized CHANGELOG raw URL through `.lint-markdown.json`.

Mechanical command: `lint-markdown fix`

Completion check: `lint-markdown check` exits 0.

### Declared Files
- README.md
- docs/index.md
- docs/requirements.md
- docs/devops.md
- CHANGELOG.md
- .gitignore
- .lint-markdown.json

Size estimate: 7 files, 150 lines

## Task Execution Steps
- [x] **[Doc]**       Run lint-markdown fix, then fix the remaining issues by hand.
- [x] **[Doc]**       Fix lead-ins, placeholders, paths, and stale references the linter misses.
- [x] **[Verify]**    Run lint-markdown check and confirm exit code 0.

## Execution Log
- [2026-11-10] **[Doc]**
  Companion task file scaffolded at task creation.

- [2026-11-12] **[Doc]**
  Ran `lint-markdown fix`, then added `.lint-markdown.json` with `github-owners`.
  Private `dev-guidelines` links now resolve to sibling checkouts instead of failing with HTTP 404.

- [2026-11-12] **[Doc]**
  Replaced the missing coordinating-work link with the plan skill URL and linked the logging and CLI guidelines.
  Dropped the dangling `../PLAN.md` index link and refreshed the README layout.

- [2026-11-12] **[Doc]**
  Removed bold lead-ins, converted placeholders to `{{kebab-case}}`, and replaced backslash `.venv` commands with cross-platform ones.

- [2026-11-12] **[Decided]**
  Skipped the CHANGELOG raw-URL exclusion: no such URL fails, and `.lint-markdown.json` has no URL exclusion setting.

- [2026-11-12] **[Implement]**
  Synced the scaffold's fresh changelog preamble with the template's, test first.
  Undeclared files touched: `src/myproject/scaffold.py` and `tests/test_scaffold.py`; the recount stays below the typical line.

- [2026-11-12] **[Implement]**
  Restored the `work/` ignore rule that plan task usage guidelines require, with a corrected comment.

- [2026-11-12] **[Verify]**
  Lint, ruff, and both test suites passed; outputs are in `validation-proof.md`.
  `devops.py check` refused to run without a worktree `.venv`, so the build step was skipped.

- [2026-11-12] **[Verify]**
  Completion validation found 3 errors; pending fix turn 1 of 2.
  - TF016.
  - TF018.

- [2026-11-12] **[Verify]**
  Recorded task outcomes.
  - Files touched: 7.
  - Lines touched: 222.
  - Reopenings: 0.

- [2026-11-12] **[Complete]**
  Task completed successfully.

