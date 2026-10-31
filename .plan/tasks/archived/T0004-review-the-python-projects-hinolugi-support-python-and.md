---
id: T0004
owner: "@claude"
needs: []
branch: task/T0004-review-the-python-projects-hinolugi-support-python-and
worktree: ./work/T0004-review-the-python-projects-hinolugi-support-python-and
status: completed
started: 2026-09-06
ended: 2026-09-06
---

# T0004: Review hinolugi-support.python and mail-utils for template gaps

## Goals

Compare this template's structure against hinolugi-support.python and mail-utils, as if both were scaffolded
from it, to surface generic conventions worth adopting here. Exclude anything specific to one project's domain.
File each finding as a separate backlog item for @gio to review.

## Task Execution Steps

- [x] **[Read]**      Inventory top-level layout, docs/, .github/, src/ across all three projects.
- [x] **[Read]**      Compare pyproject.toml, .gitignore, README, and CHANGELOG conventions across all three.
- [x] **[Decide]**    Select generic, template-worthy differences, excluding project-specific domain logic.
- [x] **[Doc]**       File one backlog TODO per major topic, owned by @gio, in TODO.md.

## Execution Log

- [2026-09-06] **[Read]**
  Compared directory layouts, CI workflows, and conventions across all three projects.
  - hinolugi-support ships `logging.py` and `publish.yml`; template has neither.
  - Both downstream projects populate `tasks/`; template does not track `tasks/`.
  - Neither project scaffolds `specs/`, `adrs/`, or `issues/` directories.
  - Downstream projects show versioning differences against current `-pre` guidelines.
  - hinolugi-support uses hatchling with custom ruff rules; template uses setuptools.
  - mail-utils has a `scripts/` directory for non-packaged dev tooling.

- [2026-09-06] **[Decide]**
  Selected 7 generic topics and excluded project-specific modules from the template scope.

- [2026-09-06] **[Doc]**
  Filed A0005-A0011 in `TODO.md` Backlog, owned by @gio, pending review.

- [2026-09-06] **[Verify]**
  Ran pytest in the worktree without source changes; all tests passed.

- [2026-09-06] **[Complete]**
  Filed seven backlog tasks for review; no source or changelog changes needed.
