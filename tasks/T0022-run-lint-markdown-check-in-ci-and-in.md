---
id: T0022
owner: ~
needs: ['T0021']
branch: —
worktree: —
status: ready
started_at: —
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
- [ ] **[Implement]** Write the tests listed in the technical spec.
- [ ] **[Verify]**    Run the new tests and capture the expected failures.
- [ ] **[Implement]** Implement the change until the new tests pass.
- [ ] **[Verify]**    Run the fast suite and the completion check; record output in validation-proof.md.
- [ ] **[Doc]**       Update the affected documentation and add a CHANGELOG.md entry.

## Execution Log
- [2026-11-10] **[Doc]**
  Companion task file scaffolded at task creation.
