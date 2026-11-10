---
id: T0016
owner: ~
needs: []
branch: —
worktree: —
status: ready
started_at: —
ended_at: —
review: agent
preview: none
protocol: standard
---
# T0016: Make myproject create and its tests work on a fresh clone, where the plan branch store leaves no PLAN.md

## Goals
Since the plan branch store (commit 6da116c), a clone has no `PLAN.md`, so `find_template_root` fails.
That breaks `myproject create`, two `tests/test_cli.py` tests, and GitHub CI on `main`.
Locate the template root by `pyproject.toml`, `CHANGELOG.md`, and `src/myproject/` only.
Skip the template's `.plan/` and `plan.code-workspace` when copying; keep writing a fresh `PLAN.md` and `.plan/tasks/.gitkeep`.
Drop the `.plan/`, `/PLAN.md`, and `/plan.code-workspace` ignore lines from the new project's `.gitignore`, so git tracks those files.

Specifications: [technical-spec.md](T0016-make-myproject-create-and-its-tests-work-on/technical-spec.md).
Completion check: `pytest -q` passes on a fresh clone after `python scripts/bootstrap-dev-environment.py`
Size estimate: 4 files, 90 lines

## Task Execution Steps
- [ ] **[Implement]** Add failing scaffold tests for a template root without `PLAN.md` and with a stale `.plan/`.
- [ ] **[Verify]**    Run the new tests and record their failure output.
- [ ] **[Implement]** Change the root markers, copy exclusions, and `.gitignore` rewrite in `scaffold.py`.
- [ ] **[Verify]**    Run lint, the full suite, and the fresh-clone bootstrap; record output.
- [ ] **[Doc]**       Update `docs/requirements.md` and CHANGELOG.md.
- [ ] **[Review]**    Obtain review approval of the finished work before completion.

## Execution Log
- [2026-11-10] **[Doc]**
  Companion task file scaffolded at task creation.
