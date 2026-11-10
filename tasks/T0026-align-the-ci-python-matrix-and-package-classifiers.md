---
id: T0026
owner: "@claude-code"
needs: []
branch: —
worktree: —
status: completed
started_at: "2026-11-10T17:12:23Z"
ended_at: "2026-11-10T17:15:30Z"
review: none
preview: none
protocol: adhoc
completion-commit: 0a59a6f544311dc5bc9b82f949c598c1310aad79
---
# T0026: Move to Python 3.15 per the Python guidelines: requires-python >=3.15, the CI matrix, classifiers, and docs.

## Goals
Follow the Python guidelines, which now require Python 3.15, the latest stable release.
Set `requires-python = ">=3.15"` in pyproject.toml, add the matching `Programming Language :: Python :: 3.15` classifier, and run CI on 3.15.
Use Python 3.15 features only where they simplify code; keep `create` producing projects with the same settings.
Update the prerequisites in docs/devops.md, README.md, and docs/requirements.md.

## Task Execution Steps
- [x] **[Implement]** Update requires-python, the classifiers, and the CI matrix to Python 3.15.
- [x] **[Verify]**    Recreate .venv with Python 3.15, then run the bootstrap and the fast suite.
- [x] **[Doc]**       Update the prerequisites and add a CHANGELOG.md entry.

## Execution Log
- [2026-11-10] **[Doc]**
  Companion task file scaffolded at task creation.

- [2026-11-10] **[Implement]**
  Raised requires-python to 3.15, added the 3.15 classifiers, set CI to 3.15, and updated the prerequisites.
  - Undeclared file: src/myproject/scaffold.py, reformatted by ruff for PEP 758.

- [2026-11-10] **[Verify]**
  Rebuilt .venv with Python 3.15.2; the bootstrap passed lint, format, 28 tests, and the build.
  - lint-markdown issue count unchanged at 43, owned by T0021.

- [2026-11-10] **[Verify]**
  Recorded task outcomes.
  - Files touched: 7.
  - Lines touched: 17.
  - Reopenings: 0.

- [2026-11-10] **[Complete]**
  Task completed successfully.

