---
id: T0026
owner: ~
needs: []
branch: —
worktree: —
status: ready
started_at: —
ended_at: —
review: none
preview: none
protocol: adhoc
---
# T0026: Align the CI Python matrix and package classifiers with requires-python >=3.10

## Goals
Make the CI matrix cover every Python version the project supports, from `requires-python` up to the newest release.
Add matching `Programming Language :: Python :: 3.x` classifiers to pyproject.toml.
Decide with the user whether to raise `requires-python` above 3.10, which reached end of life in October 2026.
Keep the prerequisites in docs/devops.md and README.md consistent with that decision.

## Task Execution Steps
- [ ] **[Decide]**    Ask the user whether to keep Python 3.10 support.
- [ ] **[Implement]** Update the CI matrix, classifiers, and requires-python.
- [ ] **[Verify]**    Build the package and run the fast suite locally.
- [ ] **[Doc]**       Update the prerequisites and add a CHANGELOG.md entry.

## Execution Log
- [2026-11-10] **[Doc]**
  Companion task file scaffolded at task creation.
