---
id: T0021
owner: ~
needs: ['T0018', 'T0019']
branch: —
worktree: —
status: ready
started_at: —
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
- [ ] **[Doc]**       Run lint-markdown fix, then fix the remaining issues by hand.
- [ ] **[Doc]**       Fix lead-ins, placeholders, paths, and stale references the linter misses.
- [ ] **[Verify]**    Run lint-markdown check and confirm exit code 0.

## Execution Log
- [2026-11-10] **[Doc]**
  Companion task file scaffolded at task creation.
