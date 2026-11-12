---
id: T0021
owner: "@claude"
session: claude-20261112-745bbb
needs: []
branch: task/T0021-fix-all-lint-markdown-issues-bold-lead-ins
worktree: .plan/work/T0021-fix-all-lint-markdown-issues-bold-lead-ins
status: active
started_at: "2026-11-12T10:49:26Z"
ended_at: —
review: none
preview: none
protocol: adhoc
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
  Ran `lint-markdown fix`: blank lines after subheadings and README table alignment.
  The private `dev-guidelines` repo returned HTTP 404 to anonymous link checks.
  Added `.lint-markdown.json` with `github-owners: ["gpellicciotta"]`, resolving those links to sibling checkouts.
  Replaced the missing `coordinating-work-guidelines.md` link with the plan task usage skill URL.
  Linked the logging and CLI guidelines; dropped the dangling `../PLAN.md` index link.
  Removed bold lead-ins in requirements.md and devops.md and bold section references in README.md.
  Converted `<...>`, `v<version>`, `X.Y.Z`, and `{{package_name}}` placeholders to `{{kebab-case}}`.
  Replaced `.venv\Scripts\...` commands with `devops.py` or active-venv commands.
  Refreshed the README layout: all test modules, `.plan/`, `.lint-markdown.json`, and `PLAN.md` as an ignored link.
  Dropped the stale root `work/` ignore rule; worktrees live under the ignored `.plan/work/`.
  **[Decided]** Skipped the CHANGELOG raw-URL exclusion: no such URL fails, and the config has no URL exclusions.
  Synced the scaffold's fresh changelog preamble (`v{{version}}-pre`) with the template's, test first.
  Committed e8eaf76 on the task branch.

- [2026-11-12] **[Verify]**
  New test `test_fresh_changelog_keeps_the_template_preamble` failed first on preamble drift, then passed.
  `lint-markdown check` (online): "All 8 markdown files passed linting.", exit code 0.
  `ruff check .` and `ruff format --check .` passed; fast suite 72 passed; slow suite 26 passed.
  `devops.py check` could not run: the worktree has no `.venv`; ran its steps with the main `.venv` instead, minus the build.
