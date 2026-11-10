---
id: T0014
owner: ~
needs: ['T0015']
branch: —
worktree: —
status: ready
started_at: —
ended_at: —
review: agent
preview: none
protocol: standard
---
# T0014: Replace scripts/devops.py with a thin DevopsCli script on the PythonProject adapter, pinning the released support-python v2.0.0

## Goals
Needs the released support-python v2.0.0; see `docs/migration-v2.md` in support-python for the full mapping.
Replace `scripts/devops.py` with a thin script running `DevopsCli(PythonProject(REPO_ROOT)).run()`.
Pin `support-python @ git+https://github.com/gpellicciotta/support.python.git@v2.0.0` in `scripts/requirements.txt`.
Keep project-specific actions through `DevopsCli.add_action`.

Specifications: [technical-spec.md](T0014-replace-scripts-devops-py-with-a-thin-devopscli/technical-spec.md).
Completion check: `python scripts/bootstrap-dev-environment.py`, then `python scripts/devops.py check` and `pytest -q`
Size estimate: 7 files, 500 lines, mostly deletions

## Task Execution Steps
- [ ] **[Verify]**    Record current `devops.py help` and `release --dry-run` output as the baseline.
- [ ] **[Verify]**    Author the failing tests from the technical spec and record their failure output.
- [ ] **[Implement]** Add `scripts/requirements.txt` and install it from `bootstrap-dev-environment.py`.
- [ ] **[Implement]** Replace `scripts/devops.py` with the thin `DevopsCli(PythonProject(...))` script.
- [ ] **[Implement]** Delete tests of release helpers that moved into support.python.
- [ ] **[Verify]**    Run the completion check and the integration scenario; record verbatim output.
- [ ] **[Doc]**       Update `docs/devops.md`, `README.md`, and CHANGELOG.md.
- [ ] **[Review]**    Obtain review approval of the finished work before completion.

## Execution Log
- [2026-11-10] **[Doc]**
  Companion task file scaffolded at task creation.
