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
# T0026: Move to Python 3.15 per the Python guidelines: requires-python >=3.15, the CI matrix, classifiers, and docs.

## Goals
Follow the Python guidelines, which now require Python 3.15, the latest stable release.
Set `requires-python = ">=3.15"` in pyproject.toml, add the matching `Programming Language :: Python :: 3.15` classifier, and run CI on 3.15.
Use Python 3.15 features only where they simplify code; keep `create` producing projects with the same settings.
Update the prerequisites in docs/devops.md, README.md, and docs/requirements.md.

## Task Execution Steps
- [ ] **[Implement]** Update requires-python, the classifiers, and the CI matrix to Python 3.15.
- [ ] **[Verify]**    Recreate .venv with Python 3.15, then run the bootstrap and the fast suite.
- [ ] **[Doc]**       Update the prerequisites and add a CHANGELOG.md entry.

## Execution Log
- [2026-11-10] **[Doc]**
  Companion task file scaffolded at task creation.
