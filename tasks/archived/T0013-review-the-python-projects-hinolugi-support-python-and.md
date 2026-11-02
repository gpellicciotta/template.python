---
id: T0013
owner: "@gemini"
needs: []
branch: task/T0013-review-the-python-projects-hinolugi-support-python-and
worktree: ./work/T0013-review-the-python-projects-hinolugi-support-python-and
status: completed
started: 2026-09-06
ended: 2026-09-06
---

# T0013: Review hinolugi-support.python and mail-utils for template gaps

## Goals

Compare this template's structure against hinolugi-support.python and mail-utils to surface generic conventions worth adopting here. Exclude project-specific domain logic and file each finding as a separate backlog item for @gio to review.

## Task Execution Steps

- [x] **[Read]**      Compare directory layouts, pyproject.toml, and tooling across all three repositories.
- [x] **[Decide]**    Select generic, template-worthy differences and exclude project-specific domain implementations.
- [x] **[Doc]**       File one backlog TODO per major topic, owned by @gio, in TODO.md.
- [x] **[Verify]**    Run test suite and linters to verify repository health.

## Execution Log

- [2026-09-06] **[Read]**
  Inventoried structure and tooling across python-project-template, hinolugi-support.python, and mail-utils.
  - mail-utils configures pytest pythonpath for direct source testing without installation.
  - hinolugi-support declares license file and project URLs in pyproject.toml.
  - mail-utils implements a cross-platform Python bootstrap script replacing setup.ps1.
  - hinolugi-support provides reusable CLI helpers that can eliminate template boilerplate.
  - CI workflow in hinolugi-support uses setup-python@v5, explicit permissions, and artifact uploads.
  - Downstream projects show additional .gitignore patterns and scaffolding exclusions.
  - Build artifact directory varies between dist/ and bin/distributions/.

- [2026-09-06] **[Decide]**
  Selected 7 generic topics for backlog creation and excluded project-specific domains.

- [2026-09-06] **[Doc]**
  Filed A0016-A0022 in `TODO.md` Backlog, owned by @gio, pending review.

- [2026-09-06] **[Verify]**
  Ran pytest, ruff check, and ruff format in worktree; all 11 tests and lint checks passed.

- [2026-09-06] **[Complete]**
  Filed seven backlog tasks for review under autonomous loop tier; no source changes needed.
