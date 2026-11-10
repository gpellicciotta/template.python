---
id: T0014
owner: "@claude-code"
needs: []
branch: —
worktree: —
status: completed
started_at: "2026-11-10T14:58:14Z"
ended_at: "2026-11-10T15:08:35Z"
review: agent
preview: none
protocol: standard
review_status: approved
review_round: 1
reviewed_by: "@claude-code-subagent"
completion-commit: a0d84f6269f49a58953b635a7c2c56b657f5bb44
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
- [x] **[Verify]**    Record current `devops.py help` and `release --dry-run` output as the baseline.
- [x] **[Verify]**    Author the failing tests from the technical spec and record their failure output.
- [x] **[Implement]** Add `scripts/requirements.txt` and install it from `bootstrap-dev-environment.py`.
- [x] **[Implement]** Replace `scripts/devops.py` with the thin `DevopsCli(PythonProject(...))` script.
- [x] **[Implement]** Delete tests of release helpers that moved into support.python.
- [x] **[Verify]**    Run the completion check and the integration scenario; record verbatim output.
- [x] **[Doc]**       Update `docs/devops.md`, `README.md`, and CHANGELOG.md.
- [x] **[Review]**    Obtain review approval of the finished work before completion.

## Execution Log
- [2026-11-10] **[Doc]**
  Companion task file scaffolded at task creation.

- [2026-11-10] **[Implement]**
  Replaced devops.py with a thin DevopsCli script that re-runs in .venv; bootstrap installs scripts/requirements.txt into .venv.
  - Size note: 574 changed lines, 457 of them deletions of the old pipeline.
  - Undeclared file touched: CLAUDE.md, now declared.

- [2026-11-10] **[Verify]**
  Lint, 24 tests, and devops check pass; fresh-clone bootstrap installs support-python 2.0.0, two create tests fail there, tracked as T0016.

- [2026-11-10] **[Review]**
  Round 1 requested (mode: agent).

- [2026-11-10] **[Implement]**
  Addressed review round 1 follow-ups: re-exec guard and tests, git isolation, stronger help test, fuller CHANGELOG, doc fixes; publish.yml duplication moved to a new task.

- [2026-11-10] **[Review]**
  Round 1 approved by @claude-code-subagent.
  - Round 2 approved all follow-ups; its guard-variable note was then applied.

- [2026-11-10] **[Verify]**
  Recorded task outcomes.
  - Files touched: 8.
  - Lines touched: 648.
  - Reopenings: 0.

- [2026-11-10] **[Complete]**
  Task completed successfully.

